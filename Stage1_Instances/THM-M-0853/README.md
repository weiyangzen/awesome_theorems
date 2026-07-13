# THM-M-0853 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0853`, the catalog entry
named `Dirac定理` (Dirac's theorem). The repository supplies only the gloss "a degree condition for
the existence of a Hamiltonian cycle," attributes it to Gabriel Dirac in 1952, and labels it
`已验证`. Under rev-5.6 that label is untrusted metadata, not a human-source audit or machine-proof
claim.

The gloss identifies the classical graph-theoretic Dirac theorem family. Its conventional reading
is that a finite simple graph with at least three vertices and minimum degree at least half its
order is Hamiltonian. The catalog, however, does not state the graph model, the order bound, the
degree inequality, or a proposition-level source. For odd graph orders, natural-number formulas
such as `n / 2 <= delta`, `(n + 1) / 2 <= delta`, and `n <= 2 * delta` are not interchangeable.
Intake therefore records the family without selecting any of these as the canonical statement.

Crossref bibliographic metadata identify a strong historical source lead: G. A. Dirac, "Some Theorems on Abstract
Graphs," *Proceedings of the London Mathematical Society* s3-2(1), 69-81 (1952), DOI
`10.1112/plms/s3-2.1.69`. The article text, exact theorem/page passage, definitions, assumptions,
proof boundary, and errata were not available for inspection here. The citation remains an
unaccepted bibliographic discovery lead rather than an `H0` source packet.

Pinned mathlib exposes finite graph degree, minimum degree, Hamiltonian-cycle, and Hamiltonian-graph
interfaces in `Mathlib.Combinatorics.SimpleGraph.Hamiltonian`. `IntakeProbe.lean` checks those APIs
and several candidate proposition shapes. A bounded pinned-source search found no Dirac
minimum-degree-to-Hamiltonicity theorem. This supports provisional `M3` statement-interface debt,
not an exact target or proof.

The provisional root vector is `[H1, M3, R4]`: a published classical theorem family and source lead
are identified but not crosswalked at proposition level; the pinned formal substrate can express
candidate statements but no canonical expression is frozen; and no source-faithful readable proof
reconstruction exists. All six downstream phases remain open. No `H0`, `M0`, `R0`, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
