# S56-M-0396-STATEMENT validation

Base revision: `1c82bc6e57ec6af8b83dec57caf215d431d3af99`.

The selected exact target is `Stage1Rev56.THMM0396.Statement`. It elaborates
from the single direct pinned import `Mathlib.NumberTheory.Height.NumberField`.
The source hash is
`adc9e134e2e2164064f33d35c056fd66aac052127dff858fa5b4b3de4ad9d094`.

## Commands and results

| Command | Cwd | Exit | Result |
|---|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | repository root | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | repository root | 0 | 1546 unique ranks and L0/rework baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0396` | repository root | 0 | rank 9, planned, L0/rework_required, theorem incomplete |
| `lake env lean --version` | `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lean ../../Stage1_Instances/THM-M-0396/Statement.lean` | `Formalizations/Lean` | 0 | `Stage1Rev56.THMM0396.Statement.{u} : Prop` |
| remove the sole import in `/tmp/THM-M-0396-noimport.lean`, then `lake env lean /tmp/THM-M-0396-noimport.lean` | `Formalizations/Lean` | 1 | required notation and number-field/height substrate unavailable; import is not removable |

The pre-existing untracked `Formalizations/Lean/.lake` link reuses the canonical
pinned cache and was not modified. No update, fetch, clone, or broad build was
run. This evidence establishes narrow statement elaboration only. Pinpoint
source audit, proof, trust, hermetic replay, independent verification, master
acceptance, and theorem completion remain open.
