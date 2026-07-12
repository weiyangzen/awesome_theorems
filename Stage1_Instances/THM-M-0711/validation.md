# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

This record covers target membership, planned-dossier structure, JSON integrity, and a narrow
pinned Lean API probe. The shared canonical `.lake` link/artifacts were used read-only. No update,
build, fetch, or clone was run. Because exact source and encoding choices remain open, no canonical
expression hash, mutation result, proof, or accepted receipt is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; planned lifecycle, empty accepted state, open formal expression, false terminal flags, and six open downstream tasks confirmed |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/IntakeProbe.lean)` | exit 0; seven group-presentation/computability API checks elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1, expected no-match; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

Known downstream work remains open: primary-source acceptance and independent review,
obligation/discovery freezes, formal-anchor audit,
proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate a truthful self-tested `planned` intake.

## Statement phase (S56-M-0711-STATEMENT)

| Command | Result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0711/Statement.lean)` | exit 0; canonical target and three expected structural mutation failures elaborated; explicit expression printed (7297 bytes, SHA-256 `1186dd31dd2f2126cb5998ef79ec6d9b64396acccdbdfc16dc6baa09c66edd3c`) |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0711` | exit 0; rank 751, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0711/statement-receipt.json` | exit 0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0711 -g '*.lean'` | exit 1, expected no-match |
| `git diff --check -- Stage1_Instances/THM-M-0711` | exit 0; no output |

The statement phase freezes and elaborates the exact repository target but supplies no proof.
Primary-source fidelity and every downstream proof/release gate remain open, so the root vector is
unchanged and `theorem_complete` remains false.
