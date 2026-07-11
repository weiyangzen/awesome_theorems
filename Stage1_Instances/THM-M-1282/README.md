# THM-M-1282 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Stage0 item named "Schoen theorem," whose
stated content is the conformally flat case of the Yamabe problem. The short label is not itself a
unique theorem citation. The intake therefore preserves that narrow scope and records the source
identification work still required rather than silently substituting the unrestricted Yamabe
theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | Existence of a constant-scalar-curvature metric conformal to a given locally conformally flat metric on a smooth compact boundaryless manifold of dimension at least three | Connectedness, regularity conventions, and exact source theorem remain to be pinned |
| Geometric formulation | A positive smooth conformal factor and the scalar-curvature transformation law | No uniqueness, prescribed constant, or volume normalization is claimed |
| Analytic formulation | Positive solution of the critical Yamabe equation | Laplacian sign, constants, function spaces, and equivalence transport are open |
| Variational formulation | Attainment of the Yamabe quotient in the conformal class | No checked equivalence or compactness argument is credited |
| Proof architecture | Strict comparison with the sphere, concentration exclusion, Green-function/mass argument, and minimizer regularity are candidate branches | The obligation registry belongs to the later obligation-tree phase |
| Lean surface | Manifolds, Riemannian metrics, scalar curvature, conformal change, Sobolev/elliptic PDE infrastructure | No declaration or exact expression has been identified or elaborated |
| Foundations | Lean 4 kernel plus versioned policies for classical analysis, choice, quotients, and geometric analysis | Profile and dependency fingerprint remain open |

The canonical provisional claim, ordered domains, hypotheses, exclusions, and candidate encodings
are structured in `intake.json`. Source genealogy and the unresolved mismatch between the Stage0
label and Schoen's broader 1984 paper are explicit in `source_statement_crosswalk.md`.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.

The next phase must first resolve `SRC-1282-1` (a pinpoint primary-source theorem for exactly the
locally conformally flat claim), then choose definitions and elaborate the exact Lean target. No
downstream node is accepted or bypassed by this intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
source/exact-statement identification: the repository supplies only a short descriptive label, and
there is no Lean declaration, normalized expression hash, environment fingerprint, or checked
transport. The theorem is not complete.

## Validation

On base revision `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`, the worker ran the commands in
`validation.md`. They establish manifest membership, repository-standard consistency, JSON syntax,
and dossier-local integrity only; no Lean kernel result is claimed.
