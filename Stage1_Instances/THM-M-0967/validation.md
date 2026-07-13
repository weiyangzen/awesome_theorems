# THM-M-0967 intake validation

Validation date: 2026-07-13 (Asia/Shanghai). This is nonrelease evidence from an isolated dirty
worker clone at base commit `fcabbf1e0ad9507eebe91663bccabfa87d22813e`, tree
`873e589c594454b7f263c7ed2342089a4d15e842`. The initial worktree contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was reused read-only; no
dependency update, build, clone, fetch, or `.lake` mutation was run.

## Commands and results

| Command | Exit | Result and boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, exactly 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0967` | 0 | rank 1501; planned; no legacy slot; legacy artifacts unaccepted; theorem-complete false |
| `git status --short --untracked-files=all` | 0 | initial status contained only `Formalizations/Lean/.lake`; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base commit and tree recorded above |
| `git blame -L 7064,7069 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded source-discovery commands below | mixed as recorded | likely primary bibliographic identity and a secondary abstract found; article text was not inspected, so no exact source or H0 claim |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| exact bounded Lean search below | 0 | no exact Kneser-graph theorem; only one irrelevant additive Freiman-Kneser URL matched; this is intake discovery, not exhaustive absence evidence |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0967/IntakeProbe.lean` | 0 | fixed-cardinality subsets, disjointness graph, and coloring interfaces elaborated; axiom reports recorded; stdout SHA-256 `28cd7a45b7dea7b13c9e0062a2990bb84f747256a854e83412d84d7b19752357`; no theorem or proof body |
| final JSON, scoped checker, prohibited-construct, and whitespace commands below | 0 | all final intake checks passed |

## Exact discovery commands

The following networked calls were mutable source discovery only. They are not the two denied-
network structured validation recipes in the provisional receipt.

```bash
curl -L --max-time 30 -sS 'https://api.crossref.org/works/10.1016%2F0097-3165%2878%2990022-5'
curl -L --max-time 30 -sS 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/0097-3165(78)90022-5?fields=title,authors,year,venue,publicationTypes,publicationDate,openAccessPdf,externalIds,url,abstract'
curl -L --max-time 30 -sS 'https://api.core.ac.uk/v3/search/works?q=doi%3A%2210.1016%2F0097-3165%2878%2990022-5%22&limit=10'
curl -L --max-time 30 -sS 'https://export.arxiv.org/api/query?search_query=all%3A%22Kneser%27s%20conjecture%2C%20chromatic%20number%2C%20and%20homotopy%22&start=0&max_results=10'
```

Crossref, Semantic Scholar, and CORE returned matching bibliographic/abstract metadata with exit 0.
The arXiv call returned exit 0 with zero results. Attempts to inspect the Elsevier full text returned
an API input error or an HTML landing page rather than article text. OpenAlex returned a rate-limit
error, Unpaywall rejected the non-personal API email parameter, and broad web searches timed out or failed to
connect. None of these failures is used as evidence of source absence.

The exact bounded formal search was:

```bash
rg -n -i --glob '*.lean' '\bkneser\b|kneserGraph|kneser_graph|KneserGraph|Lovasz.*Kneser|Lovász.*Kneser' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems
```

## Exact final checks

```bash
python3 -m json.tool Stage1_Instances/THM-M-0967/instance.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0967/task-dag.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-0967/intake-receipt.json >/dev/null
python3 -m json.tool .stage1-worker-selftest.json >/dev/null
python3 -B Stage1_Instances/THM-M-0967/check_intake.py --worker-packet .stage1-worker-selftest.json
python3 -B Stage1_Instances/THM-M-0967/check_intake.py
if rg -n --glob '*.lean' '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0967; then exit 1; else echo 'prohibited Lean construct scan: no matches'; fi
git diff --check
for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0967/*; do out=$(git diff --no-index --check /dev/null "$f" 2>&1); rc=$?; test -z "$out" && test "$rc" -eq 1 || { printf '%s\n' "$out"; exit 1; }; done
```

## Source and machine boundary

The publication metadata and secondary abstract support a provisional `H1` classification, not
`H0`: no exact primary statement, definition chain, assumptions, proof boundary, correction audit,
or independent crosswalk is accepted. The Lean probe checks adjacent substrate and a candidate
graph definition only. It does not elaborate the canonical theorem target and gives no machine-
proof credit. The provisional root vector is `[H1,M4,R4]`.

## Status boundary

This validation covers only a `planned` intake proposal. Its receipt is unsigned, provisional, and
not content-addressed validation authority. All downstream tasks, audit completion, theorem
completion, and master acceptance remain open. Exact statement elaboration, fingerprints,
transports, and mutations are deliberately left to the dependent statement node rather than being
fabricated from an underspecified catalog gloss.
