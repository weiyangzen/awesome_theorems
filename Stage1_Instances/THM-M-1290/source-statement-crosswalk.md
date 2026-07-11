# Source-statement crosswalk

## Primary source candidate

Haïm Brezis and Louis Nirenberg, “Positive solutions of nonlinear elliptic equations involving
critical Sobolev exponents,” *Communications on Pure and Applied Mathematics* 36 (1983), 437-477,
DOI `10.1002/cpa.3160360405`. This bibliographic identification is a discovery anchor only. A stable
copy, exact theorem/page, proof dependencies, assumptions, and errata have not yet been inspected,
so it is not `H0` evidence.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| “Brezis-Nirenberg problem” | critical Dirichlet existence/nonexistence theorem family | one explicitly selected proposition | family identified; variant open |
| “critical growth” | exponent `2* - 1 = (n+2)/(n-2)` | real-power or weak-form nonlinear term | included; encoding open |
| elliptic equation | `-Delta u = lambda u + u^(2*-1)` | weak Laplacian identity/test-function formulation | included; API open |
| zero boundary data | `u` belongs to `H_0^1(Omega)` | Sobolev space and trace/closure interface | included; API open |
| positive solution | nonzero solution positive in `Omega` | a.e. positivity plus nontriviality, or regular representative | convention open |
| parameter threshold | comparison with first Dirichlet eigenvalue | variational eigenvalue definition and inequalities | bounds and normalization open |
| dimension three | exceptional threshold behavior | separate theorem/case with exact domain assumptions | must not be inferred |

## Source gate

Before statement acceptance, a reviewer must verify the article's exact theorem wording and pages,
all domain and dimension assumptions, endpoint behavior, solution regularity, notation, cited lemmas,
and published errata. Each premise must then map to an ordered Lean binder or an explicit derived
lemma. No repo-local or external Lean declaration has been audited at intake.
