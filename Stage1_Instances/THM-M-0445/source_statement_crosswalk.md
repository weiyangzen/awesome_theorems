# Source-statement crosswalk

| Claim component | Repository source anchor | Lean discovery candidate | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/Stage1_Targets_rev-5.6.json`, rank 91, name `鲁宾-科利瓦金定理` | namespace `AwesomeTheorems.Stage1.S1_M_091` | Identity is fixed; mathematical statement is not |
| Human wording | `Docs/Stage0_Blueprint.md`: `椭圆曲线的BSD`, attributed to Karl Rubin/Victor Kolyvagin | none exact | Too broad for ordered binders, hypotheses, or a conclusion |
| Rank and Sha consequence | not stated separately | `StatementShape` over `RubinKolyvaginBSDInput` | Abstract input fields make this a discovery scaffold, not a source-faithful root |
| Full leading-term BSD | not stated separately | `FullBSDStatementShape` | Stronger candidate cannot be selected from the label |
| Low analytic rank, CM, Euler-system, Heegner-point, and nonvanishing conditions | absent | proposition fields within `RubinKolyvaginBSDInput` | Required hypotheses are neither concretely modeled nor sourced |

The legacy Lean file explicitly says its declarations are statement-shape boundaries and that the
elliptic-curve L-function, Mordell-Weil rank, Tate-Shafarevich group, and terminal theorem are not
available there. Its abstract `Prop` fields cannot resolve the human-source ambiguity.

Before statement work, a primary-source audit must identify the intended Rubin and/or Kolyvagin
result by edition, theorem/page, exact curve and rank hypotheses, conclusion, and errata. It must
also decide whether this target means rank equality plus Sha finiteness or the full BSD
leading-coefficient formula. Until then, there is no honest transport or mutation test to credit.
No `H0` or machine-closure claim is made.
