# THM-M-0445 rev-5.6 intake

This directory is the rev-5.6 `planned` dossier for the repository target called the
Rubin-Kolyvagin theorem. Historical artifacts are discovery inputs only.

## Scope map

| Surface | Potentially in scope | Intake boundary |
|---|---|---|
| Objects | elliptic curves over `Q`, rational points, an elliptic-curve L-function, Selmer groups, and Tate-Shafarevich groups | The source does not define these objects or fix hypotheses |
| Rank consequence | equality of analytic and Mordell-Weil ranks in a low-rank setting | Candidate interpretation, not frozen |
| Finiteness consequence | finiteness of the relevant Tate-Shafarevich group | Candidate interpretation, not frozen |
| Full BSD | leading-term formula including period, regulator, Tamagawa, torsion, and Sha factors | Must not be inferred from the broad label |
| Rubin branch | CM/Iwasawa-theoretic hypotheses and nonvanishing assumptions | Exact specialization is absent from the source |
| Kolyvagin branch | Euler-system or Heegner-point hypotheses and Selmer control | Exact specialization is absent from the source |
| Lean discovery | legacy `StatementShape` and `FullBSDStatementShape` in `S1_M_091.lean` | Abstract proposition fields are not an exact formalization or proof |

## Intake verdict

The repository's only statement text is `椭圆曲线的BSD` (BSD for elliptic curves). This is too
broad to distinguish a theorem of analytic rank at most one from full BSD, and no primary theorem,
page, assumptions, or errata are identified. The exact claim therefore remains deliberately unset.
The provisional root vector is `[H4, M4, R4]`; the first failed gate is exact source-statement
identification. The theorem is not complete.

The open phase DAG is: statement selection and elaboration, immutable anchor audit, obligation-tree
freeze, proof or pinned integration, validation, then release. No downstream phase receives credit
from this intake.

## Validation

The exact commands and results in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local integrity only.
