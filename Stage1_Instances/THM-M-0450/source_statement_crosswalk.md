# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| `E(Q)` is finitely generated | L. J. Mordell, *On the rational solutions of the indeterminate equations of the third and fourth degrees*, Proc. Cambridge Philos. Soc. 21 (1922), 179-192 | specialization of `StatementShape` to `K = Rat` | Original-case source located; scan, exact page-to-premise mapping, and errata review remain open |
| `E(K)` is finitely generated for a number field `K` | A. Weil, *L'arithmetique sur les courbes algebriques*, Acta Math. 52 (1929), 281-315 | `forall K, [Field K], [NumberField K], ...` | Historical generalization located; exact theorem/page and terminology crosswalk require primary-source audit |
| Modern elliptic-curve formulation | J. H. Silverman, *The Arithmetic of Elliptic Curves*, 2nd ed., GTM 106, Springer (2009), Chapter VIII, Theorem 4.1 | `E.IsElliptic -> AddGroup.FG E.toJacobian.Point` | Precise modern secondary statement anchor; edition and theorem locator recorded, but not an H0 primary-proof receipt |
| Rational points form an abelian group including infinity | Same modern reference, Chapter III group-law development | `WeierstrassCurve.Jacobian.Point` and its `AddCommGroup` instance | Candidate object-model correspondence; exact equivalence to the source model is deferred |
| Finite generation via descent | Silverman, Chapter VIII, especially the weak Mordell-Weil and height descent development | `AddCommGroup.fg_of_descent'` | Existing abstract Lean anchor is relevant but does not supply the arithmetic hypotheses for elliptic curves |

The root means finite generation as an abelian group: finitely many points generate every
`K`-rational point under the elliptic-curve group law. It does not request an algorithm producing
generators. The number-field formulation strictly includes Mordell's rational case and excludes the
separate function-field theorem.

The historical local file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_092.lean` supplies a candidate statement shape and
an abstract descent wrapper. It explicitly lacks the weak Mordell-Weil and elliptic-height inputs,
so it is not terminal evidence. The next phase must inspect the actual declaration type, pin the
environment, serialize a normalized expression, check the curve-model correspondence, and mutate
the nonsingularity and number-field assumptions before machine evidence is observed.

Discovery links, not immutable evidence receipts:

- Mordell bibliographic record: <https://zbmath.org/?q=an%3A48.0121.03>
- Weil article: <https://doi.org/10.1007/BF02592688>
- Silverman book: <https://doi.org/10.1007/978-0-387-09494-6>

No `H0` claim is made. Primary scans/hashes, precise premise-to-node mapping, corrections search,
and independent review remain required.
