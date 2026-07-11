# Source-statement crosswalk

## Candidate primary source

J. M. Ball, "A version of the fundamental theorem for Young measures", in *PDEs and Continuum
Models of Phase Transitions*, Lecture Notes in Physics 344, Springer (1989), pp. 207-215, is the
primary candidate for the repository's underspecified label. Its Theorem 2.1 is the candidate root.
An authoritative scan must still be inspected for the exact wording, referenced definitions, page
location, hypotheses, and errata; this bibliographic identification is not H0.

The label is intrinsically ambiguous. It can mean the fundamental extraction theorem, the Young
measure object itself, the Kinderlehrer-Pedregal characterization of gradient Young measures, or a
PDE application. Intake chooses the fundamental theorem family because it yields a theorem-shaped
compactness claim, while leaving the exact Ball formulation open until source inspection.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Young measure" | measurable parametrized probability measure | probability measure kernel modulo a.e. equality | included; representation open |
| sequence of measurable functions | source maps on a finite-measure domain | measurable `u_j` and strictly increasing subsequence | included; spaces open |
| tightness/no escape | source compactness or coercive-integrand condition | quantified compact-containment or integral bound | included; exact condition open |
| generated measure | limiting distribution at almost every base point | weakly measurable `x \mapsto nu_x` | included; API open |
| test integrands | source admissible continuous/Caratheodory functions | measurability, continuity, and integrability predicates | included; class open |
| convergence | source test-function representation formula | exact a.e./weak/integral convergence proposition | included; topology open |

## Evidence boundary

No accepted excerpt, independent source review, or Lean declaration is present for this target.
Before H0, a reviewer must verify the edition, Theorem 2.1 and its page, every assumption and
referenced definition, errata, and every row of the source-to-Lean mapping. Before any M credit, an
exact target must elaborate; later anchor work must inspect real declarations and terminal bodies
at immutable revisions. Nearby probability-kernel APIs are not evidence of this theorem.
