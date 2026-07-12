# Source-statement crosswalk

## Repository Sources

`Docs/researches/math_theorems.md:6250` records the Chinese title `Hamilton圈阈值`; the following
five lines give only "many mathematicians," "twentieth century," the gloss `随机图中Hamilton圈的
存在性` (existence of Hamiltonian cycles in random graphs), importance "high," and status
`已验证`. `Docs/Stage0_Blueprint.md:23252` repeats that metadata while explicitly leaving the exact
definitions and premises, proof route, equivalent statements, axioms, and machine artifact open.
The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

No repository record identifies a theorem, publication, edition, page, graph law, threshold
formula, limiting mode, proof boundary, or erratum. The neighboring connectivity threshold and
deterministic Hamiltonicity entries help delimit the subject, but cannot supply missing statement
content.

## Primary-Source Candidates

- Janos Komlos and Endre Szemeredi, "Hamilton cycles in random graphs," in *Infinite and Finite
  Sets*, Colloquia Mathematica Societatis Janos Bolyai 10 (1975), 1003-1010, zbMATH
  `0375.60018`.
- Janos Komlos and Endre Szemeredi, "Limit distribution for the existence of Hamiltonian cycles in
  a random graph," *Discrete Mathematics* 43(1) (1983), 55-63, DOI
  `10.1016/0012-365X(83)90021-3`.
- Lajos Posa, "Hamiltonian circuits in random graphs," *Discrete Mathematics* 14(4) (1976),
  359-364, DOI `10.1016/0012-365X(76)90068-6`.

These bibliographic records are discovery anchors only. The repository does not select either
paper, and this intake did not freeze an immutable full text, pinpoint a theorem/page, audit all
definitions and assumptions, inspect errata, or obtain independent review. Because the catalog
wording does not select one stable proposition, these candidates receive no `H` credit at intake.
The root remains `H5`; this status does not refute or declare open any theorem in the cited papers.

## Crosswalk

| Repository or candidate phrase | Mathematical component | Required Lean surface | Intake assessment |
|---|---|---|---|
| "random graph" | probability law on finite labelled simple graphs | an explicit `G(n,p)`, `G(n,m)`, or graph-process law | model not selected |
| "Hamilton cycle" | a spanning simple cycle | `SimpleGraph.IsHamiltonian` or a checked source-equivalent predicate | pinned definition probed; convention crosswalk open |
| "threshold" | transition location and theorem strength | exact parameter functions, filters/limits, inequalities, and event probabilities | absent from repository source |
| "existence" | finite positive probability, high probability, limit law, or hitting-time event | exact quantifiers and probability conclusion | meaning open |
| Komlos-Szemeredi 1975 title | possible early threshold/existence target | source-frozen statement, model, and bounds | candidate only; no theorem/page audit |
| Komlos-Szemeredi title | possible critical-window/limit-distribution target | source-frozen formula and checked encoding | candidate only; no theorem/page audit |
| Posa title | possible earlier Hamiltonicity result | source-frozen model, bounds, and conclusion | candidate only; no theorem/page audit |
| `已验证` | untrusted inventory label | no proposition and no kernel evidence | explicitly rejected as proof credit |

## Lean Discovery Boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs` defines the independent-edge measure
`SimpleGraph.binomialRandom` and proves elementary probability-measure, endpoint, and singleton-mass
facts. Its documentation explicitly distinguishes this binomial model from the historical
fixed-edge Erdos-Renyi model. Module `Mathlib.Combinatorics.SimpleGraph.Hamiltonian` defines
`SimpleGraph.Walk.IsHamiltonianCycle` and `SimpleGraph.IsHamiltonian`, along with elementary
properties and boundary conventions.

`IntakeProbe.lean` verifies those declarations elaborate together. A bounded pinned-mathlib search
found no Hamiltonicity threshold theorem connecting the measure to this event. This observation is
not a complete immutable anchor audit and says nothing about unsearched external projects. The API
probe receives no statement, source, or proof credit.

## Unblocking Crosswalk

Before statement or `H0` credit, an accountable reviewer must select an immutable primary-source
edition, pinpoint the exact proposition and referenced definitions, transcribe all ordered binders,
hypotheses, limit formulas, and exceptional cases, map each component to Lean, check corrections and
errata, and explain why that proposition rather than the other published variants is the target of
`THM-M-0852`.
