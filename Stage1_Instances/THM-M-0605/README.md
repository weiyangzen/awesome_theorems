# THM-M-0605 rev-5.6 dossier

This directory is the `planned` rev-5.6 dossier for the existence of a
seven-dimensional exotic sphere. The repository claim fixes dimension seven
but does not define "exotic sphere" or select a formal construction. The
dossier reads the standard mathematical content as existence of a smooth
7-manifold homeomorphic, but not diffeomorphic, to the standard smooth
7-sphere. The definition, representation choices, and source boundary are
made explicit in the elaborated `Statement.lean` target. The witness is an
abstract `Type 0` smooth manifold modeled on `EuclideanSpace Real (Fin 7)`.
The standard object is the unit sphere in `EuclideanSpace Real (Fin 8)`;
homeomorphism is `Nonempty Homeomorph` and non-diffeomorphism is
`IsEmpty Diffeomorph`.

The stable scope is recorded in `scope-map.md`, and
`source-statement-crosswalk.md` relates each component to the repository
record and Milnor's 1956 primary paper. The frozen architecture now lives in
`obligation-registry.json` and the seven separate graphs in
`typed-graphs.json`; `obligation-tree.md` is their readable projection. The
selected route uses Milnor's sphere-bundle construction followed by separate
topological-sphere and smooth-obstruction branches. `ObligationTree.lean`
checks only conditional terminal assembly and supplies no witness proof.

## Statement verdict

Lifecycle remains `planned`; the provisional root vector remains
`[H1, M4, R3]`. A
primary historical source is identified, but its precise premise-to-conclusion
mapping, errata status, and independent review are open. The exact Lean type,
sole direct import, serialized expression hash, and pinned environment are
frozen in `statement-receipt.json`. Four non-equivalent mutations cover a
removed hypothesis, changed domain, changed binder scope, and boundary
dimension; each fails its intended definitional identity check.

`task-dag.json` remains master-owned execution projection and is not edited by
this worker. `validation.md` records the smallest real statement checks and
their limits. The repository metadata label
`已验证` is untrusted discovery input and supplies no theorem-completion
evidence. Master acceptance remains outstanding.
