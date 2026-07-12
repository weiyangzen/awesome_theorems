# Immutable Lean anchor audit

Audit node: `S56-M-0317-ANCHOR_AUDIT`. Base revision:
`7421320db3a58c93ef0168e2164305d5798294b8`. The exact comparison target is
`AwesomeTheorems.THM_M_0317.TychonoffFixedPointTarget` in `Statement.lean`: every continuous
self-map of a nonempty compact convex subset of a Hausdorff locally convex real topological vector
space has an in-set fixed point. Names and informal resemblance receive no proof credit.

## Pinned mathlib inventory

The existing Lake manifest pins mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean at `4.29.0`. Complete source-tree name and
type-vocabulary searches found the target's component APIs but no Tychonoff/Schauder/Brouwer
compact-convex fixed-point declaration.

| Declaration | Audited role | Exact-root fit |
|---|---|---|
| `LocallyConvexSpace`, `IsCompact`, `Convex`, `Function.IsFixedPt` | exact statement vocabulary | definitions/predicates only |
| `exists_mem_Icc_isFixedPt_of_mapsTo` | continuous self-map of a real interval has a fixed point | genuine one-dimensional special case, not arbitrary `E` and `K` |
| `ContractingWith.exists_fixedPoint'` | Banach fixed point on a complete invariant subset | requires contraction and metric hypotheses absent from the root |
| `isCompact_univ_pi` | the other theorem commonly named Tychonoff: compactness of products | no fixed-point conclusion |

`AnchorAudit.lean` kernel-elaborates every credited declaration and an application of the interval
special case. Neither narrow theorem can close the root: the interval theorem fixes the ambient
ordered type and set shape, while the Banach theorem would broaden the hypotheses with contraction
and metric completeness.

## External Lean 4 discovery

Sourcegraph searches used `context:global archived:yes fork:yes lang:Lean` on 2026-07-12. Results
were discovery-only and were not installed or added to `.lake`.

| Query | Result and immutable matched revisions |
|---|---|
| `Tychonoff` | 24 indexed code matches. Lean 4 matches concern product compactness or unrelated uses: mathlib4 at `12b4b4adf73c3bf0917409bb4b9dd4c8b96f4e8f`, `teorth/analysis` at `ef032052e136994fdd4d1b8fd41f5cc093f75978`, `google-deepmind/formal-conjectures` at `fdbea4653453a764aa7f952d3b45c93007356cc9`, and `lean-liquid` at `087fffad55dc1dd8d54ab35c9816926a45b8c0fd`; none is a fixed-point proof. |
| `Tikhonov` | five matches, all regularization/tensor material in `lean-dojo/TorchLean` at `01060dcb274eab6ec361f3ae2022b41c6399f788`. |
| `Schauder fixed point` | no indexed match. |
| `exists_mem_Icc_isFixedPt` | only mathlib4's interval result, independently re-audited at the local pin rather than credited from the moving index. |

These bounded queries do not establish global absence. They establish that no concrete external
candidate was found to pin, inspect, transport, or integrate. No dependency clone, fetch, update,
or build was performed.

## Verdict

The formal anchor inventory is self-tested and suitable input to the obligation-tree phase. The
root remains `M4`: its exact proposition elaborates, but no proof-bearing exact candidate exists in
the inspected pinned closure and no external candidate was located. The likely proof route through
finite-dimensional approximation, a finite-dimensional fixed-point theorem, and compactness is
future obligation-tree work, not evidence supplied by this audit.

This node supplies no `H0`, root proof, accepted receipt, audit completion, or theorem completion.
Master acceptance remains required.
