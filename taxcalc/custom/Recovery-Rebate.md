# Recovery Rebate For Individuals

#### File Author:
*Grant M. Seiter · American Enterprise Institute* (March 2021)

#### Notes: 
The Recovery Rebates to Individuals Passed by the Senate on 03/06/2021 as part of H.R.1319 - American Rescue Plan Act of 2021.

#### Description: 
The senate passed an amended $1.9 trillion COVID-19 stimulus bill (H.R. 1319) that includes an additional $1400 recovery rebate (per eligible individual) that would phase out more quickly than in the two previous rounds. For single taxpayers, the phaseout will begin at an adjusted gross income (AGI) of $75,000 and the credit will be completely phased out for taxpayers with an AGI over $80,000 ($28 for every $1000). For married taxpayers who file jointly, the phaseout will begin at an AGI of $150,000 and end at AGI of $160,000. And for heads of households, the phaseout will begin at an AGI of $112,500 and be complete at AGI of $120,000. Under the current bill, rebates are reduced to zero for taxpayers with AGI above the phaseout end, regardless of the number of dependents.

### policy_current_law.json
```json
"Rebate_c": {
    "title": "Maximum recovery rebate per eligible person",
    "description": "The maximum amount of the refundable credit allowed for each eligible person.",
    "notes": "",
    "section_1": "Refundable Credits",
    "section_2": "Recovery Rebate",
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
    "Rebate_ps": {
        "title": "Recovery rebate phaseout start",
        "description": "For taxpayers with AGI over this amount, the refundable credit is reduced.",
        "notes": "",
        "section_1": "Refundable Credits",
        "section_2": "Recovery Rebate",
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
    "Rebate_pe": {
        "title": "Recovery rebate phaseout end",
        "description": "For taxpayers with AGI over this amount, the refundable credit is reduced to 0.",
        "notes": "",
        "section_1": "Refundable Credits",
        "section_2": "Recovery Rebate",
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
    "Rebate_prt": {
        "title": "Recovery rebate phaseout rate",
        "description": "The total amount of the refunable credit is reduced at this rate per dollar exceeding the phaseout starting agi.",
        "notes": "",
        "section_1": "Refundable Credits",
        "section_2": "Recovery Rebate",
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
"recoveryrebate": {
  "type": "float",
  "desc": "Recovery rebates to individuals",
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
def Recovery_Rebate(Rebate_c, Rebate_ps, Rebate_pe, Rebate_prt, XTOT, DSI,
            MARS, c00100):
    """
    Calculates recovery rebate for individuals, recoveryrebate.
    """
    # credit for qualifying individuals
    if DSI:
        rebate_max_credit = 0.
    else:
        rebate_max_credit = XTOT * Rebate_c
    # phaseout based on agi
    positiveagi = max(c00100, 0.)
    rebate_min = Rebate_ps[MARS - 1]
    rebate_max = Rebate_pe[MARS - 1]
    if positiveagi < rebate_min:
        recoveryrebate = rebate_max_credit
    else:
        if positiveagi > rebate_max:
            recoveryrebate = 0.
        else:
            rebate_reduced = max(0., rebate_max_credit - (Rebate_prt * (positiveagi - rebate_min)))
            recoveryrebate = min(rebate_max_credit, rebate_reduced)
    return recoveryrebate


@iterate_jit(nopython=True)
def IITAX(c59660, c11070, c10960, personal_refundable_credit, ctc_new, rptc,
          c09200, payrolltax, recoveryrebate,
          eitc, refund, iitax, combined):
    """
    Computes final taxes.
    """
    eitc = c59660
    refund = (eitc + c11070 + c10960 +
              personal_refundable_credit + ctc_new + rptc + recoveryrebate)
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
                                   Recovery_Rebate,
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
        C1040(self.__policy, self.__records)
        CTC_new(self.__policy, self.__records)
        IITAX(self.__policy, self.__records)
```
