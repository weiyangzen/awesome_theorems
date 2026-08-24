# Build validation

The authorized worker gate is `complete-target-semantic-proof-debt`, invoked through the immutable task-local validator with `--no-lean`. It checks the exact 18-path artifact set, sealed statement crosswalk, frozen provider source binding, nonempty transitive semantic census, equal semantic expression locks, absence of local semantic shadowing/substitution, forbidden Lean constructs, exact provenance import/declaration strings, M0 closure, total injective R0 mapping, and provisional release strict dominance.

The worker does not invoke Lean, Lake, or Elan. Accordingly, only a successful task-local semantic/evidence preflight is claimed here. The canonical Master must compile all three Lean artifacts at trust zero after harvest, recompute the provider transport and transitive environment from source, run clean cold offline replay, and run semantic-substitution mutations before accepting the candidate.

Executable imports are exactly `Mathlib`; the frozen provider import is a provenance comment in each Lean file. The source conjecture's `sorryAx` is not in the local root dependency graph.
