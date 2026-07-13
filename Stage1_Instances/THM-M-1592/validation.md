# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`).

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai). The automation-provided
`Formalizations/Lean/.lake` symlink was present before the work and was used read-only. No `lake
update`, `lake build`, dependency fetch/clone, or `.lake` mutation was performed. This dirty worker
snapshot is nonrelease evidence.

## Source and environment inspection

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1592` | 0 | rank 1213; planned; L0; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initially only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 11728,11733 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; no later statement or source refinement |
| Crossref query for `10.1137/0108018` | 0 | confirms Reed and Solomon, title, journal 8(2), June 1960, pages 300-304, and DOI; response SHA-256 `616d3330...440` |
| Semantic Scholar query for DOI `10.1137/0108018` | 0 | independently matches the bibliographic lead and reports closed access; response SHA-256 `367a41c3...56c` |
| publisher PDF request for DOI `10.1137/0108018` | 22 | HTTP 403; paper text and an exact internal result were not inspected or credited |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...` and tree `bdc39a31...` |
| bounded `rg` for Reed-Solomon, MDS code, evaluation code, and polynomial code in pinned mathlib and repo-local Lean | 1 | expected no-match; discovery-only lexical search, not an exhaustive anchor audit |

## Final scoped checks

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1592/IntakeProbe.lean` | 0 | nine generic Hamming, polynomial-root, and Vandermonde APIs elaborated; stdout SHA-256 `1aec1e60...3c63` |
| `python3 -m json.tool Stage1_Instances/THM-M-1592/instance.json >/dev/null` | 0 | instance JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1592/task-dag.json >/dev/null` | 0 | open DAG JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1592/intake-receipt.json >/dev/null` | 0 | provisional receipt JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1592-pycache python3 -m py_compile Stage1_Instances/THM-M-1592/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 Stage1_Instances/THM-M-1592/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, artifact inventory, worker packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-1592/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the probe contains no prohibited declaration |
| no-index whitespace check for all nine owned files and `.stage1-worker-selftest.json` | 0 | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-1592 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

The first Lean probe attempt imported Hamming and Vandermonde but tried to check
`Polynomial.card_roots'`; it failed because `Mathlib.Algebra.Polynomial.Roots` was not imported.
That exact module was then added, and the corrected final command above passed. The superseded
failure grants no statement or proof evidence.

## Boundary

These checks self-test the `planned` intake node only. They do not select an exact Reed-Solomon
proposition, establish minimal imports for a canonical target, create an expression fingerprint, or
validate any proof. Source selection, all six dependent tasks, master acceptance, audit completion,
and theorem completion remain open.
