# Build validation

The worker executed only the immutable task-local semantic/evidence validator with `--no-lean`, as required by the claim. The validator checks the complete owned path set, sealed semantic crosswalk, provenance comments, absence of forbidden Lean declarations, M0 machine closure, total injective R0 reconstruction, and provisional release dominance.

Cold offline trust-zero Lean compilation is intentionally deferred to the canonical Master after harvest. No Lean, Lake, Elan, network, clone, fetch, canonical repository read, or canonical write was performed in this worker generation.
