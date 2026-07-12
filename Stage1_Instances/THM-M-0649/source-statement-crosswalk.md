# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the theorem to Alfred Tarski, dates it to 1956, and
states only "the union of an elementary chain is an elementary extension". `Docs/Stage0_Blueprint.md`
preserves that sentence but leaves its definitions and hypotheses open. Under rev-5.6 the attached
`已验证` label is untrusted metadata, not human-source or machine-proof evidence.

## Candidate primary and reference sources

The historical result is commonly called the elementary chain theorem or Tarski union theorem.
Alfred Tarski's model-theory papers and the Tarski-Vaught literature are primary-source candidates;
the repository's exact 1956 attribution has not yet been verified against an immutable scan.
Standard model-theory texts, including Chang and Keisler's *Model Theory* and Hodges' *Model Theory*,
are secondary statement references. Exact edition, theorem number, page, original assumptions,
corrections, and errata have not been inspected in this intake. These entries are discovery
locators only and do not establish `H0`.

## Crosswalk

| Repository phrase | Frozen mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| elementary chain | a nonempty linearly ordered compatible system with elementary transition inclusions | index order, structures, elementary embeddings, coherence | included; exact encoding open |
| union | induced colimit/union containing compatible images of all stages | common-ambient `iSup` or first-order `DirectLimit` | two candidates identified |
| elementary extension | each canonical stage-to-union inclusion preserves and reflects every formula | `ElementaryEmbedding` or `Substructure.IsElementary` | included; root declaration open |
| one language | every stage interprets the same first-order signature | `L : FirstOrder.Language` and `L.Structure` instances | included |
| no stated countability limit | arbitrary nonempty linear index and arbitrary language within universe constraints | universe-polymorphic binders | included; fingerprint open |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.ElementarySubstructures` contains the Tarski-Vaught criterion
`FirstOrder.Language.Substructure.isElementary_of_exists`, while
`Mathlib.ModelTheory.DirectLimit` constructs direct limits and identifies the direct limit of an
increasing substructure system with its supremum. The scoped name/text search found no declaration
stating that a directed supremum or direct limit of elementary maps is elementary. This negative
result is not a complete anchor audit and carries no proof credit.

Before `H0`, an independent reviewer must select and inspect an immutable source edition, record the
exact theorem/page and definitions, resolve the date/attribution, check every hypothesis and errata,
and approve a row-by-row mapping to the elaborated Lean target.
