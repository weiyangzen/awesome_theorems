# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `塞尔伯格迹公式`, attributes it to
Atle Selberg, gives the year 1956, and states only `自守形式的迹公式` ("trace formula for
automorphic forms"). Stage0 repeats this metadata and explicitly leaves precise definitions,
hypotheses, proof history, axioms, and machine artifacts open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

No bibliographic work, edition, article section, displayed formula, theorem number, page,
normalization, assumptions, proof passage, errata, or formal artifact is supplied. The historical
name makes the mathematical family identifiable, so the provisional human status is `H1`, but it
does not select a proposition suitable for exact source fidelity or Lean elaboration.

## Candidate source work

The statement phase must choose an immutable primary publication or an authoritative fixed edition
that states one formula. It must record the exact passage, all hypotheses and conventions, the
spectral and geometric terms line by line, proof boundaries, and known errata, followed by
independent source review. Intake does not choose a convenient textbook version because compact,
cofinite noncompact, and representation-theoretic forms are not interchangeable.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "automorphic forms" | group/lattice, quotient, weight/representation, function space | exact bundled space and invariance/analytic predicates | absent; `ModularForm` and `CuspForm` APIs only probed |
| "trace" | convolution/kernel operator, domain, trace-class or regularization | operator plus a justified trace notion | absent; finite-dimensional `LinearMap.trace` is not sufficient |
| "spectral side" | eigenvalues/multiplicities and any continuous or residual terms | convergent sums/integrals over a frozen spectrum | absent |
| "geometric side" | identity and source-selected conjugacy/orbital terms | conjugacy-class/orbital-integral definitions with fixed measures | absent |
| "formula" | exact equality and transform conventions | one elaborated `Prop` with ordered binders and hypotheses | absent |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports modular-form, finite-dimensional trace, and Haar-measure modules and checks one API
from each. A repository-local name search found Selberg sieve declarations but no Selberg trace
formula or automorphic-form declaration. This bounded observation is not the later immutable anchor
audit and does not establish that no external or future formalization exists.
