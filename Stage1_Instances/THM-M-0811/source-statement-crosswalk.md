# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5963-5968` supplies exactly the title `欧拉路径定理`, attribution
to Leonhard Euler, the year 1736, the gloss `欧拉路径存在的充要条件` ("necessary and sufficient
conditions for the existence of an Eulerian path"), importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record neither states the conditions nor gives a
bibliography, graph definition, theorem locator, binders, hypotheses, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22145-22170` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine state, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Historical source lead

The University of the Pacific Euler Archive record for E53 identifies Leonhard Euler,
*Solutio problematis ad geometriam situs pertinentis*, written 1735 and published 1741 in
*Commentarii academiae scientiarum Petropolitanae*, volume 8, pages 128-140 (also *Opera Omnia*,
series 1, volume 7, pages 1-10). Its content summary says that Euler reduces the Konigsberg bridge
problem to vertex degrees and proves that particular configuration impossible.

The archive record is an authoritative historical locator, but it does not by itself state or
prove the catalog's modern general iff. Its written and publication dates also disagree with the
catalog's single year 1736. A PDF was retrieved outside the repository, but the downloaded copy's
xref/page structure could not be parsed by `pdfinfo` or `pdftotext`, so no proposition or proof
passage was transcribed or credited. The modern characterization source, exact assumptions,
historical relationship, corrections, and independent review remain open. The provisional human
classification is therefore `H1`, not H0.

## Component crosswalk

| Catalog/source component | Candidate mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| "Eulerian path" | a trail that uses every edge exactly once | `SimpleGraph.Walk.IsEulerian` | definition available; simple-graph and endpoint scope open |
| "exists" | existential endpoints and a walk, or a fixed `u`-to-`v` walk | `Exists fun u => Exists fun v => Exists fun p : G.Walk u v => p.IsEulerian` is one candidate shape | no canonical expression frozen |
| "necessary conditions" | endpoint parity; hence zero or two odd-degree vertices | `IsEulerian.even_degree_iff`, `IsEulerian.card_odd_degree` | pinned necessary direction elaborates |
| "sufficient conditions" | connectivity plus the corresponding degree parity constructs a trail | no theorem in the probed module; its TODO names the missing converse | full iff candidate absent from pinned module |
| connectivity | all vertices connected, or only non-isolated vertices connected | `SimpleGraph.Preconnected`, `SimpleGraph.Connected`, support/induced-subgraph APIs | exact convention unresolved |
| Euler's bridge problem | historical multigraph with parallel edges | probed surface is `SimpleGraph` | historical-to-simple-graph transport unresolved |
| `已验证` | untrusted catalog status | accepted H and M evidence would be required | no source or proof credit |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe imports
`Mathlib.Combinatorics.SimpleGraph.Trails` and checks:

- `SimpleGraph.Walk.IsEulerian`, the every-edge-exactly-once predicate;
- `SimpleGraph.Walk.isEulerian_iff` and
  `SimpleGraph.Walk.IsTrail.isEulerian_iff`, characterizations of a supplied walk;
- `SimpleGraph.Walk.IsEulerian.even_degree_iff`, the exact endpoint-parity consequence; and
- `SimpleGraph.Walk.IsEulerian.card_odd_degree`, the necessary zero-or-two conclusion.

The module header at lines 28-31 explicitly marks the converse existence theorem as TODO. Thus
these declarations justify `M3` discovery status, not M0 or an exact-root statement match. They do
not settle connectivity, isolated vertices, multigraph encoding, or open-versus-closed scope.

## Source and statement gate

Before H0, accountable reviewers must preserve an immutable complete source edition for the
selected modern theorem, locate the exact statement and proof, map every definition, binder,
hypothesis, conclusion, endpoint and boundary convention, audit corrections and the historical
date/attribution, and independently approve fidelity to `THM-M-0811`. Before machine credit, the
statement phase must select one source-approved variant, elaborate its minimal Lean expression,
serialize its expression and environment fingerprints, check every alternate transport, and run
the four required mutation classes.
