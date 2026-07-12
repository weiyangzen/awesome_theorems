# THM-M-1269 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the minimizing-sequence
existence lemma used in variational problems. The Stage0 label alone does not
fix a unique theorem, so this intake records the narrow standard claim below
and leaves exact Lean elaboration to the dependent statement phase.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A nonempty real-valued variational problem bounded below admits a sequence whose values converge to its infimum | Provisional until statement review accepts the encoding |
| Domain | An arbitrary type `X`, a functional `F : X -> Real`, and the range `Set.range F` | Extended-real and constrained-set variants require checked transports |
| Hypotheses | `X` is nonempty and `F` is bounded below | No compactness, coercivity, or attainment assumption |
| Conclusion | Existence of `u : Nat -> X` with `F (u n) -> sInf (Set.range F)` | This does not assert existence of a minimizer |
| Boundary cases | Empty domains and unbounded-below functionals are excluded | Constant and attained-minimum cases remain included |
| Foundations | Lean 4 kernel plus the classical choice needed to select approximate minimizers | Exact imports, axioms, and environment fingerprint remain open |

Potential proof architecture is the greatest-lower-bound approximation lemma,
selection of a point with value below `sInf + 1/(n+1)`, and a squeeze argument.
These are discovery nodes only; the obligation registry belongs to a later
phase.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first
failed theorem gate is exact-statement acceptance: the source entry says only
"approximation of variational problems," and no Lean expression, source
pinpoint, environment fingerprint, or mutation evidence has yet been accepted.
The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They
establish manifest membership, standard consistency, JSON syntax, and local
dossier hygiene only. No Lean proof or kernel closure is claimed.

## Statement phase

`Statement.lean` now declares the exact target as the proposition
`THM_M_1269_statement`, using only `Mathlib.Topology.Algebra.Ring.Real`. The ordered
binders, normalized expression hash, pinned environment, and three deliberately
changed mutation surfaces are recorded in `statement.json`. This phase checks
elaboration only: none of these proposition declarations supplies a proof of
the canonical claim, and theorem completion remains false.

## Anchor audit phase

The pinned mathlib declaration `exists_seq_tendsto_sInf` is a stronger usable
anchor. `AnchorAudit.lean` verifies the specialization to `Set.range F` and
the countable choice of preimages needed to recover a sequence in `X`.
Candidate revisions, search boundaries, trust output, and the honest `M1`
classification are recorded in `anchor_audit.json` and `anchor_audit.md`.
This audit does not install a canonical proof or claim theorem completion.

## Obligation-tree phase

The registry now freezes 14 semantic nodes and separate proof, refinement,
provenance, evidence, trust, documentation, and workflow graphs. The checked
composition in `ObligationTree.lean` remains conditional on the pinned
`exists_seq_tendsto_sInf` bridge. Consequently the root stays open at `M1`;
the frozen route and per-node boundaries are in `obligation-tree.md`.
