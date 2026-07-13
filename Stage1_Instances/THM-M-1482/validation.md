# THM-M-1482 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic source-lead metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, genetic-algorithm definition, Holland schema theorem,
convergence or optimality result, implementation, proof, accepted receipt, audit completion, or
theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified.

## Environment

- Repository base: `8a6dba9921138a63027dc802b77a4cc3a01f3f60`
- Base tree: `1afb3440a5a33640728678de56e261f9470af1d1`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref metadata for DOI `10.1137/0202009` was observed with
`curl -L --fail --silent --show-error --max-time 20 -H 'User-Agent: awesome-theorems-stage1-intake/1.0' 'https://api.crossref.org/works/10.1137/0202009'`
and had
SHA-256 `c9269d8e96d82f08549dfa0d667ebd64c50f22511e7c338525fe2124069d0703`. It confirms
John H. Holland, the article title, *SIAM Journal on Computing* 2(2), June 1973, and pages 88-105.
Semantic Scholar metadata was observed with
`curl -L --fail --silent --show-error --max-time 20 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/0202009?fields=title,authors,year,venue,externalIds,openAccessPdf,url'`
and had SHA-256
`d76be84277a8040bebcb17db7331bdc5fffd9e99161cded0da13533eefef74e1` and reports the
full text closed. Exact response bytes were hashed but are not retained in this provisional public
dossier. No external source was vendored; both are mutable, nonrelease discovery observations, and
neither selects the catalog's exact target.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1482` | 0 | rank 1159, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10833,10838 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| the two exact bounded `curl` commands recorded above | 0 each | matching Holland 1973 primary-source-family lead identified; response hashes recorded, bytes not retained, bibliographic discovery only |
| `rg -n -i -l 'genetic algorithm\|genetic programming\|evolutionary algorithm\|evolutionary computation\|schema theorem\|Holland' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 1 expected | no occurrence; not an absence proof |
| the same `rg` query over `Stage1_Instances --glob '*.lean'` before creating this dossier | 1 expected | no occurrence; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1482/IntakeProbe.lean` | 0 | eight adjacent multiset/PMF APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool Stage1_Instances/THM-M-1482/instance.json`, repeated for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1482-pycache python3 -m py_compile Stage1_Instances/THM-M-1482/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1482/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| `rg -n '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)([^[:alnum:]_]\|$)' Stage1_Instances/THM-M-1482/IntakeProbe.lean` | 1 expected | no prohibited declaration token |
| `git diff --check -- Stage1_Instances/THM-M-1482 .stage1-worker-selftest.json` and per-new-file `git diff --no-index -- /dev/null PATH \| git apply --check --cached --whitespace=error-all -` | 0 | no whitespace diagnostics |

The final JSON, scoped-invariant, prohibited-construct, and whitespace results were recorded after
receipt and worker-packet creation. The Lean probe's exact combined-output SHA-256 is
`55d44374d805ad698f9cdb8b2d69bc13df27e1c7075286182c637dfec70e83a7`; the scoped
validator's exact stdout SHA-256 is
`a8872b17f7de0409ff81536e281da4b75fd2cd626ace1d6cf3ea20c048050352`.

## Known failures and boundary

Master acceptance is pending. The catalog method label still lacks a selected exact proposition.
Source admission, independent algorithms/evolutionary-computation review, formal target and
mutation certificate, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle, and
independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
