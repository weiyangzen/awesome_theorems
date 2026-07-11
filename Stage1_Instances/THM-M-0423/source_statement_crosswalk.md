# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Quadratic forms over number fields obey a local-global isotropy criterion | H. Hasse, *Darstellbarkeit von Zahlen durch quadratische Formen in einem beliebigen algebraischen Zahlkorper*, Journal fur die reine und angewandte Mathematik 153 (1924), pp. 113-130 | No accepted declaration; `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_067.lean` is legacy discovery material | Original proof source identified; theorem/page premise mapping, edition hash, errata search, and independent review remain open: `H1` |
| Rational-field specialization | H. Minkowski, *Uber die Bedingungen, unter welchen zwei quadratische Formen mit rationalen Koeffizienten ineinander rational transformiert werden konnen*, Journal fur die reine und angewandte Mathematik 106 (1890), pp. 5-26 | Future rational specialization or transport | Historical source candidate only; exact statement crosswalk is not accepted |
| Global isotropy implies isotropy over every completion | Functorial scalar extension of a zero of the form | Future base-change lemma for `QuadraticForm` | Mathematical interface identified; exact types and checked transport are deferred |
| Isotropy over all completions implies global isotropy | Hasse's local-global theorem, including archimedean and nonarchimedean places | Future Hasse-Minkowski root declaration | Hard direction; no repo-local closure is credited |
| Polynomial and coordinate-free formulations agree | Choice of a basis identifies a quadratic form with a homogeneous degree-two polynomial | Future basis/coordinate equivalence | Candidate transport only; it must be elaborated and mutation-tested before credit |

The manifest phrase “Hasse principle” cannot truthfully denote an unrestricted theorem: local
solubility need not imply global solubility for general algebraic varieties. This intake therefore
selects the historically canonical proved quadratic-form theorem. It includes all places and
nonzero isotropic vectors and excludes integral-solubility variants.

Discovery links, not immutable evidence receipts:

- Hasse bibliographic record: <https://eudml.org/doc/149346>
- Minkowski digitized volume: <https://eudml.org/doc/149196>

No `H0` or machine-closure claim is made. The statement phase must fix exact universes and imports,
inspect the actual quadratic-form and completion APIs, elaborate the expression, serialize its
normalized form and environment, check any coordinate transport, and mutation-test nondegeneracy,
the nonzero witness, the set of places, and field/domain changes.
