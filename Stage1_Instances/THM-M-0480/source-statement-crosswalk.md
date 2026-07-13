# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:3525-3530` supplies exactly the title `素数定理`, attribution to
Jacques Hadamard and Charles de la Vallee Poussin, year 1896, formula `pi(x) ~ x/ln(x)`, importance
`高`, and status `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no work, edition, theorem/page,
definition of `pi`, domain, limit, asymptotic convention, assumptions, proof boundary, correction,
erratum, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:13163-13188` projects the record as `THM-M-0480` while explicitly leaving
the formal system, foundation, precise definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Rev-5.6 therefore retains
`已验证` only as untrusted metadata and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository component | Mathematical detail required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `pi(x)` | count of primes with an exact endpoint and input convention | `Nat.primeCounting`, possibly cast and composed with a reviewed floor | natural API located; real extension and identity open |
| `x` | natural sequence or real variable, domain, and exceptional values | `Nat` or `Real` input with an explicit filter | absent from the catalog |
| `~` | asymptotic equivalence at positive infinity | `Asymptotics.IsEquivalent Filter.atTop` or a checked ratio-limit form | generic API located; encoding not selected |
| `x/ln(x)` | natural logarithm, real division, coercions, and grouping | `fun x : Real => x / Real.log x` or a natural-domain cast variant | conventional candidate only |
| limiting process | `x` tends to positive infinity | `Filter.atTop` over the selected domain | implicit, not source-audited |
| alternate forms | ratio limit, `theta ~ id`, `psi ~ id`, or nth-prime asymptotic | separate propositions joined by checked transports | no alternate is credited |
| Hadamard/de la Vallee Poussin, 1896 | pinpoint works, proposition genealogy, definitions, proof and corrections | source provenance only | catalog lead, not H0 |
| `已验证` | claimed formal status | exact kernel and accepted evidence would be required | explicitly rejected |

## Human-source status

The attribution and date are credible discovery leads for the two independent 1896 proofs, but the
repository contains no preserved primary edition, scan digest, title, theorem or page locator,
transcription, definition package, proof-boundary map, translation audit, correction/errata search,
or independent review. This intake does not invent those bibliographic fields from memory and does
not treat a broad historical citation as `E4` or `H0`.

Exploratory lookup located the Numdam bibliographic item for Jacques Hadamard, *Sur la distribution
des zeros de la fonction zeta(s) et ses consequences arithmetiques*, *Bulletin de la Societe
mathematique de France* 24 (1896), 199-220, DOI `10.24033/bsmf.545`. A DJVU scan was downloaded to
temporary storage during discovery, but no proposition or incorporated definition was transcribed,
pinpointed, cross-checked, or reviewed. The bibliographic item is therefore only an `E5` source lead,
not an accepted primary-source packet or support for H0.

Before H0 or exact statement selection, accountable reviewers must preserve a lawful immutable
primary or approved authoritative source; identify the exact displayed proposition and every
incorporated definition; map domains, binders, endpoints, limiting semantics, logarithm, premises,
conclusion, proof boundary, attribution and genealogy; audit translations, corrections, and
errata; and independently approve the source-to-Lean crosswalk. The provisional `H1` records a
published, recognizable theorem family with that source reconstruction still open.

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.NumberTheory.PrimeCounting` defines `Nat.primeCounting` and proves its divergence. It does
not state PNT. `Mathlib.NumberTheory.Chebyshev` provides `theta`, `psi`, the Abel-summation identity

```text
primeCounting (floor x) = theta x / log x + an integral remainder
```

and upper/remainder estimates. The same module explicitly lists Chebyshev's lower bound as a TODO.
`Mathlib.NumberTheory.LSeries.Nonvanishing` describes its results as prerequisites for PNT and
Dirichlet's theorem, not as either terminal theorem.

A bounded exact-topic search over repository-local Lean and pinned mathlib located no terminal
declaration for `primeCounting ~ x/log(x)`, `theta ~ id`, or the named prime number theorem. That is
not a global absence claim. The Chebyshev module points to the external
`AlexKontorovich/PrimeNumberTheoremAnd` project as the origin of some upstreamed parts, but this
intake does not audit an immutable external terminal body or award external proof credit.

`IntakeProbe.lean` only authenticates adjacent pinned declarations and reports axioms for three
representative reduction/estimate theorems. It declares no target and no proof body. Consequently
the canonical module and expression, expression hash, target environment fingerprint, checked
transports, statement mutations, terminal proof provenance, and trust acceptance remain open; the
machine status is `M3`.

## First blocker and retry condition

The first downstream blocker is exact source-statement identity. Reviewers must resolve every
`pi`, domain, filter, floor/cast, logarithm, equivalence, binder, hypothesis, conclusion, alternate
form, and boundary decision recorded in the scope map. Only then may the statement phase elaborate
the exact target with minimal pinned imports, serialize its expression and environment
fingerprints, compile checked transports, and run the required mutation suite.
