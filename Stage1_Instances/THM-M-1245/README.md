# THM-M-1245 rev-5.6 intake

This directory is the `planned` intake for the Sobolev inequality. The repository source phrase
"Sobolev embedding in norm form" is scoped to the classical first-order Euclidean estimate for
compactly supported functions: when `1 <= p < n` and `1/q = 1/p - 1/n`, the `L^q` norm of a
function is bounded by a dimension/exponent dependent constant times the `L^p` norm of its
gradient.

The statement phase now freezes this as a real-valued `C^1` estimate on
`EuclideanSpace Real (Fin n)` with Lebesgue volume, compact support, `NNReal` exponents, the
`p = 1` endpoint, and a constant uniform over the function. `Statement.lean` kernel-elaborates
that boundary. The provisional root vector remains `[H2, M4, R4]`; statement elaboration is not
source acceptance or proof credit, and audit completion and theorem completion remain false.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation is
recorded in `validation.md`; statement metadata is in `statement.json`.
