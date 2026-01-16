# Phase 5: Benchmarking and Verification

Phase 5 defines requirements for constructing a benchmark of realistic queries and defines scoring rubrics and pass/fail thresholds.

In Phase 5, helper agents elicit responses from SMEs to identify potential sources that can be used to automate or semi-automate benchmark construction (e.g., types of queries, target answer types), and the resulting benchmark requirements artifact is then used by a separate agent-based workflow to generate the benchmark.

For example, to create a data search benchmark, the auxiliary workflow can identify papers that can be used to draft different queries based on each paper and extract answers (i.e. data used) to those queries, after which evaluation can be integrated into the engineering loop.

Phase 5 separates benchmark requirements (human-informed) from benchmark generation (auxiliary workflow) so evaluation becomes systematic.
