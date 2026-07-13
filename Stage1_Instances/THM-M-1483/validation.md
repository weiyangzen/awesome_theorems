# THM-M-1483 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic source-lead metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a particle-swarm algorithm, any convergence or
optimality result, a proof, an accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified. The
automation-provided canonical `.lake` link was used read-only; no update, build, clone, fetch, or
other dependency mutation was performed.

## Environment

- Repository base: `e552e0758e29de307cf357a703e6ecd16e40fb69`
- Base tree: `492b45021fb6ce4973452d8173d32fe2c212a877`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref, Semantic Scholar, and Unpaywall metadata for DOI
`10.1109/ICNN.1995.488968` were observed through bounded HTTP requests. Their response SHA-256
values were, respectively, `31573248e79707f2b5e3cf9721bf778f6c0c7b79f001099797703f734d651f36`,
`aade6f1755aa84024afc346bb5ec35a3c22824920fb74227eacad8db4de46bbd`, and
`c7808cecee58a5c036187ef4ec3a095b02c86992c44e8cd75c11f9c9530c2678`. They identify the
Kennedy-Eberhart paper and report the full text closed; no external source was vendored. These are
mutable, nonrelease discovery observations.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1483` | 0 | rank 1160, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10840,10845 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref, Semantic Scholar, Unpaywall, and DBLP observations for DOI `10.1109/ICNN.1995.488968` | 0 | matching Kennedy-Eberhart source lead identified; metadata/abstract discovery only, with full text reported closed |
| attempted IEEE PDF observation | 22 | HTTP 418; no article body was received, inspected, or credited |
| bounded case-insensitive topic search over pinned mathlib, repo-local Lean, and existing Stage1 Lean files | 0 due to unrelated substring matches | no source-selected particle-swarm, Kennedy, Eberhart, personal-best, or global-best terminal declaration located; `Pso` in Lie algebra and `PComp` oracle internals are explicit false positives; not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1483/IntakeProbe.lean` | 0 | five adjacent pinned APIs elaborated; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced; exact output SHA-256 `9855c6b2ece2f818591c2113f5f999b1d540f798018463cb5d767b5513f066bc` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1483-pycache python3 -m py_compile Stage1_Instances/THM-M-1483/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1483/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1483 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results were recorded after receipt and worker-packet creation.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. Source
admission, independent source/optimization review, formal target and mutation certificate,
exhaustive anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification
remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
