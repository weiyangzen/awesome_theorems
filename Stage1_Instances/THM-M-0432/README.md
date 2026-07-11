# THM-M-0432 rev-5.6 intake

This is the `planned` dossier for the global Langlands correspondence over function fields. The
repository's Chinese label, "function-field Langlands correspondence", is not precise enough to
freeze one theorem: it can denote Drinfeld's rank-two result or Laurent Lafforgue's general
`GL_n` result. The neighboring target names the `GL_n` theorem but does not resolve the duplication.
The statement phase must therefore select a primary-source theorem before exact elaboration.

## Scope map

| Surface | Provisional scope | Intake boundary |
|---|---|---|
| Root variant | Laurent Lafforgue's global `GL_n` correspondence is the leading reading | Variant and precise theorem number require source acceptance |
| Base | Global function field `F` over a finite constant field | Curve/function-field and constant-field conventions must be fixed |
| Galois side | Continuous irreducible rank-`n` l-adic representations with finite determinant | Coefficients, continuity, isomorphism classes, and ramification API are absent |
| Automorphic side | Cuspidal automorphic representations of `GL_n(A_F)` with finite central character | Function-field adeles and automorphic representation objects are absent |
| Compatibility | Equality of unramified Frobenius and Satake characteristic-polynomial data | Normalization and exceptional-place quantifiers are not frozen |
| Boundaries | `n >= 1`; `n = 1` should recover class field theory; `n = 0` excluded | Drinfeld `GL_2` is only a specialization under the leading reading |
| Existing Lean | `AwesomeTheorems.Stage1.S1_M_060.StatementShape` | Discovery scaffold only: its rank equality is not the source theorem |
| Trust | Lean 4 kernel and a pinned mathlib closure | Exact toolchain, axioms, quotients, classical choice, and dependencies remain open |

The proof scope must eventually include construction in both directions or an accepted bijection,
cuspidality/irreducibility and finite-character restrictions, equivalence-class well-definedness,
and local-global compatibility at every unramified place. No special case or one-way map may replace
that root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source statement identification. Consequently the existing Lean declaration is not a canonical
formal target, no machine closure is credited, and theorem completion is false.

## Validation

The commands and exact results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, dossier references, and text hygiene only. Master acceptance and every
dependent phase remain outstanding.
