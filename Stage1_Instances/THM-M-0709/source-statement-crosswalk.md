# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` supplies only the title, Emil Post, 1946, and the gloss "Post
correspondence problem is undecidable." `Docs/Stage0_Blueprint.md` repeats this and marks formal
status `已验证`; the rev-5.6 manifest correctly retains that label only as untrusted metadata. These
records contain no definition, exact quantifiers, alphabet restriction, proof citation, or Lean
artifact.

## Primary source candidate

Emil L. Post, "A variant of a recursively unsolvable problem," *Bulletin of the American
Mathematical Society* **52** (1946), 264-268, DOI
`10.1090/S0002-9904-1946-08555-9` is the historical primary-source candidate. It is a locator, not
an accepted H0 receipt: the exact scan and content hash, pinpoint definition/theorem text, notation,
alphabet assumptions, reduction boundary, and errata still require inspection and independent
review. The Project Euclid locator was network-reachable during intake only through a denial page,
so this worker does not pretend to have inspected the article text.

## Crosswalk

| Claim component | Human-source anchor | Lean candidate | Intake status |
|---|---|---|---|
| Finite list of word pairs | Post 1946, exact definition/passage pending | `List (List Sigma × List Sigma)` or an encoded equivalent | semantic shape frozen; representation open |
| A correspondence solution | Post 1946, exact notation/passage pending | nonempty `List (Fin tiles.length)` with equal paired concatenations | bounded probe elaborates; source pinpoint open |
| Uniform decision problem | Article title and historical theorem family; exact theorem text pending | a predicate on effective instance codes | code and malformed-input policy open |
| "Recursively unsolvable" | Post's 1946 computability convention, exact model audit pending | `¬ ComputablePred HasSolution` or no deciding Turing machine | equivalence between conventions must be checked |
| Fixed alphabet restriction | exact source assumption and later strengthening must be separated | likely a fixed binary `Fintype` alphabet | not selected; unary/empty degeneracy excluded |
| Modified versus ordinary PCP | the article title signals a variant; exact reduction chain needs inspection | separate predicates plus a many-one reduction | neither may silently stand for the other |

No machine status follows from this citation. The bounded repo/mathlib search found general
computability APIs but no PCP declaration; that observation is only intake discovery and not the
immutable anchor audit required by the later `ANCHOR_AUDIT` item.

## Statement-phase handoff

The next phase must inspect and pin the primary source (plus a precise modern reference if needed),
freeze an effective coding and exact Lean target, connect semantic tile matches to codes, and test
mutations for empty witnesses, different index sequences, bounded witness length, alphabet
degeneracy, malformed codes, and the scope of computability/negation.

