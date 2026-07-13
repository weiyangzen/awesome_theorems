# THM-M-1591 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `BCH码` (BCH
codes). The mathematical catalog supplies only the gloss `能纠正多个错误的码` ("codes capable of
correcting multiple errors"), the names Bose, Chaudhuri, and Hocquenghem, and the year 1959. Its
`已验证` field is untrusted inventory metadata, not an exact theorem or proof record.

The label denotes a classical theorem family, but the gloss does not choose a construction, the
BCH designed-distance bound, a dimension estimate, or decoder correctness. It also leaves open the
alphabet, finite extension, length, primitive and narrow-sense conventions, consecutive-root
interval, designed distance or correction radius, generator polynomial, code representation,
decoder, ordered binders, and boundary cases. Intake does not silently choose the familiar binary
primitive formulation or turn "multiple" into an invented numerical bound.

An NCSU repository scan of Bose and Ray-Chaudhuri's September 1959 mimeograph was inspected. It
contains several plausible roots, including a weight/error-correction criterion, a binary
rank-matrix criterion, and a binary `t`-error-correcting code construction with a dimension bound. The
catalog does not select among them, and the report's parity-check construction is not verbatim the
modern consecutive-root BCH-bound formulation. Hocquenghem's relationship, exact assumptions,
errata, and independent review also remain open. The report therefore supports provisional `H1`,
not `H0`.

Pinned mathlib provides Hamming-distance, finite-field, and polynomial/root-of-unity substrate.
`IntakeProbe.lean` authenticates a small set of those interfaces. A bounded exact-topic search
found no BCH or cyclic-code target declaration; generic infrastructure is not a BCH theorem. The
provisional vector is therefore `[H1, M4, R4]`.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the ambiguity and non-substitution boundary. All six
dependent phases remain open in `task-dag.json`. No canonical proposition, exact Lean target,
accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
