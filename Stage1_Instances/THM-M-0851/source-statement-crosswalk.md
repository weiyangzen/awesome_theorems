# THM-M-0851 source-statement crosswalk

## Repository Sources

`Docs/researches/math_theorems.md:6243-6248` records the title `连通性阈值`, Erdos/Renyi, 1959,
the gloss `随机图连通的阈值`, high importance, and status `已验证`. The same six-line record occurs
at lines 8164-8169 in another catalog category. `Docs/Stage0_Blueprint.md:23225-23250` retains the
first record as `THM-M-0851` while explicitly leaving exact definitions and premises, proof route,
equivalent statements, axioms, and machine artifacts open. The rev-5.6 manifest preserves the
status only as `source_status_untrusted`.

No repository record identifies a theorem number, page, graph law, threshold formula, asymptotic
quantifiers, proof boundary, correction, or erratum. The neighboring giant-component, phase-
transition, and Hamiltonicity entries delimit the topic but cannot supply missing mathematics.

## Primary-Source Candidate

Paul Erdos and Alfred Renyi, *On Random Graphs I*, **Publicationes Mathematicae Debrecen** 6
(1959), 290-297, is a strong source-family candidate matching the catalog authors and year. A
candidate scan is available from the Renyi Institute Erdos archive as `1959-11.pdf`.

The inspected scan introduces a uniformly selected labelled graph with `n` possible vertices and
`N` edges, calls it completely connected when it has no isolated vertices and is connected in the
ordinary sense, and announces four asymptotic questions. For fixed real `c`, equation (1) sets
`N_c = floor((n * log n) / 2 + c * n)`. Theorem 1 on page 291 states that the probability of
complete connectivity at `N_c` tends to `exp(-exp(-2 * c))`. Theorem 4 instead concerns the number
of edges required in a successive-edge process to become connected. These are inequivalent
candidate roots.

This record is discovery evidence only. The repository does not cite the paper; the archive scan is
not vendored or content-bound in this dossier; no complete incorporated-definition, assumption,
proof-page, dependency, correction/errata, or independent-review map is frozen. It supports `H1`,
not `H0`, and does not select Theorem 1, Theorem 4, or any modern reformulation as the root.

## Crosswalk

| Source phrase or candidate surface | Mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| `随机图` / random graph | probability law on labelled finite simple graphs | explicit fixed-edge, independent-edge, or process law | model not selected |
| `连通` / completely connected | reachability plus the source's vertex/isolated-point conventions | `SimpleGraph.Connected` or a checked source-equivalent event | predicate probed; convention mapping open |
| `阈值` / threshold | transition scale and theorem strength | exact parameter functions, filters/limits, inequalities, and probability expression | absent from repository record |
| Erdos-Renyi Theorem 1 | fixed-edge critical-window law at `N_c = floor((n log n)/2 + cn)` with limit `exp(-exp(-2c))` | fixed-edge measure, exact integer edge count, connectivity event, real limit, and source conventions | strong candidate only; complete proof/correction review open |
| Erdos-Renyi Theorem 4 | possible successive-edge stopping law | coupled graph process, stopping variable, scaling, and distributional limit | candidate only; different proposition family |
| `已验证` | untrusted inventory label | no proposition and no kernel evidence | explicitly rejected as source or proof credit |

## Lean Discovery Boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs` defines the independent-edge measure
`SimpleGraph.binomialRandom`. Its module documentation explicitly notes that the historical
Erdos-Renyi model is closely related but different. Module
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected` defines `SimpleGraph.Preconnected` and
`SimpleGraph.Connected` and records endpoint graph conventions.

`IntakeProbe.lean` verifies that these declarations elaborate together and prints the axiom profile
of two boundary lemmas. A bounded pinned-mathlib name search found no declaration connecting
`binomialRandom` to a connectivity threshold. This is not the exhaustive immutable anchor audit
and says nothing about unsearched external projects. The probe receives no statement or proof
credit.

## Unblocking Crosswalk

Before statement work or `H0`, accountable reviewers must select one immutable primary-source
edition and exact proposition; pinpoint all incorporated definitions and proof passages; freeze the
graph law, event, parameters, binder order, formula, convergence mode, and boundary cases; audit
corrections and errata; map every component to Lean; and explain why that proposition rather than
the other fixed-edge, independent-edge, or graph-process variants is the target of `THM-M-0851`.
