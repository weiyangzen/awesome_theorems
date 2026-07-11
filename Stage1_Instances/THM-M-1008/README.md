# THM-M-1008 rev-5.6 intake

This directory is the new rev-5.6 `planned` instance for the Hewitt-Savage zero-one law. The
historical `S1_M_288.lean` module is discovery input only and supplies no statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every measurable event of an iid sequence that is invariant under finite coordinate permutations has probability zero or one | Exact Lean binders and expression fingerprint belong to the statement phase |
| Probability model | A probability space, a countable sequence of measurable random variables, mutual independence, and a common law | Completion and measurability conventions remain to be frozen |
| Symmetry | Invariance of a path-space event under every permutation with finite support | Invariance only in measure, arbitrary permutations, and exchangeability of the law are not substitutes |
| Conclusion | Probability of the pulled-back path event is `0` or `1` | Almost-sure constancy formulations require checked transports |
| Proof route | Finite-coordinate approximation, move the approximant to disjoint coordinates, independence, and limiting comparison | Architecture only; no proof closure is credited |
| Foundations | Lean 4 kernel plus pinned mathlib measure/probability APIs | Toolchain, imports, TCB, classical choice, and dependency fingerprints remain open |

The theorem includes arbitrary measurable state spaces only if the selected source and Lean
measurability interfaces support that scope. The statement phase must not silently replace the iid
hypothesis by mere exchangeability, or the finite-permutation-invariance hypothesis by tail-event
measurability.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The source record and a primary
historical paper have been identified, but pinpoint premise and errata review remain open. The first
failed theorem gate is the exact Lean statement gate. The theorem is not complete.

## Validation

On base revision `9c650bd6aac0dca129c8bc8ac01e0d7432669386`, the commands in `validation.md`
established target membership, standard consistency, JSON syntax, and dossier-local hygiene only.

