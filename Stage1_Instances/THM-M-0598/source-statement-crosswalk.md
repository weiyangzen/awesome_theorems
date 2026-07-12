# Source-statement crosswalk

## Repository record

`Docs/Stage0_Blueprint.md` records the Chinese title "Morse theory", the gloss "the topology of
manifolds and the critical points of smooth functions", attribution to Marston Morse, and the year
1934. It leaves the exact definitions, hypotheses, proof, axioms, and machine artifact unspecified.
The generated `已验证` label is untrusted metadata under rev-5.6 and receives no source or proof
credit.

## Candidate human sources

- Marston Morse, *The Calculus of Variations in the Large*, American Mathematical Society
  Colloquium Publications, volume 18 (1934). This is the historical primary monograph candidate
  matching the inventory attribution and date.
- John Milnor, *Morse Theory*, Annals of Mathematics Studies 51, Princeton University Press (1963),
  especially the standard sublevel-set and handle-attachment development. This is a stable modern
  exposition candidate for choosing an exact root and conventions.

These are bibliographic discovery anchors only. This intake did not independently inspect a stable
edition, pinpoint theorem/page, incorporated definitions, proof boundaries, corrections, or errata,
so it does not claim `H0`.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Morse theory" | a family of critical-point/topology theorems | one exact selected proposition | family identified; root selection open |
| smooth function | `f : M -> R` with source regularity/properness | smooth manifold and smooth real-valued map | included; domains and hypotheses open |
| critical point | vanishing differential | differential and critical-point predicate | intended; encoding open |
| nondegenerate critical point | nonsingular Hessian | Hessian and nondegeneracy predicate | required for provisional family; conventions open |
| Morse index | number/dimension of negative Hessian directions | finite-dimensional negative subspace/index | intended; scalar and finiteness model open |
| topology of the manifold | topology of sublevel sets changes at critical values | sublevel sets and equivalence/attachment objects | conclusion family identified; exact relation open |
| no critical values | regular band has no topology change | checked diffeomorphism/deformation theorem | companion branch; exact conclusion open |
| crossing one critical value | attach a handle/cell of the critical index | concrete handle/cell attachment and pair equivalence | provisional central branch; attachment data open |

## Formal-source boundary

A repository-wide case-insensitive search for "Morse theory", "Morse function", and
`MorseFunction` found no theorem-specific Lean source under `Formalizations`; the only hits were the
inventory and research prose. This negative local search is not the required pinned mathlib or
external-project anchor audit. The later anchor phase must search aliases and component APIs at
immutable revisions and record exact declarations, types, terminal bodies, axioms, and integration
status.

Before `H0`, an independent reviewer must approve the selected edition, theorem/page, all imported
definitions and hypotheses, proof boundary, and errata. Before statement acceptance, every row must
map to an elaborated Lean expression with ordered binders, minimal imports, expression hash,
environment fingerprint, checked transports, and mutation tests.
