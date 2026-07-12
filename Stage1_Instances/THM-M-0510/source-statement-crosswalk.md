# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Hardy and Ramanujan, gives the year 1918, and says only
"an asymptotic formula for the integer partition function." Stage0 repeats that gloss and leaves
the exact definitions, assumptions, proof path, equivalent formulations, axioms, and formal
artifact open. The manifest intentionally preserves `已验证` as `source_status_untrusted`.

## Identified original article

Crossref DOI metadata for `10.1112/plms/s2-17.1.75` identifies G. H. Hardy and S. Ramanujan,
"Asymptotic Formulaae in Combinatory Analysis," *Proceedings of the London Mathematical Society*,
series 2, volume 17, issue 1 (1918), pages 75-115. This is a bibliographic locator, not an inspected
theorem/page crosswalk: the article text, exact displayed formula, assumptions, and errata were not
available from that metadata. Consequently this intake claims H2, not H0.

## Statement crosswalk

| Source component | Intended mathematics | Candidate Lean component | Intake status |
|---|---|---|---|
| integer partitions | unordered positive parts summing to `n` | `Nat.Partition n` | pinned API elaborated |
| `p(n)` | number of such partitions | `Fintype.card (Nat.Partition n)` | candidate encoding elaborated |
| `n -> infinity` | natural-number limit | `Filter.atTop` | pinned API elaborated |
| asymptotic formula | quotient tends to one | `Asymptotics.IsEquivalent Filter.atTop` | candidate relation elaborated |
| leading term | `exp(pi*sqrt(2*n/3))/(4*n*sqrt(3))` | `Real.exp`, `Real.pi`, `Real.sqrt`, real coercions | candidate expression elaborated |
| `已验证` | untrusted inventory label | no theorem or proof credit | explicitly rejected |

## Remaining source gate

The statement/source phases must inspect an immutable scan or edition, cite the exact formula and
page, record all definitions and assumptions plus known errata, and obtain independent review. They
must also determine whether the conventional modern formula above is literally the source theorem
or a corollary/normalization requiring a source-backed bridge. No external formalization candidate
was credited during this intake; that search belongs to the later anchor-audit phase.
