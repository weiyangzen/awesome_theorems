# THM-M-1485 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, primary-source discovery boundary, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a network or backward-recurrence specification, an
update or convergence theorem, a proof, an accepted receipt, audit completion, or theorem
completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. The shared pinned `.lake`
target was used read-only. No dependency update, build, clone, fetch, authority-file change,
generated-checklist change, execution-DAG state change, or other target modification was performed.

## Environment

- Repository base: `e552e0758e29de307cf357a703e6ecd16e40fb69`
- Base tree: `492b45021fb6ce4973452d8173d32fe2c212a877`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The author-hosted Nature facsimile for DOI `10.1038/323533a0` was inspected with a bounded HTTP
request and had observed SHA-256
`d26997baf588222109d32545604a2a2ed400dc769a21fd49a5acdc4a955396ae`. Crossref metadata
confirmed the title, authors, journal, volume, issue, pages, and 1986 publication. No external file
was vendored. These mutable remote observations are nonrelease discovery evidence, not an admitted
source bundle or `H0` crosswalk.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1485` | 0 | rank 1162, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10854,10859 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref and author-hosted facsimile inspection for DOI `10.1038/323533a0` | 0 | matching 1986 primary-source lead and formula loci identified; discovery only |
| exact topic searches over pinned mathlib and repo-local Lean | 1 expected for exact backpropagation forms | no exact `backprop`, `back-propag`, or `reverse-mode` declaration found; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1485/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1485-pycache python3 -m py_compile Stage1_Instances/THM-M-1485/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1485/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token |
| `git diff --check -- Stage1_Instances/THM-M-1485 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The Lean probe's exact combined-output SHA-256 is
`243818375ceb737f1723af65b9c871378159f436dbb4644741eeafbd19fdfa5e`.

## Known failures and boundary

Master acceptance is pending. The catalog algorithm label still lacks a selected exact proposition.
Immutable source admission, correction audit, independent source/domain review, formal target and
mutation certificate, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle, and
independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
