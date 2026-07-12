# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` provide only the label, author,
year, and phrase "existence of a basis in Banach spaces". This is secondary metadata, not an exact
mathematical proposition and not evidence for `H0`.

## Primary-source candidate

- Juljusz Schauder, "Eine Eigenschaft des Haarschen Orthogonalsystems", *Mathematische
  Zeitschrift* 28 (1928), 317-320, DOI `10.1007/BF01181164`.

Crossref confirms the bibliographic record and pages, but the article's proposition has not yet
been inspected line by line. Its exact theorem locator, function space, exponent range,
normalization, assumptions, and corrections remain open. The repository's date `1927` may refer to
the work's provenance rather than this publication year and must not be used to infer its statement.

Schauder's "Zur Theorie stetiger Abbildungen in Funktionalräumen", *Mathematische Zeitschrift* 26
(1927), 47-65, DOI `10.1007/BF01475440`, is a bibliographically verified background candidate, not
yet established as the source of the basis claim.

## Crosswalk

| Repository phrase | Source question | Required Lean component | Intake status |
|---|---|---|---|
| "basis" | Haar, Faber-Schauder, or another system? | an explicit sequence and coordinate maps | unresolved |
| "Banach spaces" | which concrete complete normed space? | exact type, norm, completeness, and scalar field | unresolved |
| "existence" | construction, basis property, or abstract existence? | a term of `SchauderBasis 𝕜 X` or a checked equivalent | unresolved |
| convergence | norm and order of partial sums | `SummationFilter.conditional ℕ` expansion | likely interface; uncredited |
| uniqueness | explicit theorem or consequence? | biorthogonality/linear independence and coordinates | unresolved |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Normed.Module.Bases` defines `GeneralSchauderBasis` and its classical abbreviation
`SchauderBasis`. It also defines `RankOneDecomposition.basis`, which constructs a basis from nested
finite-rank projections converging pointwise to the identity. `IntakeCheck.lean` kernel-checks these
API types. No repository or pinned-mathlib declaration for the Haar/Faber-Schauder existence
theorem was identified during this limited intake search, and a full anchor audit remains a later
node.

Before `H0`, a source reviewer must inspect a stable copy of the selected primary theorem, record
its exact locator and wording, map every assumption and boundary convention, check errata, and sign
the row-by-row mapping. Before statement credit, the selected claim must be elaborated rather than
inferred from these candidates.
