| Parameter     | Type    | Required | Notes                                                        |
|---------------|---------|----------|--------------------------------------------------------------|
| keyword       | string  | Yes      | Targeted free-text term(s) derived from science question — must be specific enough that the best match ranks first |
| variable_name | string  | No       | Variable name(s) inferred from question or literature        |
| short_name    | string  | No       | Dataset short name if known (retrieve via CMR keyword search)|
| instrument    | string  | No       | Instrument filter                                            |
| temporal[]    | array   | No       | ISO timestamps: `temporal[]=start,end`                       |
| spatial[]     | array   | No       | Bounding box; if omitted → global search                     |
| page_size     | integer | No       | Always set to 1. Query must be targeted enough to surface the best result first. |

Always request UMM-JSON format (umm_json=true).
Do not paginate — if the top result is not relevant, reformulate the query rather than fetching more pages.
