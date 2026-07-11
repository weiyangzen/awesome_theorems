# THM-M-1031 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Brownian martingale representation theorem.
It does not inherit proof credit from the source label `已验证` or the legacy `S1_M_224.lean` module.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Real square-integrable martingales on an augmented Brownian natural filtration have a predictable stochastic-integral representation | Horizon, augmentation, equality mode, and integrability convention require statement-phase freezing |
| Probability objects | Probability measure, real Brownian motion, its natural filtration, adapted martingale | General filtrations carrying Brownian motion are excluded |
| Analytic construction | Predictable integrands, simple-process integral, Ito isometry, L2 completion | No construction is credited by this intake |
| Representation argument | Density/closed-subspace or equivalent Brownian-filtration generation argument | Architecture only; terminal proof remains open |
| Variants | Fixed terminal variable and local-martingale forms are transport candidates | Neither is substituted for the root without checked equivalence |
| Lean surface | Lean 4 plus pinned mathlib; legacy `AwesomeTheorems.Stage1.S1_M_224` is discovery input | The legacy `StatementShape` assumes its representation conclusion and is not the exact root |
| Foundations | Kernel-checked measure theory with an accepted classical/choice/quotient policy | Exact environment and TCB fingerprints remain open |

The structured claim, ordered domains, assumptions, exclusions, and provisional formal target are in
`intake.json`. Source genealogy and the source-to-statement mapping are in
`source_statement_crosswalk.md`. The dependent statement phase must replace the provisional target
with an elaborated proposition and mutation-test the filtration, square-integrability, horizon, and
equality conventions before inspecting proof closure.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no normalized expression hash, environment fingerprint,
checked transport, or mutation record. The theorem is not complete.

## Validation

On base revision `dbd29db42090d2fce49f69d84d4631769ef7e9c3`, the commands and exact scoped results in
`validation.md` establish target membership, repository-standard consistency, JSON validity, and
dossier hygiene only. No Lean proof or kernel closure is claimed.
