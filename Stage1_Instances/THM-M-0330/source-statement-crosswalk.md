# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` identifies `THM-M-0330` as the Hille-Yosida theorem, dates it to 1948,
attributes it to Einar Hille and Kosaku Yosida, and describes its content as the characterization of
generators of strongly continuous semigroups. Its label `已验证` is untrusted metadata under
rev-5.6 and supplies neither an exact statement nor proof credit.

## Candidate mathematical sources

- Einar Hille, *Functional Analysis and Semi-Groups*, American Mathematical Society Colloquium
  Publications 31 (1948). This is a historical primary monograph candidate. The exact theorem,
  page, edition-specific wording, and corrections have not been inspected in this intake.
- Kosaku Yosida, "On the differentiability and the representation of one-parameter semi-group of
  linear operators", *Journal of the Mathematical Society of Japan* 1 (1948), 15-21. This is a
  primary-paper candidate; its precise relationship to the intended modern equivalence remains to
  be audited.
- Klaus-Jochen Engel and Rainer Nagel, *One-Parameter Semigroups for Linear Evolution Equations*,
  Graduate Texts in Mathematics 194, Springer (2000), Chapter II. This is a modern formulation
  candidate and cross-check, not a primary-source substitute or a pinpoint citation at intake.

These entries are discovery anchors only. None establishes `H0`; the statement/source phase must
inspect stable copies, record theorem and page identifiers, map assumptions, and check errata.

## Claim crosswalk

| Repository phrase | Source component to pin | Required Lean component | Intake state |
|---|---|---|---|
| "strongly continuous semigroup" | semigroup parameter set, law, identity, and strong continuity | concrete operator-family or bundled `C0` semigroup API | included; encoding open |
| "generator" | domain and strong derivative at zero | partially defined linear operator plus generator relation | included; encoding open |
| generator characterization | exact `if and only if`, including existence and uniqueness boundaries | canonical `Iff` or two checked directions | included; variant open |
| dense and closed operator | density of domain and closed graph | domain subspace/density and graph closedness | included; encoding open |
| resolvent half-line | exact set of real parameters and sign convention | invertibility or range of `lambda I - A` | included; bounds open |
| resolvent powers | quantified positive powers and norm constants | bounded inverse powers and operator-norm inequalities | included; constants open |
| growth or contraction bound | `||T(t)|| <= M exp(omega t)` or the contraction specialization | norm estimate for every nonnegative time | variant-dependent |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_234.lean` and the dossier for `THM-M-1041` are
repo-local discovery leads for the same named family. The legacy `HilleYosidaData` packages core
generator and resolvent facts as abstract fields, so projection wrappers from that data cannot
establish the theorem. Cross-target artifacts cannot be inherited by `THM-M-0330` in any event.

The statement phase selects the standard real contraction form associated with Engel-Nagel,
Chapter II, Theorem 3.5: positive resolvent axis, bound `||R(a,A)|| <= 1/a`, and a strongly
continuous contraction semigroup on nonnegative time. `Statement.lean` elaborates this exact choice
with concrete predicates. Before source fidelity can reach `H0`, an independent reviewer must still
inspect the cited source, primary-source counterparts, and errata and approve the row-by-row map.
