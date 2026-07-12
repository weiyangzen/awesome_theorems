# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `伍丁基数`, attributes it to W. Hugh
Woodin, gives the year 1984, and states only `伍丁基数的性质` ("properties of Woodin cardinals").
Stage0 repeats that gloss and explicitly leaves the exact definition, assumptions, proof route,
dependencies, and evidence type open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`. No theorem, hypotheses, conclusion, edition, page, proof source, errata,
or formal artifact is supplied.

## Candidate source work

Foundational papers and authoritative set-theory monographs are candidate locators, but intake has
not accepted an edition or passage. The source audit must locate a passage that states the intended
definition and exact theorem, record edition, theorem/definition number and page, assumptions,
foundation, proof boundary, and errata, then obtain independent review. Attribution and date in the
inventory do not establish statement identity or `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "cardinal" | an infinite initial ordinal/cardinal in an ambient set theory | `Cardinal`, `Ordinal`, or a ZFC-set encoding | pinned APIs probed; representation open |
| "Woodin" | function/embedding or subset/strongness characterization | rank hierarchy, elementary embeddings, critical point, closure/strongness or extenders | definition absent; no substitute admitted |
| "properties" | equivalence, reflection, consequence, existence, or consistency claim | one concrete proposition with all hypotheses | absent from source record |
| `1984`, attribution | historical metadata | source identity and passage | insufficient for statement freeze |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.SetTheory.Cardinal.Regular` and `Mathlib.SetTheory.ZFC.Cardinal`. It checks
cardinal/ordinal types, regular and inaccessible-cardinal predicates, ZFC sets and ZFC-set
cardinality. These are nearby encoding ingredients only. A bounded case-insensitive search found no
`woodin` occurrence in pinned mathlib. This is not the later immutable anchor audit and makes no
claim about all external Lean projects.
