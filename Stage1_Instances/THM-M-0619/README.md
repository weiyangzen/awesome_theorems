# THM-M-0619 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the point-set-topology
Bolzano-Weierstrass target. The repository catalog gives Bernard Bolzano/Karl Weierstrass, 1817,
and the gloss `紧度量空间序列有收敛子列` (every sequence in a compact metric space has a
convergent subsequence). It supplies no citation or binder-complete proposition.

The received wording leaves two close readings open: every sequence in a compact metric carrier,
or every sequence whose values lie in a compact subset of a metric space. It also leaves metric
versus pseudometric conventions, the selector encoding, the exact convergence expression, limit
membership, universes, binder order, and boundary cases unstated. Intake preserves these choices
rather than selecting one by convention.

Pinned mathlib contains direct nearby interfaces in `Mathlib.Topology.Sequences`, including
`CompactSpace.tendsto_subseq` and `IsCompact.tendsto_subseq`. The former is more general than the
literal metric wording, while the latter adds a compact set and explicit membership data.
`IntakeProbe.lean` authenticates those APIs and their axiom reports only; it does not freeze a root,
provide a source transport, or claim proof credit. The duplicate `THM-M-0264` separately owns the
bounded-sequence wording in the real-analysis catalog category; its carrier is not source-fixed.

The provisional vector is `[H-unclassified, M3, R4]`: the catalog identifies a classical theorem
family but does not name a mathematical source, while a direct pinned Lean interface exists; exact
source fidelity, a canonical expression, proof-body provenance, and a readable source-faithful
reconstruction remain open. `instance.json` is the
structured scope authority, the scope map and crosswalk record the unresolved choices, and
`task-dag.json` leaves all six dependent phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
