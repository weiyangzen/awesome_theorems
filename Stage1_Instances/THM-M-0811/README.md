# THM-M-0811 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0811`, the Eulerian-path
theorem family. The repository supplies only the gloss "necessary and sufficient conditions for
the existence of an Eulerian path." It does not state those conditions or fix the graph model,
finiteness, connectivity convention, endpoint convention, or treatment of isolated vertices.

The University of the Pacific Euler Archive record for Euler's E53 paper was inspected as a
historical primary-source locator. It describes the Konigsberg impossibility argument and records
the paper as written in 1735 and published in 1741, rather than establishing the catalog's modern
general iff or its date 1736. No source passage supporting one exact modern characterization has
therefore been accepted.

Pinned mathlib defines `SimpleGraph.Walk.IsEulerian` and proves that an Eulerian trail forces the
expected endpoint parity and zero-or-two odd-degree condition. The same module explicitly lists
the converse existence direction as TODO. `IntakeProbe.lean` checks these interfaces against the
pinned environment. They are vocabulary and necessary-direction evidence only, not the catalog's
unspecified iff and not proof credit.

The provisional root vector is `[H1, M3, R4]`: the classical theorem family and a relevant
historical source are known, but the exact modern source statement and assumptions are not mapped;
pinned Lean supplies definitions and one direction but not a frozen exact root; and no reviewed
readable proof reconstruction exists. `instance.json` is the structured scope authority and
`task-dag.json` leaves all six downstream phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
