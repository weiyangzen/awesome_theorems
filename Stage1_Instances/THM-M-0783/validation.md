# Intake validation

Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`.

The worker clone begins with the expected untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned build artifacts. It was not created or mutated by this task. This is scoped worker
self-test evidence, not clean release evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0783` | 0 | rank 788; planned; hard-statement-first lane; theorem completion false |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0783/intake.json >/dev/null` | 0 | intake artifact is valid JSON |
| dossier-local reference check recorded below | 0 | both public merge targets and every owned Markdown reference resolve |
| forbidden-placeholder scan recorded below | 0 | no Lean proof placeholder or fake accepted state occurs in the dossier |
| `git diff --check -- Stage1_Instances/THM-M-0783 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The dossier-local reference check parses `intake.json`, requires the exact theorem/item/lifecycle
identity, rejects any accepted proof state or theorem-complete claim, verifies every public merge
target exists, and verifies each backtick reference in the README that names a dossier file. The
placeholder scan rejects the proof tokens `sorry`, `admit`, `sorryAx`, and any nonempty
`accepted_proof_state`; prose discussing why an unproved axiom earns no proof credit is intentional.

No Lean theorem was elaborated because intake has truthfully left the formal expression open. The
Lean command above validates availability of the pinned toolchain only; it is not statement or
proof evidence. The first remaining gate is selection and elaboration of an exact foundational
encoding during `S56-M-0783-STATEMENT`, after master acceptance of this intake.
