# THM-M-0133 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 38 canonical obligations for
`S56-M-0133-OBLIGATION_TREE` before the proof phase observes or assigns closure.
Thirty-two are root-relevant machine and human-source obligations; six `X*`
records are informational provenance/trust overlays. All 38 require readable
coverage. No mathematical obligation is excluded for being difficult or open.
The ordered denominator and its canonical SHA-256 projection are authoritative
in `obligation-registry.json`.

The exact root fingerprint is inherited from the accepted statement artifact.
Every other signature is explicitly `planned:v1` and therefore remains M4
until the proof phase supplies and elaborates an exact Lean signature. A later
split, merge, exclusion, or eligibility change requires a new registry version
and append-only ID delta; it cannot silently alter these denominators.

## Typed proof route

```text
M0133-ROOT  exact natural-number FLT [open M2]
|-- M0133-S  exact statement, boundary, transport, and foundation policy
|-- M0133-N  exhaustive reduction to exponent four or an odd prime
|-- M0133-B
|   |-- M0133-B-FOUR  pinned fixed-exponent branch
|   |-- M0133-B-ODD   arbitrary odd-prime branch [open]
|   |   |-- M0133-C   primitive counterexample and Frey construction
|   |   `-- M0133-L   modularity/level-lowering contradiction
|   |       |-- M0133-L-MOD  semistable modularity
|   |       |   |-- residual modularity and deformation problems
|   |       |   |-- Hecke algebras and Taylor-Wiles primes
|   |       |   `-- patching, minimal R=T, and non-minimal lifting
|   |       |-- M0133-L-LOWER  Ribet level lowering
|   |       |-- M0133-L-EMPTY  weight-two level-two nonexistence
|   |       `-- M0133-L-CONTRA
|   `-- M0133-B-RECOMPOSE  conditional mathlib assembly
`-- M0133-T  exact transport back to the frozen target
```

Proof and refinement edges reach every required obligation and are acyclic.
Provenance, evidence, trust, documentation, and workflow relations live in
separate graphs, so an imported name, source link, or task transition cannot
be counted as a proof premise. Nonleaf nodes are marked `split-required`;
leaf-shaped planned nodes have substantive premise/inference/output ledgers
below 100 steps but must be split again if exact formalization exposes hidden
work.

## Composition and provenance boundary

`ObligationTree.lean` kernel-checks the conditional composition from all odd
prime cases through `FermatLastTheorem.of_odd_primes` to the exact natural root.
It deliberately assumes that open family as a typed premise. The pinned
exponent-four and regular-prime declarations are candidate bodies for later
node-scoped validation only. The Imperial exact-root declaration is retained
solely as rejected provenance because its audited terminal chain contains a
proof gap.

The remaining root cut set is semistable modularity (`M0133-L-MOD`) together
with the Frey/Ribet level-lowering bridge (`M0133-L-LOWER`). The architecture
does not assert either result, does not close any obligation, and does not
claim `AUDIT-Z`, `THEOREM-Z`, H0, R0, release trust, or master acceptance.
