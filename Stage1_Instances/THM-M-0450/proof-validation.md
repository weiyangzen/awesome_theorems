# THM-M-0450 proof-phase validation

Item: `S56-M-0450-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented bodies

`Proof.lean` adds genuine local bodies for the group-theoretic part of the
frozen model-transport obligation. It proves that additive equivalences
preserve finite generation, the doubling subgroup, its finite-index property,
and all three height-package laws under pullback. The point-model results
specialize to mathlib's checked
`Jacobian.Point.toAffineAddEquiv`.

The file also imports `Statement.lean` and proves
`exactTarget_of_descent_packages` with result type the canonical
`Stage1Instances.THM_M_0450.ExactTarget`. This removes the earlier composition
ambiguity caused by the standalone obligation module's namespace-local copy of
`ExactTarget`.

These bounded bodies do not construct weak Mordell-Weil or an elliptic height.
No whole frozen obligation is therefore claimed closed, and the exact root
remains `M3`.

## Commands and results

Validation ran in the worker clone at 2026-07-13T16:49Z
(2026-07-14T00:49+08:00). The existing canonical
pinned `.lake` artifacts were reused. No dependency update, build, clone,
fetch, or `.lake` mutation was run.

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0450
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" Proof.lean
rm -f Statement.olean ObligationTree.olean
  exit 0
  All ten proof declarations elaborated. Every `#print axioms` result was
  exactly `[propext, Classical.choice, Quot.sound]`.

bash Stage1_Instances/THM-M-0450/check_proof.sh
  exit 0
  All ten declarations replayed in a temporary directory. The script checked
  exact axiom-report coverage and the recorded axiom set, ran the prohibited
  token scan, and then ran `check_proof.py`.
  PASS THM-M-0450 proof phase: model transports and exact conditional assembly checked
  PASS THM-M-0450 pinned proof replay: 10 declarations, exact recorded axiom set
  root closure: open (M3); weak Mordell-Weil and elliptic height remain open

python3 Stage1_Instances/THM-M-0450/check_obligation_tree.py
  exit 0
  PASS THM-M-0450 obligation tree: 14 obligations, 31 typed edges
  registry denominator sha256: 72f2ac93d10c6e4c5b106c189ee5823c50970d512e054fb247b6796ad00d8e24
  root closure: open (M3); weak Mordell-Weil and elliptic-height packages remain open

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0450
  exit 0: rank 92, planned, theorem_complete=false

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' \
  Stage1_Instances/THM-M-0450/Proof.lean
  exit 1 with empty output: no prohibited proof device

python3 -m json.tool Stage1_Instances/THM-M-0450/proof-receipt.json >/dev/null
  exit 0

git diff --check -- Stage1_Instances/THM-M-0450 .stage1-worker-selftest.json
  exit 0
```

The immediate mathematical-package cut is `M0450-B-WEAKMW` plus
`M0450-H-HEIGHT`. The full frozen remaining cut also retains
`M0450-X-TRANSPORT`, because only proper transport subbranches are proved here,
and `M0450-X-SOURCE`, `M0450-X-PROVENANCE`, and `M0450-X-TRUST`. Downstream
validation, release, independent review, and master acceptance also remain
open. This is a self-tested partial proof contribution, not a Mordell-Weil
theorem-completion claim.
