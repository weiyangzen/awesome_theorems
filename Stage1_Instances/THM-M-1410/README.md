# THM-M-1410 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Rokhlin塔`
(`Rokhlin tower`). The catalog supplies Vladimir Rokhlin, the year 1948, and only the gloss
`遍历理论的工具` (`an ergodic-theory tool`). It does not state a proposition. Its `已验证`
(`verified`) label is untrusted metadata under rev-5.6.

The classical Rokhlin lemma is the leading discovery candidate. An inspected secondary source
states a unit-interval, Lebesgue-measure version for an aperiodic invertible measure-preserving
transformation; another inspected source describes a standard-measure-space version for an
aperiodic nonsingular automorphism. Those are not definitionally interchangeable. The catalog does
not choose between them, a primary theorem passage has not been accepted, and selecting either one
would silently add missing mathematics.

The intake therefore freezes the ambiguity rather than a convenient theorem. `scope-map.md` lists
the decisions required before a statement can be approved, and `source-statement-crosswalk.md`
separates the literal repository record, bibliographic candidates, and pinned Lean ingredients.
`IntakeProbe.lean` checks only adjacent APIs for measure-preserving maps, periodic points, standard
Borel spaces, probability measures, atomlessness, and almost-everywhere disjointness. It is not a
Rokhlin statement or proof.

The provisional root vector is `[H5, M4, R4]`, pending master review. `H5` is scoped only to the
literal catalog wording, which is not a stable proposition; it does not say that any classical
Rokhlin lemma is false. Because `H5` is terminal, the next phase is a target-correction gate: it must
select a source-approved proposition and then recompute `H` before ordinary proof work. `M4` records
that no usable formal artifact for an approved root has been located, despite the checked adjacent
infrastructure. Lifecycle remains `planned`, accepted state is empty, and all downstream tasks are
open. No source fidelity, exact Lean target, proof, audit completion, or theorem completion is
claimed.
