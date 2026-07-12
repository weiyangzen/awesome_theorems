# THM-M-0777 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Godel's first incompleteness theorem.
The repository supplies only the Chinese gloss "a consistent formal system containing arithmetic is
incomplete", an attribution to Kurt Godel, the year 1931, and an untrusted `已验证` status.

That gloss does not determine a theorem. It omits effective axiomatizability, the object language and
proof calculus, the required arithmetic strength, the exact consistency condition, and whether the
conclusion is syntactic undecidability, unprovability of a constructed Godel sentence, or another
form of incompleteness. The original Godel formulation and later Rosser-strengthened formulation
must not be silently conflated: their consistency hypotheses differ.

The intake freezes this scope ambiguity and the downstream work needed to resolve it. The root is
`[H1, M4, R4]`: the classical theorem has a known published proof tradition, but the exact target
and source-to-statement mapping have not been audited. A pinned Lean probe confirms only mathlib's
Godel beta-function coding lemma. Mathlib describes that file as a step toward an eventual first
incompleteness proof, so it provides no proof credit for this target. Exact validation is recorded
in `validation.md`.
