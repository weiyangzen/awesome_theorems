# THM-M-0918 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6714-6719` supplies exactly the Chinese title
`Rogers-Ramanujan identities`, the joint attribution Leonard Rogers/Srinivasa Ramanujan, the date
1894, the gloss `an identity of the partition function`, importance "high," and status `verified`
(English here translates the catalog fields). All six uncited lines entered the repository in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, definition, bibliography,
ordered binder, hypothesis, conclusion, proof boundary, errata, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25039-25064` repeats the gloss while explicitly leaving the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. The rev-5.6 manifest retains `verified`
only as `source_status_untrusted` and resets the item to `L0 / rework_required`.

## Modern authoritative statement lead

NIST Digital Library of Mathematical Functions section 17.2(vi), "Rogers-Ramanujan Identities,"
was inspected at `https://dlmf.nist.gov/17.2.vi` on 2026-07-13. Equations 17.2.49 and 17.2.50 at
stable permalinks `https://dlmf.nist.gov/17.2.E49` and `https://dlmf.nist.gov/17.2.E50` display the
two analytic sum-product identities. The inherited DLMF convention from section 17.1 takes `q` to
be complex with `|q| < 1` unless stated otherwise. Section 17.2(vi) points to George E. Andrews,
*The Theory of Partitions* (1976), section 7.3.

DLMF section 26.10(iv), inspected at `https://dlmf.nist.gov/26.10.iv`, explicitly calls equations
26.10.13 and 26.10.14 the Rogers-Ramanujan identities and links them back to section 17.2(vi). With
definitions incorporated from 26.10(i), they state the two restricted-partition count equalities;
the section cites Andrews (1976), pages 5, 104, and 116.

These are strong modern statement and definition leads, not an `H0` packet. The repository does not
cite DLMF or select analytic versus combinatorial form. This intake has no immutable admitted copy,
independent transcription review, complete premise/proof/errata map, or reviewed proof-source
crosswalk. DLMF is also a reference work rather than the original proof source.

## Historical source lead and date conflict

Crossref discovery metadata identifies L. J. Rogers, "Second Memoir on the Expansion of certain
Infinite Products," *Proceedings of the London Mathematical Society* s1-25, pages 318-343, DOI
`10.1112/plms/s1-25.1.318`, with a published date in November 1893. The publisher content was
Cloudflare-blocked during intake, so no exact theorem/page or proof passage was inspected. The
catalog's 1894 date therefore conflicts with this metadata and remains unverified; it must not be
silently reconciled with Ramanujan's later rediscovery or publication history.

## Clause crosswalk

| Catalog component | Source-backed candidate component | Prospective Lean surface | Intake result |
|---|---|---|---|
| plural identity name | both analytic equations 17.2.49-50 and combinatorial equations 26.10.13-14 | two named roots or one explicit conjunction plus checked transports | pair recognized; root shape open |
| partition function | equality of counts of partitions under two restrictions | finite filtered `Nat.Partition n` types and cardinalities | exact restriction predicates absent |
| first identity | difference at least two versus parts congruent to plus/minus one mod five | adjacency predicate and residue predicate | source definitions require transcription/review |
| second identity | first restriction with no part one versus parts congruent to plus/minus two mod five | minimum-part and residue predicates | source definitions require transcription/review |
| analytic equivalent | convergent q-series equals an infinite reciprocal product | `HasSum`/`tsum`, `HasProd`/`tprod`, or formal power series | domain and encoding not selected |
| Rogers/Ramanujan, 1894 | historical provenance | immutable source edition and source-to-node map | Rogers 1893 metadata conflicts; original passage unavailable |
| `verified` | inventory label only | accepted human and kernel receipts would be required | no H or M credit |

## Non-substitution boundary

One of the two identities cannot stand for the conventional pair without an approved target
correction. An analytic identity is not definitionally the same proposition as equality of every
coefficient or restricted-partition count. Glaisher's theorem and Euler's partition identities use
different restrictions. Gordon's and Andrews's generalizations require exact specialization and
transport rather than a name match.

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
search found no Rogers-Ramanujan or q-Pochhammer declaration. The pinned partition library provides
`Nat.Partition`, `restricted`, `countRestricted`, `genFun`, and generating-function product
theorems. The power-series topology provides infinite sums and products such as
`multipliable_one_sub_X_pow`. These are plausible substrate only. Existing restrictions do not
encode adjacent differences by two or the required residue classes, and no probed declaration
states either target identity.

The canonical module, expression, expression and environment fingerprints, checked transports,
and statement mutation results remain null. The later source and statement phases must preserve an
immutable lawful edition, independently review the exact pair and definitions, decide the root
shape, and elaborate precisely that claim before any H0, M0, R0, audit-completion, or
theorem-completion credit is possible.
