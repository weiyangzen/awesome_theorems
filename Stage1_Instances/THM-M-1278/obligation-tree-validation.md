# Obligation-tree validation record

Item: `S56-M-1278-OBLIGATION_TREE`  
Base revision: `4fefd52b2fcf2d237b21cafcc2d72511afaf5cfb`

## Frozen architecture

Registry version 1 contains 15 stable semantic obligations and 54 typed edges across separate
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs. The frozen
machine denominator has 13 required obligations; source and provenance are explicit informational
overlays and cannot earn proof credit. The mandatory branch layer is inapplicable because the
selected normalization route has no mathematical case split; that disposition still awaits master
review.

The direct route subtracts the spherical mean, proves the shifted representative has zero mean and
unchanged energy, factors the exponential integral, invokes the still-open sharp zero-mean Onofri
estimate, and composes back to the exact root. `ObligationTree.lean` checks the exact composition
interface while treating its two unproved semantic children as explicit hypotheses. It contains no
proof placeholder or new axiom.

## Exact validation

All commands ran in this worker clone using the existing pinned Lake environment. No dependency was
fetched, updated, built, or otherwise mutated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1278/build_obligation_artifacts.py` | 0 | deterministically generated 15 obligations and 54 typed edges; denominator SHA-256 `82859ac069b3ced4256f655ed25af787359c256a68dd45861af3672567baf674` |
| `python3 Stage1_Instances/THM-M-1278/check_obligation_tree.py` | 0 | schemas, denominators, eligibility, reciprocal indexes, graph reachability/acyclicity, ledgers, and open closure boundary passed |
| `lake env lean ../../Stage1_Instances/THM-M-1278/ObligationTree.lean` from `Formalizations/Lean` | 0 | root, sharp-estimate, shift-transport interfaces and the exact child-to-root composition theorem elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/typed-graphs.json` | 0 | valid JSON |
| `rg -n 'sorry\\b|^\\s*axiom\\b|^\\s*unsafe\\b' Stage1_Instances/THM-M-1278/ObligationTree.lean` | 1 | no forbidden construct; exit 1 is ripgrep's no-match result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets valid |
| `python3 scripts/stage1_target.py show THM-M-1278` | 0 | rank 449, planned, L0/rework-required, theorem incomplete |

## Status boundary

This node freezes architecture only and is self-tested pending master acceptance. The closed
obligation set is empty and the root remains M3. In particular, the sharp analytic estimate, sphere
area normalization, integrability/positivity package, source pinpointing, proof implementation,
hermetic validation, and independent review remain open. Neither the checked composition harness nor
this receipt proves Onofri or establishes audit or theorem completion.
