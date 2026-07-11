# Source-statement crosswalk

The repository metadata says only "Log-Sobolev inequality" and "upper bound for entropy." Since
log-Sobolev inequalities form a family, that wording cannot itself be formalized exactly. Leonard
Gross's Gaussian inequality is chosen because the metadata attributes the result to Gross in 1975.

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Logarithmic Sobolev inequality associated with Gaussian measure | Leonard Gross, *Logarithmic Sobolev Inequalities*, American Journal of Mathematics 97(4), 1975, pp. 1061-1083, DOI 10.2307/2373688 | finite-dimensional standard-Gaussian root | Primary paper identified; exact theorem/page and premise mapping still require source audit: `H1` |
| Entropy of `f^2` | Gross's entropy/integral formulation | `integral (f^2 * log(f^2)) - m log m` | Convention and integrability must be made explicit in Lean |
| Dirichlet energy and factor `2` | Gaussian normalization of Gross's inequality | `2 * integral ||grad f||^2` | Covariance and generator normalization are root-relevant; changing the factor is a required mutation |
| Normalized formulation | Common specialization `integral f^2 = 1` | normalized candidate transport | Not credited until homogeneity and the `m = 0` boundary are checked |
| Abstract Wiener-space formulation | General setting of Gross's work | possible later generalization | Deliberately not the initial formal root; specialization requires a checked bridge |

The source metadata's `已验证` label is untrusted and is not evidence that any Lean declaration
exists. A repo-local search performed at intake found no target-specific dossier or recorded Lean
anchor. The later anchor-audit phase must search the pinned dependency tree and external projects at
immutable revisions; this intake makes no negative claim about all upstream formalizations.

Before statement acceptance, the next phase must freeze the Gaussian measure construction, the
regularity class, the zero-log-zero convention, all integrability hypotheses, binder order, and the
dimension-zero case. It must elaborate the exact expression and mutation-test removal of each
hypothesis, covariance rescaling, constant `2`, entropy normalization, and normalized versus
unnormalized forms.

Discovery link (not an immutable evidence receipt): <https://doi.org/10.2307/2373688>.

No `H0` or machine-closure claim is made. Edition/file hash, pinpoint theorem mapping, corrections
or errata search, and independent review remain open.
