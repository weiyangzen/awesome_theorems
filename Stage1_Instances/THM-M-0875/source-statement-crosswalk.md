# THM-M-0875 source-statement crosswalk

## Repository record

The complete catalog record is `Docs/researches/math_theorems.md:6411-6416`. All six uncited lines
entered in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The generated Stage0
projection at `Docs/Stage0_Blueprint.md:23873-23898` repeats the same gloss while leaving exact
definitions and premises, proof path, dependencies, equivalent statements, axioms, machine status,
and formal artifact links open.

| Catalog field | Exact received value | Intake interpretation |
|---|---|---|
| title | `Weisfeiler-Lehman算法` | algorithm-family label; spelling differs from the usual `Weisfeiler-Leman` |
| attribution | `Weisfeiler/Lehman` | metadata only; no cited work or identity-resolution evidence |
| time | `1968` | metadata only; no edition, publication, theorem, section, or page |
| statement | `图同构的启发式算法` | "a heuristic algorithm for graph isomorphism"; not truth-valued |
| importance | `高` | scheduling metadata, not a mathematical premise |
| formalization status | `已验证` | explicitly untrusted in the rev-5.6 manifest; supplies no H/M/R credit |

The record contains no graph definition, algorithm variant, dimension, initialization, refinement
operator, stopping rule, output, cost model, ordered binders, hypotheses, conclusion, proof, source,
correction, or reviewer. There is therefore no exact human statement to transcribe into Lean.

## Historical source-family lead, not H0

A bounded observation on 2026-07-13 inspected the University of West Bohemia's WL2018 materials:

- B. Yu. Weisfeiler and A. A. Leman, *The Reduction of a Graph to Canonical Form and the Algebra
  Which Appears Therein*, English translation by Grigory Ryabov of the original Russian paper;
- the original scan itself prints the Russian title, authors B. Yu. Weisfeiler and A. A. Leman,
  `NTI`, Series 2, no. 9 (1968), on pages 12-16; the expanded journal-title transliteration still
  requires authoritative normalization;
- the 11-page translation at
  `https://www.iti.zcu.cz/wl2018/pdf/wl_paper_translation.pdf`, observed SHA-256
  `4dd47b0568910d2ccb787b192a870aeeb9a2b7802dff54d92486d2f3181a55af`;
- the 5-page original scan at `https://www.iti.zcu.cz/wl2018/pdf/wl_paper_orig.pdf`, observed
  SHA-256 `3bb783bde4360767e73e0a349dae88eb24d1904808609fd3c0ff566b113ef93c`;
- the conference preface at `https://www.iti.zcu.cz/wl2018/wlpaper.html`, observed SHA-256
  `ed622e1e5d65c14d13643e9a22f37e23821bb82772a408b79ead36b2afacd4a6`.

The translation's abstract and Sections 1-3 describe a canonical-form procedure for finite
multigraphs, vertex-class refinement, ordered-arc coloring, coherent algebra, and further
individualization. This is richer and materially different from a single modern 1-WL heuristic
claim. The preface says the original conjectures that the algorithm solves graph isomorphism were
incorrect and distinguishes later `k`-tuple variants. That correction is decisive negative
boundary evidence against inventing a generic completeness theorem.

These materials are discovery leads only. The catalog cites none of them; journal-title and title
transliterations still vary across secondary bibliographies, and the exact incorporated
definitions/result/proof boundary, translation fidelity, full correction history, and independent
review are not admitted. They therefore do not supply H0 or select the target proposition.

## Source-to-statement decision

| Required statement element | Repository support | Intake decision |
|---|---|---|
| canonical claim | absent | null; blocked pending source selection |
| domains and universes | absent | open |
| ordered binders | absent | empty, not inferred |
| hypotheses | absent | empty, not inferred |
| conclusion | absent | open |
| alternate encodings | absent | none credited |
| degenerate cases | absent | none excluded |
| source theorem/page/proof | absent | H5; primary-source crosswalk and review open |
| corrections/errata | absent | the 2018 preface is a discovery warning, not a completed audit |

Choosing isomorphism invariance, sound rejection, stabilization, complexity, a completeness theorem
for a special class, a counterexample, or the full historical canonical-form procedure would
change the proposition. The statement phase must select one exact, corrected source result and
obtain independent source and scope review before elaboration.

## Formal discovery boundary

`IntakeProbe.lean` checks pinned mathlib's `SimpleGraph`, graph isomorphism, neighborhood,
finite-neighbor, and degree interfaces. These are substrate only. A bounded case-insensitive search
of repo-local Lean and pinned mathlib for Weisfeiler/Leman spellings and color-refinement terms found
no source-identical implementation or theorem. This is not the exhaustive downstream anchor audit
or a global absence claim.

The source state is provisionally `H5`; the machine state is `M4`; readable state is `R4`. H5
classifies the received nonpropositional gloss, not the validity of properly stated
Weisfeiler-Leman theorems. No exact target, proof credit, audit completion, theorem completion, or
master acceptance is claimed.
