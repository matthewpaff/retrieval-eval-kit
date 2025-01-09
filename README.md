# Retrieval Eval Kit

Calculate recall at a supplied cutoff and reciprocal rank for recorded retrieval results.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external service, or network access is required.

## Run

```console
python -m evaluation_tool --help
python -m evaluation_tool examples/sample.json
python -m evaluation_tool --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires k (1–100) and queries [{id,relevant,ranked}]. IDs must be unique within each list and query set. Recall@k is relevant hits in the first k results divided by relevant count; reciprocal rank@k is the first relevant result's inverse rank within k. Empty relevance sets score zero and are included in macro averages; an empty query set has zero aggregates. Metrics round to six decimals. No embeddings, search engine, or quality claims about a provider are supplied.

## Learning focus

User-directed personal AI/LLM/agent exploration. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `evaluation_tool/core.py`: validated parsing, storage, or state transitions.
- `evaluation_tool/cli.py`: JSON command interface.
- `evaluation_tool/generate_fixtures.py`: original deterministic validation cases.
- `evaluation_tool/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 260 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
