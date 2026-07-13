# THM-M-0477 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0477`, the catalog entry
named `中国剩余定理` (Chinese remainder theorem). The repository supplies only the gloss
`同余方程组的解法` (a method or solution for systems of congruences), attributes it broadly to
ancient Chinese mathematicians around the third century, and labels it `已验证`. Under rev-5.6,
that label is untrusted metadata rather than human-source or Lean proof evidence.

The title identifies the classical Chinese-remainder theorem family, but the gloss is not a
binder-complete proposition. It does not choose the historical Sunzi residue puzzle or a later
general theorem, natural or integer congruences, finite or potentially infinite systems, two
moduli or an arbitrary indexed family, pairwise-coprime hypotheses or the more general
gcd-compatibility condition, existence alone or uniqueness modulo a product/lcm, or a canonical
bounded representative. It also supplies no source edition, theorem/page locator, incorporated
definitions, proof boundary, translation, corrections, errata review, or independent source
review. The canonical mathematical statement and canonical Lean expression therefore remain null
at intake.

Pinned mathlib contains several direct exact-topic interfaces. `Nat.chineseRemainder'` handles two
compatible congruences, `Nat.chineseRemainder` specializes to coprime moduli,
`Nat.chineseRemainderOfList` and `Nat.chineseRemainderOfFinset` construct finite-family solutions,
and `ZMod.chineseRemainder` packages a two-modulus result as a ring equivalence. `IntakeProbe.lean`
elaborates these interfaces and reports representative axiom dependencies. Their materially
different scopes confirm that a declaration name cannot select the catalog root. They are
candidate-level `M3` observations only; because none is mapped to an exact root, the proposed root
machine status remains `M4`.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received catalog gloss as not yet
a stable truth-valued proposition; it does not refute the classical Chinese remainder theorem.
`M4` records that no checked interface has been mapped to the exact root, despite the direct pinned
candidate observations. No readable reconstruction can attach to an exact root yet. All six
downstream phases remain open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
