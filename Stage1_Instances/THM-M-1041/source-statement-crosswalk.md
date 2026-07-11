# Source-statement crosswalk

## Candidate sources

- Einar Hille, "Functional Analysis and Semi-Groups", American Mathematical Society Colloquium
  Publications 31 (1948). This is a historical primary monograph candidate; exact theorem/page,
  wording, edition, and corrections have not been inspected.
- Kôsaku Yosida, "On the differentiability and the representation of one-parameter semi-group of
  linear operators", *Journal of the Mathematical Society of Japan* 1 (1948), 15-21. This is a
  primary-paper candidate; the exact hypotheses and relation to the intended modern formulation
  still require inspection.
- Klaus-Jochen Engel and Rainer Nagel, *One-Parameter Semigroups for Linear Evolution Equations*,
  Graduate Texts in Mathematics 194, Springer (2000), the Hille-Yosida generation theorem in
  Chapter II. This is a modern cross-check candidate, not yet an exact edition/page anchor.

These are discovery anchors only and do not establish `H0`. The next phase must inspect stable
copies and record exact theorem identifiers/pages, definitions, assumptions, and errata.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "generator characterization" | equivalence between generation and analytic conditions on `A` | concrete generator relation and `Iff` | included; variant open |
| densely defined, closed | domain dense in `X` and graph closed | unbounded operator/domain/closed graph API | included; encoding open |
| resolvent half-line | `(omega, infinity)` lies in the resolvent set | invertibility/range of `lambda I - A` | included; sign open |
| resolvent power bound | norm bounds for every positive power | iterated bounded resolvent and operator norm | included; constants open |
| `C0` semigroup | semigroup law and strong continuity at nonnegative times | bundled or explicit operator family | included; API open |
| growth bound | `||T(t)|| <= M exp(omega t)` in the general form | operator norm and real exponential | variant-dependent |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_234.lean` supplies useful names for discovery but
does not freeze the theorem. In particular, `HilleYosidaData` stores `resolventRangeCondition`,
`resolventPowerBound`, `generatorIdentifiesSemigroup`, and uniqueness as unconstrained proposition
fields. Consequently `StatementShape` is neither a faithful concrete statement nor proof closure.
Its imports and comments must be re-audited against the pinned dependency during anchor audit.

Before `H0`, an independent reviewer must approve the selected source variant and a row-by-row
mapping of every hypothesis, quantifier, constant, boundary condition, and conclusion to Lean.
