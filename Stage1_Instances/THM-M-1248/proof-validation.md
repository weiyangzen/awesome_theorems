# THM-M-1248 proof-phase execution

Item: `S56-M-1248-PROOF`  
Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`  
Run date: `2026-07-14` (`Asia/Shanghai`)

## Implemented proof bodies

`Proof.lean` adds three unconditional, placeholder-free local declarations. The
first extracts the exhaustive `a = 0`, `a = 1`, or `0 < a < 1` split from the
frozen admissibility bounds. The second proves that at `a = 0` the frozen weight
and scaling equations force `gamma = beta` and `r = q`. The third uses those
equalities and `C = 1` to prove the exact lower-order endpoint estimate.

These bodies close the planned signatures for `M1248-N-PARAM` and
`M1248-B-A0`. They do not prove the positive endpoint, interior interpolation,
weighted Sobolev/Hardy, singular-origin, Holder, real-power assembly, analytic
package, or exact root obligations. The root therefore advances only from
interface-only `M3` to partial `M2`; it is not machine-complete.

## Narrow validation

Commands ran in this worker clone using the existing pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, network action, or `.lake`
mutation was performed. Temporary compiled modules were isolated below the
worker root and removed after elaboration.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure accepted: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest accepted: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | rank 428; lifecycle `planned`; L0/rework-required; theorem incomplete |
| Temporary-copy pinned Lean recipe below | 0 | `statement_exit=0 obligation_tree_exit=0 proof_exit=0`; all three local declarations elaborated and `#print sorries` reported `Declarations are sorry-free!` |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | frozen registry remains structurally valid: 18 obligations and 43 typed edges; recorded root is open |
| `python3 -m json.tool Stage1_Instances/THM-M-1248/proof-receipt.json >/dev/null` | 0 | partial proof receipt parses as JSON |
| token-anchored prohibited-device scan over owned Lean files | 1 (expected) | no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | no scoped whitespace errors |

The exact Lean recipe was:

```bash
TMP=$(mktemp -d .thm1248-proof.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cp Stage1_Instances/THM-M-1248/{Statement,ObligationTree,Proof}.lean "$TMP/"
LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 300 "$LEAN" --trust=0 -t0 \
  --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 300 "$LEAN" --trust=0 -t0 \
  --root="$TMP" -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 300 "$LEAN" --trust=0 -t0 \
  --root="$TMP" "$TMP/Proof.lean"
rm -rf "$TMP"
```

For `admissible_parameter_split`, `admissible_a_zero_forces_lower_order_parameters`,
and `caffarelliKohnNirenberg_a_zero`, `#print axioms` reported exactly
`[propext, Classical.choice, Quot.sound]`, with no `sorryAx`.

## Blocker and boundary

Verdict: `blocked`; the assigned proof phase is incomplete. The immediate
graph-derived root cut remains `M1248-T-ALL-PARAMS`. Its first unavailable
analytic dependency is `M1248-L-ORIGIN`: the pinned closure has no proof of the
measurability, integrability, and limiting facts for the singular radial
weights. Consequently `M1248-L-WEIGHTED`, the `a = 1` endpoint, and the interior
Holder/rpow construction cannot be assembled. The audited unweighted Sobolev
theorem does not state these results and receives no root proof credit.

Retry requires placeholder-free local implementations, or an immutable
compatible pinned dependency, for the positive and interior weighted analytic
packages and their exact composition into `CKNAnalyticPackage`. Assuming that
package, adding an axiom, or substituting an unweighted inequality would violate
the frozen target. Lifecycle remains `planned`, root vector is provisionally
`[H1, M2, R3]`, and `theorem_complete=false`. Because the assigned proof phase
is not complete, no `.stage1-worker-selftest.json` is emitted.
