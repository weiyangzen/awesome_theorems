# THM-M-0222 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Cauchy integral formula. The
repository attributes the result to Augustin Cauchy in 1831 and gives only the gloss
`全纯函数由边界值表示` ("a holomorphic function is represented by boundary values"). Its `已验证`
label is untrusted metadata under rev-5.6, not a source audit, an exact Lean proposition, or proof
evidence.

The gloss identifies a classical theorem family but omits proposition-changing choices. It does
not select a scalar or Banach-valued function, a circle or general contour/domain formulation,
the continuity and holomorphicity assumptions, the contour orientation and winding convention,
the normalization, the evaluation point, or whether formulas for derivatives are included.
Choosing one familiar variant at intake would silently strengthen or narrow the received claim.

NIST DLMF section 1.9 supplies an authoritative modern source lead for the scalar simple-closed-
contour formula and its derivative extension. It was inspected at stable equation locators
1.9.E30 and 1.9.E31, but it is not the catalog's cited source, does not by itself settle the
historical 1831 attribution, and has no independent source review. It is therefore a source lead,
not `H0` evidence.

Pinned mathlib contains strong formal candidates in
`Mathlib.Analysis.Complex.CauchyIntegral`. `IntakeProbe.lean` authenticates normalized and
unnormalized Banach-valued circle formulas, a scalar division formula, and their current axiom
reports. A foreign wrapper in the legacy module for `THM-M-1559` is also recorded as discovery
input. None is identified with a source-selected root here, and none receives proof credit.

The provisional root vector is `[H1, M3, R4]`: the classical proved family and a modern source lead
are known; strong pinned formal candidates exist; but the exact source statement, source-to-Lean
transport, and source-faithful readable proof reconstruction remain open. `instance.json` is the
structured scope authority, and `task-dag.json` keeps all six downstream phases open. No canonical
mathematical or Lean statement, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
