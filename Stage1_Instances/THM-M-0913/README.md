# THM-M-0913 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `容斥原理`
(inclusion-exclusion principle). The catalog supplies only the gloss `并集元素个数的计算公式`
(a formula for the number of elements in a union), the attribution "many mathematicians," the
period "19th century," and an untrusted `已验证` label. That identifies the inclusion-exclusion
family, but it does not select one exact proposition.

The wording leaves open two sets versus an arbitrary finite family, finite sets versus finite
measures, the index and set encodings, the coefficient ring and subtraction convention, the empty
family case, and whether complement or weighted-sum forms belong to the root. Intake does not
silently replace this family with the convenient pinned `Finset.inclusion_exclusion_card_biUnion`
declaration, although that declaration is a strong downstream candidate.

The provisional catalog-target vector is `[H5, M3, R4]`. `H5` classifies the received gloss as not
yet one stable proposition; it does not say that source-selected inclusion-exclusion theorems are
false or open. `M3` records that pinned mathlib exposes an exact finite-family cardinality
interface, while its fidelity to an approved source proposition remains unestablished. The Lean
probe authenticates candidate interface names and types only; it adds no theorem or proof body.

`instance.json` is the structured scope authority. `scope-map.md` freezes proposition-changing
choices and exclusions, `source-statement-crosswalk.md` records provenance and unresolved mapping,
and `task-dag.json` leaves all six downstream phases open. This is a self-tested worker proposal
only. No canonical statement, H0, M0, R0, accepted state, audit completion, theorem completion, or
master acceptance is claimed.
