# THM-M-1258 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes nine canonical records before proof-phase closure is observed. Five are
root-relevant mathematical obligations, two are checked degenerate-case analyses, and two are
provenance/workflow overlays with no independent proof credit. The ordered denominator and its
canonical digest are stored in `obligation-registry.json`.

This target is a predicate, not a closed claim that every family of fields satisfies the condition.
Accordingly, the root remains open: a later use must supply concrete fields and discharge the
pointwise span obligation. Splits, merges, exclusions, or eligibility changes require a new registry
version and append-only delta.

## Typed proof route

```text
M1258-ROOT  exact condition-valued declaration [open M4]
|-- M1258-S-DOMAIN     n, r, Omega, X0, X and boundary policy
|-- M1258-S-GENERATED  finite inductive Lie-bracket closure
|-- M1258-N-POINTWISE  unfold to every x in Omega
|   `-- M1258-L-SPAN   establish span = top for the supplied family [open cut]
|-- M1258-B-EMPTY      checked empty-domain boundary
`-- M1258-B-ZERODIM    checked dimension-zero boundary

M1258-X-APIS           pinned Lie-bracket/span provenance only
M1258-W-FOLLOWUP       proof -> validation -> release ordering and input gate
```

The proof graph contains reciprocal `proof_requires`/`composes` edges from the root through the
pointwise normalization to `M1258-L-SPAN`. Refinement, provenance, evidence, trust, documentation,
and workflow edges are stored separately in `typed-graphs.json`; none can masquerade as a proof
premise.

## Node ledgers

### m1258-root

The output is exactly the frozen predicate. It does not assert an inhabitant for arbitrary fields.

### m1258-s-domain

The ordered context is `n`, `r`, `Omega`, `X0`, `X`. Empty domains, `n = 0`, and `r = 0` remain in
scope rather than being silently excluded.

### m1258-s-generated

The inductive family contains the drift and square fields and closes under binary Lie brackets, so
every member has a finite construction tree.

### m1258-n-pointwise

Unfolding the root produces one span equality for each `x` together with `x in Omega`.

### m1258-l-span

This is the unique generic root cut. It cannot be proved without facts about the supplied fields;
the anchor audit found no theorem that manufactures those facts for arbitrary inputs.

### m1258-b-empty

The membership premise is impossible for the bottom open set. `ObligationTree.lean` checks this.

### m1258-b-zerodim

The ambient vector space is a subsingleton, hence every submodule equals top. The harness checks the
result without an extra field hypothesis.

### m1258-x-apis

Pinned mathlib supplies `VectorField.lieBracket` and `Submodule.span`; these are formulation APIs,
not a terminal theorem for the span equality.

### m1258-w-followup

Any proof task must first identify a concrete family or an explicit span premise. Validation and
release remain downstream and open.

## Status boundary

`ObligationTree.lean` checks conditional child-to-parent composition plus the two boundary cases.
It uses no `sorry`, axiom declaration, placeholder, external solver, or fetched dependency. No node
is marked closed, and this architecture claims neither H0, M0, R0, `AUDIT-Z`, `THEOREM-Z`, nor
master acceptance.
