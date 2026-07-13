# THM-M-1492 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `线性规划` (linear programming).
The repository catalog gives only the gloss `线性目标函数的优化` (optimization of a linear
objective function), attributes the entry to George Dantzig and 1947, and labels it `已验证`.
These are untrusted discovery fields: they provide no citation, mathematical proposition,
assumptions, proof, or formal artifact.

The title and gloss identify a problem family, not a truth-valued theorem. They do not choose a
minimization or maximization model, decision space, scalar field, objective, constraints, standard
form, feasibility hypotheses, or a conclusion such as attainment, a boundedness alternative,
optimality at an extreme point, duality, or algorithm correctness. Selecting a familiar linear
programming theorem would manufacture or substitute missing mathematics. This intake therefore
freezes the ambiguity rather than inventing an exact human or Lean statement.

The provisional root is `[H5, M4, R4]`. `H5` applies only to the received catalog wording, which is
not yet a stable proposition; it does not say that standard linear-programming theorems are false
or open. `M4` records that no source-identical formal target can be selected before the proposition
is fixed. `R4` records that no source-faithful proof reconstruction can attach to an unknown root.

`IntakeProbe.lean` elaborates adjacent pinned proper-cone, separation, and meta simplex-certificate
APIs. Mathlib's own cone module lists definitions of linear programs and LP duality as future work,
while the simplex implementation is a meta-level certificate-search oracle for `linarith`, not a
kernel theorem for this catalog target. The probe establishes API feasibility only and carries no
statement or proof credit. Every downstream task remains open; neither audit completion nor theorem
completion is claimed.

See `scope-map.md`, `source-statement-crosswalk.md`, and `validation.md` for the precise boundary and
self-test evidence.
