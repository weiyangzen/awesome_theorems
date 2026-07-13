# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6621-6626` supplies exactly the title `Galvin定理`, attribution to
Fred Galvin, the year 1995, the gloss `Dinitz猜想的证明` ("proof of the Dinitz conjecture"), high
importance, and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, definitions,
ordered binders, hypotheses, conclusion, proof locator, correction history, reviewer, or formal
artifact. A phrase describing a proof is not a proposition by itself.

`Docs/Stage0_Blueprint.md:24683-24708` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets this target to `L0 / rework_required`.

## Published source lead

Fred Galvin, *The List Chromatic Index of a Bipartite Multigraph*, Journal of Combinatorial Theory,
Series B 63(1), January 1995, pages 153-158, DOI `10.1006/jctb.1995.1011`, is the exact primary
bibliographic lead. Crossref metadata observed on 2026-07-13 confirms the author, title, journal,
date, volume, issue, page range, DOI, and publisher article identifier `S0095895685710118`; the
observed response had SHA-256
`eed54493a58d40dd85efa9458a374fd0b6ff1379f23ce032e4439a6d236ac052`.

The DOI landing path was reachable, but the publisher article page returned an access challenge
and no primary theorem text was inspected. OpenAlex reported no repository full text. Consequently
the theorem numbering, verbatim definitions, exact hypotheses and conclusion, proof boundary,
correction and errata history, and the source's explicit relationship to the array formulation were
not audited. The network downloads remained outside the repository and are bibliographic discovery
evidence only.

A familiar later summary says that every `k`-edge-colorable bipartite multigraph is
`k`-edge-choosable. That identifies the standard family but is not substituted for the uninspected
primary statement. The published lead plus explicit unresolved mapping supports provisional `H1`,
not H0.

## Clause crosswalk

| Repository/source component | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Fred Galvin / 1995 | Galvin's published list-chromatic-index paper | source metadata only | strong identity lead; primary theorem text not inspected |
| `Dinitz猜想的证明` | proof or implication yielding the Dinitz array result | checked theorem or transport, not a proof label | catalog does not select a truth-valued root |
| paper title: bipartite multigraph | graph with two parts and parallel-edge identity | a future multigraph structure; pinned `SimpleGraph` is insufficient by itself | graph model, loops, finiteness, and incidence open |
| list chromatic index | list-respecting proper edge coloring | per-edge finite color collections plus a properness predicate | list representation, size, palette, and properness open |
| familiar `k` slogan | `k`-edge-colorable implies `k`-edge-choosable | existence of a witness or invariant inequality | exact `k` domain and premise/conclusion forms open |
| Dinitz corollary | apply the graph theorem to `K_(n,n)` with cells as edges | checked array/edge equivalence and list transport | belongs at the boundary with `THM-M-0904`; no status shared |
| `已验证` | untrusted inventory label | source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`SimpleGraph.Coloring`, `SimpleGraph.Colorable`, `SimpleGraph.IsBipartite`,
`SimpleGraph.EdgeLabeling`, `SimpleGraph.lineGraph`, and the line-graph adjacency characterization.
These are ordinary simple-graph interfaces. `EdgeLabeling` does not impose properness or per-edge
lists, and a simple graph does not preserve distinct parallel edges.

A bounded search of repo-local Lean and pinned mathlib found no Dinitz, Galvin, list-coloring,
edge-choosability, or list-chromatic declaration. This is scoped intake discovery only, not the
later immutable external anchor audit and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must preserve and hash an approved immutable edition,
inspect a pinpoint theorem and its proof boundary, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, finiteness and multigraph convention, list and palette
semantics, boundary case, and correction or erratum, reconcile the exact relationship to
`THM-M-0904`, and independently approve fidelity to `THM-M-0905`. Only then may the statement phase
freeze minimal imports, an elaborated expression and environment fingerprint, checked alternate
encodings, and the required removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations.
