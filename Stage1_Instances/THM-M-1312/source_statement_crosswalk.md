# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Maximal development of Einstein initial data | Y. Choquet-Bruhat and R. Geroch, *Global aspects of the Cauchy problem in general relativity*, Communications in Mathematical Physics 14 (1969), 329-335, especially the theorem on p. 330 | `AwesomeTheorems.Stage1.S1_M_168.StatementShape` | Primary paper and pinpoint located; premise-by-premise transcription and errata audit remain open: `H1` |
| Initial data and constraints | Same paper, pp. 329-330, where initial data and the constraint equations are introduced | candidate initial-data structures in the legacy module | The vacuum/constraint scope is retained; exact smoothness and Lean encoding require statement work |
| Development relation | Same paper, definitions preceding the theorem on p. 330 | candidate development predicate and embedding relation | Must preserve the embedded initial hypersurface and induced metric/second fundamental form; no checked correspondence yet |
| Global hyperbolicity and maximality | Same theorem and the paper's extension construction, pp. 330-334 | candidate globally-hyperbolic/maximal predicates | Maximal among globally hyperbolic developments, not geodesic completeness or inextendibility among all spacetimes |
| Uniqueness | Same theorem, expressed through equivalence/isometry of maximal developments | candidate uniqueness-up-to-isometry formulation | Uniqueness is structural, not literal equality; exact quotient/category transport is open |

The source theorem is commonly summarized as existence and uniqueness of the
maximal globally hyperbolic development. The generated legacy description
"Einstein equations global existence" is too coarse: it can be misread as
future geodesic completeness, which the theorem does not assert. This intake
therefore freezes the narrower Cauchy-development claim.

Discovery link (not an immutable evidence receipt):

- Primary paper: <https://doi.org/10.1007/BF01645389>

No `H0` claim is made. The source audit must still record a content hash or
archived edition, map all assumptions and definitions, check corrections and
errata, and obtain independent review. The statement phase must inspect and
elaborate the candidate declaration rather than inherit its historical status.
