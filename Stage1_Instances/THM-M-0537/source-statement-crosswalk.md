# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names Samuel Eilenberg and Norman Steenrod, dates the item to
1945, and gives only the Chinese gloss `同调理论的公理化` ("axiomatization of homology theory").
That metadata establishes the topic but neither an exact proposition nor the conventions needed
for a Lean declaration. Its `已验证` label is explicitly untrusted under rev-5.6.

## Primary-source candidates

- Samuel Eilenberg and Norman E. Steenrod, "Axiomatic Approach to Homology Theory," *Proceedings
  of the National Academy of Sciences of the United States of America* 31 (1945), 117-120. This
  matches the repository authors and date. Exact axiom wording, theorem anchors, assumptions, and
  errata have not yet been inspected from a stable copy.
- Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology*, Princeton University
  Press (1952), especially the opening axiomatic development. This is a fuller primary monograph
  candidate, but the statement phase must record edition, chapter/theorem/page, definitions, and
  errata before using it for H0.

These are discovery anchors, not source acceptance. An independent review is required.

## Crosswalk

| Repository phrase | Intended source component | Required Lean surface | Intake status |
|---|---|---|---|
| "homology theory" | graded functorial invariants of topological pairs | category of pairs, graded object-valued functors, induced maps | included; categories open |
| "axiomatization" | homotopy, exactness, excision, and dimension laws | fields/laws with natural connecting morphisms | included; exact formulations open |
| Eilenberg/Steenrod | historical ordinary-homology framework | source-faithful namespace and declaration | authorship anchor only |
| 1945 | initial article rather than a modern paraphrase | immutable bibliographic/source revision | article identified; text not inspected |
| "verified" | unsupported source metadata status | no Lean proof credit | rejected as evidence |

## Statement-kind crosswalk

| Possible formal root | What it would establish | Eligibility at intake |
|---|---|---|
| `structure HomologyTheory` | an exact encoding of the axioms | definition artifact only, not a theorem closure |
| singular homology satisfies the structure | existence of a concrete model satisfying every axiom | plausible theorem root; source and API audit required |
| uniqueness/natural equivalence theorem | characterization of homology theories on a specified category | distinct stronger theorem; eligible only if source wording is selected |

The statement phase must select exactly one row as canonical or record a hard source-ambiguity
blocker. It must not broaden the short gloss by conjoining all three.
