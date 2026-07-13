# THM-M-0230 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Weierstrass factorization
theorem. The repository supplies Karl Weierstrass, the year 1876, and only the gloss "infinite-
product representation of entire functions." Its catalog label `已验证` ("verified") is untrusted
inventory metadata under rev-5.6 and supplies no human-source or Lean proof credit.

The gloss identifies a classical theorem family, but not one exact proposition. It does not choose
between constructing an entire function with prescribed discrete zeros and factoring a given
nonzero entire function. Nor does it specify multiplicities, the zero at the origin, primary
factors, genus choices, local-uniform convergence, representation of the residual zero-free factor
as an exponential, the identically-zero case, or any uniqueness or converse clause. Intake does
not silently fill these
proposition-changing gaps with a familiar textbook formulation.

Bibliographic metadata for Weierstrass's *Zur Theorie der eindeutigen analytischen Functionen* and
an associated erratum, together with NIST DLMF's modern special-case Weierstrass product, were
inspected as source leads. No primary theorem text, exact locator, complete premise/conclusion map,
correction audit, or independent review was admitted, so they do not establish `H0`.

Pinned mathlib provides zero-order, isolated-zero, locally uniform product, finite-support
zero/pole extraction, and Euler sine-product machinery. `IntakeProbe.lean` authenticates those
interfaces. A bounded search found no terminal universal entire-function Weierstrass factorization
declaration. The similarly named power-series preparation theorem, the finite-support meromorphic
decomposition, the disk/Blaschke factor, and the sine product are not substitutes for this target.

The provisional vector is `[H1, M4, R4]`: a historically established theorem family and source
leads are known but the exact source statement and assumptions are not accepted; no usable exact
Lean artifact is credited; and no source-faithful proof reconstruction exists. `instance.json` is
the structured scope authority, and `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
