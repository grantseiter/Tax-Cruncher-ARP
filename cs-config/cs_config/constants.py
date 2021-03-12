import paramtools
from marshmallow import fields, Schema

class MetaParameters(paramtools.Parameters):
    array_first = True
    defaults = {
        "year": {
            "title": "Year",
            "description": "Tax Year Selection.",
            "type": "int",
            "value": 2021,
            "validators": {
                "choice": {
                    "choices": [
                        yr for yr in range(2021, 2021 + 1)
                    ]
                }
            }
        }
    }
