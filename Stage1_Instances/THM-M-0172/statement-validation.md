# Statement blocker validation

Base revision: `4db87ed5646981780f2e885e21052d997afd1be7`.

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No dependency update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0172` | exit 0; rank 667, lifecycle `planned`, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0172/StatementInfrastructure.lean` | exit 0; four available manifold/Riemannian declarations checked and four required representative identifiers rejected by `#check_failure` |
| scoped `rg` searches of pinned mathlib for the required interfaces | no target-capable interface found; details in `statement-blocker.md` |
| `rg -n '(sorry\|axiom\|placeholder\|admit\|unsafe)' Stage1_Instances/THM-M-0172/StatementInfrastructure.lean` | exit 1; no prohibited token matches |
| `git diff --check -- Stage1_Instances/THM-M-0172` | exit 0; no output |

This validation can establish the infrastructure blocker, not the assigned
statement completion. The exact target, expression fingerprint, transports,
and mutation tests remain unavailable.
