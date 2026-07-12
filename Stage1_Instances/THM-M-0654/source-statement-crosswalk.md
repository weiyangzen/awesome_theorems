# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` attributes the item to Abraham Robinson, dates it to 1956, and
gives only the gloss "consistency of theories". Its `已验证` label is untrusted discovery metadata
under rev-5.6 and supplies neither a proposition nor machine-proof credit.

The next Stage0 entry is separately named "joint consistency theorem". The intake does not assume
that these records are distinct theorems or aliases; resolving that possible duplicate is part of
the source audit.

## Leading primary-source candidate

Abraham Robinson, "A Result on Consistency and its Application to the Theory of Definition",
*Indagationes Mathematicae (Proceedings)* 59 (1956), 47-58,
DOI `10.1016/S1385-7258(56)50008-X`.

The bibliographic fields were checked against the Crossref DOI record on 2026-07-12. Crossref is a
locator, not the primary mathematical evidence. The paper text, its numbered result, exact symbols,
proof, cited prerequisites, corrections, and errata were not available in the repository and have
not been independently inspected here. Consequently this citation supports `H1` at most, not `H0`.

## Provisional crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "theories" | first-order theories `T₁`, `T₂` | concrete theory type over concrete signatures | family included; domains open |
| "consistency" | no contradiction, or satisfiability via completeness | derivability consistency and/or model existence | exact convention open |
| two languages | `L₁`, `L₂` with a common fragment | signatures, embeddings, renaming/transport | representation open |
| union of theories | both axiom sets in a common language | transported theory union | exact coercions open |
| common consequences | sentences expressible in the common language | sentence maps and entailment/derivability | criterion wording open |
| incompatible consequences | provisional pair `T₁ ⊢ φ`, `T₂ ⊢ ¬φ` | negation and two proof/semantic judgments | polarity and iff status open |
| 1956 / Robinson | historical and bibliographic locator | no formal object and no proof credit | candidate identified |

## Source and machine boundary

A repository-wide title/name search and a scoped pinned-mathlib text search found no declaration
specific to Robinson's joint consistency theorem. This is negative intake evidence only, not the
later immutable anchor audit. No source proposition was reconstructed from secondary summaries and
no Lean statement was invented to make elaboration possible.

Before `H0`, an independent reviewer must inspect a stable copy of the 1956 paper, identify the
exact result and pages, record every definition and assumption, check errata and later corrections,
resolve the adjacent "joint consistency" entry, and approve a row-by-row source mapping. Before
statement credit, those accepted rows must map to an elaborated Lean expression with checked
language transports and mutations.
