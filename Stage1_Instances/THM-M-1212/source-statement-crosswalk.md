# Source-statement crosswalk

## Repository source and candidate source family

The repository's immediate source is `Docs/researches/math_theorems.md`, which records "NLS
well-posedness theory", attributes it to many mathematicians in the twentieth century, and labels
it `verified`. That metadata does not identify a theorem, proof, edition, or page and is not H0.

Two primary-source families provide candidates for resolving the phrase, but neither is selected
at intake:

- Jean Ginibre and Giorgio Velo, "On a class of nonlinear Schrodinger equations. I. The Cauchy
  problem, general case", *Journal of Functional Analysis* 32 (1979), 1-32, DOI
  `10.1016/0022-1236(79)90076-4`.
- Thierry Cazenave and Fred B. Weissler, "The Cauchy problem for the critical nonlinear
  Schrodinger equation in H^s", *Nonlinear Analysis* 14 (1990), 807-836, DOI
  `10.1016/0362-546X(90)90023-A`.

The statement phase must inspect authoritative copies and select an exact theorem that represents
the generic metadata without duplicating a neighboring named target. Bibliographic candidates
alone provide no accepted source or machine evidence.

## Crosswalk

| Repository phrase | Required source component | Required Lean component | Intake status |
|---|---|---|---|
| "nonlinear Schrodinger equation" | exact normalized Cauchy problem | typed evolution equation and initial trace | family included; conventions open |
| "well-posedness theory" | one theorem's existence, uniqueness, and stability clauses | quantified solution predicate and data-to-solution topology | intended root; exact clauses open |
| initial data | source data space and regularity | concrete function-space type and membership hypotheses | open |
| local interval | source lifespan convention | nontrivial interval and solution restriction | open |
| uniqueness | source's conditional or unconditional class | equality quantified over exactly that class | open |
| continuous dependence | source topology and parameter range | explicit convergence or continuity statement | open |
| stronger conclusions | continuation, global existence, or scattering if present | separate conclusions with every extra hypothesis | excluded unless source-selected |

## Evidence boundary

Before H0, an independent reviewer must verify an immutable edition, theorem/page, referenced
definitions, every exponent and endpoint restriction, errata, and a row-by-row mapping. Before any
M-credit, an exact Lean target must elaborate and subsequent anchor work must inspect declarations,
terminal bodies, revisions, imports, axioms, and placeholders. No public Lean closure is asserted.
