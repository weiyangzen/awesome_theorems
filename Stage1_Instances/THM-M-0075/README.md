# THM-M-0075 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Artin
theorem. The repository gives the Chinese gloss `关于诱导特征标的线性无关性` ("about the linear
independence of induced characters"), attributes it to Emil Artin in 1931, and labels it verified.
Under rev-5.6 that label is untrusted inventory metadata, not an exact proposition, a source audit,
or proof evidence.

The wording does not fix a group, finiteness assumptions, subgroups, characters, induction map,
coefficient ring, indexing family, or the precise independence relation. More seriously, the
inspected standard modern result called Artin's theorem is an induction or spanning theorem, not a
linear-independence theorem. Serre's Theorem 17 says that a family of subgroups covering a finite
group up to conjugacy is equivalent to finite cokernel of the sum of induction maps on character
rings. Its cyclic-subgroup corollary expresses every character as a rational linear combination of
induced characters. Intake does not silently replace "linear independence" by this materially
different claim.

The historical Artin paper associated with the standard induction result was identified by DOI and
bibliographic metadata, but no exact original proposition, definition chain, or errata history was
accepted. The Serre statement is a strong source lead and exposes the catalog mismatch, but it is
not evidence that the catalog intended that statement. This keeps the human-source state at `H1`.

Pinned mathlib supplies finite-group representation characters and representation induction, and it
also supplies Dedekind's linear independence of monoid homomorphisms. `IntakeProbe.lean`
authenticates these adjacent interfaces. None is credited as the requested theorem: the induction
API does not provide Artin induction on a virtual-character ring, and Dedekind independence is
about distinct multiplicative homomorphisms, not induced representation characters.

The provisional root vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority,
and `task-dag.json` keeps all six downstream phases open. No canonical proposition, exact Lean
target, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
