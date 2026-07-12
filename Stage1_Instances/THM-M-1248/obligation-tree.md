# THM-M-1248 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 18 canonical semantic obligations for
`S56-M-1248-OBLIGATION_TREE` before proof execution. The route follows the primary theorem's
endpoint/interpolation architecture: preserve the full admissible region, separate `a = 0`,
`a = 1`, and interior cases, establish the weighted Sobolev/Hardy endpoint, and use Holder plus
real-power arithmetic for the interior estimate. The anchor audit found no exact terminal Lean 4
candidate, so no nearby unweighted theorem receives proof credit.

Machine, human-source, and readable denominators are explicit ordered ID sets in
`obligation-registry.json`. Source, provenance, and trust boundaries are separately typed and do
not count as proof bodies. A later correction, split, merge, or eligibility change requires
registry version 2 and an append-only old/new ID delta.

## Typed proof route

```text
M1248-ROOT  exact CaffarelliKohnNirenbergTarget [open M3]
|-- M1248-T-ALL-PARAMS  analytic package for every admissible tuple [open M4]
|   |-- M1248-N-PARAM  exact a=0 / a=1 / interior parameter split
|   |   `-- M1248-S-ADMISSIBLE  frozen admissible region
|   |-- M1248-B-A0  lower-order endpoint
|   |   |-- M1248-S-DEFS  explicit weighted quantities
|   |   `-- M1248-S-TEST  compactly supported smooth test functions
|   |-- M1248-B-A1  weighted derivative endpoint
|   |   `-- M1248-L-WEIGHTED  weighted Sobolev/Hardy inequality
|   |       `-- M1248-L-ORIGIN  singular-weight analytic side conditions
|   `-- M1248-B-INTERIOR  interior endpoint construction
|       |-- M1248-L-WEIGHTED
|       |-- M1248-L-HOLDER  exact weighted Holder bridge
|       |   `-- M1248-L-ORIGIN
|       `-- M1248-L-RPOW  Real.rpow and constant assembly
`-- M1248-T-ASSEMBLE  checked conditional root interface [M0-L]
```

`M1248-S-FOUNDATION`, `M1248-X-SOURCE`, `M1248-X-PROVENANCE`, and `M1248-X-TRUST`
remain trust/source support nodes in their correctly typed graphs. The bundle contains reciprocal
`proof_requires`/`composes` edges plus refinement, provenance, evidence, trust, documentation, and
workflow graphs.

## Leaf and composition policy

Every node has a substantive semantic ledger and a planning ceiling of at most 100 steps. These
ceilings are split triggers, not closure or readability claims. Proof execution must version and
split any node whose exact Lean signature reveals hidden boundary cases, representation
transports, imported central results, or more than 100 material transitions. In particular,
`M1248-L-WEIGHTED` cannot be replaced by an opaque citation, and `M1248-L-ORIGIN` must account for
singular radial weights rather than relying only on compact support.

`ObligationTree.lean` checks only the final child-to-root interface. Its theorem consumes the
explicit `CKNAnalyticPackage` premise and produces the exact public target; it does not construct
that premise. Thus `M1248-T-ASSEMBLE` is locally closed while the root stays open, with the minimal
root cut `M1248-T-ALL-PARAMS`.

## Status boundary

The obligation registry and seven typed graphs are frozen and structurally self-tested. This phase
does not prove a weighted Sobolev/Hardy estimate, integrability at singular weights, the endpoint
or interior cases, the analytic package, or the exact root. It establishes neither H0/R0 nor audit
completion, trust closure, hermetic replay, independent validation, or theorem completion.
Lifecycle remains `planned`; master acceptance is outstanding.
