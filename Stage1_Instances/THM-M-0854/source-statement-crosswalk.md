# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:6264-6269` records `Ore定理`, Oystein Ore, 1960, the gloss
`Hamilton圈存在的度和条件`, high importance, and `已验证`. The six fields originate at repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:23306-23331`
repeats them while leaving the exact definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact link open. Rev-5.6 retains `已验证` only as
`source_status_untrusted`.

The neighboring Dirac, Chvatal-Erdos, and random-graph Hamiltonicity entries delimit the intended
subject but cannot supply missing assumptions or transfer evidence.

## Primary-source lead

Crossref bibliographic metadata identify Oystein Ore, *Note on Hamilton Circuits*, *The American
Mathematical Monthly* 67(1) (January 1960), p. 55, DOI `10.2307/2308928`. This exactly matches the
catalog author, year, and subject. The publisher page was access-controlled in this worker run, so
the article statement and proof were not admitted or transcribed.

This is an `H1` lead, not `H0`: there is no preserved immutable primary text, exact proposition or
definition locator, assumption/proof-node mapping, correction and errata audit, or independent
review. A versioned modern secondary source, Pan, Su, and Kao (arXiv `1805.05149v1`), states in
Theorem 1 on PDF page 2 that a simple graph of order at least three is Hamiltonian when every
nonadjacent pair has degree sum at least the order. The inspected PDF has SHA-256
`60e37541a790f905531f8fd9ff5f31deab3d6a6bc0ba7a97a56836683a66555b`.
This is precise secondary corroboration, not primary-source authority, a proof crosswalk, or `H0`.

## Crosswalk

| Source phrase or field | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Ore theorem / 1960 | classical finite-graph Hamiltonicity criterion | one source-mapped root, not another Ore theorem from algebra | family identified; exact source text open |
| degree-sum condition | `deg(u) + deg(v) >= |V|` | `G.degree u + G.degree v >= Fintype.card V` | candidate only |
| nonadjacent vertices | distinct `u, v` with no edge | `u != v` and `not G.Adj u v`, or a checked equivalent pair encoding | distinctness omitted by catalog; material |
| finite graph order | finite simple undirected `G` with `3 <= |V|` | `[Fintype V]`, `G : SimpleGraph V`, cardinality lower bound | candidate convention; source review open |
| Hamilton circuit | spanning simple cycle | `SimpleGraph.IsHamiltonian` plus a source-convention transport | pinned predicate probed; transport open |
| `已验证` | inventory metadata | no proposition and no kernel evidence | explicitly rejected as credit |

## Pinned Lean substrate

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Finite` supplies `SimpleGraph.degree`, and
`Mathlib.Combinatorics.SimpleGraph.Hamiltonian` supplies `SimpleGraph.IsHamiltonian` and boundary
lemmas including `not_isHamiltonian_of_card_eq_two`. A bounded source search found no Ore or
Bondy-Chvatal graph theorem in the pinned `Mathlib` tree. `IntakeProbe.lean` checks only these APIs
and states no target theorem.

## External formal lead, not credited

The pre-existing mathlib Git object database contains remote ref
`refs/remotes/origin/meow-sister/BondyChvatal_PR` at immutable commit
`c83689ab8f1abfba1f646e65dc8b131fd256b73f` (tree
`1f6492c5aeafeec2cfe969d8afd0aad15e2bee81`). Its
`Mathlib/Combinatorics/SimpleGraph/BondyChvatal.lean` blob
`fe5f079d24abc6f3ceece4f9b67240022c06827a` has SHA-256
`624699fead58ca9ef346d7ed60bb68dc534508ac1ab66985e8610d5f2e41894d`.
Lines 398-411 contain a source-visible `SimpleGraph.ore_theorem` with a three-vertex lower bound,
degree-sum premise, and Hamiltonian conclusion.

This branch is not the pinned dependency: its merge base with the pin is
`3bebc671e9c9c1b535ad7ce3a6f96a2263835424`, while the pin and branch are respectively 16,380
and 79 commits beyond that base. It targets Lean `v4.12.0-rc1`; neither that toolchain nor branch
`.olean` artifacts are available locally. The source scan found no proof hole or bodyless axiom in
the candidate file and its three direct imports, but no kernel or CI receipt was reproduced.
The candidate is therefore an unvalidated external source lead only: no M1, M0-P, or root proof
credit is assigned. Also, its premise as printed quantifies only `not G.Adj u v`, so exact identity
with the standard distinct-pair source statement needs particular scrutiny.

## Unblocking criteria

Before statement acceptance or `H0`, preserve a lawful immutable primary edition, pinpoint and
transcribe the result and incorporated definitions, map all domains, binders, hypotheses,
conclusion, and boundary cases, inspect corrections or errata, and obtain independent review.
Before any machine credit, freeze and mutation-test the exact Lean root, then audit the external
candidate's statement match, immutable build evidence, terminal body, imports, axioms, and
provenance or port it into the pinned closure and re-elaborate it.
