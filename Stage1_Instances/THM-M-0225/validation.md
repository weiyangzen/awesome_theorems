# Intake validation

## Boundary

This record validates only `S56-M-0225-INTAKE`: target membership, a `planned` dossier, the scope
map, source-statement crosswalk, exact-topic pinned API discovery, and the six-node open downstream
task DAG. The canonical statement and Lean expression remain null. No source is admitted to `H0`,
no candidate is transported to the root or credited as a proof body, and no audit or theorem
completion is claimed.

The worker clone began at commit `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`, tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run. This is
nonrelease worker evidence; integration must recapture content-addressed evidence before
acceptance.

## Commands and results

Commands ran from the repository root on 2026-07-13 (Asia/Shanghai), except where a working
directory is shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0225` | 0 | rank 1238; `planned`; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; tree `9d7c8fe49a4c859d90f3069dc47973ffc5ced768` |
| `git blame -L 1626,1631 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` on the six-line catalog record and Stage0 projection | 0 | `a3e17069...7303` and `546543ab...8a62`; both are frozen in `instance.json` |
| `curl -L --fail --silent --show-error 'https://encyclopediaofmath.org/index.php?title=Maximum-modulus_principle&oldid=54115'` plus `wc`, `sha256sum`, and scoped text inspection | 0 | immutable secondary revision returned 18,821 bytes, SHA-256 `347e19aa...6161`; it distinguishes nonconstant local/global/boundary forms and cites Ahlfors (1979), page 241; discovery only, not H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Analysis/Complex/AbsMax.lean'` | 0 | mathlib revision `8a178386...eea95`, tree `bdc39a...5e2b`, and source blob `e8ff6a7...ff5fa` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0225/IntakeProbe.lean)` | 0 | six direct named interfaces elaborated; four candidates report `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `d1e9e19f8ffb30b45cf3156ce1e91b152172e2faa816b9942c2402c8b3cd8255` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| isolated `python3 -m py_compile Stage1_Instances/THM-M-0225/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0225/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | manifest/DAG identity, source and dependency hashes, `[H1, M3, R4]` boundary, null target, exact artifact inventory, receipt/packet agreement, and six open tasks agree |
| token-anchored prohibited declaration scan over the owned Lean file | 1 as expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` is allowed |
| scoped per-file new-file whitespace checks and `git diff --check` | 0 | no whitespace diagnostics |

## Known open gates

No immutable primary or authoritative theorem passage, incorporated definition chain, ordered
statement, assumption/exception/conclusion map, proof boundary, correction or errata disposition,
or independent source review is accepted. In particular, the literal catalog wording omits the
constant-function exception and does not select the local, global connected-domain, or boundary
form.

Canonical Lean target, minimal imports, elaborated expression and environment fingerprints,
checked transports, statement mutations, exhaustive anchor and provenance audit, discovery and
obligation freezes, typed graphs, proof and composition, accepted trust closure, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion all remain open. These failures do not
invalidate a truthful, self-tested `planned` intake.
