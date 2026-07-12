# Obligation-tree validation receipt

Node: `S56-M-1027-OBLIGATION_TREE`. Base revision:
`26d86e8061117f2975b8278f35ca3b2aac5e0efb`. Date: 2026-07-12. The pre-existing
untracked `Formalizations/Lean/.lake` link supplies the canonical pinned artifacts and was neither
created nor modified by this phase.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1027/build_obligation_artifacts.py` | 0 | generated 20 obligations; denominator `3379c790ba57cf8132dcf05c9a3602157708d9e0ef3e431b0057b46d79fd4481` |
| `python3 Stage1_Instances/THM-M-1027/check_obligation_tree.py` | 0 | PASS: 20 obligations, 40 typed edges; root open M3; witness package and external integration M4 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets with ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1027` | 0 | rank 218; planned; L0/rework-required; theorem incomplete |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP="$(cd Formalizations/Lean && lake env printenv LEAN_PATH):Stage1_Instances/THM-M-1027"; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1027 Stage1_Instances/THM-M-1027/Statement.lean -o Stage1_Instances/THM-M-1027/Statement.olean; LEAN_PATH="$LP" "$LEAN" -R Stage1_Instances/THM-M-1027 Stage1_Instances/THM-M-1027/ObligationTree.lean; rm -f Stage1_Instances/THM-M-1027/Statement.olean Stage1_Instances/THM-M-1027/Statement.ilean` | 0 | pinned Lean 4.29.0 elaborated the exact statement and conditional composition; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary local interface artifacts were removed |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1027; test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1027 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

The Lean recipe uses only the executable and `LEAN_PATH` emitted by `lake env`. It creates the
local `Statement.olean` required by `import Statement`, then removes it. It performs no Lake update,
build, dependency fetch, or mutation.

## Result boundary

The registry projection hash, ordered eligibility denominators, mandatory node fields, step
budgets, typed-edge endpoints, reciprocal proof edges, graph separation, proof acyclicity, root
reachability, and open closure boundary are self-tested. Lean checks the exact conditional
witness-to-root interface. No `WienerWitnessPackage` is constructed, the external project remains
absent from the local dependency closure, and the root remains M3. Audit completion, H0/R0, trust
and provenance closure, hermetic replay, master acceptance, and theorem completion remain open.
