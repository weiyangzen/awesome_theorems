# Intake validation record

Base revision: `c6aa0f2ba41dd389c2bcf01dd532923615781719`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0985` | 0 | rank 265, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0985/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f` for `README.md`, `source_statement_crosswalk.md`, and `intake.json` | 0 | required dossier artifacts exist |
| `! rg -nw 'sorry\|admit\|axiom\|placeholder\|THM-M-0387' Stage1_Instances/THM-M-0985/{README.md,intake.json,source_statement_crosswalk.md}` | 0 | no forbidden proof-hole token or copied fixture ID appears |
| `git diff --check` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. It validates membership, standard
consistency, artifact structure, and honest status boundaries. No Lean declaration is introduced,
so no kernel result is claimed. Master acceptance and all dependent phases remain outstanding.

## Statement validation

Base revision: `ae3a77da9f973d2fb833b68ab90f37e9c6bc2ddd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0985` | 0 | rank 265; planned; rework required; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0985/Statement.lean)` | 0 | canonical target, checked expansion, boundary lemmas, and four mutation probes elaborated; pretty-printed exact declaration emitted |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0985/Statement.lean 2>/dev/null \| sed -n '/^def Stage1Instances.THMM0985.KolmogorovStrongLaw/,$p' \| sha256sum)` | 0 | `517642192400a8c1319fd8e75ed0074439a8667c9a8f5ec09798da654004f5ca` |
| `python3 -m json.tool Stage1_Instances/THM-M-0985/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `! rg -n '\\bsorry\\b|\\badmit\\b|\\baxiom\\b|placeholder' Stage1_Instances/THM-M-0985/Statement.lean` | 0 | no forbidden proof construct found |
| `git diff --check -- Stage1_Instances/THM-M-0985` | 0 | no whitespace errors |

The existing pinned cache was reused without update, build, clone, fetch, or other `.lake`
mutation. This evidence establishes statement elaboration only. Primary-source acceptance,
anchor audit, proof inhabitation, trust closure, reproducible release, independent verification,
master acceptance, and theorem completion remain open.

## Anchor-audit validation

Base revision: `46ae82675e83fbd3605819f1c3a6d6fb2e7328cd`.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib show -s --format='%T' HEAD` | 0 | immutable source tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0985/AnchorAudit.lean)` | 0 | candidate types printed; mutual-to-pairwise bridge and exact expanded target witness elaborated; both declarations report only `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool Stage1_Instances/THM-M-0985/anchor_audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `rg -n -i 'strong.?law\|kolmogorov' Formalizations/Lean/.lake/packages --glob '*.lean'` plus the analogous repo-local search | 0 | pinned mathlib StrongLaw is the only terminal iid strong-law implementation; external package and local-wrapper hits classified |
| `! rg -n '\\bsorry\\b\|\\badmit\\b\|\\baxiom\\b' Stage1_Instances/THM-M-0985/AnchorAudit.lean` | 0 | no forbidden proof construct in the audit witness |
| `git diff --check -- Stage1_Instances/THM-M-0985` | 0 | no whitespace errors |

The existing pinned cache was not updated, built, cloned, or fetched. This
self-test completes only the anchor-audit work product; the obligation tree,
proof, full validation, release, and master-acceptance nodes remain open.
