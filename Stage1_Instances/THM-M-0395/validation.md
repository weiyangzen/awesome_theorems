# Validation handoff

Validation was run on base revision
`c6c42c0e2299434c893a99fb40cc6f586e261523`. The pinned Lean 4.29.0 kernel
elaborated the statement, all three local terminal transports, and three
separately reconstructed probes in `Validation.lean`. `#print axioms` reported
only `propext`, `Classical.choice`, and `Quot.sound`. The fail-closed verifier
checked proof-receipt freshness, the 17-node registry/graph identity, the
mathlib revision, the exact partial-support boundary, and local hygiene.

This is truthful warm-cache worker evidence, not release-grade hermetic or
independent evidence. The proof prerequisite has no closed frozen obligation:
the Faltings root, its arithmetic-geometric inputs, and root composition remain
open at M4. The run reused the canonical pinned `.lake` cache, and the
independent reconstruction ran in this same checkout. There is no empty-cache
offline replay, distinct signed runner, complete TCB/provenance closure,
H0/R0 review, SBOM/license archive, deterministic release bundle, or master
acceptance. The first failed gate is therefore dependency/root closure; the
first release-only failure is the hermetic cold-build gate.

Exact structured recipes, input hashes, results, invalidation inputs, and retry
conditions are recorded in `validation-receipt.json`. The theorem remains
incomplete.
