# Proof outline: Boxdot Conjecture

<a id="N0-membership"></a>
## N0 — choose a theorem of L

Hypotheses: a normal modal logic `L`, the faithful boxdot equivalence `H`, a
formula `φ`, and `hφ : L ⊢ φ`.

Inference: unfold the desired inclusion pointwise; it is enough to prove
`KT ⊢ φ` for this arbitrary `φ`.

Output: the local goal `KT ⊢ φ`.

Formal anchor: `boxdotConjecture`, introduction of `φ hφ`.

Downstream use: supplies `hφ` to N1 and fixes the formula reflected by N2.

Exceptional cases: none; `φ` is arbitrary and no syntactic case split is used.

Trust boundary: this is ordinary dependent-function and set-subset
introduction, checked by the Lean kernel at trust zero.

<a id="N1-translation"></a>
## N1 — close L under the boxdot translation

Hypotheses: `hφ : φ ∈ L` and the claim-owned translation-closure input
`translation_closed : Set.MapsTo boxdot L L`.

Inference: specialize translation closure at `hφ`.

Output: `hboxdot : boxdot φ ∈ L`.

Formal anchor: `boxdotConjecture_translation_step`.

Downstream use: N2 consumes `hboxdot` as the forward premise of faithfulness.

Exceptional cases: atomic, implication, and necessity cases belong to the
proof of translation closure; none is suppressed by this composition node.

Trust boundary: translation closure is an explicit hypothesis of the
claim-owned equivalent proposition, not a provider oracle or hidden axiom.

<a id="N2-reflection"></a>
## N2 — reflect the translated theorem into KT

Hypotheses: `hboxdot : boxdot φ ∈ L` and
`faithful φ : boxdot φ ∈ L ↔ φ ∈ KT`.

Inference: apply the forward direction of the equivalence.

Output: `φ ∈ KT`.

Formal anchor: `boxdotConjecture_reflection_step`.

Downstream use: discharges the pointwise inclusion goal from N0.

Exceptional cases: faithfulness is quantified over every formula, so no
formula constructor or proof branch is excluded.

Trust boundary: only an explicitly supplied equivalence is eliminated; the
source theorem body containing `sorryAx` is never imported or invoked.

<a id="N3-inclusion"></a>
## N3 — assemble the inclusion

Hypotheses: the outputs and unchanged hypotheses of N0–N2.

Inference: compose translation closure with faithful reflection for the
arbitrary member selected in N0.

Output: `L ⊆ KT`.

Formal anchor: `boxdotConjecture` and `boxdotConjecture_audit_root`.

Downstream uses: satisfies the claim-owned Boxdot statement and is transported
bidirectionally to the frozen elementwise reading by the audit declarations.

Exceptional cases: none; set inclusion is proved for every member of `L`.

Trust boundary: the composition is a local theorem body under `import Mathlib`;
canonical Master compilation and semantic-environment recomputation remain
mandatory after harvest.
