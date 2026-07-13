# Source-statement crosswalk

## Repository Sources

`Docs/researches/math_theorems.md:6236` records the Chinese title `巨分量定理`; the following
five lines give only Erdos/Renyi, 1960, the gloss `随机图中巨分量的出现` (the appearance of a
giant component in a random graph), importance "high," and status `已验证`. Those lines entered
the raw repository source pool in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the source-pool record is not a primary mathematical
citation. `Docs/Stage0_Blueprint.md:23198` repeats the metadata while explicitly leaving exact
definitions and premises, proof route, dependencies, equivalent statements, axioms, and machine
artifact open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

No repository record identifies a theorem, publication, edition, page, graph law, parameter
regime, limiting mode, component-size formula, uniqueness conclusion, proof boundary, or erratum.
The identical gloss under `THM-M-1114` is duplicate metadata, not a statement-selection rule and
not evidence transferable to this target.

## Primary-Source Candidate

Paul Erdos and Alfred Renyi, "On the evolution of random graphs," *Publications of the
Mathematical Institute of the Hungarian Academy of Sciences* 5 (1960), 17-61, is a historical
primary-paper candidate consistent with the repository attribution and year.

This bibliographic record is a discovery anchor only. The repository does not identify the exact
numbered result, and this intake did not freeze an immutable complete edition, pinpoint a theorem
and its referenced definitions, audit assumptions or errata, or obtain independent review. It
therefore gives no `H0` credit and does not select a canonical proposition. A modern `G(n,c/n)`
formulation may help disambiguate notation, but cannot silently replace the historical fixed-edge
model or a stronger/weaker result.

## Crosswalk

| Repository or candidate phrase | Mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| "random graph" | a probability law on finite labelled simple graphs | an explicit `G(n,m)`, `G(n,p)`, or graph-process law | model not selected |
| "component" | an equivalence class under graph reachability | `SimpleGraph.ConnectedComponent`, its support, and source-equivalent cardinality conventions | pinned definitions probed; encoding not selected |
| "giant" | component size macroscopic in `n` | exact existential/largest-component predicate, linear bound or density, rounding, and tie rules | informal role only; quantitative meaning absent |
| "appearance" | threshold, phase transition, or process emergence | exact parameter regime, quantifier order, asymptotic filter, and probability conclusion | unresolved |
| Erdos/Renyi, 1960 | historical source family | immutable edition, theorem/definition pinpoint, assumptions, errata, and reviewed row mapping | candidate paper only |
| `已验证` | untrusted inventory label | accepted human review and kernel receipts | explicitly rejected as proof credit |
| duplicate `THM-M-1114` | separately scheduled catalog identity with the same gloss | independent dossier, receipts, and master state | no evidence or status transfer |

## Lean Discovery Boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs` defines the independent-edge measure
`SimpleGraph.binomialRandom`. Its documentation expressly says that the usual Erdos-Renyi name is
historically inaccurate because Erdos and Renyi introduced a related but different model. Module
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Finite` exposes finite connected-component
vocabulary and imports the underlying support definition.

`IntakeProbe.lean` verifies these declarations elaborate together. A bounded pinned-mathlib search
found the binomial-random-graph definitions but no giant-component, largest-component, or
random-component theorem. This is not a complete immutable anchor audit and says nothing about
unsearched external projects. The API probe receives no statement, source, or proof credit.

## Unblocking Crosswalk

Before statement or `H0` credit, an accountable reviewer must preserve and hash an immutable
complete primary edition, pinpoint the exact proposition and referenced definitions, transcribe
all ordered binders, hypotheses, parameter scalings, probability limits, size and uniqueness
claims, and exceptional cases, map each component to Lean, check corrections and errata, and
explain why that proposition rather than another giant-component variant is the target of
`THM-M-0850`. Any translation between historical `G(n,m)` and binomial `G(n,p)` must be an explicit
mathematical bridge, not a naming convention.
