# THM-M-1518 proof-phase validation

Item: `S56-M-1518-PROOF`
Date: `2026-07-14`
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

## Verdict

`provisional_worker_selftest`: the exact frozen Lean target is kernel-closed.
`Proof.lean` proves the first-variation identity by differentiating under the
interval integral. `WeakToPointwise.lean` proves the analytic bridge using
fixed-endpoint integration by parts, the smooth-test fundamental lemma, and a
continuity upgrade. `ExactProof.lean` composes both packages with the frozen
`ObligationTree.exactTarget_of_packages` certificate.

The public declarations `firstVariationFormula`, `weakToPointwise`, and
`stationaryActionEulerLagrange` report exactly `propext`, `Classical.choice`,
and `Quot.sound`. Transitive `assert_no_sorry` checks pass. No axiom,
placeholder, unsafe declaration, oracle, broadened theorem, or unpinned
dependency was added.

This is proof-phase evidence, not theorem completion. The frozen obligation
graph still records its pre-proof M4 observation, and the accepted state is
unchanged until the integration lane reviews the receipt. Validation, release,
complete trust/provenance review, cold offline replay, independent verification,
H0/R0, AUDIT-Z, and THEOREM-Z remain open.

## Proof route

The first-variation proof obtains a compact uniform bound for the parameter
derivative over `[-1, 1] × uIcc a b`, then applies
`intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le`.

For the pointwise equation, the proof sets the position derivative to `A` and
velocity derivative to `P`. For arbitrary `v`, it tests the scalar residual
`A t v - deriv P t v` against every smooth compactly supported `g` in the open
interval. The variation `g • v` is admissible, integration by parts removes
`deriv g`, and the fundamental lemma makes the residual almost everywhere
zero. `Measure.eqOn_open_of_ae_eq` upgrades this to pointwise equality by
continuity; extensionality in `v` yields the continuous-linear-map derivative.

## Commands and results

All commands ran in the worker clone with the existing pinned Lean artifacts.
No `lake update`, `lake build`, clone, fetch, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and the ordered manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-1518` | 0 | Rank 187; authoritative state remains planned and theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1518/check_statement.py` | 0 | Exact-expression SHA-256 `4cc157...979f`; all four statement mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1518/check_obligation_tree.py` | 0 | Frozen registry, 12 obligations, 26 typed edges, and conditional composition passed; its pre-proof root boundary remains open. |
| `python3 Stage1_Instances/THM-M-1518/check_proof.py` | 0 | Fresh temporary `--trust=0` oleans elaborated the statement, tree, both analytic packages, and exact root; axiom and transitive-sorry checks passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1518/proof-receipt.json` | 0 | Provisional node receipt is valid JSON. |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|opaque\|external\|constant)\b' Stage1_Instances/THM-M-1518 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean construct. |
| `git diff --check -- Stage1_Instances/THM-M-1518 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `git diff --no-index --check /dev/null <new-file>` for each new owned proof artifact and the worker packet | 1 each | Expected new-file difference exits with no whitespace diagnostics. |

The node-specific provisional receipt is `proof-receipt.json`. Only the
integration lane may accept it or change authoritative item state.
