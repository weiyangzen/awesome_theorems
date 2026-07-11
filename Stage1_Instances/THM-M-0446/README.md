# THM-M-0446 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Wiles-Taylor semistable modularity
theorem. The legacy label "modularity lifting" is potentially broader than a single theorem; this
intake fixes the root to the published claim that every semistable elliptic curve over `Q` is
modular. A later phase may model the lifting theorems as proof obligations, but may not silently
replace the root with one of them.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | Every semistable elliptic curve over `Q` is modular | Wiles (1995), Theorem 0.4; source acceptance remains open |
| Domain | Elliptic curves over the rational numbers | Singular cubic models are excluded |
| Hypothesis | Semistability at every prime | The exact reduction predicate and local data API are not selected |
| Conclusion | Association with a weight-two modular eigenform | Exact level, normalization, and Lean predicate are not selected |
| Proof architecture | residual modularity, deformation rings, Hecke algebras, patching/numerical criterion, representation-to-curve bridge | Architecture only; no leaf or composition is credited |
| Companion source | Taylor-Wiles ring-theoretic completion of the argument | Premise-to-node and errata audits remain open |
| Formal surface | Lean 4 plus pinned mathlib and, if audited, a pinned external Lean 4 dependency | No candidate declaration or elaborated expression has been found or checked |

The scope deliberately excludes the later full modularity theorem for every elliptic curve over
`Q`. It also excludes treating a general-purpose modularity-lifting implication as though it were
the elliptic-curve root. The structured binders, definitions, and exclusions are in `intake.json`;
the source genealogy and statement correspondence are in `source_statement_crosswalk.md`.

## Open task DAG

`STATEMENT` must choose an actual Lean object model, define or locate semistability and modularity,
elaborate the exact target, fingerprint the environment, and mutation-test its domain and
hypothesis. `ANCHOR_AUDIT` must then search pinned mathlib and external Lean 4 candidates and audit
the two primary papers. Only afterward may `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE`
freeze architecture, implement proof bodies, produce kernel evidence, and seek master acceptance.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: no declaration, elaborated expression, environment fingerprint, or
checked transport exists. The theorem is not complete.

## Validation

The exact intake-only checks and their outputs are recorded in `validation.md`. They establish
manifest membership, repository-standard consistency, JSON syntax, and dossier-local integrity
only. No Lean theorem or kernel result is claimed.
