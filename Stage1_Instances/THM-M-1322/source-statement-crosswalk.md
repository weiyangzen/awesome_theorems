# Source-statement crosswalk

## Primary-source candidate

P. Kroger, "Upper bounds for the Neumann eigenvalues on a bounded domain in Euclidean space,"
*Journal of Functional Analysis* **106** (1992), 353-357. This bibliographic identification is a
discovery anchor only. The article text, exact theorem/page, hypotheses, notation, and errata have
not been independently inspected in this intake, so it is not `H0` evidence.

The repository supplies only the proposer, year, and gloss "upper bound for the first eigenvalue."
It supplies no citation, formula, assumptions, or formal artifact. Its historical `已验证` label is
explicitly untrusted under rev-5.6.

## Crosswalk

| Repository datum | Candidate source component | Required Lean component | Intake status |
|---|---|---|---|
| "Kroger theorem" | theorem in the 1992 Neumann-eigenvalue paper | named exact proposition | paper identified; theorem anchor open |
| "first eigenvalue" | ambiguous eigenvalue index | explicit ordered sequence and index convention | unresolved; hard statement blocker |
| "upper bound" | source inequality with exact constants | inequality over concrete spectral values | formula intentionally not guessed |
| PDE category | Neumann Laplacian on a Euclidean domain | operator/form/eigenvalue realization | included; API audit open |
| Pedro Kroger, 1992 | author and publication year | provenance metadata | consistent with candidate paper |

Before source fidelity can advance, a reviewer must inspect a stable copy of the paper, record the
exact theorem and page, transcribe all quantifiers and constants, check corrections/errata, and map
each source definition to Lean. Candidate secondary summaries may aid discovery but cannot replace
that comparison.

