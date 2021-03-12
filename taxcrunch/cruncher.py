import json
import os
import numpy as np
import pandas as pd
import taxcalc as tc

from paramtools import Parameters

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


class CruncherParams(Parameters):

    defaults = os.path.join(CURRENT_PATH, "defaults.json")


class Cruncher:
    """
    Constructor for the Cruncher class

    Parameters
    ----------
    inputs: file path to input adjustment file
        The default is cruncher/adjustment_template.json.

    custom_reform: file path to json policy reform file
        If you choose to specify a custom reform (as opposed to the
        preset reforms in the Tax-Calculator repo), change the adjustment
        file 'reform_options' field to 'Custom'.

    Returns
    -------
    class instance: Cruncher
    
    """

    INPUT_PATH = os.path.join(CURRENT_PATH, "adjustment_template.json")

    def __init__(self, inputs=INPUT_PATH, custom_reform=None, baseline=None):
        self.inputs = inputs
        self.custom_reform = custom_reform
        self.baseline = baseline
        self.params = CruncherParams()
        self.adjustment = self.adjust_inputs()
        self.params.adjust(self.adjustment)
        self.ivar, self.mtr_options, self.reform_options = self.taxsim_inputs()
        self.batch_ivar = self.batch_inputs(self.ivar)
        self.data = self.translate(self.ivar)
        self.ivar2, self.mtr_wrt = self.choose_mtr()
        self.data_mtr = self.translate(self.ivar2)
        self.pol = self.choose_baseline()
        self.pol2 = self.choose_reform()
        self.calc1, self.calc_reform, self.calc_mtr = self.run_calc()
        self.df_basic_vals = self.basic_vals()
        self.df_mtr = self.mtr_table()
        self.df_calc = self.calc_table()

    def adjust_inputs(self):
        """
        Adjust inputs based on 'adjustment_template.json' or a different specified json file
        """
        if isinstance(self.inputs, str) and os.path.isfile(self.inputs):
            self.adjustment = self.inputs
        else:
            self.adjustment = self.inputs
        return self.adjustment

    def taxsim_inputs(self):
        """
        Iterates through params object to extract parameter values

        Returns:
            self.ivar: a Pandas dataframe with Taxsim-style variables
            self.mtr_options: a string with the user's choice of how to calculate marginal tax rates
            self.reform_options: a string with the user's choice of reform

        """

        self.mtr_options = self.params.to_array("mtr_options")

        self.reform_options = self.params.to_array("reform_options")

        # construct list of taxsim param names
        param_list = []
        for key in self.params.dump().keys():
            if key == "mtr_options":
                pass
            else:
                if "section_1" in self.params.dump()[key]:
                    param_list.append(key)

        param_list.insert(0, "year")
        param_list.insert(0, "RECID")

        # construct list of values for params
        param_vals = []
        for param in param_list:
            val = self.params.to_array(param)
            param_vals.append(val)

        # store values as dataframe
        self.ivar = pd.DataFrame(param_vals).transpose()

        return self.ivar, self.mtr_options, self.reform_options

    def batch_inputs(self, ivar):
        """
        Translates string parameters to integers for Batch processing.
        """
        self.batch_ivar = ivar
        # convert mstat to int
        mstat = ivar.loc[:, 2]
        # Single -> 1; Joint -> 2
        mstat_int = np.where(mstat == "Single", 1, 2)
        # convert sstb to int
        sstb = ivar.loc[:, 16]
        # True -> 1; False -> 0
        sstb_int = np.where(sstb, 1, 0)
        self.batch_ivar.loc[:, 2] = mstat_int
        self.batch_ivar.loc[:, 16] = sstb_int
        return self.batch_ivar

    def translate(self, ivar):
        """
        Translate TAXSIM-27 input variables into Tax-Calculator input variables.

        Returns:
            self.invar: a Pandas dataframe with Tax-Calculator variables
        """
        self.invar = pd.DataFrame()
        self.invar["RECID"] = ivar.loc[:, 0]
        self.invar["FLPDYR"] = ivar.loc[:, 1]
        # no Tax-Calculator use of TAXSIM variable 3, state code
        mstat = ivar.loc[:, 2]
        self.invar["age_head"] = ivar.loc[:, 3]
        self.invar["age_spouse"] = ivar.loc[:, 4]

        nu06 = ivar.loc[:, 5] #TAX CRUNCH -- NUMBER OF CHILDREN UNDER 6  FIX .loc still
        self.invar["nu06"] = nu06 # TAXCALC -- NUMBER OF CHILDREN UNDER 6
        nu13 = ivar.loc[:, 6] #TAX CRUNCH -- NUMBER OF CHILDREN 6-12
        self.invar["f2441"] = nu06 + nu13 #CDCTC eligible dependents
        n1316 = ivar.loc[:, 7] #TAX CRUNCH -- NUMBER OF CHILDREN 13-16
        n17 = ivar.loc[:, 8] #TAX CRUNCH -- NUMBER OF CHILDREN 17  FIX .loc still
        self.invar["nu18"] = nu06 + nu13 + n1316 + n17 # TAXCALC -- NUMBER OF CHILDREN UNDER 18
        self.invar["n24"] = nu06 + nu13 + n1316 # TAXCALC -- CTC NUMBER OF CHILDREN UNDER 17
        n1819 = ivar.loc[:, 9] #TAX CRUNCH -- NUMBER OF CHILDREN 18 AND 19-24 fts  FIX .loc still          
        num_eitc_qualified_kids = nu06 + nu13 + n1316 + n17 + n1819

        self.invar["EIC"] = np.minimum(num_eitc_qualified_kids, 3) #number of EIC qualifying children (range: 0 to 3)
        other_dep = ivar.loc[:, 10]
        num_deps = num_eitc_qualified_kids + other_dep
        # convert both Cruncher and Batch inputs (i.e. Single/Joint
        # and 0/1)
        mars = np.where( #[1=single, 2=joint, 3=separate, 4=household-head, 5=widow(er)]
            np.logical_or(mstat.astype(str) == "Single", mstat == 1),
            np.where(num_deps > 0, 4, 1),
            2,
        )
        self.invar["MARS"] = mars
        assert np.all(np.logical_or(mars == 1, np.logical_or(mars == 2, mars == 4)))
        num_taxpayers = np.where(mars == 2, 2, 1) #[1=single, 2=joint, 3=separate, 4=household-head, 5=widow(er)]
        self.invar["XTOT"] = num_taxpayers + num_deps
        self.invar["e00200p"] = ivar.loc[:, 11] #Wages, salaries, and tips for filing unit net of pension contributions Payer
        self.invar["e00200s"] = ivar.loc[:, 12] #Wages, salaries, and tips for filing unit net of pension contributions Spouse
        self.invar["e00200"] = self.invar["e00200p"] + self.invar["e00200s"] #Wages, salaries, and tips for filing unit net of pension contributions
        self.invar["e00650"] = ivar.loc[:, 13] #Qualified dividends included in ordinary dividends
        self.invar["e00600"] = self.invar["e00650"] #Ordinary dividends included in AGI
        self.invar["e00300"] = ivar.loc[:, 14] # Taxable interest income
        self.invar["p22250"] = ivar.loc[:, 15] #Sch D: Net short-term capital gains/losses
        self.invar["p23250"] = ivar.loc[:, 16] #Sch D: Net long-term capital gains/losses
        self.invar["e26270"] = ivar.loc[:, 17] #Sch E: Combined partnership and S-corporation net income/loss
        sstb_bool = ivar.loc[:, 18] # Value of one implies business income is from a specified service trade or business (SSTB)
        # convert both Cruncher and Batch inputs (i.e. True/False and 0/1
        self.invar["PT_SSTB_income"] = np.where(
            np.logical_or(sstb_bool, sstb_bool == 1), 1, 0 #Value of one implies business income is from a specified service trade or business (SSTB)
        )
        self.invar["PT_binc_w2_wages"] = ivar.loc[:, 19] # Filing unit’s share of total W-2 wages paid by the pass-through business
        self.invar["PT_ubia_property"] = ivar.loc[:, 20] # Filing unit’s share of total business property owned by the pass-through business

        e02000 = ivar.loc[:, 21] # Sch E total rental, royalty, partnership, S-corporation, etc, income/loss
        self.invar["e00800"] = ivar.loc[:, 22] # Alimony received
        self.invar["e01700"] = ivar.loc[:, 23] # Taxable pensions and annuities
        self.invar["e01500"] = self.invar["e01700"] # Total pensions and annuities
        self.invar["e02400"] = ivar.loc[:, 24] # Total social security (OASDI) benefits
        self.invar["e02300"] = ivar.loc[:, 25] # Unemployment insurance benefits
        # no Tax-Calculator use of TAXSIM variable 22, non-taxable transfers
        # no Tax-Calculator use of TAXSIM variable 23, rent paid
        self.invar["e18500"] = ivar.loc[:, 26] # Itemizable real-estate taxes paid
        self.invar["e18400"] = ivar.loc[:, 27] # Itemizable state and local income/sales taxes
        self.invar["e32800"] = ivar.loc[:, 28] # Child/dependent-care expenses for qualifying persons from Form 2441
        self.invar["e19200"] = ivar.loc[:, 29] # Itemizable interest paid
        
        # e26270 is included in e02000
        self.invar["e02000"] = self.invar["e26270"] + e02000 #Sch E total rental, royalty, partnership, S-corporation, etc, income/loss
        
        return self.invar

    def choose_mtr(self):
        """
        Creates data to analyze marginal tax rates by adding $1 to the type
            of income specified in 'mtr_options'

        Returns:
            self.ivar2: a Pandas dataframe with Taxsim-style variables
            self.mtr_wrt: User's choice for MTR analysis as a Tax-Calculator variable
        """
        self.ivar2 = self.ivar.copy()
        if self.mtr_options == "Taxpayer Earnings":
            self.ivar2.loc[:, 11] = self.ivar2.loc[:, 11] + 1
            self.mtr_wrt = "e00200p"
            return self.ivar2, self.mtr_wrt
        elif self.mtr_options == "Spouse Earnings":
            self.ivar2.loc[:, 12] = self.ivar2.loc[:, 12] + 1
            return self.ivar2, "e00200s"
        elif self.mtr_options == "Qualified Dividends":
            self.ivar2.loc[:, 13] = self.ivar2.loc[:, 13] + 1
            return self.ivar2, "e00650"
        elif self.mtr_options == "Interest Received":
            self.ivar2.loc[:, 14] = self.ivar2.loc[:, 14] + 1
            return self.ivar2, "e00300"
        elif self.mtr_options == "Short Term Gains":
            self.ivar2.loc[:, 15] = self.ivar2.loc[:, 15] + 1
            return self.ivar2, "p22250"
        elif self.mtr_options == "Long Term Gains":
            self.ivar2.loc[:, 16] = self.ivar2.loc[:, 16] + 1
            return self.ivar2, "p23250"
        elif self.mtr_options == "Business Income":
            self.ivar2.loc[:, 17] = self.ivar2.loc[:, 17] + 1
            return self.ivar2, "e26270"
        elif self.mtr_options == "Pensions":
            self.ivar2.loc[:, 23] = self.ivar2.loc[:, 23] + 1
            return self.ivar2, "e01700"
        elif self.mtr_options == "Gross Social Security Benefits":
            self.ivar2.loc[:, 24] = self.ivar2.loc[:, 24] + 1
            return self.ivar2, "e02400"
        elif self.mtr_options == "Real Estate Taxes Paid":
            self.ivar2.loc[:, 26] = self.ivar2.loc[:, 26] + 1
            return self.ivar2, "e18500"
        elif self.mtr_options == "Mortgage":
            self.ivar2.loc[:, 29] = self.ivar2.loc[:, 29] + 1
            return self.ivar2, "e19200"


    def choose_baseline(self):
        """
        Creates Tax-Calculator Policy object for baseline policy

        The default baseline policy is current law.

        Returns:
            self.pol: Tax-Calculator Policy object for baseline policy
        """
        REFORMS_URL = (
            "https://raw.githubusercontent.com/"
            "PSLmodels/Tax-Calculator/master/taxcalc/reforms/"
        )

        # if no baseline policy is specified, baseline is current law
        if self.baseline is None:
            self.pol = tc.Policy()
        # if a baseline policy is specified, first see if user created json
        # policy file
        else:
            exists = os.path.isfile(self.baseline)
            if exists:
                baseline_file = self.baseline
                self.pol = tc.Policy()
                self.pol.implement_reform(tc.Policy.read_json_reform(baseline_file))
            # if the user did not create a json file, try the Tax-Calculator
            # reforms file
            else:
                try:
                    baseline_file = self.baseline
                    baseline_url = REFORMS_URL + baseline_file
                    self.pol = tc.Policy()
                    self.pol.implement_reform(tc.Policy.read_json_reform(baseline_url))
                except:
                    print("Baseline file does not exist")

        return self.pol

    def choose_reform(self):
        """
        Creates Tax-Calculator Policy object for reform analysis

        Returns:
            self.pol2: Tax-Calculator Policy object for reform analysis
        """
        REFORMS_URL = (
            "https://raw.githubusercontent.com/"
            "PSLmodels/Tax-Calculator/master/taxcalc/reforms/"
        )

        # if user specified a preset reform in their adjustment file, pull
        # reform from Tax-Calculator reforms folder
        if self.reform_options != "None" and self.custom_reform is None:
            reform_name = self.reform_options
            reform_url = REFORMS_URL + reform_name
            self.pol2 = tc.Policy()
            self.pol2.implement_reform(tc.Policy.read_json_reform(reform_url))
        # otherwise, look for user-provided json reform file
        # first as file path
        elif self.reform_options == "None" and isinstance(self.custom_reform, str):
            try:
                reform_filename = self.custom_reform
                self.pol2 = tc.Policy()
                self.pol2.implement_reform(tc.Policy.read_json_reform(reform_filename))
            except:
                print("Reform file path does not exist")
        # then as dictionary
        elif self.reform_options == "None" and isinstance(self.custom_reform, dict):
            reform = self.custom_reform
            self.pol2 = tc.Policy()
            try:
                self.pol2.implement_reform(reform)
            except:
                self.pol2.adjust(reform)
        # raise error if preset reform is chosen and custom reform is specified
        elif self.reform_options != "None" and self.custom_reform is not None:
            raise AttributeError(
                "You have specified a preset reform and a custom reform. Please choose one reform."
            )
        # if no reform file was given, set reform to current law
        else:
            self.pol2 = tc.Policy()

        return self.pol2

    def run_calc(self):
        """
        Creates baseline, reform, and + $1 Tax-Calculator objects

        Returns:
            self.calc1: Calculator object for current law
            self.calc_reform: Calculator object for reform
            self.calc_mtr: Calculator object for + $1
        """

        year = int(self.data.iloc[0][1])
        recs = tc.Records(data=self.data, start_year=year, gfactors=None, weights=None)

        self.calc1 = tc.Calculator(policy=self.pol, records=recs)
        self.calc1.advance_to_year(year)
        self.calc1.calc_all()

        self.calc_reform = tc.Calculator(policy=self.pol2, records=recs)
        self.calc_reform.advance_to_year(year)
        self.calc_reform.calc_all()

        recs_mtr = tc.Records(
            data=self.data_mtr, start_year=year, gfactors=None, weights=None
        )
        self.calc_mtr = tc.Calculator(policy=self.pol2, records=recs_mtr)
        self.calc_mtr.advance_to_year(year)
        self.calc_mtr.calc_all()

        return self.calc1, self.calc_reform, self.calc_mtr

    def basic_vals(self):
        """
        Creates basic output table

        Returns:
            self.basic_vals: a Pandas dataframe with basic results
        """

        basic = ["iitax", "payrolltax"]
        basic_vals1 = self.calc1.dataframe(basic)
        basic_vals1 = basic_vals1.transpose()

        basic_vals2 = self.calc_reform.dataframe(basic)
        basic_vals2 = basic_vals2.transpose()

        self.basic_vals = pd.concat([basic_vals1, basic_vals2], axis=1)
        self.basic_vals.columns = ["Previous Law", "American Rescue Plan"]
        self.basic_vals.index = [
            "Individual Income Tax",
            "Employee + Employer Payroll Tax",
        ]

        self.basic_vals["Change"] = self.basic_vals["American Rescue Plan"] - self.basic_vals["Previous Law"]

        self.basic_vals = self.basic_vals.round(2)

        return self.basic_vals

    def mtr_table(self):
        """
        Creates MTR table

        Returns:
            self.df_mtr: a Pandas dataframe MTR results with respect to 'mtr_options'
        """

        mtr_calc = self.calc1.mtr(
            calc_all_already_called=True, wrt_full_compensation=False
        )
        self.mtr_df = pd.DataFrame(
            data=[mtr_calc[1], mtr_calc[0]],
            index=["Income Tax Marginal Rate", "Payroll Tax Marginal Rate"],
        )

        mtr_calc_reform = self.calc_reform.mtr(
            calc_all_already_called=True, wrt_full_compensation=False
        )
        mtr_df_reform = pd.DataFrame(
            data=[mtr_calc_reform[1], mtr_calc_reform[0]],
            index=["Income Tax Marginal Rate", "Payroll Tax Marginal Rate"],
        )

        self.df_mtr = pd.concat([self.mtr_df, mtr_df_reform], axis=1)
        self.df_mtr.columns = ["Previous Law", "American Rescue Plan"]
        # convert decimals to percents
        self.df_mtr = self.df_mtr * 100

        self.df_mtr["Change"] = self.df_mtr["American Rescue Plan"] - self.df_mtr["Previous Law"]

        return self.df_mtr

    def basic_table(self):
        """
        Combines output from basic_vals() and mtr_table() to create table with basic output

        Returns:
            self.df_mtr: a Pandas dataframe with basic output
        """
        self.df_basic = pd.concat(
            [
                self.df_basic_vals.iloc[:1],
                self.df_mtr.iloc[:1],
                self.df_basic_vals.iloc[1:],
                self.df_mtr.iloc[1:],
            ]
        )

        # format each row
        self.df_basic.iloc[0, :] = self.df_basic.iloc[0, :].apply(
            lambda x: "{:,.2f}".format(x)
        )
        self.df_basic.iloc[1, :] = self.df_basic.iloc[1, :].apply(
            lambda x: "{:,.2f}".format(x)
        )
        self.df_basic.iloc[2, :] = self.df_basic.iloc[2, :].apply(
            lambda x: "{:,.2f}".format(x)
        )
        self.df_basic.iloc[3, :] = self.df_basic.iloc[3, :].apply(
            lambda x: "{:,.2f}".format(x)
        )

        return self.df_basic

    def calc_table(self):
        """
        Creates detailed output table

        Returns:
            self.df_calc: a Pandas dataframe with federal tax calculations for base, reform, and + $1

        """
        calculation = [
            "c00100",
            "e02300",
            "c02500",
            "standard",
            "c04470",
            "qbided",
            "c04800",
            "taxbc",
            "c07220",
            "c11070",
            "c07180",
            "eitc",
            "recoveryrebate",
            "c62100",
            "c09600",
            "niit",
            "c05800",
            "payrolltax"
        ]
        labels = [
            "Adjusted Gross Income (AGI)",
            "Unemployment Insurance in AGI",
            "Social Security in AGI",
            "Standard Deduction (Zero for Itemizers)",
            "Itemized Deductions",
            "Qualified Business Income Deduction",
            "Taxable Income",
            "Income Tax Liability Before Credits",
            "Non-Refundable Child Tax Credit (CTC)",
            "Refundable Child Tax Credit",
            "Child and Dependent Care Tax Credit (CDCTC)",
            "Earned Income Tax Credit (EITC)",
            "Recovery Rebate Credit (Stimulus Check)",
            "Alternative Minimum Tax (AMT) Taxable Income",
            "AMT Liability",
            "Net Investment Income Tax",
            "Income Tax Before Credits (Regular + AMT)",
            "Payroll Tax (Employee + Employer)"
        ]

        df_calc1 = self.calc1.dataframe(calculation).transpose()

        df_calc2 = self.calc_reform.dataframe(calculation).transpose()

        # df_calc_mtr = self.calc_mtr.dataframe(calculation).transpose()

        self.df_calc = pd.concat([df_calc1, df_calc2], axis=1)

        # mtr_label = "+ $1 ({})".format(self.mtr_options)

        self.df_calc.columns = ["Previous Law", "American Rescue Plan"]
        self.df_calc.index = labels

        twostepctc = self.calc_reform.array("twostepctc")
        cdcc_new = self.calc_reform.array("cdcc_new")

        self.df_calc["American Rescue Plan"]["Refundable Child Tax Credit"] = twostepctc
        self.df_calc["American Rescue Plan"]["Child and Dependent Care Tax Credit (CDCTC)"] = cdcc_new

        self.df_calc["Previous Law"] = self.df_calc["Previous Law"].apply(lambda x: "{:,.2f}".format(x))
        self.df_calc["American Rescue Plan"] = self.df_calc["American Rescue Plan"].apply(lambda x: "{:,.2f}".format(x))

        return self.df_calc

    def calc_diff_table(self):
        """
        Creates detailed output table. Instead of column for MTR analysis, column displays difference
            between baseline and reform amounts

        Returns:
            self.df_calc_diff: a Pandas dataframe with federal tax calculations for base, reform, and change

        """
        self.df_calc_diff = self.df_calc.copy()
        if len(self.df_calc_diff.columns) == 3:
            del self.df_calc_diff["+ $1"]
        calc_diff_vals = self.df_calc_diff["American Rescue Plan"] - self.df_calc_diff["Previous Law"]
        self.df_calc_diff["Change"] = calc_diff_vals
        return self.df_calc_diff
