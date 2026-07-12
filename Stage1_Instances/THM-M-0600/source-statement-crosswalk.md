# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` names Marston Morse, gives 1925, and describes the result as the
local normal form at a nondegenerate critical point. `Docs/Stage0_Blueprint.md` repeats that phrase.
Their `已验证` label is explicitly untrusted under rev-5.6 and supplies neither a proof source nor
machine evidence.

## Candidate primary and standard sources

- Marston Morse, "Relations between the critical points of a real function of n independent
  variables", *Transactions of the American Mathematical Society* 27 (1925), 345-396. This is the
  historical source candidate matching the repository's date. The exact theorem/page, notation,
  assumptions, and any errata have not yet been inspected.
- John Milnor, *Morse Theory*, Annals of Mathematics Studies 51, Princeton University Press (1963),
  Lemma 2.2 (the Morse lemma). This is the candidate modern statement/proof anchor. The exact pages,
  edition wording, differentiability conventions, and errata must be checked against a stable copy
  before this record can support `H0`.

These references support the provisional `H1` classification only. They are not machine anchors and
have not received independent source review.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| nondegenerate critical point | `df p = 0` and nonsingular Hessian | Fréchet derivative plus nondegenerate second derivative/bilinear form | included; API open |
| local standard form | equality on a neighborhood after smooth coordinates | local diffeomorphism/chart centered at `p` and neighborhood equality | included; encoding open |
| Morse index | number `lambda` of negative square directions | finite-dimensional inertia/index witness | included; representation open |
| negative and positive squares | exact quadratic normal form, not asymptotic equality | coordinate decomposition and finite sums of squares | included; sign transport open |
| manifold formulation | transfer of the Euclidean local lemma through a chart | smooth manifold/model-with-corners interfaces and chart transport | included; boundary excluded |

## Formal-source boundary

No theorem-specific Lean file or legacy slot was found by the intake repository search. This absence
is not a complete mathlib/external audit, so the root remains `M4` provisionally rather than claiming
that no formalization exists. The statement phase must elaborate the exact target; anchor audit must
then search pinned mathlib and external Lean 4 sources and inspect terminal proof provenance.

Before `H0`, an independent reviewer must verify a fixed source edition, exact theorem/page, every
hypothesis and convention, the proof and errata status, and the row-by-row source-to-Lean mapping.
