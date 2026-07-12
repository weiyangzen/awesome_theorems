# THM-M-1362 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `叉形分岔`
(pitchfork bifurcation). The catalog supplies only that name, a collective twentieth-century
attribution, and the gloss `对称性破缺的分岔` (a bifurcation of symmetry breaking). It supplies no
cited proposition, model, definitions, hypotheses, conclusion, or proof source. Its `已验证`
status is explicitly untrusted metadata under rev-5.6.

"Pitchfork bifurcation" names a family of related statements, not one binder-complete theorem.
The source could intend the elementary scalar normal form, a local theorem for odd or equivariant
families, a supercritical or subcritical classification, an existence-only result, or a result that
also classifies stability and conjugacy. Those readings require different regularity, symmetry,
spectral, transversality, nondegeneracy, locality, and boundary assumptions. Choosing one from
memory would silently substitute a new target.

This intake freezes that ambiguity rather than inventing missing mathematics. The provisional root
vector is `[H5, M4, R4]`. `H5` records that the supplied phenomenon gloss is not yet a stable
truth-valued proposition; it does not say that standard pitchfork theorems are false or open. No
source-identical Lean target or proof reconstruction can be attached before a proposition is
selected.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 6.5, was inspected
as an authoritative discovery lead. It identifies the scalar family `x' = mu*x - x^3` as a
pitchfork example and records its fixed-point and stability behavior, but it does not state a
general pitchfork theorem. The repository does not cite that book or say whether this example,
another normal form, or a general symmetry-breaking theorem is intended. Nothing from it is
accepted as the root.

`IntakeProbe.lean` checks only pinned calculus, ODE, flow, and fixed-point interfaces adjacent to a
future encoding. It states no pitchfork theorem and receives no statement or proof credit. The
structured scope authority is `instance.json`, the resolution boundary is in `scope-map.md`, the
literal source crosswalk is in `source-statement-crosswalk.md`, and all six downstream phases remain
open in `task-dag.json`.

The lifecycle is `planned`. No canonical Lean expression, H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
