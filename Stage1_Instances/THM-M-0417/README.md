# THM-M-0417 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Minkowski's convex body theorem. Historical
Stage1 files are discovery inputs only and confer no accepted proof or statement credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A centrally symmetric convex body of sufficiently large volume contains a nonzero lattice point | Exact choices of ambient real space, lattice, measure, strict inequality, and body regularity are deferred to the statement phase |
| Strict form | Measurable convex symmetric set with volume strictly greater than `2^n` times lattice covolume | The legacy mathlib-shaped candidate uses an additive fundamental domain; it is not yet credited |
| Boundary form | Compact convex symmetric set with volume at least `2^n` times lattice covolume | This is a candidate strengthening with extra topology hypotheses, not an interchangeable root |
| Object-model bridge | Full-rank lattice/covolume language to `AddSubgroup` plus `IsAddFundamentalDomain` and `mu F` | Requires a checked transport and explicit lattice hypotheses |
| Degenerate cases | Dimension zero, trivial ambient space, zero/infinite measures, boundary equality | Must be mutation-tested rather than silently excluded |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure/topology dependencies | Exact toolchain, import closure, axioms, and TCB remain open |

The mandatory architecture starts with statement normalization, lattice/fundamental-domain
transport, symmetry and convexity hypotheses, the geometry-of-numbers core, and extraction of a
nonzero lattice point. This intake does not freeze the later obligation registry.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the statement gate: no canonical elaborated expression hash, environment fingerprint, checked
transport, or mutation record exists. The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and dossier hygiene only; they do not establish a
Lean theorem or accept the legacy wrapper.
