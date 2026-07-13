# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `Elekes theorem`, Gyorgy Elekes, the year 1997,
and the complete gloss `a lower bound for sumsets and product sets`. It gives no bibliography,
domain, definitions, exponent, constant, binders, hypotheses, conclusion, proof, or formal artifact.
`Docs/Stage0_Blueprint.md` repeats that gloss while leaving definitions, assumptions, proof route,
dependencies, equivalent formulations, axioms, and machine status open. The rev-5.6 manifest
preserves `verified` only as `source_status_untrusted`; it supplies no proof credit.

## Primary source candidate

Gyorgy Elekes, "On the number of sums and products," *Acta Arithmetica* **81** (1997), no. 4,
365-367, DOI `10.4064/aa-81-4-365-367` is the exact bibliographic match. An archive copy at
`http://matwbn.icm.edu.pl/ksiazki/aa/aa81/aa8145.pdf` was inspected during intake: 3 pages, 158206
bytes, observed SHA-256
`f217314fce5ca286a44d98ca0f8154dfa2a13749610ecad73f41798028c39a44`.

The opening paragraph on printed page 365 defines the source domain and notation. Theorem 1 on the
same page supplies the complete candidate conclusion. Section 2 on page 366 supplies a complete
proof using Proposition 1, the Szemeredi-Trotter theorem stated on that page. The PDF is a
discovery-time external input, not vendored immutable evidence, an accepted edition, or an `H0`
packet. Master source acceptance must preserve a lawful immutable copy, independently hash and
review it, inspect corrections and errata, and approve all premise and conclusion mappings.

Crossref DOI metadata independently matches the title, sole author, year, journal, volume, issue,
and pages. It is bibliographic corroboration, not the mathematical proof source.

## Crosswalk

| Source component | Candidate mathematical meaning | Prospective Lean component | Intake status |
|---|---|---|---|
| opening convention, p. 365 | `A` is a finite subset of `Real \ {0}`; `n = |A|` | `A : Finset Real` plus `forall a in A, a != 0`; `A.card` | exact candidate mapping; encoding not frozen |
| `A + A`, p. 365 | `{a + a' | a, a' in A}` | pointwise `A + A` or explicit `Finset.image2` | adjacent API elaborates; checked transport open |
| `A * A`, p. 365 | `{a * a' | a, a' in A}` | pointwise `A * A` or explicit `Finset.image2` | adjacent API elaborates; checked transport open |
| `|S|`, p. 365 | finite set cardinality | `Finset.card`, cast to `Real` in the inequality | cast convention open |
| "positive absolute constant" | one `c > 0` independent of `n` and `A` | outer `exists c : Real, 0 < c /\ ...` | binder order is candidate only |
| Theorem 1, p. 365 | `c n^(5/4) <= max(|A+A|, |A*A|)` | `Real.rpow` on the cast cardinality and cast maximum | proposition-shaped probe elaborates; not canonical |
| Proposition 1, p. 366 | rich-line incidence upper bound | future incidence theorem/bridge | no matching pinned declaration located in bounded search |
| Section 2, p. 366 | affine-line construction, incidence application, product bound, maximum conclusion | future obligation tree and checked composition | complete human proof route located; no Lean proof credit |
| catalog `verified` | untrusted inventory label | no Lean proposition or proof object | explicitly rejected as evidence |

## Source and formal boundary

The candidate supports provisional `H1`: a primary paper with a complete proof and pinpoint
statement has been inspected, while immutable admission, correction and errata status, complete
definition/premise mapping, and independent review remain open. It is not `H0`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks pointwise finite real sumsets and product sets, their cardinalities, the cardinality maximum,
`Real.rpow`, and a candidate proposition shape. A bounded name search found no Elekes,
Szemeredi-Trotter, or exact sum-product lower-bound declaration. This justifies provisional `M3`
for the elaborated shape and interfaces only; it is not an exhaustive absence claim, anchor audit,
statement fingerprint, proof, or root closure.

