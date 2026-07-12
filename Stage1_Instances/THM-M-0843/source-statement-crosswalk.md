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

| Repository/source component | Inspected effective formulation | Pinned Lean component | Intake status |
|---|---|---|---|
| finite graph | every finite graph `G` | `G : SimpleGraph alpha`, `Fintype alpha`, decidable adjacency | exact candidate API checked |
| positive tolerance | `epsilon > 0` | `hε : 0 < ε`, with `ε : Real` inferred by the module | exact candidate API checked |
| requested number of parts | natural `l`, graph has at least `l` vertices | `l : Nat`, `hl : l <= Fintype.card alpha` | exact candidate API checked |
| regular partition | all but a controlled proportion of pairs are regular | `Finpartition.IsUniform G ε`; off-diagonal ordered nonuniform pairs are bounded by `epsilon` times `k(k-1)` | definition checked; source convention review open |
| equitable | part sizes differ by at most one | `Finpartition.IsEquipartition` | definition checked |
| partition of all vertices | nonempty pairwise-disjoint parts cover `V(G)` | `P : Finpartition (Finset.univ : Finset alpha)` | exact candidate type checked |
| graph-independent upper bound | some `L = L(epsilon,l)`; formalisation makes it explicit | `card P.parts <= SzemerediRegularity.bound ε l` | effective refinement candidate; canonical relationship open |
| dense graph | usual dense-graph context | no global density hypothesis in the candidate | wording mismatch to resolve |
| `已验证` | untrusted inventory label | no proposition, declaration, or receipt | explicitly rejected as evidence |

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- Module: `Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma`.
- Declaration: `szemeredi_regularity`.
- Displayed type:

  `(G : SimpleGraph alpha) -> 0 < epsilon -> l <= Fintype.card alpha -> Exists P : Finpartition Finset.univ, P.IsEquipartition /\\ l <= P.parts.card /\\ P.parts.card <= SzemerediRegularity.bound epsilon l /\\ P.IsUniform G epsilon`,

  under `DecidableEq alpha`, `Fintype alpha`, and `DecidableRel G.Adj`.
- The source file contains a real proof body. Intake has not audited its terminal provenance,
  declaration dependencies, axioms, unsafe/oracle boundary, or exact source identity. Those belong
  to `S56-M-0843-ANCHOR_AUDIT` and later nodes.

The narrow probe also checks `SimpleGraph.IsUniform`, `Finpartition.IsUniform`,
`Finpartition.IsEquipartition`, and `SzemerediRegularity.bound`. No alternate formulation is
credited without a checked transport.

## Work required for closure

The statement/source audit must preserve one complete lawful source snapshot, inspect the 1975
source or an accepted authoritative edition, map its definition and exceptional-pair conventions,
assumptions, conclusion, proof boundary, and corrections, decide whether the effective equitable
mathlib theorem is equal to or implies the canonical claim, and obtain independent review. A later
formal audit must separately inspect the actual pinned proof object and trust closure.
