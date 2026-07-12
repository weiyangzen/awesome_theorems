# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation ran on 2026-07-13 in the
isolated worker clone. Existing pinned `.lake` artifacts were used read-only; no update, build,
clone, fetch, or dependency mutation was run.

## Validation boundary

Validation covers target membership, the planned dossier, scope and source crosswalk, source-lead
discrimination, exact open task topology, pinned adjacent Lean APIs, prohibited constructs, and
file hygiene. Because the catalog does not determine a proposition, there is no canonical Lean
expression, target expression fingerprint, proof body, axiom report, or theorem-completion result.
The probe authenticates interfaces only.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1392` | 0 | Rank 1002, planned, no accepted legacy artifacts, theorem incomplete |
| `git status --short` before editing | 0 | Only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | Base revision and tree recorded above |
| `git blame -L 10139,10144 -- Docs/researches/math_theorems.md` | 0 | All six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| author-hosted Teschl book, official errata, and Crossref inspection | 0 | One regular Sturm--Liouville Green-kernel source lead mapped; catalog selection and independent review remain open |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| pinned mathlib revision/tree/status check | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1392/IntakeProbe.lean` | 0 | Six adjacent API checks elaborated; output SHA-256 `3e4762bb8b6d49a483439ac49eadecb9f41c820d1192997a1383f5469775ce91` |
| exact-topic `rg` search of pinned mathlib Lean | 1 expected | No Green-function or Green-kernel declaration under the bounded patterns |
| exact-topic `rg` search of repository Lean | 0 | Four unrelated predicate-boundary or prose hits; no ODE target candidate |
| `python3 -m json.tool` on all structured owned files and the worker packet | 0 | Valid JSON after finalization |
| parse `check_intake.py` with Python `ast` | 0 | Validator syntax accepted without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1392/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | Manifest/DAG identity, pins, null target, H5/M4/R4 boundary, exact inventory, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1392/check_intake.py` | 0 | Public replay mode passed without scheduler-only packet input |
| prohibited Lean construct scan | 1 expected | No `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` on each changed file | 0 aggregate | No whitespace diagnostics; each expected new-file difference was normalized |
| `git diff --check -- Stage1_Instances/THM-M-1392 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics |

## Result and boundary

The assigned intake is self-tested as a provisional `[_]` worker proposal. Its receipt is unsigned,
mutable, non-content-addressed, and not accepted. The authoritative checklist remains unchanged.
Ordinary theorem-proof execution is blocked by `H5` until an accountable correction or source
selection yields one stable proposition. Exact statement elaboration, source `H0`, formal anchor
audit, obligation registry, proof, composition, trust closure, readable reconstruction, hermetic
replay, and independent release gates remain open. Audit completion and theorem completion are
both false.
