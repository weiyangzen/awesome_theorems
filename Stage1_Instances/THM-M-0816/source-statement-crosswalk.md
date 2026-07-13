# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5998-6003` supplies the name Turán's theorem, attribution Pál
Turán, year 1941, and the gloss `不含完全子图的图的最大边数` (the maximum number of edges in a graph
containing no complete subgraph). Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no graph model, forbidden clique
order, quantifiers, exact bound, equality convention, exceptional cases, proof locator, or formal
declaration.

`Docs/Stage0_Blueprint.md:22280-22305` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Historical source lead

The official REAL-J OAI and EPrints metadata for archive record `7297` identifies *Matematikai és
Fizikai Lapok*, volume 48 (1941), published by the Eötvös Loránd Mathematical and Physical Society.
Its contents include Pál Turán, "Egy gráfelméleti szélsőérték feladatról" ("On an extremal problem
in graph theory"). The immutable metadata observed during intake reports the public volume scan as
320,878,611 bytes with MD5 `ce19dc2521b25d59df7c793146b70c56` and modification time
`2016-08-24 07:35:16`.

That archive metadata authenticates a plausible 1941 primary-source location and title, but the
article's printed pages, exact theorem, assumptions, proof transitions, and corrections were not
successfully extracted and reviewed during intake. Common bibliographic references place the
article at pages 436-452, but that pagination is deliberately not accepted as source evidence here.
No independent reviewer is assigned. This is a named primary-source lead supporting `H1`, not the
pinpoint statement/assumption/proof crosswalk required for `H0`.

## Component crosswalk

| Catalog/source component | Unresolved source meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| graph | presumably a finite simple undirected graph | `G : SimpleGraph V`, `[Fintype V]`, decidable adjacency | strong family match; exact source domain open |
| complete subgraph | order is omitted | `G.CliqueFree (r + 1)` | likely parameterized match; binder and indexing convention open |
| maximum edges | could mean an upper bound or the exact extremal value | `CliqueFree.card_edgeFinset_le` and `extremalNumber_top` | both plausible; root selection open |
| extremal construction | absent from the gloss | `turanGraph n r`, a balanced complete multipartite graph | canonical modern candidate, not yet source-mapped |
| equality case | absent from the gloss | `isTuranMaximal_iff_nonempty_iso_turanGraph` | materially stronger candidate; no automatic root credit |
| exact arithmetic | absent from the gloss | `card_edgeFinset_turanGraph` uses quotient/remainder arithmetic | formula and boundary conventions require review |
| `已验证` | untrusted catalog status | no proof object or accepted receipt | no H or M credit |

## Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the module
`Mathlib.Combinatorics.SimpleGraph.Extremal.Turan` documents Turán's theorem as saying that the
`(r + 1)`-clique-free graph on `n` vertices with the most edges is the complete `r`-partite graph
with part sizes as equal as possible. The API includes, schematically:

```text
isTuranMaximal_iff_nonempty_iso_turanGraph (hr : 0 < r) :
  G.IsTuranMaximal r <-> Nonempty (G ≃g turanGraph (Fintype.card V) r)

CliqueFree.card_edgeFinset_le (cf : G.CliqueFree (r + 1)) :
  #G.edgeFinset <= #(turanGraph (Fintype.card V) r).edgeFinset
```

The actual upper-bound declaration unfolds the right side to an exact quotient/remainder formula;
the schematic second line above records its mathematical role, not a frozen Lean expression.
`IntakeProbe.lean` elaborates the real declarations and supporting definitions against the pinned
environment. That establishes a usable exact-family formal candidate and justifies `M3` discovery
status only. It does not establish canonical statement identity, minimal imports, checked
transports, proof-body provenance, axiom policy, placeholder freedom, or trust closure.

Before leaving H1, accountable reviewers must inspect an immutable copy of the article, identify
the exact proposition and proof boundary, map every parameter, hypothesis, construction, equality
condition, and exceptional case, and audit corrections or errata. Before machine credit, the
statement phase must select that claim, freeze and mutation-test one elaborated Lean target, and
compile every credited alternate-form transport.

