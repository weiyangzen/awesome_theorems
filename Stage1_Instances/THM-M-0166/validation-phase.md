# S56-M-0166-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `cd2070316d8a25117b90105fb1da2b6853a71999`.

The validation recipes re-elaborate the exact frozen statement, the conditional child-to-root
composition, and both proof-phase declarations. Kernel reports for the composition and partial proof
bodies contain only `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` is reported. A
code-aware hygiene scan finds no prohibited proof construct in the three Lean inputs. The mathlib
checkout is clean at the manifest-pinned revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Validation fails closed at `proof.root_kernel_closure`. The proof phase closed only
`M0166-L-SUBSEGMENT`; `M0166-C-PROPER` and `M0166-L-EXISTENCE` remain the exact root cut set, so the
root stays `M2`. The worker reused the pre-existing canonical pinned `.lake` artifacts as required;
therefore no empty-cache cold build or archive replay is claimed. `check_validation.py` is a
separately implemented evidence checker, but execution in this same checkout and shared cache is not
the distinct independently provisioned runner required by the release protocol.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0166/Statement.lean)` | 0 | exact universe-explicit target elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0166/ObligationTree.lean)` | 0 | conditional root composition elaborated; axioms were exactly the accepted three |
| `(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0166/check_proof.sh)` | 0 | subsegment proof and conditional root wrapper elaborated; same axiom profile; hygiene passed |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0166/check_statement.py)` | 0 | expression hash `8965e82e...97da55`; four structural mutations killed |
| `python3 Stage1_Instances/THM-M-0166/check_obligation_tree.py` | 0 | seven canonical nodes, typed graphs, open root, checked composition |
| `python3 Stage1_Instances/THM-M-0166/check_validation.py` | 0 | frozen inputs and truthful partial-closure boundary independently recomputed |
| `git diff --check -- Stage1_Instances/THM-M-0166` | 0 | no whitespace errors |

This is a self-tested validation-phase handoff pending master acceptance. It claims neither
hermetic release evidence, independent-runner acceptance, audit completion, nor theorem completion.
