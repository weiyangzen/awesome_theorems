# THM-M-0054 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Perron-Frobenius theorem.
The repository's mathematical catalog supplies only the gloss "spectral properties of
nonnegative matrices," attributes it to Oskar Perron and Ferdinand Frobenius, gives the year
1907, and labels it verified. Under rev-5.6 that label is untrusted inventory metadata, not a
source audit, an exact proposition, or proof evidence.

The gloss does not choose among the materially different theorems for entrywise-positive,
irreducible nonnegative, primitive nonnegative, or arbitrary nonnegative square matrices. It also
does not fix the scalar field, finite index type, order convention, spectral-radius encoding,
eigenvector normalization, simplicity notion, peripheral-spectrum clause, or zero-dimensional and
zero-matrix cases. Intake does not silently supply those proposition-changing clauses.

Perron's 1907 paper *Zur Theorie der Matrices* is a credible historical source lead matching the
catalog date. Crossref identifies *Mathematische Annalen* 64(2), pages 248-263, DOI
`10.1007/BF01449896`. A complete edition, pinpoint result, incorporated definitions, assumption
map, correction history, and independent review have not been admitted. Frobenius's later
nonnegative-matrix extensions also remain to be identified precisely. These are source leads, not
`H0` evidence.

Pinned mathlib supplies nonnegative-matrix irreducibility and primitivity definitions, their
power/path characterizations, matrix spectrum/eigenvalue infrastructure, and generic spectral
radius APIs. `IntakeProbe.lean` authenticates representative declarations. A bounded search found
no Perron-Frobenius spectral conclusion joining these APIs. The checked declarations are
ingredients or related facts, not substitutes for the source-selected theorem.

The provisional theorem-family intake assessment is `[H1, M4, R4]`: a classical proved theorem family and primary-source lead
are known but exact statement/source fidelity is unaudited; no usable exact formal artifact is
credited; and no source-faithful proof reconstruction is available. `instance.json` is the
structured scope authority, while `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed. The root vector remains unclassified until the canonical statement, fingerprint, and root
obligation are frozen; the `M4` family assessment is not an exhaustive external-candidate audit.
