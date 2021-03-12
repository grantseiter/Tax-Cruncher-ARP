# Two-Step-Child-Tax-Credit

#### File Author:
*Grant M. Seiter · American Enterprise Institute* (March 2021)

#### Notes: 
The Child Tax Credit Expansion Passed by the Senate on 03/06/2021 as part of H.R.1319 - American Rescue Plan Act of 2021.

#### Description:
The child tax credit is increased from $2,000 to $3,000 for 2021. In the case of a qualifying child who has not attained the age of 6 as of the close of the calendar year, the credit is increased to $3,600. In addition, the term “qualifying child” is broadened to include a qualifying child who has not attained the age of 18 (instead of 17). Finally, the child tax credit amount is subject to a second phaseout, which applies in addition to the phaseout under present law. The second phaseout applies to taxpayers with income above an applicable threshold amount. The applicable threshold amounts are lower than those under the present-law child tax credit phaseout: $150,000 for taxpayers filing jointly (as compared to $400,000 for the present-law phaseout), $150,000 for surviving spouses (as compared to $200,000), $112,500 for head of household taxpayers (as compared to $200,000), and $75,000 for all other taxpayers (as compared to $200,000). The amount of child tax credit is reduced by $50 for each $1,000 (or fraction thereof) of modified AGI over the applicable threshold amount. However, the additional phaseout is limited so that it only applies to the temporary increased child tax credit for 2021 ($1,600 per child under age 6 and $1,000 per child age 6 and older); it does not reduce the child tax credit amount provided to a taxpayer under present law.

### policy_current_law.json
```json
 "CTC_2Step_c1": {
        "title": "Two Step refundable child tax credit maximum amount per child",
        "description": "In addition to all credits currently available for dependents, this parameter gives each qualifying child a Two Step refundable credit with this maximum amount (step 1).",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_c1_under6_bonus": {
        "title": "Bonus Two Step refundable child tax credit maximum for qualifying children under defined age threshold",
        "description": "This parameter is not reflected in current law.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_ps1": {
        "title": "Two Step refundable child tax credit phaseout starting AGI",
        "description": "The total amount of Two Step child tax credit step 1 is reduced for taxpayers with AGI higher than this level.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "MARS": "single",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "mjoint",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "mseparate",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "headhh",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "widow",
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_prt1": {
        "title": "Two Step refundable child tax credit amount phase out rate",
        "description": "The maximum amount of the Two Step child tax credit step 1 is is reduced at this rate per dollar exceeding the phaseout starting AGI.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": false,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
     "CTC_2Step_c2": {
        "title": "Two Step refundable child tax credit maximum amount per child",
        "description": "In addition to all credits currently available for dependents, this parameter gives each qualifying child a Two Step refundable credit with this maximum amount (step 2).",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_c2_under6_bonus": {
        "title": "Bonus Two Step refundable child tax credit maximum for qualifying children under defined age threshold",
        "description": "The maximum amount of the Two Step refundable child tax credit step 2 allowed for each child is increased by this amount for qualifying children under 6 years old.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_ps2": {
        "title": "Two Step refundable child tax credit phaseout starting AGI",
        "description": "The total amount of Two Step child tax credit step 2 is reduced for taxpayers with AGI higher than this level.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": true,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "MARS": "single",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "mjoint",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "mseparate",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "headhh",
                "value": 0.0
            },
            {
                "year": 2013,
                "MARS": "widow",
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_prt2": {
        "title": "Two Step refundable child tax credit amount phase out rate",
        "description": "The maximum amount of the Two Step child tax credit step 2 is is reduced at this rate per dollar exceeding the phaseout starting AGI.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": false,
        "indexed": false,
        "type": "float",
        "value": [
            {
                "year": 2013,
                "value": 0.0
            }
        ],
        "validators": {
            "range": {
                "min": 0,
                "max": 9e+99
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CTC_2Step_Age": {
        "title": "Whether or not maximum amount of the new refundable child tax credit is available to 17 year olds.",
        "description": "If True, this substitutes n24 with n24 + max(0,XTOT-n24-n1820 -n21 -num).",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "Two Step Refundable Child Tax Credit",
        "indexable": false,
        "indexed": false,
        "type": "bool",
        "value": [
            {
                "year": 2013,
                "value": false
            }
        ],
        "validators": {
            "range": {
                "min": false,
                "max": true
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
```

### records_variables.json
```json
"twostepctc": {
	"type": "float",
	"desc": "search taxcalc/calcfunctions.py for how calculated and used",
	"form": {"2013-20??": "calculated variable"}
},
```

### records.py
```python
NONE
```

