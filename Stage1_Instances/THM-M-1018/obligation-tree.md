# THM-M-1018 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 canonical obligations before proof execution. Fifteen are
root-relevant machine obligations; `X-SOURCE` and `X-PROVENANCE` are separately typed source and
release overlays. Planned fingerprints bind intended interfaces and do not assert Lean closure.
Any correction, split, merge, eligibility, risk, or terminal-body change requires a new registry
version and an append-only delta.

## Typed proof route

```text
M1018-ROOT exact frozen Levy inversion target [open M3]
`-- M1018-T-ASSEMBLE checked conditional binder composition
    `-- M1018-T-ANALYTIC fixed-data inversion [open M3]
        |-- M1018-N-FUBINI truncated characteristic-function/Fubini identity
        |   `-- M1018-C-APPROX measurable approximate-indicator kernel
        |-- M1018-L-INTEGRAL-LIMIT measure-level limiting argument
        |   |-- M1018-C-APPROX (shared construction)
        |   |-- M1018-N-SCALE translation and scaling normalization
        |   |-- M1018-B-POSITION endpoint-aware position branches
        |   `-- M1018-L-DIRICHLET exact sine-integral limits
        `-- M1018-L-ENDPOINTS atom-free endpoint mass identity
            `-- M1018-B-POSITION (shared branch policy)
```

## Node ledger

<a id="m1018-root"></a>`M1018-ROOT` is exactly `LevyInversionTarget`; no uniqueness, density
inversion, or generic Fourier inversion substitute is admitted.

<a id="m1018-s-exact"></a>`M1018-S-EXACT` fixes `Measure Real`, the probability typeclass,
`a < b`, both singleton-null hypotheses, `Ioc a b`, the symmetric `Icc (-T) T` truncation, and
the `atTop` limit.

<a id="m1018-s-kernel"></a>`M1018-S-KERNEL` owns the negative-exponential half-open-interval
kernel and its removable value `b-a` at zero. It is paired with mathlib's positive-sign `charFun`.

<a id="m1018-s-boundary"></a>`M1018-S-BOUNDARY` exposes the three position regions and both
endpoint branches. Removing endpoint hypotheses, reversing endpoint order, changing to `Icc`, or
changing the transform sign is outside the target.

<a id="m1018-s-transport"></a>`M1018-S-TRANSPORT` is only the checked `target_iff_expanded`
binder transport; it creates neither a second semantic obligation nor proof-body credit.

<a id="m1018-s-foundation"></a>`M1018-S-FOUNDATION` keeps the classical, integration, axiom,
import, kernel, and transitive TCB audit open.

<a id="m1018-n-fubini"></a>`M1018-N-FUBINI` must justify the exact complex Fubini exchange for
the truncated integral rather than invoke a formal interchange without integrability evidence.

<a id="m1018-n-scale"></a>`M1018-N-SCALE` isolates translations by `a` and `b`, scaling by
`T`, orientation/sign behavior, and the zero-parameter convention.

<a id="m1018-b-position"></a>`M1018-B-POSITION` freezes the exhaustive regions `x <= a`,
`a < x <= b`, and `b < x`, with `x=a` and `x=b` explicitly retained.

<a id="m1018-c-approx"></a>`M1018-C-APPROX` constructs the measurable truncated kernel on
physical space and proves the algebraic identity consumed by Fubini.

<a id="m1018-l-dirichlet"></a>`M1018-L-DIRICHLET` owns the central improper sine-integral
limits, including exact normalization, sign, and one-sided endpoint values. A short invocation of
a future library theorem remains a provenance and source obligation.

<a id="m1018-l-integral-limit"></a>`M1018-L-INTEGRAL-LIMIT` passes from pointwise kernel limits
to an arbitrary probability measure. It must not assume a false uniform integrable domination;
the required finite-measure approximation or equivalent argument is part of this node.

<a id="m1018-l-endpoints"></a>`M1018-L-ENDPOINTS` uses both singleton-null hypotheses to
identify the boundary-valued limit with exactly `mu (Ioc a b)`.

<a id="m1018-t-analytic"></a>`M1018-T-ANALYTIC` is the minimal open root cut: the fixed-data
analytic inversion theorem after all Fubini, limit, branch, and endpoint obligations compose.

<a id="m1018-t-assemble"></a>`M1018-T-ASSEMBLE` is kernel-checked by `root_compose` against the
binder-expanded formula already related to the canonical target by `target_iff_expanded`. It merely
quantifies an explicit `T-ANALYTIC` premise and therefore proves no unconditional inversion result.

<a id="m1018-x-source"></a>`M1018-X-SOURCE` remains open for primary theorem/page, assumptions,
normalization, genealogy, errata, node crosswalk, and independent review.

<a id="m1018-x-provenance"></a>`M1018-X-PROVENANCE` remains open for bodies, wrappers, imports,
axioms, trust closure, immutable replay, and content-addressed evidence.

## Status boundary

Proof, refinement, provenance, evidence, trust, documentation, and workflow edges are stored in
separate graphs. Every leaf budget is at most 100, but budgets are not readability or proof credit.
The frozen root cut is `M1018-T-ANALYTIC`. This phase claims no analytic closure, H0, readable
reconstruction acceptance, audit completion, theorem completion, release readiness, or master
acceptance.
