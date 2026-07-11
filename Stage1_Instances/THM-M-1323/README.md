# THM-M-1323 rev-5.6 intake

This is the `planned` dossier for the Stage0 phrase "comparison of eigenvalues of different
domains." The phrase is underdetermined by itself. This intake adopts the standard domain
monotonicity theorem for variational Dirichlet Laplacian eigenvalues as the candidate root, while
making that interpretive choice reviewable rather than silently treating it as source fact.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Operator | Dirichlet Laplacian, understood through its Rayleigh/min-max spectrum | Sign, Sobolev-space, and eigenvalue conventions require statement work |
| Domains | Nested bounded open subsets of Euclidean space | Minimum regularity and compact-resolvent assumptions require a primary-source pinpoint |
| Comparison | Inclusion reverses ordered eigenvalues: `Omega1 subset Omega2` implies `lambda_k(Omega2) <= lambda_k(Omega1)` | No strict inequality is claimed |
| Indices | Positive variational eigenvalue indices | Lean indexing convention is not frozen |
| Exclusions | Neumann monotonicity, unrelated operators, Cheng manifold comparison | These are materially different claims |
| Proof architecture | extension by zero, inclusion of trial spaces, min-max comparison | Architecture is uncredited until the obligation-tree phase |
| Formal target | Lean 4 plus pinned mathlib | No declaration or exact expression has been selected |

The source crosswalk records why this reading is plausible and exactly what remains unresolved.
The structured scope, exclusions, profiles, and state boundary are authoritative in `intake.json`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source identification: the repository metadata gives no edition, theorem number, boundary
condition, domain regularity, operator, or eigenvalue convention. Consequently the dependent Lean
statement phase must not elaborate a guessed theorem until source review accepts or corrects this
candidate reading. The theorem is not complete.

## Validation

The commands and exact outcomes in `validation.md` establish target membership, standard
consistency, JSON syntax, dossier structure, and clean text only. They provide no kernel evidence.
