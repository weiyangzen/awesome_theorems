# THM-M-0318 rev-5.6 intake

This directory is the `planned` intake dossier for the Schauder fixed-point theorem. The intended
human claim is the compact-convex form: a continuous self-map of a nonempty compact convex subset
of a real normed vector space has a fixed point. This is narrower and more precise than the Stage0
phrase "a fixed-point theorem on Banach spaces" and does not silently substitute Banach's
contraction theorem or the finite-dimensional Brouwer theorem.

The primary 1930 Schauder paper has been identified bibliographically, but its exact theorem text,
page-level anchor, hypotheses, and errata have not yet been inspected. Accordingly the human claim
is frozen only at intake scope, while the exact source-controlled statement and canonical Lean
expression remain open for `S56-M-0318-STATEMENT`. `IntakeProbe.lean` checks only that the pinned
Lean environment exposes the vocabulary needed to express the scope; it is not the theorem.

The provisional root vector is `[H2, M4, R4]`. No source fidelity (`H0`), elaborated target, proof,
audit completion, or theorem completion is claimed. The scope map, source crosswalk, and open task
DAG are the authoritative navigation for subsequent phases.
