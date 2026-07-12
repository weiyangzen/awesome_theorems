# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `赫米特函数完备性`, attributes the entry to
Charles Hermite and the year 1864, and supplies only the sentence `Hermite函数构成L^2的完备正交基`
("Hermite functions form a complete orthonormal basis of L2"). `Docs/Stage0_Blueprint.md` repeats
that sentence but leaves exact definitions, assumptions, proof history, equivalent formulations,
axioms, and machine artifacts open. The rev-5.6 manifest deliberately retains `已验证` only in the
field `source_status_untrusted`.

These repository records identify the theorem family but are not a primary proof source. They give
no edition, theorem number, page, normalization, scalar field, measure, assumptions, proof, or
errata. The historical attribution and date are therefore inventory metadata, not accepted `H0`
evidence.

## Statement selection and required source audit

For a literal Lean target, the statement gate selects the standard complex-valued Lebesgue-space
normalization

`psi_n(x) = pi^(-1/4) / sqrt(n!) He_n(sqrt(2)x) exp(-x^2/2)`,

where `He_n` is mathlib's monic probabilists' `Polynomial.hermite n`. This is the usual normalized
physicists' Hermite function rewritten through `H_n(x) = 2^(n/2) He_n(sqrt(2)x)`. The canonical
conclusion identifies these literal functions, almost everywhere, with a `Nat`-indexed complex
`HilbertBasis` of `Lp Complex 2 volume`.

The source audit must inspect an immutable edition of a primary or authoritative analysis source
that states the complete orthonormal-basis theorem. It must record the exact definition of
the Hermite polynomials and normalized functions, the `L^2` measure and scalar field, the theorem
and page, all assumptions, proof boundary, and errata. An independent reviewer must verify the
statement and assumption crosswalk before `H0` can be claimed.

## Crosswalk

| Repository phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Hermite functions" | exact polynomial convention, Gaussian factor, normalization constant | `hermiteFunction : Nat -> Real -> Complex` | standard probabilists' rewrite frozen and elaborated |
| "L^2" | real line, Lebesgue measure, real or complex values, a.e. equality | `Lp Complex 2 leb` | complex Lebesgue type frozen and elaborated |
| "orthonormal" | unit norm and pairwise orthogonality | `Orthonormal K` for the concrete family | abstract interface available; theorem open |
| "complete" | dense linear span, or equivalently zero orthogonal complement | dense-span proposition and checked equivalence to the chosen basis packaging | abstract `HilbertBasis.mk` API available; Hermite proof open |
| "basis" | complete orthonormal sequence, not a Hamel basis | `HilbertBasis Nat Complex (Lp Complex 2 leb)` | canonical representation frozen |
| `已验证` | untrusted repository label | no proposition or proof credit | rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe confirms the probabilists' `Polynomial.hermite`, its Gaussian derivative identity, the
general `MeasureTheory.Lp` type, and `HilbertBasis` construction/dense-span interfaces. A scoped
source-name search found Hermite polynomial files but no Hermite-function `L^2` basis declaration.
This is only an intake boundary observation, not the immutable exhaustive anchor audit assigned to
the later anchor-audit phase.