### calcfunctions.py
```python
@iterate_jit(nopython=True)
def TwoStepChildTaxCredit(n24, nu06, nu18, MARS, c00100,
                   CTC_2Step_c1, CTC_2Step_c1_under6_bonus,
                   CTC_2Step_ps1, CTC_2Step_prt1,
                   CTC_2Step_c2, CTC_2Step_c2_under6_bonus,
                   CTC_2Step_ps2, CTC_2Step_prt2, CTC_2Step_Age,
                   XTOT, n1820, n21, num):
    """
    Computes the proposed refundable child tax credit Scheduled For Markup by The
    House Committee on Ways and Means on February 10, 2021.
    """
    if not CTC_2Step_Age:
        if n24 > 0:
            step1 = CTC_2Step_c1 * nu18 + CTC_2Step_c1_under6_bonus * nu06
            step2 = CTC_2Step_c2 * nu18 + CTC_2Step_c2_under6_bonus * nu06
            posagi = max(c00100, 0.)
            ymax1 = CTC_2Step_ps1[MARS - 1]
            ymax2 = CTC_2Step_ps2[MARS - 1]
            if posagi > ymax1:
                step1_reduced = max(step2, step1 - CTC_2Step_prt1 * (posagi - ymax1))
                if posagi > ymax2:
                    step2_reduced = max(0., step1_reduced - CTC_2Step_prt2 * (posagi - ymax2))
                    twostepctc = min(step1_reduced, step2_reduced)
                else:
                    step2_reduced = max(0., step1_reduced)
                    twostepctc = min(step1_reduced, step2_reduced)
            else:
                twostepctc = max(0., step1)
        else:
            twostepctc = 0.
    else:
        if (n24 + max(0,XTOT - n24 -n1820 -n21 - num)) > 0:
            step1 = CTC_2Step_c1 * (n24 + max(0,XTOT - n24 -n1820 -n21 - num)) + CTC_2Step_c1_under6_bonus * nu06
            step2 = CTC_2Step_c2 * (n24 + max(0,XTOT - n24 -n1820 -n21 - num)) + CTC_2Step_c2_under6_bonus * nu06
            posagi = max(c00100, 0.)
            ymax1 = CTC_2Step_ps1[MARS - 1]
            ymax2 = CTC_2Step_ps2[MARS - 1]
            if posagi > ymax1:
                step1_reduced = max(step2, step1 - CTC_2Step_prt1 * (posagi - ymax1))
                if posagi > ymax2:
                    step2_reduced = max(0., step1_reduced - CTC_2Step_prt2 * (posagi - ymax2))
                    twostepctc = min(step1_reduced, step2_reduced)
                else:
                    step2_reduced = max(0., step1_reduced)
                    twostepctc = min(step1_reduced, step2_reduced)
            else:
                twostepctc = max(0., step1)
        else:
            twostepctc = 0.
    return twostepctc


@iterate_jit(nopython=True)
def IITAX(c59660, c11070, c10960, personal_refundable_credit, ctc_new, rptc,
          c09200, payrolltax, recoveryrebate, twostepctc,
          eitc, refund, iitax, combined):
    """
    Computes final taxes.
    """
    eitc = c59660
    refund = (eitc + c11070 + c10960 +
              personal_refundable_credit + ctc_new + rptc + recoveryrebate + twostepctc)
    iitax = c09200 - refund
    combined = iitax + payrolltax
    return (eitc, refund, iitax, combined)
```

### calculator.py
```python
from taxcalc.calcfunctions import (TaxInc, SchXYZTax, GainsTax, AGIsurtax,
                                   NetInvIncTax, AMT, EI_PayrollTax, Adj,
                                   DependentCare, ALD_InvInc_ec_base, CapGains,
                                   SSBenefits, UBI, AGI, ItemDedCap, ItemDed,
                                   StdDed, AdditionalMedicareTax, F2441, EITC,
                                   RefundablePayrollTaxCredit,
                                   ChildDepTaxCredit, AdditionalCTC, CTC_new,
                                   Recovery_Rebate, TwoStepChildTaxCredit,
                                   PersonalTaxCredit, SchR,
                                   AmOppCreditParts, EducationTaxCredit,
                                   CharityCredit,
                                   NonrefundableCredits, C1040, IITAX,
                                   BenefitSurtax, BenefitLimitation,
                                   FairShareTax, LumpSumTax, BenefitPrograms,
                                   ExpandIncome, AfterTaxIncome)


   # Calculate taxes with optimal itemized deduction
        self._taxinc_to_amt()
        F2441(self.__policy, self.__records)
        EITC(self.__policy, self.__records)
        RefundablePayrollTaxCredit(self.__policy, self.__records)
        PersonalTaxCredit(self.__policy, self.__records)
        AmOppCreditParts(self.__policy, self.__records)
        SchR(self.__policy, self.__records)
        EducationTaxCredit(self.__policy, self.__records)
        CharityCredit(self.__policy, self.__records)
        ChildDepTaxCredit(self.__policy, self.__records)
        NonrefundableCredits(self.__policy, self.__records)
        AdditionalCTC(self.__policy, self.__records)
        Recovery_Rebate(self.__policy, self.__records)
        TwoStepChildTaxCredit(self.__policy, self.__records)
        C1040(self.__policy, self.__records)
        CTC_new(self.__policy, self.__records)
        IITAX(self.__policy, self.__records)
```