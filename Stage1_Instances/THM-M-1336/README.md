# THM-M-1336 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item "comparison
theorem" in ordinary differential equations. The repository supplies only the Chinese title
`比较定理`, attributes it generically to many mathematicians in the twentieth century, and glosses
it as `微分不等式与解的比较` ("comparison of differential inequalities and solutions"). It
supplies no primary citation, exact theorem, ordered binders, hypotheses, or conclusion. The
catalog label `已验证` is explicitly untrusted metadata and gives no human-source or Lean proof
credit.

That wording can describe several non-equivalent results: a fencing theorem comparing two scalar
functions from derivative inequalities, an ODE subsolution/supersolution principle, a first-contact
comparison theorem for solutions of a scalar or ordered system, or a quantitative Gronwall-type
bound. The neighboring catalog entries separately own Gronwall and Bihari-LaSalle inequalities.
Choosing any one formulation from background knowledge would therefore broaden or substitute the
received target.

This intake freezes the ambiguity, admissible scope questions, and source-to-statement crosswalk.
It does not freeze a canonical mathematical proposition or Lean target. The provisional vector is
`[H5, M4, R4]`: `H5` says only that the received catalog wording is not yet a stable proposition,
not that established comparison theorems are false or mathematically open. No source-identical
formal artifact or readable proof reconstruction is credited.

Pinned mathlib exposes relevant fencing, Gronwall, and ODE-trajectory comparison declarations.
`IntakeProbe.lean` checks those APIs only to document the ambiguity and feasibility surface. It is
not a target declaration, exact-statement check, anchor audit, or proof. The authoritative intake
data are in `instance.json`; all six dependent phases remain open in `task-dag.json`.

No source acceptance, statement closure, H0, M0, R0, audit completion, theorem completion, or
master acceptance is claimed.
