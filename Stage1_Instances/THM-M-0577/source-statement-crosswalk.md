# Source-statement crosswalk

## Available repository records

`Docs/researches/math_theorems.md` gives the label `伍德沃德定理`, the period `20世纪`, the
attribution `众多数学家`, and the phrase `配边理论中的结果`. `Docs/Stage0_Blueprint.md` repeats
those fields but supplies no definition, premise, conclusion, bibliography, or artifact. The
rev-5.6 manifest preserves the label, category, and untrusted status while uniformly resetting the
target to `L0 / rework_required`.

The records are not independent sources and their `已验证` value is expressly untrusted. A scoped
repository search found no theorem-specific publication locator or Lean declaration. This is a
truthful negative intake result, not a comprehensive source or anchor audit.

## Primary-source status

No primary source can be named from the available metadata without speculation. In particular,
"Woodward theorem" plus "cobordism theory" is not a sufficient bibliographic key. The statement
phase must perform identity resolution before treating any author or paper as a candidate, and
must retain rejected candidates with the reason they do not match the repository description.

## Crosswalk

| Repository phrase | Information actually supported | Required source fact | Required Lean component | Intake status |
|---|---|---|---|---|
| `伍德沃德定理` / "Woodward theorem" | a surname-based label | full author identity and documented theorem attribution | none until identity is fixed | unresolved |
| "twentieth century" | coarse date range | exact publication and theorem date | no proof component | unresolved |
| "many mathematicians" | non-specific attribution | author(s), origin, and proof provenance | no proof component | unresolved |
| "result in cobordism theory" | broad subject tag | exact cobordism category, objects, hypotheses, and conclusion | concrete cobordism definitions and target type | unresolved |
| topology / algebraic topology | inventory classification | source-confirmed mathematical domain | imports selected from the exact target | provisional only |
| `已验证` | inventory metadata | inspectable human and machine evidence | checked declaration and terminal body | untrusted; no credit |

## Non-substitution boundary

The repository evidence does not license choosing Thom cobordism theory (`THM-M-0563`), generic
cobordism theory (`THM-M-0603`), or any familiar named cobordism theorem. Similarity of topic is
not a source-statement transport. A valid crosswalk must quote or transcribe the recovered theorem
row by row, including all definitions, assumptions, boundary cases, and the exact conclusion, and
then map those rows to one elaborated Lean expression.

Before `H0`, an independent reviewer must verify the stable source, theorem/page, definitions,
assumptions, proof boundary, corrections, and errata. Before machine credit, the separate anchor
audit must search pinned mathlib and credible external Lean 4 projects at immutable revisions and
record exact declaration types, imports, terminal bodies, and trust boundaries.
