# Source-statement crosswalk

## Candidate sources

- Norbert Wiener, "The Dirichlet problem," *Journal of Mathematics and Physics* 3 (1924),
  127-146. This is the historical primary-paper candidate. Exact theorem location, scanned
  wording, assumptions, and subsequent corrections have not yet been inspected.
- N. S. Landkof, *Foundations of Modern Potential Theory*, Springer, 1972, the chapter on the
  Dirichlet problem and regular boundary points. This is a modern source candidate; exact
  theorem/page, translation conventions, and errata remain to be checked.

These are discovery anchors, not `H0` evidence. Statement work must inspect a stable copy and must
not reconstruct constants or endpoint conventions from the theorem name.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "boundary point regularity" | Perron solution converges to arbitrary continuous boundary data at `p` | concrete Dirichlet/Perron solution and limit predicate | included; encoding open |
| complement near `p` | `Omega^c` intersected with shrinking annuli | Euclidean metric annular obstacle | included; endpoints open |
| Newtonian capacity | variational/potential-theoretic capacity in `R^n`, `n >= 3` | concrete capacity definition and equivalence lemmas | included; normalization open |
| Wiener series | sum of annular capacities divided by the dimensionally scaled radius term | `ENNReal` or real series divergence predicate | included; exact formula open |
| if and only if | necessity and sufficiency for regularity | checked equivalence with both directions | required |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_143.lean` supplies useful discovery material for
dyadic obstacles, harmonic APIs, and statement-shape experiments. Its `VariationalCapacityAPI` is
an assumed interface rather than Newtonian capacity, and its regularity packages similarly assume
terminal analytic facts. Therefore no declaration there establishes the Wiener criterion. Its
upstream search observations must be repeated at the pinned revision during anchor audit.

Before `H0`, an independent reviewer must verify bibliographic identity, theorem/page, every
domain and boundary hypothesis, normalization, annular convention, equivalent formulations, and
errata, then approve the source-to-Lean mapping row by row.
