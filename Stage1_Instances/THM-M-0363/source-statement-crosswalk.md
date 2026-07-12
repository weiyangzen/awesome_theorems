# Source-statement crosswalk

## Repository source phrase

`Docs/Stage0_Blueprint.md` states only "BMO is the dual space of H^1", attributes the result to
Charles Fefferman, and gives 1971. This identifies a theorem family but omits the domain, scalar
field, definitions, quotient by constants, pairing, and norm comparison. Its `已验证` source label
is explicitly untrusted under rev-5.6.

## Candidate primary source

Charles Fefferman, "Characterizations of bounded mean oscillation", *Bulletin of the American
Mathematical Society* **77** (1971), no. 4, 587-588,
DOI `10.1090/S0002-9904-1971-12763-5`.

The bibliographic metadata (author, title, journal, volume, issue, year, and pages) was checked
against the DOI/Crossref record during intake. The article text, exact theorem numbering/wording,
definitions referenced by the announcement, assumptions, and errata were not independently
inspected in this phase. It is therefore a primary-source candidate and supports provisional `H1`,
not `H0`. A later source audit must inspect an immutable scan or edition and add a pinpoint
statement/proof crosswalk.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `H^1` | real Hardy space on Euclidean space | concrete `H^1(R^n)` construction and Banach-space instance | included; model open |
| `BMO` | locally integrable functions with bounded mean oscillation | BMO seminormed space and a.e.-constant quotient | included; definition open |
| "dual space" | continuous linear dual, not algebraic dual | `ContinuousLinearMap` dual and topology/norm data | included |
| BMO to dual | integration gives a bounded functional | well-defined pairing and continuous extension | included; domain open |
| dual to BMO | every functional has a representing BMO class | existence of representative and norm estimate | included; proof architecture open |
| uniqueness | representatives differ by constants | quotient equality / kernel characterization | included |
| norm relation | equivalent norms with convention-dependent constants | two-sided estimates or continuous linear equivalence | included; constants open |

## Formal boundary

A repository-wide search found no target-specific Lean module and no definitions or declarations
named for BMO, bounded mean oscillation, or a real-variable Hardy space in the pinned local mathlib
sources. This is only intake discovery, not the immutable anchor audit required by the next phases.
Generic `MeasureTheory`, integration, normed-space, quotient, and continuous-linear-map APIs do not
by themselves encode the theorem.

Before `H0`, an independent reviewer must verify the primary text or a selected complete primary
proof source, edition and page/theorem anchors, all hypotheses and definitions, proof boundaries,
errata, and every row of the source-to-formal mapping.
