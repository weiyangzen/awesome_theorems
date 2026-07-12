# THM-M-0012 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 20 semantic obligations before proof-phase acceptance. Fifteen are
root-relevant machine obligations or checked formal interfaces; the remainder are explicit source,
provenance, trust, readability, and workflow boundaries. The denominator is content-derived from
the stable registry fields and bound to the exact statement and anchor-audit inputs.

No node is accepted closed. `Complex.exists_root` is recorded as the single pinned terminal body;
`Complex.isAlgClosed` and generic root existence for `Complex` are deduplicated because the complex
instance is constructed from that same theorem.

## Typed proof route

```text
M0012-ROOT
`-- M0012-T-ROOT-COMPOSE
    |-- M0012-N-DEGREE
    `-- M0012-A-POSITIVE-ROOT
        `-- M0012-B-NO-ROOT
            `-- M0012-T-ANALYTIC-COMPOSE
                |-- M0012-L-RECIPROCAL-DIFF
                |-- M0012-L-RECIPROCAL-DECAY
                |-- M0012-L-LIOUVILLE
                `-- M0012-L-POLYNOMIAL-CONSTANT
```

The checked root composition consumes both the nonconstant-to-positive-degree bridge and the exact
positive-degree anchor. A separate checked analytic composition consumes differentiability, decay,
Liouville, and polynomial-identity engines to derive the no-root contradiction. Both compositions
are conditional; neither installs the anchor.

## m0012-root

`M0012-ROOT` is the exact frozen proposition over `Polynomial Complex`, with no monicity,
irreducibility, real-coefficient, fixed-degree, or extension-field hypothesis.

## m0012-s-interface

`M0012-S-INTERFACE` fixes the binder order, exclusion of every `Polynomial.C c`, existential
complex witness, and `Polynomial.IsRoot` conclusion.

## m0012-s-boundary

`M0012-S-BOUNDARY` excludes zero and every constant polynomial while retaining `X`, every linear
polynomial, and all higher positive-degree inputs.

## m0012-s-encodings

`M0012-S-ENCODINGS` owns checked transports to positive degree and evaluation at zero.
Algebraic-closedness packaging is not a second proof obligation or proof body.

## m0012-s-foundation

`M0012-S-FOUNDATION` owns the final decision on `propext`, `Classical.choice`, `Quot.sound`, the
Lean kernel, and the no-oracle/computation policy. Transitive acceptance remains open.

## m0012-n-degree

`M0012-N-DEGREE` converts the canonical nonconstancy premise to `0 < f.degree`. This representation
crossing stays explicit rather than being hidden inside the one-line anchor adapter.

## m0012-a-positive-root

`M0012-A-POSITIVE-ROOT` is the central bridge `Complex.exists_root` from pinned mathlib revision
`8a178386`. The anchor audit found an exact `M0-W` candidate, but this architecture phase gives it
no proof acceptance.

## m0012-b-no-root

`M0012-B-NO-ROOT` is the only proof branch: assume no complex root, derive a contradiction, and
recompose by classical contradiction into positive-degree root existence.

## m0012-c-reciprocal

`M0012-C-RECIPROCAL` exposes the function `z -> (f.eval z)^-1` and its root-free nonzero invariant.
It is definitionally total and is not counted as a separate machine premise.

## m0012-l-reciprocal-diff

`M0012-L-RECIPROCAL-DIFF` uses differentiability of polynomial evaluation and differentiability of
the inverse away from zero.

## m0012-l-reciprocal-decay

`M0012-L-RECIPROCAL-DECAY` separates polynomial norm growth at infinity from the inverse limit at
zero, yielding cocompact convergence of reciprocal evaluation.

## m0012-l-liouville

`M0012-L-LIOUVILLE` is a material imported bridge: a differentiable complex function tending to
zero at infinity is pointwise zero. It cannot be treated as a foundation primitive.

## m0012-l-polynomial-constant

`M0012-L-POLYNOMIAL-CONSTANT` uses inverse injectivity and polynomial extensionality to obtain
`f = C 0`, contradicting positive degree.

## m0012-t-analytic-compose

`M0012-T-ANALYTIC-COMPOSE` is checked by `noRootContradiction_of_engines`. It consumes every
analytic engine and invokes no unconditional root theorem.

## m0012-t-root-compose

`M0012-T-ROOT-COMPOSE` is checked by `root_of_degreeBridge_and_positiveDegreeAnchor`. It consumes
both explicit premises and yields the exact architecture-local copy of the frozen root.

## m0012-x-source

`M0012-X-SOURCE` remains `H1`: primary-source pinpointing, assumption/errata review, node mapping,
and independent acceptance remain open.

## m0012-x-provenance

`M0012-X-PROVENANCE` records immutable terminal-body identity, aliases, source blobs, imports,
licenses, and historical revisions. Full transitive closure remains open.

## m0012-x-trust

`M0012-X-TRUST` owns transitive declaration, artifact, executable, axiom, replay, and supply-chain
closure for release.

## m0012-x-readable

`M0012-X-READABLE` requires a complete independently reviewed mathematical reconstruction of the
Liouville route. This architecture ledger is not `R0`.

## m0012-x-workflow

`M0012-X-WORKFLOW` binds proof, validation, freshness, revocation, independent verification, and
release receipts without becoming a proof premise.

## Status boundary

Proof, refinement, provenance, evidence, trust, documentation, and workflow remain separate typed
graphs. The root remains accepted `H1/M3/R4` with an empty accepted proof state. This phase claims
no H0, accepted M0, R0, transitive trust closure, audit completion, theorem completion, release,
or master acceptance.
