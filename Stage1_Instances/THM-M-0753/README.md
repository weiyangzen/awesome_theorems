# THM-M-0753 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the recursion-theory catalog item
`跳跃反演定理` (jump inversion theorem). The repository supplies only the gloss `跳跃算子的像`
("the image of the jump operator"), a twentieth-century date, and an untrusted `已验证` label. It
does not supply a formula, attribution, primary source, or the conventions needed to identify one
of the several results called jump inversion.

The standard all-Turing-degree candidate is the Friedberg jump inversion shape: every Turing degree
above the jump of the computable degree is the jump of some degree. That wording is recorded only as
a candidate family. The catalog does not say whether it intends this result, a relativized or
iterated version, inversion inside the computably enumerable degrees, or an inversion theorem for a
different reducibility or degree structure. Selecting one would invent missing mathematics.

Pinned mathlib's `Mathlib.Computability.TuringDegree` provides Turing reducibility, equivalence,
degrees, and their partial order, but the inspected source contains no Turing-jump definition or
jump-inversion declaration. `IntakeProbe.lean` checks that adjacent substrate only. It declares no
canonical target and supplies no proof or formal-anchor credit.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: a stable classical theorem family and a strong secondary statement lead
are known, but exact source identity and all premise/conclusion mapping remain open; no exact Lean
target exists; and no reviewed reconstruction can attach to an unfrozen root. All six downstream
tasks remain open. Neither audit completion nor theorem completion is claimed.
