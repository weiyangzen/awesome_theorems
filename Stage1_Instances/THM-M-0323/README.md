# THM-M-0323 rev-5.6 intake

This directory is the `planned` intake for the repository label "Schauder basis theorem". The
repository's literal description, "existence of a basis in Banach spaces", does not determine a
true theorem: interpreted universally, it conflicts with the adjacent Enflo target recording that
some Banach spaces have no Schauder basis. Intake therefore preserves that wording as source
provenance but does not silently turn it into a universal existence claim.

The historical source candidate is Schauder's 1928 paper on the Haar orthogonal system. A likely
stable theorem family concerns a concrete Schauder basis for a specified function space, rather
than every Banach space. The exact function space, scalar field, norm, enumeration, endpoint
conventions, and source proposition must be inspected and selected during the statement phase.

Pinned mathlib contains the concrete `SchauderBasis` interface and a construction from rank-one
projections. `IntakeCheck.lean` verifies only those APIs; it does not prove an existence theorem.
The provisional vector is `[H2, M3, R4]`. No exact source statement, canonical Lean target, H0,
M0, R0, audit completion, or theorem completion is claimed.

See `scope-map.md`, `source-statement-crosswalk.md`, and `task-dag.json` for the frozen ambiguity,
crosswalk, and downstream work. Reproducible intake checks are recorded in `validation.md`.
