# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `弗雷德霍姆择一定理`, attributes it to
Erik Fredholm, dates it to 1903, and gives only `紧算子方程的可解性` ("solvability of
compact-operator equations"). Stage0 repeats those fields while marking exact definitions,
assumptions, proof path, axioms, and artifacts as open. The rev-5.6 manifest preserves the source's
`已验证` only as `source_status_untrusted`.

This is secondary inventory metadata, not a statement or an H0 source. No primary-source edition,
theorem/page, exact operator equation, assumptions, proof boundary, or errata record is supplied.
The attribution and date are retained only as search keys pending source audit.

## Crosswalk

| Repository phrase | Possible mathematical component | Lean component | Intake status |
|---|---|---|---|
| "compact operator" | compact continuous linear endomorphism | `IsCompactOperator T` | pinned API probed; exact space open |
| "operator equation" | `(T - mu I)x = y` or `(I - T)x = y` | continuous-linear-map algebra and evaluation | equation absent from source |
| "alternative" | eigenvalue versus resolvent membership | `HasEigenvalue ... mu` / `mu ∈ resolventSet ...` | exact pinned candidate exists |
| "alternative" | injective versus surjective/bijective | `Function.Injective`, `Function.Surjective`, `Function.Bijective` | possible transport, not selected |
| "solvability" | range membership or existence of a solution | `∃ x, ... = y` | right-hand side and criterion absent |
| adjoint form | orthogonality to an adjoint kernel | Hilbert adjoint and orthogonal complement APIs | possible reading; Hilbert assumptions absent |
| `已验证` | untrusted inventory label | no proposition or proof evidence | explicitly rejected as credit |

## Pinned formal candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Operator.FredholmAlternative` documents
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet` as the Fredholm alternative. Its shape is:
for a compact continuous linear endomorphism `T` of a complete normed space over a nontrivially
normed field and `mu != 0`, `mu` is an eigenvalue of `T` or belongs to the resolvent set of `T`.

That declaration is a strong anchor candidate, not yet a source-statement match. The later anchor
audit must inspect its exact elaborated type, proof body, dependencies, axioms, and provenance after
the source has selected a formulation. The nearby theorem
`IsCompactOperator.hasEigenvalue_iff_mem_spectrum` and bijectivity/resolvent APIs indicate plausible
transports, but none is credited at intake.

## Required source work

The statement phase needs an immutable, independently inspected primary or authoritative source
that states the intended version. It must record edition, theorem and page, all assumptions,
notation correspondence, proof boundary, and errata, then map every clause to the Lean target.
Without that evidence, declaring the pinned spectral theorem canonical would be a substitution.
