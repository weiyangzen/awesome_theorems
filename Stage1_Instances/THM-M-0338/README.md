# THM-M-0338 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the Kadison-Singer problem. The
repository supplies only the gloss "unique extension of pure states". The conventional problem
concerns pure states on the diagonal maximal abelian C-star subalgebra of bounded operators on a
separable infinite-dimensional Hilbert space and their extensions to the full operator algebra.

The statement phase freezes this conventional affirmative claim as
`Stage1.THM_M_0338.KadisonSingerStatement`: a `Nat`-indexed complex Hilbert basis, the star
subalgebra characterized by vanishing off-diagonal matrix coefficients, extreme-point pure states,
and existence and uniqueness among all normalized positive extensions. See `statement.json` and
`statement-validation.md` for the exact boundary and pinned elaboration evidence.

The statement elaborates, but it is not proved. The bounded anchor audit found no terminal Lean
proof, and registry version 1 now freezes 16 obligations plus separate typed proof, provenance,
source, trust, and workflow graphs. The checked `root_of_components` theorem validates only the
child-to-root logical composition; its existence and uniqueness package is an explicit open premise.
Primary-source closure, every substantive proof leaf, release validation, and independent review
remain open. The obligation phase records root machine debt M3 and supplies no theorem-completion
credit.
