# THM-M-0862 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the catalog entry named Menger's
theorem with the gloss "vertex connectivity and disjoint paths." The wording identifies a theorem
family but not one proposition. It does not select a local separator equality or a global
`k`-connectivity characterization, terminal sets or vertices, finite or infinite graphs, the path
disjointness convention, the separator convention, or the boundary cases.

Karl Menger's 1927 paper *Zur allgemeinen Kurventheorie* was retrieved from its publisher and its
bibliographic identity was checked through DOI metadata. Visual inspection of the image-only scan
located `Satz beta` on printed pages 100-102: a theorem about pairwise disjoint arcs between two
finite sets in a compact regular one-dimensional space under a point-separation condition. Its
definitions and German-to-graph transport have not been independently reviewed, so this does not
select a finite-graph root. An inspected modern source, Reinhard Diestel's *Graph Theory*, sixth
edition (2025), separates the finite set-to-set theorem (Theorem 3.3.1), its point-to-point
corollary (Corollary 3.3.5), and a global connectivity form (Theorem 3.3.6). Diestel further
attributes the global version to Whitney in 1932. That distinction exposes a conflict between the
catalog's Menger/1927 attribution and its global-sounding gloss rather than resolving the intended
root.

The repository also schedules `THM-M-0813`, whose Menger-family gloss is "the maximum number of
disjoint paths in a graph." No accepted alias, deduplication, or ownership decision relates the two
targets. Evidence cannot be transferred between them.

Pinned mathlib supplies paths, reachability, induced graphs, and edge-connectivity interfaces.
`IntakeProbe.lean` authenticates those adjacent APIs. A bounded exact-topic search found no Menger
declaration or vertex-separator/path-packing characterization. These interfaces are ingredients,
not a canonical target or proof, so the provisional vector is `[H1, M4, R4]`.

The canonical statement and Lean target remain null and all six downstream tasks remain open. No
exact proposition, H0, M0, R0, accepted state, audit completion, theorem completion, or master
acceptance is claimed. Only the integration lane may accept this self-tested worker proposal.
