# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records the Chinese title `Szemerédi正则性引理`, Endre
Szemerédi, 1975, and only the gloss `稠密图的正则划分` ("regular partition of a dense graph").
Stage0 repeats that metadata and explicitly leaves exact definitions, assumptions, proof path,
axioms, and machine artifacts open. All six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

The record is too short to choose one of the materially different standard formulations. In
particular, "dense graph" may describe the method's usual setting rather than a global density
hypothesis, and "regular partition" does not say equitable, exceptional-class, diagonal, degree,
existential-bound, or effective-bound.

## Inspected formalisation source

Yaël Dillies and Bhavik Mehta, "Formalising Szemerédi's Regularity Lemma in Lean", *13th
International Conference on Interactive Theorem Proving (ITP 2022)*, LIPIcs 237, Article 9,
pages 9:1-9:19, DOI `10.4230/LIPIcs.ITP.2022.9`, is an inspected immutable source lead.

- Theorem 1 on article page 9:3 states that for `epsilon > 0` and natural `l`, an integer `L`
  exists such that every graph with at least `l` vertices has an `epsilon`-uniform
  equipartition into `m` parts with `l <= m <= L`.
- Section 3, article page 9:10, displays the effective Lean-facing statement
  `szemeredi_regularity`, with an explicit bound.
- Section 3.1 defines finite partitions as nonempty pairwise-disjoint finite parts covering the
  carrier and equipartitions by part sizes differing by at most one. Section 6.1.2 explains the
  selected partition-uniformity convention; the formal definition counts ordered off-diagonal
  nonuniform pairs.
- The paper says its regularity-lemma proof principally follows Andrew Thomason's 2019 lectures and
  cites Szemerédi, "Regular partitions of graphs" (1975). Neither complete primary source has been
  incorporated or independently reviewed here.
- The paper expressly says displayed code may replace omitted proofs with `sorry` and may omit
  implicit arguments or shorten names. Therefore the PDF is human/source evidence and a
  statement-family/type-shape locator only, never proof-body or exact current-type evidence.
- H1 is provisional because the theorem and complete formalisation are published, while the exact
  primary proof-source, assumption, errata, and node mapping remain unaudited and no independent
  reviewer has accepted the crosswalk.

## Component crosswalk

| Repository/source component | Inspected effective formulation | Frozen Lean component | Statement status |
|---|---|---|---|
| finite graph | every finite graph `G` | `G : SimpleGraph alpha`, `Fintype alpha`, decidable adjacency | selected and elaborated |
| positive tolerance | `epsilon > 0` | `hε : 0 < ε`, `ε : Real` | selected and elaborated |
| requested number of parts | natural `l`, graph has at least `l` vertices | `l : Nat`, `hl : l <= Fintype.card alpha` | selected and elaborated |
| regular partition | page 9:10 uses the formalisation's partition uniformity | `Finpartition.IsUniform G ε`; ordered off-diagonal nonuniform pairs are bounded by `epsilon` times `k(k-1)` | selected exact formal predicate; broader prose convention transport not credited |
| equitable | part sizes differ by at most one | `Finpartition.IsEquipartition` | selected and elaborated |
| partition of all vertices | nonempty pairwise-disjoint parts cover `V(G)` | `P : Finpartition (Finset.univ : Finset alpha)` | selected and elaborated |
| graph-independent upper bound | the page-9:10 form is explicit | `card P.parts <= SzemerediRegularity.bound ε l` | selected; implication to same-predicate existential form checked |
| dense graph | usual dense-graph context | no global density hypothesis | resolved as contextual wording for this selected target |
| `已验证` | untrusted inventory label | no proposition, declaration, or receipt | explicitly rejected as evidence |

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- Module: `Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma`.
- Declaration: `szemeredi_regularity`.
- Displayed type:

  `(G : SimpleGraph alpha) -> 0 < epsilon -> l <= Fintype.card alpha -> Exists P : Finpartition Finset.univ, P.IsEquipartition /\\ l <= P.parts.card /\\ P.parts.card <= SzemerediRegularity.bound epsilon l /\\ P.IsUniform G epsilon`,

  under `DecidableEq alpha`, `Fintype alpha`, and `DecidableRel G.Adj`.
- The source file contains a real proof body. The anchor audit now binds that body at
  `Lemma.lean:79-155`, checks an exact local adapter, records the direct regularity source boundary,
  and obtains the machine axiom set `propext`, `Classical.choice`, and `Quot.sound`. Full transitive
  declaration/TCB acceptance and release-grade provenance remain later gates.

The narrow probe also checks `SimpleGraph.IsUniform`, `Finpartition.IsUniform`,
`Finpartition.IsEquipartition`, and `SzemerediRegularity.bound`. No alternate formulation is
credited without a checked transport.

## Statement selection

`Stage1Instances.THM_M_0843.SzemerediRegularityTarget` selects the effective Lean-facing statement
displayed on article page 9:10 and serializes the corresponding current pinned API proposition. The
statement-only module imports `Regularity.Bound` and `Regularity.Uniform`; it deliberately excludes
the proof-bearing `Regularity.Lemma` module. The canonical root therefore fixes mathlib's exact
ordered-off-diagonal `Finpartition.IsUniform` predicate rather than silently treating every prose
regularity convention as definitionally identical.

`szemerediRegularityTarget_implies_existentialBoundTarget` checks only the implication to an
existential-bound formulation using that same formal predicate. No converse and no transport to a
differently normalized unordered-pair convention is credited. The current pinned declaration
`szemeredi_regularity` is now an exact self-tested `M0-W / E2` candidate: `AnchorAudit.lean`
literally restates the frozen target and closes it with that theorem. This provisional
classification is not accepted `E1`, full trust closure, audit completion, or theorem completion.

## Work required for closure

The source audit must preserve one complete lawful source snapshot, inspect the 1975 source or an
accepted authoritative edition, map its definition and exceptional-pair conventions, assumptions,
conclusion, proof boundary, and corrections, and obtain independent review. Formal work still must
freeze the obligation and typed provenance/trust graphs, compute and accept the full transitive
declaration and TCB closure, and pass the downstream proof, validation, and release gates.
