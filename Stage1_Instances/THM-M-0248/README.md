# THM-M-0248 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `毕晓普定理`
(Bishop's theorem). The catalog gives Errett Bishop, the year 1959, and only the gloss `有理逼近的
充要条件` ("a necessary and sufficient condition for rational approximation"). Its `已验证`
("verified") label is untrusted metadata and supplies no human-source or Lean proof credit.

Bishop's 1959 paper *Some theorems concerning function algebras* is a strong source candidate. Its
Theorem 4 treats a compact plane set without interior, the uniform closure of rational functions
whose poles lie off the set, and a minimal-boundary condition; the paper explicitly calls this a
necessary and sufficient condition for uniform rational approximation of every continuous
function. This close match identifies the intended theorem family, but the uncited catalog does not
select that paper or freeze the definitions and one of Theorem 4's four equivalent conditions.

The intake therefore records Theorem 4 only as a candidate statement family. The canonical human
and Lean statements remain null pending an independently reviewed, definition-complete source
crosswalk. The provisional vector is `[H1, M4, R4]`: a published proof source candidate is known,
but exact source fidelity remains open; no usable exact Lean artifact is identified; and no proof
reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` freezes the candidate boundary
and prohibited substitutions, while `source-statement-crosswalk.md` records the source-to-formal
decisions still open. The six dependent phases are open in `task-dag.json`. `IntakeProbe.lean`
checks adjacent pinned interfaces only and states no target theorem. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
