| Parameter      | Type   | Required | Notes                                                          |
|----------------|--------|----------|----------------------------------------------------------------|
| concept_scheme | string | Yes      | One of: sciencekeywords, instruments, platforms                |
| query_term     | string | Yes      | Free-text term to look up or normalize                         |
| format         | string | No       | Response format: json (default), xml, csv                      |

Science Keyword fields to extract:
- Category, Topic, Term
- Variable_Level_1, Variable_Level_2, Variable_Level_3
- Detailed_Variable (if present)

Instrument / Platform fields to extract:
- Short_Name, Long_Name, Associated URIs
