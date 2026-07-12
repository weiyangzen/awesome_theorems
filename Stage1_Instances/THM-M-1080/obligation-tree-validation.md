# THM-M-1080 obligation-tree validation

Item: `S56-M-1080-OBLIGATION_TREE`  
Validation date: `2026-07-12`  
Base revision: `18bd714383d0c5ac5efe034e3c041e6345479bf7`

## Frozen architecture

Registry v1 contains 18 unique semantic obligations. Fifteen are machine-required. The pinned
mathlib candidate, human-source overlay, and release-provenance overlay are explicitly
informational or not applicable for machine closure and cannot inflate proof coverage. The
required route retains the arbitrary measurable space and expands the direct exponential-moment
argument: martingale differences, telescoping, conditional Hoeffding, MGF iteration,
exponential Markov, parameter optimization, and separate positive/zero-threshold terminals.

The frozen denominator digest is
`869c1a9abe79908244280909afaadc8e84b294df0d6b1e290b81e5363243df14`.
The bundle binds `Statement.lean` and `anchor-audit.json` by SHA-256. Seven typed graphs contain
42 edges; all proof requirements have reciprocal composition edges. The validator checks complete
schemas, unique IDs, derived denominators, source bindings, reciprocity, proof reachability,
acyclicity, validation-recipe coverage, placeholder absence, and the fail-closed root boundary.

`ObligationTree.lean` checks only exact recomposition of explicit `t > 0` and `t = 0` premises.
Lean reports its ordinary mathlib axiom closure as `propext`, `Classical.choice`, and `Quot.sound`.
Both terminal packages remain open, so the composition theorem is not an Azuma proof.

## Commands and results

All Lean work reused the existing pinned `.lake` symlink. No update, build, clone, fetch, or
dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1080/build_obligation_artifacts.py` | 0 | built 18 obligations and 42 typed edges; printed the denominator digest above |
| `python3 Stage1_Instances/THM-M-1080/check_obligation_tree.py` | 0 | PASS; 18 obligations, 42 typed edges; root open at M3 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1080/ObligationTree.lean` | 0 | conditional threshold composition elaborated; axioms printed as above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1080` | 0 | rank 522; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1080` | 0 | no output |
| `rg -n -i '\\b(sorry\|admit\|axiom)\\b' Stage1_Instances/THM-M-1080 --glob '*.lean'` | 0 | no matches (the shell command used `|| true` only to keep the evidence batch running on no match) |

## Open boundary

The remaining root cut set is `M1080-T-POSITIVE` and `M1080-T-ZERO`. In particular, the critical
arbitrary-space conditional Hoeffding bridge and its MGF iteration have no proof bodies. Root debt
therefore remains `M3`; primary-source pinpoint review remains `H2`; readable reconstruction is
not accepted. This packet self-tests only the obligation architecture pending master acceptance.
It does not claim `H0`, `M0`, `R0`, audit completion, root closure, or theorem completion.
