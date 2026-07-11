# Source-statement crosswalk

## Repository source inspected

`Docs/researches/math_theorems.md` lines 1068-1073 gives: label `川又维数定理`, proposer Eiji
Kawamata, year 1985, statement gloss `代数簇的极小模型`, importance high, and status `已验证`.
`Docs/Stage0_Blueprint.md` repeats the gloss without a citation. Neither location provides a title,
edition, theorem number, page, hypotheses, or conclusion. The manifest deliberately classifies the
status label as `source_status_untrusted`.

## Crosswalk

| Repository datum | What it establishes | What remains open |
|---|---|---|
| `川又维数定理` | a discovery label associated with Kawamata | standard English/Japanese name and exact result |
| Eiji Kawamata, 1985 | author/year search keys | publication, edition, theorem/page, errata |
| `代数簇的极小模型` | broad minimal-model topic | domains, hypotheses, binders, and conclusion |
| `已验证` | historical metadata only | human-source fidelity and all machine evidence |

## Primary-source gate

No primary source is cited by the repository, and intake did not invent one. Statement work must
locate and inspect the 1985 source meant by the catalog, demonstrate that its theorem is actually
the label intended here, and record publication metadata, theorem/page, assumptions, definitions,
and known errata. If the year or label instead conflates multiple Kawamata results, the catalog
owner must disambiguate it before an exact target can truthfully be frozen.

After identification, every source hypothesis and conclusion must receive a row mapping it to a
concrete Lean binder or expression. Independent source review is still required for H0.
