# THM-M-1447 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Cholesky
decomposition. The repository supplies only the gloss "decomposition of a symmetric positive
definite matrix", an Andre-Louis Cholesky attribution, the year 1910, and an `已验证` label. Under
rev-5.6 the label is untrusted inventory metadata, not a source-reviewed proposition or machine
proof.

The gloss identifies a classical theorem family but is not binder-complete. It does not choose real
symmetric versus complex Hermitian matrices, finite dimension or ordered indices, lower versus
upper factor orientation, transpose versus conjugate transpose, diagonal normalization,
existence-only versus existence-and-uniqueness, or the zero-dimensional case. Selecting the usual
`A = L * Lᵀ` theorem, a complex `A = L * Lᴴ` theorem, or an upper-triangular variant would add
mathematics absent from the repository source. The canonical statement and Lean target therefore
remain null.

Netlib's LAPACK Users' Guide, section 2.3.4, was inspected as an authoritative numerical-linear-
algebra source lead. It distinguishes real symmetric and complex Hermitian positive-definite
matrices and lower/upper Cholesky orientations. It corroborates the theorem family but is not the
catalog's cited source, does not settle every source-fidelity and exact-mathematical convention, and
has no independent review here. It receives no H0 credit.

Pinned mathlib defines `Matrix.PosDef` and proves adjacent properties, including Hermitian symmetry,
positive diagonal entries, invertibility, and positive definiteness of injective Gram factors. It
also constructs an `LDLᴴ` decomposition in `Mathlib.Analysis.Matrix.LDL`; that module still marks
lower-triangularity of its `LDL.lower` factor as a TODO and does not state the requested normalized
`LLᴴ` Cholesky result. The intake probe checks those APIs. A bounded search found no Cholesky-named
or exact factor-existence declaration. This is discovery evidence only, not an exhaustive anchor
audit or proof.

The provisional vector is `[H1, M4, R4]`: the classical family and an authoritative source lead are
known, but no repository-cited, pinpoint, independently reviewed exact proposition is frozen; no
source-identical formal artifact is credited; and no proof reconstruction exists. `instance.json`
freezes this boundary and `task-dag.json` leaves all six downstream phases open. No accepted state,
audit completion, theorem completion, or master acceptance is claimed.
