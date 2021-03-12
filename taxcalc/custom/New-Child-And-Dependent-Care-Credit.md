# New Child and Dependent Care Credit

#### File Author:
*Grant M. Seiter · American Enterprise Institute* (March 2021)

#### Notes: 
The Child and Dependent Care Tax Credit Expansion Passed by the Senate on 03/06/2021 as part of H.R.1319 - American Rescue Plan Act of 2021.

#### Description: 
For households earning less than $125,000 annually, the child and dependent care tax credit would be made refundable tax credit of up to half a family's child care costs. It would max out at $8,000 for one child or $16,000 for two or more children. Families earning between $125,000 and $400,000 will qualify for partial credits. (Note for revenue estimates: this variable is limited by PUF e32800 cap at $6000)

### policy_current_law.json
```json
"CDCC_new_c": {
    "title": "Maximum new child & dependent care refundable credit per dependent (max of CDCC_new_c*2 for two or more children)",
    "description": "The maximum amount of refundable credit allowed for each qualifying dependent.",
    "notes": "This parameter is not reflected in current law.",
    "section_1": "Refundable Credits",
    "section_2": "New Child And Dependent Care",
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
    "CDCC_new_rt": {
        "title": "New child & dependent care refundable credit rate",
        "description": "This is the fraction of eligible child and dependent care expenses used in calculating CDCC_new.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "New Child And Dependent Care",
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
                "max": 1
            }
        },
        "compatible_data": {
            "puf": true,
            "cps": true
        }
    },
    "CDCC_new_ps": {
        "title": "New child & dependent care credit phaseout start",
        "description": "For taxpayers with AGI over this amount, the credit is reduced.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "New Child And Dependent Care",
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
    "CDCC_new_pe": {
        "title": "New child & dependent care credit phaseout end",
        "description": "For taxpayers with AGI over this amount, the credit is disallowed.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "New Child And Dependent Care",
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
    "CDCC_new_prt": {
        "title": "New child & dependent care refundable credit phaseout rate",
        "description": "The total amount for the new child and dependent care credit is reduced at this rate per dollar exceeding the phaseout starting agi.",
        "notes": "This parameter is not reflected in current law.",
        "section_1": "Refundable Credits",
        "section_2": "New Child And Dependent Care",
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
                "max": 1
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
"cdcc_new": {
  "type": "float",
  "desc": "Refundable new child and dependent care credit",
  "form": {"2013-20??": "calculated variable"},
  "availability": "taxdata_puf, taxdata_cps"
},
```

### records.py
```python
NONE
```

### data.py
```python
NONE
```

### calcfunctions.py
```python
@iterate_jit(nopython=True)
def CDCC_new(CDCC_new_c, CDCC_new_rt, CDCC_new_ps, CDCC_new_pe, CDCC_new_prt, cdcc_new,
            MARS, f2441, e32800, earned_s, earned_p, c05800, e07300, c00100):
    """
    Calculates new refundable child and dependent care expense credit, cdcc_new.
    """
    # credit for at most two cared-for individuals and for actual expenses
    cdcc_new_max_credit = min(f2441, 2) * CDCC_new_c
    cdcc_new = max(0., min(e32800 * CDCC_new_rt, cdcc_new_max_credit))
    # phaseout based on agi
    positiveagi = max(c00100, 0.)
    cdcc_min = CDCC_new_ps[MARS - 1]
    if positiveagi < cdcc_min:
        cdcc_new = cdcc_new
    else:
        cdcc_new_reduced = max(0., cdcc_new - (CDCC_new_prt * (positiveagi - cdcc_min)))
        cdcc_new = min(cdcc_new, cdcc_new_reduced)
    return cdcc_new


@iterate_jit(nopython=True)
def IITAX(c59660, c11070, c10960, personal_refundable_credit, ctc_new, rptc,
          c09200, payrolltax, recoveryrebate, twostepctc, cdcc_new,
          eitc, refund, iitax, combined):
    """
    Computes final taxes.
    """
    eitc = c59660
    refund = (eitc + c11070 + c10960 +
              personal_refundable_credit + ctc_new + rptc + recoveryrebate + twostepctc + cdcc_new)
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
                                   CDCC_new,
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
        CDCC_new(self.__policy, self.__records)
        C1040(self.__policy, self.__records)
        CTC_new(self.__policy, self.__records)
        IITAX(self.__policy, self.__records)
```
