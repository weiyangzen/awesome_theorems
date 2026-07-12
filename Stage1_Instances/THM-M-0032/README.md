# THM-M-0032 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the catalog item named
"Auslander-Buchsbaum theorem." The repository's literal claim is "a regular local ring is a UFD,"
attributed to Maurice Auslander and David Buchsbaum and dated 1958. The catalog's `verified` label
is untrusted metadata and supplies no human-source or Lean proof credit.

## Scope frozen at intake

The received claim points to Auslander and Buchsbaum's paper *Unique Factorization in Regular
Local Rings*. Its Theorem 5 on page 734 says that every regular local ring is a unique
factorization domain. The paper was published in May 1959, so the catalog's unexplained 1958 date
is held as a source discrepancy. This target is not the commonly named Auslander-Buchsbaum
projective-dimension/depth formula, and that formula cannot replace the catalog claim.

The source uses prior notation for regular local rings and a reduction through dimension at most
three. Its incorporated definitions, assumption transport, proof boundary, and the 1958/1959
discrepancy remain open on the human-source axis. This does not prevent freezing the catalog's
conventional unrestricted proposition for the machine statement gate.

## Formal boundary

The statement phase freezes
`Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget` as
`forall (R : Type u) [CommRing R] [IsRegularLocalRing R], UniqueFactorizationMonoid R`.
`IsRegularLocalRing` already includes local, Noetherian, and nontrivial structure. The zero ring is
therefore excluded by the accepted antecedent, while fields and dimension zero remain included.
The sole direct import is `Mathlib.RingTheory.RegularLocalRing.Defs`; a checked iff transports to
an explicit regularity hypothesis, and four structural mutations plus the rational-field boundary
are self-tested.

Pinned mathlib contains no located declaration connecting regular local rings to unique
factorization. The provisional vector is `[H1, M3, R4]`: exact statement/interface evidence is
self-tested, but the source mapping and independent review remain open and no proof or readable
reconstruction is credited. The statement proposal awaits master acceptance, and every later task
remains open. No accepted proof state, audit completion, or theorem completion is claimed.
