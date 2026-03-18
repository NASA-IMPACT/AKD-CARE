**Paper Search endpoint:** GET /graph/v1/paper/search

| Parameter | Type    | Required | Notes                                              |
|-----------|---------|----------|----------------------------------------------------|
| query     | string  | Yes      | Science question keywords (5–10 words recommended) |
| limit     | integer | No       | Number of results; 5–10 recommended                |
| fields    | string  | No       | Comma-separated: title,abstract,year,doi,topics,citationCount |

**Paper Detail endpoint:** GET /graph/v1/paper/{paperId}

| Parameter | Type   | Required | Notes                              |
|-----------|--------|----------|------------------------------------|
| paperId   | string | Yes      | ID from paper search result        |
| fields    | string | No       | Same field list as above           |

Rate limit constraint: insert 1-second delay between consecutive requests.
