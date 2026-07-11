# Source-statement crosswalk

| Claim component | Primary-source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Fixed-point formula for an elliptic complex | M. F. Atiyah and R. Bott, “A Lefschetz Fixed Point Formula for Elliptic Complexes: I,” *Annals of Mathematics* 86 (1967), 374-407, DOI 10.2307/1970694 | future exact declaration; legacy `StatementNormalizationBoundary` is abstract | Primary paper and page span identified, but the exact numbered result and assumptions have not yet been independently checked: `H1` |
| General fixed-component/localization development | M. F. Atiyah and R. Bott, “A Lefschetz Fixed Point Formula for Elliptic Complexes: II. Applications,” *Annals of Mathematics* 88 (1968), 451-491, DOI 10.2307/1970721 | future fixed-component branch | Companion primary source identified; theorem-to-node and errata audits remain open |
| Lefschetz number / equivariant index character | Trace on the cohomology of the elliptic complex in the cited papers | legacy `AtiyahBottFixedPointFormulaData.IndexCharacter` | The legacy field carries no analytic meaning by itself; concrete cohomology/index semantics are required |
| Fixed locus | Fixed points/components of the inducing endomorphism | legacy `fixedPointSet` and `FixedComponent` | Set-level fixed points are concrete; smooth component structure and normal bundle are absent |
| Local contribution | Fiber/symbol action together with the determinant of the action on normal directions; component versions use characteristic-class/localization data | legacy `LocalContribution` | An unconstrained function is not an encoding of the source local term |
| Global equality | Lefschetz/index value equals the aggregate of local fixed-set contributions | legacy `AtiyahBottFixedPointFormula` | Correct schematic direction only; too abstract for statement or proof credit |
| Isolated nondegenerate specialization | Point contributions when the relevant normal determinant is invertible | future specialization theorem | Candidate consequence, not a substitute for the selected root |

The repository metadata phrase “equivariant elliptic operator fixed-point formula”
is therefore retained as a conservative family-level claim. Intake does not decide
whether the canonical root will use complexes, a single operator, isolated fixed
points, or fixed components. That decision must be made from a page-level reading
of the primary source and then reflected exactly in Lean.

No `H0` or machine-closure claim is made. Follow-up must preserve immutable source
copies or hashes, identify the exact theorem/equation and all notation-dependent
assumptions, check corrections/errata, map every source premise to the Lean binder
list, and obtain independent review.
