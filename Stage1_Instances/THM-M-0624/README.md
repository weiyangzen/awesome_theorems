# THM-M-0624 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-0624`, the
Nagata-Smirnov metrization theorem. The repository attributes the entry to Jun-iti Nagata and Yuri
Smirnov in 1950, gives only the gloss "necessary and sufficient conditions for a topological space
to be metrizable," and labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not
human-source or kernel evidence.

The name identifies the classical theorem family, but the catalog does not state its conditions.
A stable secondary discovery page states the familiar regular/Hausdorff plus countable union of
locally finite basis families characterization. Intake records that formulation only as a candidate:
the separation convention, exact basis decomposition, empty-space boundary, and primary proof
source have not been selected or reviewed. Promoting the familiar wording to the canonical claim at
intake would add proposition-changing mathematics not present in the repository source.

`IntakeProbe.lean` checks only the adjacent pinned interfaces for metrizability, regularity,
separation, topological bases, and locally finite indexed families. A bounded local search found no
Nagata-Smirnov terminal declaration or packaged sigma-locally-finite-basis predicate in pinned
mathlib. The probe and search are discovery observations, not the later exhaustive anchor audit.

The provisional root vector is `[H1, M4, R4]`: a classical published theorem family and a secondary
statement lead are known, but no primary-source crosswalk, exact Lean target, or readable proof
reconstruction is accepted. All six downstream phases remain open in `task-dag.json`. This intake
claims no H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance.
