# THM-M-0815 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0815`, Hall's marriage
theorem. The repository supplies Philip Hall, 1935, and only the gloss "the condition for the
existence of a perfect matching in a bipartite graph." Its `已验证` label is untrusted metadata and
provides no source, statement, or proof credit under rev-5.6.

The original article is bibliographically identified as P. Hall, *On Representatives of Subsets*,
JLMS s1-10 (1935), 26-30, DOI `10.1112/jlms/s1-10.37.26`. The primary text was not obtained, so no
exact theorem/page, incorporated-definition, proof, or errata audit is claimed. An inspected
secondary formalization paper gives the standard finite indexed-family, relation, and one-side
bipartite-matching formulations. It also exposes why the catalog gloss is ambiguous: Hall's
standard graph theorem saturates one bipartition, whereas a perfect matching saturates every
vertex and needs balance or a correspondingly stronger condition.

Pinned mathlib contains checked interfaces for both readings. `IntakeProbe.lean` authenticates the
indexed-family equivalences, relation equivalences, one-side graph matching theorem, and a
graph-wide perfect-matching sufficient theorem. They are candidates only. Intake does not choose
between finite and compactness-generalized index scope, one-side saturation and graph-wide
perfection, or the exact graph coverage and finiteness premises.

The provisional vector is `[H1, M3, R4]`: the historical publication is bibliographically
identified and an inspected secondary source reports a proof, but the primary text, exact
catalog-to-source mapping, and independent review remain open; direct pinned formal interfaces
exist without a frozen root or proof credit; and no accepted readable reconstruction exists.
`instance.json` is the structured scope authority, and `task-dag.json` keeps all six downstream
phases open.

No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
