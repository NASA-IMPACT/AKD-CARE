# cmr_collection_search — Response Patterns

| Scenario | Condition | File |
|----------|-----------|------|
| no_results | hits == 0 for the given keyword/variable combination | no_results.md |
| incomplete_metadata | One or more key UMM fields (Abstract, TemporalExtents, Spati... | incomplete_metadata.md |
| too_many_results | hits > 50 and researcher has specified temporal or spatial c... | too_many_results.md |
| success | hits > 0 and response parses successfully | success.md |
