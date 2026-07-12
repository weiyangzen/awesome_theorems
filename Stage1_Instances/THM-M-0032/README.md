# THM-M-0032 rev-5.6 intake

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
three. Intake therefore does not yet ratify a binder-complete modern proposition, incorporated
definitions, assumption transport, or proof boundary. The exact commutative-ring convention,
domain consequence, local/Noetherian/regular definitions, and UFD encoding remain for the
statement and source-review gates.

## Formal boundary

Pinned mathlib exposes `IsRegularLocalRing` and `UniqueFactorizationMonoid` but contains no located
declaration connecting them. `IntakeProbe.lean` checks only those adjacent interfaces. It does not
declare the target, inspect a terminal proof body, or grant machine closure.

The provisional vector is `[H1, M4, R4]`: a primary theorem and modern corroborating source are
located, but the full source mapping and independent review are open; no usable exact formal
artifact is credited; and no source-faithful proof reconstruction is complete. All six downstream
tasks remain open. No accepted state, audit completion, theorem completion, or master acceptance
is claimed.
