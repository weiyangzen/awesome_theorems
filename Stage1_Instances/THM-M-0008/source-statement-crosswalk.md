# Source-statement crosswalk

## Repository source

The only located source record is `Docs/researches/math_theorems.md`: proposer "many
mathematicians", date "1950s", statement "properties of the Tor functor", and status `已验证`.
It provides no author, title, edition, theorem number, page, hypotheses, or conclusion. The generated
Stage1 entry adds a suggested category-level work scope but explicitly remains `not completed`.

| Metadata phrase | Mathematical possibilities | Lean consequence | Disposition |
|---|---|---|---|
| "Tor theorem" | no uniquely standard theorem by that name | no canonical declaration type follows | blocking |
| "properties" | balancedness, vanishing, exact sequences, or derived-tensor laws | materially different binders and assumptions | blocking |
| "1950s" | historical subject placement only | cannot pin a source snapshot | discovery only |
| `已验证` | untrusted source label | supplies neither human-proof nor kernel evidence | no credit |

## Candidate source search contract

The statement phase must inspect a stable primary source, record exact theorem/page and definitions,
check errata, and map every assumption and conclusion. Likely search loci include Cartan and
Eilenberg's *Homological Algebra* and a precise modern derived-functor reference, but these are
search directions rather than citations: no edition or theorem location has yet been verified.

## Lean discovery boundary

The legacy file imports `Mathlib.CategoryTheory.Monoidal.Tor` and records genuine candidate anchors
such as `CategoryTheory.Tor`, `CategoryTheory.Tor'`,
`CategoryTheory.isZero_Tor_succ_of_projective`, and its primed analogue. Those names must be audited
at the pinned revision during the anchor phase. At intake they receive no exact-statement, source,
or proof credit. In particular, a structure whose fields assume balanced comparison, naturality,
and long-exactness cannot establish those results.

An H0 decision requires a pinpoint primary source, assumption-by-assumption crosswalk, errata check,
and independent review. An M0 decision separately requires an exact elaborated target and kernel
evidence; neither decision has been made.
