# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7043-7048` records only the name, Hilton/Milner attribution, year
1967, importance, untrusted label `已验证`, and the gloss `非平凡相交族的最大大小` (maximum size of a
nontrivial intersecting family). Git history places the uncited record at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26281-26306` repeats the gloss while leaving the exact definitions,
premises, proof, equivalences, axioms, machine state, and artifact links open. The rev-5.6 manifest
therefore correctly resets the item to `L0 / rework_required`; its source status is not proof
evidence.

There is also a stable-ID history boundary. Immediately before deduplication commit
`c61be3c80710c07c5f7626e3404e51f40ecb39a6`, bare ID `THM-M-0964` denoted Vosper's theorem and
Hilton-Milner was `THM-M-0992`; after that commit Hilton-Milner is the current `THM-M-0964`.
Provenance must therefore bind the current ID together with title, attribution, and gloss, never a
historical bare ID alone.

## Primary-source lead and access boundary

A. J. W. Hilton and E. C. Milner, *Some Intersection Theorems for Systems of Finite Sets*, *The
Quarterly Journal of Mathematics* 18(1) (1967), 369-384, DOI
`10.1093/qmath/18.1.369`. Crossref confirms the authors, title, journal, volume, issue, pages, year,
DOI, and publisher version-of-record PDF locator.

The DOI landing page and PDF returned an OUP Cloudflare challenge/HTTP 403 in this worker. The
primary article body was therefore not inspected or hashed. No numbered theorem, printed page,
definition, proof, correction, or erratum from that article is claimed. The authenticated
bibliography supports source discovery only and cannot establish H0.

## Immutable secondary statement leads

Glenn Hurlbert and Vikram Kamat, *New injective proofs of the Erdős-Ko-Rado and Hilton-Milner
theorems*, arXiv:`1609.04714v3`, Theorem 11, states the following modern form. For
`2 <= r < n/2`, if `F` is an intersecting family of `r`-subsets of `[n]` with empty total
intersection, then

```text
|F| <= choose (n - 1) (r - 1) - choose (n - r - 1) (r - 1) + 1.
```

It also classifies equality up to isomorphism: the standard Hilton-Milner family `H`, or, when
`r = 3`, an exceptional family `K`. The observed v3 PDF SHA-256 is
`6e354fcdcad0280e92f2406251db1f8ba1ad3d97944f99a58e97ad6797719035`.

Denys Bulavka and Russ Woodroofe, *A short proof of the Hilton-Milner Theorem*,
arXiv:`2411.02513v4`, Theorem 1, independently gives the same bound for pairwise-intersecting
`k`-subsets with empty total intersection under `k <= n/2`. Its observed v4 PDF SHA-256 is
`b01196bd2e54e24b333dc0f40da5ff2da017e4bdd292cd544be6e42ccc96bb2c`.
Its displayed Theorem 1 is bound-only; later discussion treats uniqueness in a stricter range.

These are credible immutable proposition discriminators, not substitutes for the primary source.
Their different endpoint and equality scopes are exactly why intake leaves the canonical claim null.

## Component crosswalk

| Catalog/source component | Secondary-source meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| finite universe | `[n]` | `Fin n` | routine-looking model choice, but no transport frozen |
| uniform family | family of `k`-subsets | `Finset (Finset (Fin n))` plus `Set.Sized k` | candidate encoding only |
| intersecting | every two members meet | `Set.Intersecting` | agrees on nonempty members; exact convention/boundaries open |
| nontrivial | total intersection is empty | image to `Set (Set (Fin n))` then `Set.sInter = ∅` | candidate encoding; star-equivalence and empty-family behavior open |
| range | `2 <= k` and strict half-range in Theorem 11; weak half-range in Theorem 1 | Nat inequalities | primary endpoint and boundary behavior open |
| maximum bound | binomial difference plus one | `Nat.choose`, truncated subtraction | candidate expression elaborates, but is not canonical |
| attainment | standard family `H` reaches the bound | no local declaration | absent from candidate probe |
| equality | `H`, plus `K` for `k = 3`, in one restatement | no local declaration/isomorphism encoding | catalog incorporation open |
| `已验证` | catalog metadata | no accepted receipt | no H or M credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded name and
exact-topic searches found generic set-family infrastructure and `Finset.erdos_ko_rado`, but no
Hilton-Milner declaration. `IntakeProbe.lean` checks `Set.Intersecting`, `Set.Sized`, `Set.sInter`,
fixed-cardinality powersets, `Nat.choose`, and the EKR neighbor. It also elaborates an unproved
`CandidateTargetShape` matching the strict-range bound-only secondary statement.

This supports `M3` statement/interface discovery only. The proposition definition has no proof
body, no expression fingerprint, and no source-admission status. `Finset.erdos_ko_rado` proves a
different upper bound without the nontrivial-family improvement and receives no root credit. The
anchor-audit phase must later conduct exhaustive candidate, terminal-body, dependency, placeholder,
axiom, unsafe, and provenance checks.

## Required admission

Before H0, accountable reviewers must admit and hash a complete primary edition, identify the exact
theorem and definitions, map every binder, premise, conclusion, endpoint, construction, and equality
clause, inspect corrections/errata, and independently review the translation. Before statement-gate
or machine credit, one selected claim must be elaborated with minimal imports, serialized and
fingerprinted, mutation-tested, and linked to every alternate encoding by checked witnesses.
