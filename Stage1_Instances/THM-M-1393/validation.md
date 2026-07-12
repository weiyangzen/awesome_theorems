# Intake validation

Base revision: `02cc55f883d5b5d091ead6851bffe89199eb8391` (tree
`035212d041a1e61553b3d2f465964c9bbb35e47d`). Final scoped validation ran from
2026-07-13 05:04:36 through 05:04:39 Asia/Shanghai in the
isolated worker clone. Existing pinned `.lake` artifacts were used read-only; no update, build,
clone, fetch, or dependency mutation was run.

## Validation boundary

Validation covers target membership, the planned dossier, scope and source crosswalk, neighboring
target separation, exact open task topology, pinned candidate APIs, prohibited constructs, and file
hygiene. Because the catalog does not determine one proposition, there is no canonical Lean target,
expression fingerprint, proof body, axiom report, mutation certificate, or theorem-completion
result. The probe authenticates interfaces only.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1393` | 0 | Rank 1003, planned, no accepted legacy artifacts, theorem incomplete |
| `git status --short` before editing | 0 | Only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | Base revision and tree recorded above |
| `git blame -L 10146,10151 -- Docs/researches/math_theorems.md` | 0 | All six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work query for DOI `10.1007/BF02421317` | 0 | Ivar Fredholm, 1903, *Acta Mathematica* 27, pages 365-390; bibliographic lead only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| pinned mathlib revision/tree/status check | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1393/IntakeProbe.lean` | 0 | Seven compact-operator, spectral, and ODE API checks elaborated; output SHA-256 `ed83cfc1f38c0bef9904995c3c700d3842c2a705681097da280e9ed9ce19270f` |
| `rg -n -i 'linear boundary.value.*Fredholm\|Fredholm.*linear boundary.value\|boundary condition.*adjoint.*Fredholm\|Fredholm.*adjoint.*boundary' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 expected | No linear-boundary-value/adjoint Fredholm declaration under the bounded conjunctions |
| `python3 -m json.tool` on all structured owned files and the worker packet | 0 | Valid JSON after finalization |
| parse `check_intake.py` with Python `ast` | 0 | Validator syntax accepted without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1393/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | Manifest/DAG identity, pins, null target, H1/M4/R4 boundary, exact inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1393/check_intake.py` | 0 | Public replay mode passed without scheduler-only packet input |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1393 --glob '*.lean'` | 1 expected | No prohibited declaration or proof hole |
| per-file `git diff --no-index --check /dev/null` on each changed file | 0 aggregate | No whitespace diagnostics; each expected new-file difference was normalized |
| `git diff --check -- Stage1_Instances/THM-M-1393 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics |

## Result and boundary

The assigned intake is self-tested as a provisional `[_]` worker proposal. Its receipt is unsigned,
mutable, non-content-addressed, and not accepted. The authoritative checklist remains unchanged.
Exact source selection and review, statement elaboration, checked BVP/operator bridges, source `H0`,
formal anchor audit, obligation registry, proof, composition, trust closure, readable reconstruction,
hermetic replay, and independent release gates remain open. Audit completion and theorem completion
are both false.
