# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:712-717` supplies exactly the title `哈里斯-钱德拉定理`,
attribution to Harish-Chandra, year 1951, gloss `半单李群表示的特征标` ("characters of
representations of semisimple Lie groups"), importance "high," and status `已验证`. Git history
attributes all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
The record has no bibliography, theorem locator, formula, definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:2767-2792` repeats the gloss while leaving the formal system,
foundations, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Primary-source leads

The catalog year aligns with Harish-Chandra, *Representations of Semisimple Lie Groups: III.
Characters*, Proceedings of the National Academy of Sciences 37 (1951), no. 6, 366-369, DOI
`10.1073/pnas.37.6.366`. PubMed identifies the full subtitle, PMID `16578368`, and PMCID
`PMC1063374`; Crossref's title omits the subtitle. The bibliographic endpoints were inspected, but
the PMC open-access service reported `idIsNotOpenAccess`, so no complete statement or proof from
this paper is transcribed or credited. Its character-distribution construction is a plausible
root, but its identity explains only why the catalog says 1951, not which exact proposition the
gloss denotes.

Harish-Chandra, *The Characters of Semisimple Lie Groups*, Transactions of the American
Mathematical Society 83 (1956), no. 1, 98-163, DOI
`10.1090/S0002-9947-1956-0080875-7`, was inspected from the AMS scan on 2026-07-13.
Crossref confirms the bibliographic metadata. The observed PDF SHA-256 is
`168a818a20a2fba12051310e89610fbc2a5847f84ff8aa8c6648cb963f112277`.

The paper's introduction, printed page 98, starts with a quasi-simple irreducible representation
of a connected semisimple Lie group, defines its trace distribution from compactly supported
smooth functions and Haar measure, and announces analyticity on the regular set. Section 3,
printed pages 108-109, defines a larger quasi-regular set. Section 11, printed pages 144-145,
defines the paper's `quasi-simple` conditions and the distribution character. Theorem 6 on printed
page 145 states that this character coincides with an analytic function on the quasi-regular set.
The proof continues through Lemmas 34-40 and closes on printed page 154.

This is a strong primary-source lead, but not `H0`: the catalog does not cite it or select Theorem
6 rather than a result in the 1951 note; the paper relies on definitions and earlier
papers in its series; scan OCR is not an accepted transcription; correction history, modern
terminology and domain transport, lawful preservation, node-level proof crosswalk, and independent
review remain open. The paper also contains Theorems 7-8 and formula results, so title matching
alone does not identify the catalog's intended root.

## Clause crosswalk

| Catalog component | 1956 source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "semisimple Lie group" | connected semisimple Lie group `G`; real Lie algebra and its complexification | `LieGroup`, group/topological/manifold structures, `LieAlgebra.IsSemisimple` after an explicit group-to-algebra bridge | exact group model and semisimplicity bridge open |
| "representation" | Hilbert-space representation satisfying the three `quasi-simple` conditions on central/infinitesimal characters and K-types | `Representation` plus future continuous/unitary/admissible structures | algebraic API alone is too weak; representation class open |
| "character" | trace distribution of the integrated operator against compactly supported smooth test functions and Haar measure | future Lie-group test functions, integration, trace-class/summability, and distribution construction | no matching composite pinned API located |
| regular locus | quasi-regular set defined via centralizers and a cocompact normal abelian subgroup; contains regular elements | future adjoint action, centralizer, Cartan and regularity predicates | no selected encoding or checked equivalence |
| Theorem 6 conclusion | distribution character coincides with an analytic function on the quasi-regular set | distribution induced by an analytic function on an open submanifold | exact equality, analyticity, and manifold-distribution transport open |
| later/global variants | often phrased as local integrability plus analyticity on regular semisimple elements | `LocallyIntegrable` plus distribution equality and analytic restriction | plausible different root; not merged into Theorem 6 |
| `已验证` | untrusted inventory label | source review and kernel receipt required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib has `Representation`, the finite-dimensional algebraic
`Representation.character`, `LieAlgebra.IsSemisimple`, `LieGroup`,
`MeasureTheory.Measure.haarMeasure`, `LocallyIntegrable`, `TestFunction`, and `Distribution`.
They establish nearby vocabulary but the algebraic trace character is not the distribution
character of an infinite-dimensional
semisimple-Lie-group representation and no Harish-Chandra regularity theorem. The current
`Distribution` API is chart-domain infrastructure, not a ready global distribution on an
arbitrary Lie group.

A bounded search of repo-local Lean and pinned mathlib found no `HarishChandra`, character-
regularity, quasi-simple-representation, or quasi-regular-Lie-group terminal result. The
`THM-M-0063` local-Langlands file has an abstract `realizesHarishChandraCharacter` proposition
field and explicitly says its concrete API is missing; it is not proof evidence for this target.
These findings are intake discovery only, not a complete external anchor audit.

## Source gate

Before leaving `H1`, reviewers must inspect and preserve approved immutable editions of the
relevant 1951/1956 sources, choose an exact result, and transcribe and map every incorporated
definition, binder, hypothesis, conclusion and proof node. They must resolve the source-identity
and later-variant boundary, audit corrections and
dependent earlier papers, and independently approve fidelity to `THM-M-0097`. Only then may the
statement phase freeze minimal imports, an elaborated Lean expression and environment hashes,
checked alternate encodings, and required domain, binder, hypothesis, and boundary mutations.
