# THM-M-0934 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the repository target
`Erdős-Heilbronn猜想` (Erdos-Heilbronn conjecture). The catalog supplies only the gloss
`子集和的大小下界` (a lower bound for the size of subset sums), the names Paul Erdos and Hans
Heilbronn, the year 1964, and the label `已验证`. Under rev-5.6 that label is untrusted metadata,
not human-source or machine-proof evidence.

The gloss is not a binder-complete proposition. In particular, Chinese `子集和` can mean the set
of sums of all subsets, while the theorem name conventionally points to restricted addition of
distinct elements modulo a prime. Even within restricted addition, the catalog does not select the
one-set bound, the later two-set version, or the general `h`-fold Dias da Silva-Hamidoune theorem.
Those variants have different binders, boundary cases, conclusions, and proof ownership.

An immutable secondary survey, arXiv:1210.6509v2, was inspected. Its Theorem 2.2 states a two-set
restricted-sum lower bound over `Z/pZ`, distinguishes the `A = B` case proved by Dias da Silva and
Hamidoune from the later general case, and warns that the conjecture did not appear in the cited
1964 Erdos-Heilbronn paper. Crossref metadata identifies that 1964 paper and the 1994 proof paper,
but no primary theorem passage, complete premise map, correction record, or independent source
review is admitted here. These records support `H1`, not `H0` or statement selection.

Pinned mathlib provides all-subset sums and the neighboring unrestricted Cauchy-Davenport theorem.
`IntakeProbe.lean` checks those exact interfaces. Neither is the restricted sumset theorem, and a
bounded exact-topic search found no obvious Erdos-Heilbronn or Dias da Silva-Hamidoune declaration.
The probe is encoding/discovery evidence only, so the machine status remains `M4`.

Accordingly, the canonical mathematical statement and Lean target remain null, the provisional
root vector is `[H1, M4, R4]`, and all six downstream tasks remain open. No exact statement,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
