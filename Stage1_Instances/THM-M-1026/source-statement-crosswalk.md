# Source-statement crosswalk

## Inventory

The repository metadata in `Docs/researches/math_theorems.md` gives only the Chinese name, the
twentieth century, attribution to multiple mathematicians, and the statement gloss "domains of
attraction of stable distributions". It contains no author, edition, theorem/page, normalization,
or hypotheses. Its `已验证` label is untrusted screening metadata.

Discovery candidates for the source-audit phase are B. V. Gnedenko and A. N. Kolmogorov,
*Limit Distributions for Sums of Independent Random Variables*, and V. M. Zolotarev,
*One-Dimensional Stable Distributions*. These are bibliographic leads only: this intake has not
fixed an edition, translation, theorem number, page, immutable scan, or errata record, and assigns
them no H0 credit.

| Claim component | Metadata anchor | Candidate formal surface | Intake assessment |
|---|---|---|---|
| normalized sums | generalized CLT name | laws of `(sum X k - b n) / a n` | expected, exact convention open |
| iid summands | classical generalized-CLT family | independence plus identical laws | expected, not explicit in metadata |
| nondegenerate limit | stable attraction family | weak convergence to `nu`, not a Dirac law | essential boundary, source wording open |
| stability necessity | stable distributions | `IsStableLaw nu` follows from a nonempty domain of attraction | selected direction |
| converse | domain of attraction | every stable `nu` has some attracting probability law | selected direction |
| analytic characterization | "domains of attraction" | tail balance and regular variation | stronger refinement excluded from root |

The statement phase freezes the combined biconditional as
`Stage1Instances.THM_M_1026.Statement`; `statement_iff_expanded` checks its expanded form. This is a
statement elaboration record, not an accepted proof or source-fidelity verdict. The formal-candidate
and immutable-source audits belong to the dependent anchor-audit phase.
