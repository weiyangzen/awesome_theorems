# THM-M-0097 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Harish-Chandra theorem. The repository gives only the gloss "characters of representations of
semisimple Lie groups," attributes it to Harish-Chandra in 1951, and labels it verified. Under
rev-5.6 that label is untrusted inventory metadata, not a source audit, an exact proposition, or
Lean proof evidence.

The gloss does not identify one theorem. Plausible roots include the trace construction of a
distribution character, regularity of that character, analyticity on the regular or quasi-regular
set, a local-integrability theorem, and explicit character-formula results. These differ in their
group and representation hypotheses,
the definition of character, the regular locus, and the conclusion. Intake does not silently
choose among them.

The catalog year matches Harish-Chandra's *Representations of Semisimple Lie Groups: III.
Characters*, PNAS 37 (1951), 366-369; its bibliographic identity was confirmed, but full text was
not available from the inspected lawful endpoint. Harish-Chandra's later paper *The Characters of
Semisimple Lie Groups*, Transactions of the AMS 83 (1956), 98-163, was inspected as a
primary-source lead. Its Theorem 6 states that the distribution
character of a quasi-simple representation of a connected semisimple Lie group coincides with an
analytic function on the paper's quasi-regular set. The catalog neither cites this paper nor
selects either source or Theorem 6. Definition-chain mapping, corrections,
modern terminology, preservation, and independent review remain open. The source is therefore a
lead, not `H0` evidence.

Pinned mathlib provides algebraic representations, semisimple Lie algebras, manifold Lie groups,
Haar measures, local integrability, and distributions on open subsets of finite-dimensional
normed spaces. `IntakeProbe.lean` authenticates those interfaces. A bounded search found no
Harish-Chandra character regularity or formula declaration. Adjacent APIs and abstract fields in
an unrelated local-Langlands artifact are not substitutes for this target.

The provisional vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority, and
`task-dag.json` keeps all six downstream phases open. No canonical proposition, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
