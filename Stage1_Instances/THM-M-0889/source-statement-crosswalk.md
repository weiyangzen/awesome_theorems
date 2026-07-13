# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6509-6514` supplies exactly the title `Alon-Milman定理`, the
attribution `Noga Alon/Vitali Milman`, the year `1985`, the gloss `谱隙与扩展性`, importance `高`,
and status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24251-24276` repeats the gloss while explicitly leaving definitions and
premises, proof route, dependencies, equivalent formulations, axiom policy, machine status, and
artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata and resets
the target to `L0 / rework_required`.

The repository gives no bibliography, theorem number, graph convention, spectral operator,
expansion invariant, constant, binder order, proof boundary, errata review, or reviewer. It therefore
identifies a historical result family but not a unique truth-valued proposition.

## Matching primary source

N. Alon and V. D. Milman, *lambda_1, Isoperimetric Inequalities for Graphs, and
Superconcentrators*, *Journal of Combinatorial Theory, Series B* 38(1) (1985), 73-88,
DOI `10.1016/0095-8956(85)90092-9`, PII `0095895685900929`; received March 24, 1984.

An author-hosted 16-page scan was inspected at
`https://web.math.princeton.edu/~nalon/PDFS/Publications2/lambda%20%20isoperimetric%20inequalities%20for%20graphs%20and%20superconcentrators.pdf`.
Its SHA-256 is `5942686400daeac3383624c285ae24d795f39de838726d5fa24c231a4e3fe868`.
Crossref DOI metadata and the author's publication list corroborate the bibliographic identity.
This source is an exact family match, not yet an accepted canonical root.

## Definition and result crosswalk

| Source location | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Section 2, p. 76 | finite connected graph `G=(V,E)`; oriented incidence matrix `C`; `Q=C^T C=diag(d(v))-A_G` | finite simple graph, incidence/Laplacian matrix, real coefficients | orientation independence and graph-model transport remain to be frozen |
| Section 2, p. 76 | `0=lambda_0 < lambda_1 <= ...` are eigenvalues of `Q`; `lambda_1` is the second-smallest eigenvalue | Hermitian Laplacian spectrum and multiplicity ordering | modern notation often calls this `lambda_2`; exact encoding open |
| Lemma 2.1, pp. 77-78 | disjoint `A,B`, distance `rho`, `a=|A|/n`, `b=|B|/n`, and internal edge sets imply `lambda_1*n <= rho^-2*(a^-1+b^-1)*(|E|-|E_A|-|E_B|)` | finite sets, graph distance, real cardinality ratios, edge boundary | exact numbered root candidate; zero denominators and coercions open |
| Theorem 2.5, pp. 78-79 | under `rho>1` and maximum degree `d`, `b <= (1-a)/(1+(lambda_1/d)*a*rho^2)` | metric-neighborhood/isoperimetric inequality | strongest literal spectral-gap-to-expansion candidate, but not selected by catalog |
| Theorem 2.6, p. 79 | if `dist(A,B)>p>=1`, then `b <= (1-a)*exp(-log(1+2*a)*floor(sqrt(lambda_1/(2*d))*p))` | real threshold, square root, floor, exponential, neighborhood growth | different conclusion and extra analytic encoding |
| Theorem 2.7, pp. 79-80 | `diam(G) <= 2*floor(sqrt(2*d/lambda_1)*log_2(n))` for `n>1` | diameter, real square root, floor, and base-two logarithm | structure consequence rather than a direct expansion predicate |
| Definitions 4.1-4.2, pp. 82-83 | enlarger means `k`-regular with `lambda_1>=epsilon`; the extended double cover adds the matching edge and graph-neighbor edges | regularity, spectral predicate, bipartite cover | source-specific definitions required by Theorem 4.3 |
| Theorem 4.3, pp. 83-84 | the cover is an `(n,k+1,c)` expander for `c=4*epsilon/(k+4*epsilon)`, using `|N(A)| >= (1+c*(1-|A|/n))*|A|` for every input subset `A` | cover construction and nonlinear external-neighborhood inequality | explicit candidate with a different graph and conclusion |

The paper itself says in Remark 4.4 that a properly stated converse to Theorem 4.3 follows from a
discrete version of Cheeger's result and would appear elsewhere. This makes it unsafe to silently
turn the catalog gloss into a two-sided exact theorem without defining the chosen later packaging
and its source boundary.

## Secondary formulation boundary

Hoory, Linial, and Wigderson, *Expander Graphs and their Applications*, *Bulletin of the AMS* 43
(2006), Definition 4.10 and Theorem 4.11, packages a standard finite connected `d`-regular
edge-expansion statement:

`(d-lambda)/2 <= h(G) <= sqrt(2*d*(d-lambda))`,

where `lambda` is the second adjacency eigenvalue and
`h(G)=min_{S subset V, |S|<=|V|/2} |E(S,V-S)|/|S|`. It attributes the discrete theorem
independently to Dodziuk, Alon-Milman, and Alon. This is valuable disambiguation evidence, but it is
a later secondary normalization, not evidence that AM85 itself proves both displayed directions and
not automatic authority to replace the unspecified catalog root.

The converse lead is N. Alon, *Eigenvalues and Expanders*, *Combinatorica* 6(2) (1986), 83-96,
DOI `10.1007/BF02579166`. Its magnifier definition and constants differ from both AM85's extended
double cover and the later edge-expansion formula. It is a separate source boundary, not proof that
the catalog selected a two-sided formulation.

## Required source admission

The statement phase must select one candidate root or an explicitly approved reformulation;
preserve a lawful immutable edition; transcribe all definitions, binders, hypotheses, constants,
and the exact conclusion; map every incorporated proof premise and direction; search for relevant
corrections or errata; reconcile `THM-M-0888`; and obtain independent review. It must then freeze
and mutation-test the same exact Lean expression.

Until those gates pass, the canonical mathematical and Lean targets remain null and the human
source classification remains `H1`. The pinned Lean probe establishes only adjacent API
feasibility. No primary result is audited to `H0`, no formal statement or proof is credited, and
the later exhaustive anchor and provenance audit remains open.
