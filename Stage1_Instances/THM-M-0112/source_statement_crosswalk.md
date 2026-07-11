# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Weak topological root and range | SGA 2, Expose XII, the Lefschetz theorem for homotopy groups (Springer LNM 340, 1973) | no declaration selected | Primary-source family identified, but theorem/page, edition scan hash, assumptions, and errata still require audit: `H1` |
| Smooth complex projective ambient variety and smooth hyperplane section | Same SGA 2 development; the repo's source metadata says only "topological properties of a hyperplane section" | future scheme/analytification object model | Exact source-to-Lean representation is open |
| Isomorphism below `n-1`, surjection at `n-1` | Standard homotopy-group formulation of weak Lefschetz | future map on `HomotopyGroup.Pi` | Range and basepoint conventions require exact statement work |
| Relative formulation `pi_k(X,Y)=0` for `k<n` | Standard equivalent formulation via the long exact sequence of a pair | future checked transport | Candidate equivalence, no credit |
| Connectedness and fundamental-group consequences | Specializations in sufficiently large dimension | legacy `S1_M_035.lean` statement shapes | Discovery only, not the root and not proof evidence |

The source metadata is too short to distinguish topological weak Lefschetz from cohomological weak
Lefschetz or hard Lefschetz. This dossier selects the weak topological theorem because the legacy
artifact explicitly records that choice, while retaining `H1` until an independent reviewer checks
the precise primary-source locator and hypotheses. SGA 2 bibliographic discovery anchor:
Grothendieck et al., *Cohomologie locale des faisceaux coherents et theoremes de Lefschetz locaux et
globaux*, North-Holland/Springer, 1968/1973 reprint, Expose XII. No immutable source receipt or H0
claim is made here.

The statement phase must choose concrete Lean types, expose universe and basepoint binders, serialize
the normalized expression, and mutation-test smoothness, projectivity, connectedness, dimension
bounds, section smoothness, conclusion range, and the relative-homotopy transport before machine
evidence is inspected.
