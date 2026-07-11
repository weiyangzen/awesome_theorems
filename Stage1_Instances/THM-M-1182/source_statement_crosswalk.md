# Source-statement crosswalk

## Repository source record

| Claim component | Repository anchor | Intake assessment |
|---|---|---|
| Name | `Docs/researches/math_theorems.md`, "Caffarelli边界正则性" | Identifies a theorem family, not a unique theorem |
| Attribution | Luis Caffarelli | Plausible but insufficient for source identity |
| Statement | "严格凸区域的边界正则性" (boundary regularity of strictly convex domains) | Missing equation, unknown, domains, hypotheses, and conclusion |
| Historical status | `已验证` | Untrusted metadata under rev-5.6; supplies no proof or machine credit |

## Primary-source candidates, not accepted anchors

| Candidate | Why it is relevant | Why it cannot yet define the target |
|---|---|---|
| L. A. Caffarelli, *Boundary regularity of maps with convex potentials*, Communications on Pure and Applied Mathematics 45 (1992), 1141-1151, DOI `10.1002/cpa.3160450905` | Title directly concerns boundary regularity of convex-potential maps in optimal transport | The repository wording does not say that the target is this paper's map theorem or preserve its hypotheses/conclusion |
| L. A. Caffarelli, *Boundary regularity of maps with convex potentials. II*, Annals of Mathematics 144 (1996), 453-496, DOI `10.2307/2118564` | A neighboring primary continuation in the same theorem family | Selecting part II, or one theorem within it, would be an unsupported substitution until theorem/page and assumption matching are performed |

No primary theorem number/page crosswalk is claimed. The two citations are discovery candidates,
not immutable evidence receipts and not evidence for `H0`.

## Required exact-statement fields

The statement phase must fill all of these from one pinpointed primary theorem before elaboration:

1. ambient dimension and the source/target domains;
2. the precise strict/uniform convexity and boundary smoothness assumptions;
3. the convex potential, map, equation, measure densities, and boundary condition;
4. lower/upper bounds and regularity assumptions on densities;
5. local versus global conclusion and the exact regularity class/exponent;
6. normalization, uniqueness, constants, and excluded degeneracies;
7. edition/file hash, theorem/page, errata search, and independent source review.

Until those fields are resolved there is no truthful source-to-Lean row, checked transport, or
mutation target. The correct classifications are `H4` (source identity unresolved), `M4` (exact
formal proposition unavailable), and `R4` (no uniquely anchored reconstruction).
