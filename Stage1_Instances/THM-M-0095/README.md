# THM-M-0095 rev-5.6 intake

`THM-M-0095` is the representation-theory catalog item named the Cartan decomposition theorem.
The repository explicitly glosses that name as "root-space decomposition of a semisimple Lie
algebra," attributes it to Elie Cartan in 1913, and supplies an untrusted `verified` label.

## Intake result

This directory is a fail-closed `planned` dossier. The gloss identifies the classical root-space
decomposition family, but it is not an exact proposition. It omits the coefficient field,
characteristic, finite-dimensionality, splitting assumptions, choice and definition of a Cartan
subalgebra, ordinary versus generalized root spaces, the root index, and whether "decomposition"
asserts only spanning, an internal direct sum, bracket compatibility, or a larger package.

Pavel Etingof's author-issued MIT 18.745 lecture notes were inspected as a modern source lead.
Proposition 19.11(i), in the finite-dimensional algebraically closed characteristic-zero setting,
states the direct decomposition of a semisimple Lie algebra into a Cartan subalgebra and its
nonzero ordinary root spaces. Parts (ii)-(iv) add bracket and bilinear-form properties. The catalog
does not cite this edition or decide whether the companion clauses belong to its root. No complete
definition, assumption, proof-node, correction, historical-attribution, or independent-review map
has been admitted. The source therefore supports `H1`, not `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates pinned ordinary and generalized weight-space APIs, independence and
spanning results, the Cartan plus nonzero generalized-root spanning theorem, and an `IsKilling`
ordinary-root bridge. These interfaces are substantive `M3` statement and reduction substrate, but
not closure of the received theorem. In particular, pinned mathlib defines `rootSpace` using
generalized weight spaces, and its ordinary-root bridge assumes nondegenerate Killing form; the
library documents that the converse from semisimplicity in characteristic zero is still absent.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M3, R4]`. All six downstream tasks remain open. No accepted execution state, exact statement,
proof, audit completion, theorem completion, or master acceptance is claimed.
