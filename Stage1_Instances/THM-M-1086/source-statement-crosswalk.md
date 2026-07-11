# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` attributes the result to Vladimir Sudakov in 1971 and gives only
the phrase "lower bound for Gaussian processes" plus the untrusted status `已验证`.
`Docs/Stage0_Blueprint.md` repeats that phrase while leaving definitions, hypotheses, equivalent
forms, axioms, and machine artifacts open. These records identify the named theorem family but do
not determine a unique formal proposition.

## Candidate sources

- V. N. Sudakov, "Gaussian random processes and measures of solid angles in Hilbert space,"
  *Soviet Mathematics Doklady* 12 (1971), 412-415. This is the historical primary-paper candidate;
  its exact result, translated wording, assumptions, and correction history require direct
  inspection.
- M. Ledoux and M. Talagrand, *Probability in Banach Spaces: Isoperimetry and Processes*, Springer,
  1991. This is a modern source candidate for the standard metric-entropy formulation and its
  conventions; the exact theorem/page and edition errata remain to be checked.

These are discovery anchors only, not `H0` evidence. In particular, the bibliographic metadata has
not been used to infer an exact constant or a source-approved covering/packing convention.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Gaussian process" | jointly Gaussian centered real family | probability space, random variables, Gaussian finite-dimensional laws, centering | included; encoding open |
| "lower bound" | expected supremum bounded from below | expectation and supremum with explicit finiteness/measurability | included; exact codomain open |
| canonical distance | `L2` size of Gaussian increments | integrability, expectation of squared difference, square root, pseudometric laws | standard claim-family component; source locator open |
| metric entropy at scale `epsilon` | size of a separated packing or covering | finite cardinal/extended cardinal convention and logarithm | included; convention open |
| universal constant | bound independent of process, index set, and scale | an existential positive real constant with correct binder scope | included; normalization open |
| arbitrary index set | extension beyond a finite Gaussian vector | separability, approximation, convergence, and measurability bridge | included only if selected source supports it |
| `已验证` | repository screening label | inspectable proof body and accepted kernel receipt | no credit |

## Evidence boundary

No repo-local Lean declaration or external formal candidate is accepted or claimed at intake. The
statement and anchor-audit phases must search the pinned mathlib revision and credible Lean 4
projects, recording exact modules, declaration types, revisions, axioms, placeholders, and terminal
proof-body provenance. Before `H0`, an independent reviewer must inspect a chosen primary edition,
verify the exact theorem locator, all assumptions and convention transports, check errata, and
approve the row-by-row mapping to the canonical Lean expression.
