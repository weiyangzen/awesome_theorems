# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `谱映射定理`, collective attribution, the period
"20th century", and only the gloss `全纯函数演算的谱` ("the spectrum of the holomorphic functional
calculus"). Stage0 repeats this metadata. The rev-5.6 manifest carries `已验证` solely as
`source_status_untrusted`. No primary source, edition, theorem/page, hypotheses, proof, errata, or
formal declaration is supplied.

The gloss narrows the topic beyond the many other results called spectral mapping theorems, but it
does not determine a formal proposition. A source audit must inspect an immutable authoritative
edition, record the exact theorem and assumptions, map its notation to the canonical target, check
errata, and obtain independent review. Until then the conventional equality is a candidate reading,
not an `H0` claim.

## Crosswalk

| Repository phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "spectrum" | noninvertibility spectrum over `Complex` | `spectrum` and the source-selected algebra hypotheses | generic API elaborates; exact domain open |
| "holomorphic" | holomorphic on an open neighborhood of the spectrum | a neighborhood plus a precise complex differentiability predicate | absent from source record |
| "functional calculus" | contour-integral holomorphic calculus producing `f(a)` | a pinned construction and its hypotheses | exact API/candidate not established at intake |
| "spectral mapping" | `spectrum (f(a)) = f '' spectrum(a)` | exact elaborated equality or checked transport | conventional candidate only |
| `已验证` | untrusted inventory status | no proposition or proof credit | rejected as evidence |

## Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe checks
`spectrum`, the continuous-functional-calculus theorem `cfc_map_spectrum`, and the polynomial
theorems `spectrum.map_polynomial_aeval_of_degree_pos` and
`spectrum.map_polynomial_aeval_of_nonempty`. The first is explicitly a continuous calculus theorem
with its own predicate/typeclass regime; the latter two concern polynomials over algebraically
closed fields. They demonstrate nearby infrastructure but do not establish statement identity with
the requested holomorphic calculus. Full candidate and provenance auditing belongs to the later
anchor-audit node.
