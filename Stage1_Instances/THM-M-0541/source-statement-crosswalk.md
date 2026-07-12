# Source-statement crosswalk

## Repository source snapshot

The repository record in `Docs/Stage0_Blueprint.md` says only `单纯复形的同调` ("homology of a
simplicial complex"). `Docs/researches/math_theorems.md` repeats that phrase and attributes the
topic to many mathematicians. Neither record supplies hypotheses, coefficients, a theorem number,
or a proof source. The target manifest's `已验证` label is explicitly untrusted metadata.

## Candidate human sources

- Samuel Eilenberg and Norman Steenrod, *Foundations of Algebraic Topology*, Princeton University
  Press (1952), the simplicial-complex and homology development. This is a primary foundational
  source candidate, but an exact edition section/theorem and errata have not yet been inspected.
- Allen Hatcher, *Algebraic Topology* (2002), Section 2.1, "Simplicial and Singular Homology."
  This is a stable modern exposition candidate for definitions, boundary-square, and induced maps;
  its exact proposition/page anchors and published corrections still require inspection.

These are discovery anchors, not `H0` evidence. The statement phase selected Hatcher's standard
ordered, unreduced integral boundary-square formulation, but no immutable source snapshot,
pinpoint pages, errata audit, or reviewed assumption crosswalk exists yet. Therefore no source
credit is claimed.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "simplicial complex" | finite simplices closed under faces | concrete abstract-complex object and morphisms | included; exact representation open |
| "simplicial chains" | free coefficient objects on oriented `n`-simplices | coefficient-valued degree objects | included; coefficients/orientation open |
| "boundary" | alternating sum of codimension-one faces | differential with sign convention | included; concrete bridge open |
| `boundary^2 = 0` | cancellation makes a chain complex | checked chain-complex differential law | required root component |
| "homology" | cycles modulo boundaries in each degree | `HomologicalComplex.homologyFunctor` or checked equivalent | included; exact object open |
| simplicial maps | maps preserve faces and induce chain maps | signed treatment of reordered or identified vertices | deferred to a checked downstream bridge |

The elaborated root is `Stage1Instances.THM_M_0541.StatementShape`. It quantifies over a linearly
ordered vertex type and an `AbstractSimplicialComplex`, uses integral finite-support chains on
faces of cardinality `n + 1`, specifies the alternating vertex-deletion boundary on basis chains,
and concludes that consecutive boundaries compose to zero. Homology is then the downstream
construction from this chain complex; the statement node does not mistake that definition for a
proved boundary-square law.

## Existing Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates `AbstractSimplicialComplex`,
`AlgebraicTopology.alternatingFaceMapComplex`, and
`HomologicalComplex.homologyFunctor`. These declarations show relevant infrastructure, not the
claimed construction from an abstract simplicial complex. No repo-local theorem specific to
`THM-M-0541` was found during intake.

Before `H0`, an independent reviewer must inspect the selected source snapshot, its definitions,
coefficients, ordering/orientation conventions, edge cases, proof, and errata, then approve a
row-by-row source-to-Lean map. Before machine credit, anchor audit must separately locate and inspect
the concrete terminal declarations and their proof bodies.
