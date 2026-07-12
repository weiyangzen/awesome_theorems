# THM-M-0365 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source label "Tb theorem." It starts from
`L0 / rework_required` and inherits no source, proof, or acceptance credit from the metadata value
`source_status_untrusted: 已验证`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Repository wording | "singular integrals under nondegeneracy conditions" | This does not supply ordered binders, formal hypotheses, or a conclusion |
| Named theorem family | A Tb criterion relating testing on one or more accretive objects to boundedness of a Calderon-Zygmund operator | Global, local, non-homogeneous, square-function, bilinear, and operator-valued variants are inequivalent |
| Ambient analysis | A measure-bearing space, function spaces, and a Calderon-Zygmund operator | Dimension, measure, scalar field, kernel estimates, truncations, and initial operator domain are unspecified |
| Testing objects | One `b`, a pair `(b1,b2)`, or local testing systems | Accretivity versus para-accretivity, normalization, support, and quantitative constants are unspecified |
| Possible hypotheses | Weak boundedness and cancellation/testing conditions involving `T`, `T*`, and the testing objects | Exact pairings, BMO interpretation, adjoint, and necessity/sufficiency direction are not supplied |
| Possible conclusion | Usually an `L2` bounded extension with a quantitative norm bound | The repository wording does not state this conclusion, so it is not yet the canonical root |
| Neighboring target | `THM-M-0364` separately names the T1 theorem | T1 cannot be used as a simpler substitute for Tb |
| Lean surface | A future exact proposition after source and variant selection | No declaration, expression, imports, or elaboration claim exists at intake |
| Trust surface | Lean 4 kernel plus pinned mathlib candidate | Toolchain fingerprint, dependency closure, axioms, and TCB policy belong to later phases |

The likely historical lead is the 1985 para-accretive Calderon-Zygmund paper by Guy David,
Jean-Lin Journe, and Stephen Semmes. That lead is recorded for discovery only. The repository gives
no pinpoint theorem and its attribution names only David and Journe, so selecting a standard modern
formulation would broaden or substitute the supplied claim.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R4]`. `H1` records that a published
Tb theorem family is known while exact statement and source fidelity remain unaudited; it is not an
`H0` source claim. The first failed downstream gate is exact source-statement identification. The
statement phase must select a primary-source variant and freeze every domain, operator, testing,
accretivity, cancellation, boundedness, endpoint, and constant dependency before Lean elaboration.

This intake node itself is structurally self-tested. It creates no Lean declaration, makes no
kernel claim, and does not claim theorem completion. Exact commands and results are in
`validation.md`.
