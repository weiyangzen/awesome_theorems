# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1794-1799` supplies exactly the title `梅尔格良定理`, attribution
to Sergei Mergelyan, the year 1951, the gloss `紧集上连续函数的多项式逼近` ("polynomial
approximation of continuous functions on compact sets"), importance "high," and status `已验证`.
Git blame attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, definition,
connected-complement condition, holomorphicity condition, ordered binders, exact conclusion,
boundary policy, proof locator, errata record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6896-6921` repeats that gloss while explicitly leaving exact definitions
and premises, formal system, foundation, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Inspected source leads

The permalink revision `32115` of the *Encyclopedia of Mathematics* entry "Mergelyan theorem" was
observed on 2026-07-13. It states that if `K` is a compact subset of the complex plane with
connected complement, then every function continuous on `K` and holomorphic at its interior points
can be uniformly approximated on `K` by polynomials in `z`. The entry cites:

- S. N. Mergelyan, "On the representation of functions by series of polynomials on closed sets,"
  *Doklady Akademii Nauk SSSR* 78:3 (1951), 405-408; English translation in *American Mathematical
  Society Translations* 3 (1962), 287-293.
- S. N. Mergelyan, "Uniform approximation to functions of a complex variable," *Uspekhi
  Matematicheskikh Nauk* 7:2 (1952), 31-122; English translation in *American Mathematical Society
  Translations* 3 (1962), 294-391.

The stable arXiv artifact Arthur A. Danielyan, "On the zero-free polynomial approximation
problem," arXiv:1501.00247v1 (2015), page 1, defines `A(E)` as complex-valued functions continuous
on compact `E` and analytic in its interior, assumes `C \\ E` connected, and states Theorem A: for
each positive epsilon and `f` in `A(E)`, a polynomial is pointwise within epsilon throughout `E`.
It identifies this as Mergelyan's theorem and cites primary/standard sources. The inspected PDF has
SHA-256 `19270fa85fa42a7042b41e946ec8171cfc7f4c2a73c5db61550b691298f2bdc1`.

Both are credible secondary witnesses to the intended family, but neither is an admitted pinpoint
primary-source edition. The encyclopedia page is mutable despite the revision URL; Danielyan's
paper invokes rather than proves Mergelyan. The catalog cites neither. A primary-text preservation
decision, theorem and incorporated-definition locator, assumption/proof crosswalk, translation and
errata audit, and independent review remain open. These leads support provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog phrase | Source-lead component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "compact set" | compact `K` contained in the complex plane | `K : Set Complex`, `IsCompact K` | ambient space and encoding omitted by catalog |
| missing condition | complement of `K` is connected | `IsConnected Kᶜ` or sourced equivalent | indispensable clause absent from catalog |
| "continuous function" | complex-valued `f` continuous on `K` | `f : Complex -> Complex`, `ContinuousOn f K`, or bundled map | codomain and representation omitted |
| missing condition | `f` is holomorphic on `interior K` | `DifferentiableOn Complex f (interior K)` or checked analytic equivalent | indispensable clause absent from catalog |
| "polynomial approximation" | for every positive epsilon, some complex polynomial has uniform pointwise error below epsilon on `K` | `p : Polynomial Complex`, `forall z in K, norm (p.eval z - f z) < epsilon` or a checked norm/density form | quantifier order, norm, strictness, and evaluation encoding open |
| 1951 / Mergelyan | 1951 short paper and 1952 long treatment identified by secondary bibliography | immutable source IDs and reviewed locators | primary text and correction audit not admitted |
| `已验证` | untrusted inventory label | source and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib exposes `IsCompact`, `IsConnected`, `ContinuousOn`, `interior`,
`AnalyticOnNhd`, `Polynomial.eval`, `Polynomial.toContinuousMapOn`, and
`polynomialFunctions`. It proves real polynomial density and a complex
`polynomialFunctions.starClosure_topologicalClosure`; the latter explicitly uses star closure and
therefore conjugation. Those are substrate or non-substitutes, not an exact Mergelyan theorem.

A bounded exact-topic search over repo-local Lean and pinned mathlib found no declaration named for
Mergelyan, complex polynomial approximation on compact sets with connected complement, or the
corresponding `A(K)` density theorem. This is scoped intake discovery only, not the later immutable
formal-candidate audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must admit an immutable primary edition, locate the
theorem and every incorporated definition, map the complex domain, compactness, connected
complement, continuity, interior holomorphicity, approximation quantifiers and boundary cases,
audit translations and errata, and independently approve fidelity to `THM-M-0249`. Only then may
the statement phase freeze minimal imports, an exact Lean expression and environment fingerprint,
checked alternate encodings, and the required statement mutations.
