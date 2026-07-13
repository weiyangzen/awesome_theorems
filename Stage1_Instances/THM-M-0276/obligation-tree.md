# THM-M-0276 frozen obligation architecture

Item: `S56-M-0276-OBLIGATION_TREE`.

Registry version 1 freezes 29 canonical obligations before proof-phase closure
credit. The architecture follows the visible pinned `Banach.lean` proof through the real
and complex branches, controlled exact preimages, residual series, Baire cover, rescaling,
closure witnesses, and the final open-image neighborhood argument. Provenance, evidence,
trust, documentation, and workflow relations remain separate from proof premises.

## Proof route

```text
ROOT -> exact adapter + literal pinned semilinear terminal
  adapter -> Real and Complex branches + same-field normalization
  upstream terminal -> IsOpenMap terminal
    -> local open-ball image argument -> exact controlled preimages
      -> approximate selection + residual contraction + geometric series
        -> summability + telescoping + continuity/limit uniqueness
      -> approximate controlled preimages
        -> surjective Baire cover -> nonempty interior
        -> scalar shell rescaling -> paired closure witnesses
```

Only the exact root adapter/composition is checked in this phase. Every internal relation
is frozen as a source-body decomposition and remains unverified as child-to-parent
composition until a later proof task supplies an exact abstract-child harness.

## Node ledger

### m0276-root

For real and complex Banach spaces, every surjective bounded linear operator is open.

Formal target: `Stage1Instances.THM_M_0276.BanachOpenMappingTarget`. Output: The exact frozen real-and-complex conjunction. Source boundary: Statement.lean:32-34; expression sha256 0cfb9796...82fa.
Budget: 12 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0276-s-target

Preserve both scalar branches, independent universes, complete normed-space instances, ordinary continuous linear maps, surjectivity, and IsOpenMap.

Formal target: `Stage1Instances.THM_M_0276.{RealOpenMappingTarget,ComplexOpenMappingTarget,BanachOpenMappingTarget}`. Output: The exact ordered root interface. Source boundary: Statement.lean:20-34.
Budget: 20 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-s-boundary

Retain trivial spaces, the zero map onto a trivial codomain, and noninjective surjections while excluding incomplete spaces and nonsurjective maps.

Formal target: `the ordered binders and hypotheses of BanachOpenMappingTarget`. Output: No strengthened or omitted boundary premise. Source boundary: Statement.lean:18-34; statement.json degenerate_cases.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-s-open-expansion

Expand IsOpenMap to openness of every image without changing scalar, operator, completeness, or surjectivity scope.

Formal target: `Stage1Instances.THM_M_0276.banachOpenMappingTarget_iff_expandedOpenMappingTarget`. Output: The checked open-image formulation. Source boundary: Statement.lean:36-57.
Budget: 12 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-s-foundation

Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, imports, and the no-oracle policy.

Formal target: `planned transitive foundation and TCB report`. Output: An accepted logical-foundation boundary. Source boundary: AnchorAudit.lean axiom and closure probes.
Budget: 24 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-n-same-field

Specialize the pinned semilinear theorem to the identity scalar homomorphism for ordinary same-field Real and Complex maps.

Formal target: `identity RingHomInvPair and RingHomIsometric specialization of ContinuousLinearMap.isOpenMap`. Output: The exact same-field terminal interface. Source boundary: AnchorAudit.lean:49-56; Banach.lean:227-248.
Budget: 22 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-t-assemble

Assemble the exact real and complex branch conclusions into the frozen conjunction.

Formal target: `conjunction introduction inside Stage1Instances.THM_M_0276_Obligations.terminal_adapter`. Output: The exact canonical conjunction. Source boundary: ObligationTree.lean#terminal_adapter.
Budget: 10 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0276-t-adapter

Specialize the literal pinned semilinear terminal to identity scalar homomorphisms and assemble the exact Real-and-Complex root.

Formal target: `Stage1Instances.THM_M_0276_Obligations.terminal_adapter`. Output: The exact frozen root from the upstream terminal interface. Source boundary: ObligationTree.lean#terminal_adapter.
Budget: 18 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0276-t-upstream

Expose the literal polymorphic semilinear proposition proved by ContinuousLinearMap.isOpenMap without relocating its body.

Formal target: `Stage1Instances.THM_M_0276_Obligations.MathlibTerminal`. Output: The pinned semilinear open mapping proposition. Source boundary: ObligationTree.lean#pinned_mathlib_terminal; Banach.lean:227-248.
Budget: 14 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-b-real

Prove the real scalar branch at its exact binders.

Formal target: `Stage1Instances.THM_M_0276.RealOpenMappingTarget`. Output: The real Banach open mapping proposition. Source boundary: Statement.lean:20-25; Banach.lean:227-248.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-b-complex

Prove the complex scalar branch at its exact binders.

Formal target: `Stage1Instances.THM_M_0276.ComplexOpenMappingTarget`. Output: The complex Banach open mapping proposition. Source boundary: Statement.lean:27-31; Banach.lean:227-248.
Budget: 18 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-t-isopenmap

Turn a positive controlled-preimage constant into a neighborhood of every image point and hence an open image.

Formal target: `ContinuousLinearMap.isOpenMap`. Output: IsOpenMap f for a surjective continuous linear map. Source boundary: Banach.lean:227-248.
Budget: 30 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0276-l-local-open-ball

For y=f x in an open source image, choose an epsilon-ball around x and lift every nearby z through a controlled preimage of z-y.

Formal target: `Metric.isOpen_iff; ContinuousLinearMap.map_add; Set.mem_image_of_mem`. Output: The ball of radius epsilon/C around y lies in the image. Source boundary: Banach.lean:230-248.
Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-exact-preimage

Produce an exact preimage of every y with a uniform positive norm bound from half-error approximate preimages.

Formal target: `ContinuousLinearMap.exists_preimage_norm_le`. Output: There is C>0 with f x=y and norm x <= C*norm y. Source boundary: Banach.lean:160-225.
Budget: 46 substantive steps maximum; structured ledger: 6 recorded step(s).

### m0276-c-approx-selection

Choose an approximate-preimage function g and residual map h(y)=y-f(g y), preserving the half-error and norm bounds.

Formal target: `Classical choice package immediately after exists_approx_preimage_norm_le`. Output: Functions g and h with geometric residual contraction. Source boundary: Banach.lean:164-175.
Budget: 24 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-residual-geometric

Inductively bound the nth residual and the nth approximate preimage by powers of one half.

Formal target: `local hle, hnle, and ule estimates`. Output: Geometric norm bounds for h^[n] y and u n. Source boundary: Banach.lean:171-188.
Budget: 30 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-summable-series

Use the geometric majorant and completeness of the domain to sum the approximate preimage series.

Formal target: `Summable.of_nonneg_of_le; Summable.of_norm; tsum`. Output: A limit x = sum' u with a controlled norm. Source boundary: Banach.lean:189-207.
Budget: 36 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-telescope

Show that applying f to every finite partial sum telescopes to y minus the nth residual.

Formal target: `local fsumeq induction`. Output: f(sum i<n, u i)=y-h^[n] y. Source boundary: Banach.lean:208-213.
Budget: 22 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-limit-image

Pass the partial-sum identity to the limit using continuity of f, residual convergence, and uniqueness of limits.

Formal target: `HasSum.tendsto_sum_nat; Continuous.tendsto; tendsto_nhds_unique`. Output: The series sum x satisfies f x=y. Source boundary: Banach.lean:214-225.
Budget: 30 substantive steps maximum; structured ledger: 4 recorded step(s).

### m0276-l-approx-preimage

Use Baire category, rescaling, and two closure witnesses to approximate every y within half its norm while controlling the preimage norm.

Formal target: `ContinuousLinearMap.exists_approx_preimage_norm_le`. Output: There is C>=0 and an approximate controlled preimage for every y. Source boundary: Banach.lean:85-153.
Budget: 48 substantive steps maximum; structured ledger: 5 recorded step(s).

### m0276-c-baire-cover

Cover the codomain by the countable union of closures of images of radius-n balls using surjectivity.

Formal target: `union n, closure (f '' Metric.ball 0 n) = Set.univ`. Output: A countable closed cover of the complete codomain. Source boundary: Banach.lean:94-101.
Budget: 24 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-l-baire-interior

Apply Baire category to the closed cover and extract a ball inside one closure.

Formal target: `nonempty_interior_of_iUnion_of_closed`. Output: Some closure(f '' ball 0 n) contains a nonempty open ball. Source boundary: Banach.lean:102-105; Topology/Baire/Lemmas.lean:243-248.
Budget: 28 substantive steps maximum; structured ledger: 2 recorded step(s).

### m0276-l-rescale-shell

Rescale a nonzero y by a scalar whose norm lies in a controlled shell and retain inverse-norm control.

Formal target: `rescale_to_shell`. Output: A scalar d placing d*y inside the Baire ball with bounded inverse norm. Source boundary: Banach.lean:106-113; Analysis/Seminorm.lean:1379-1382.
Budget: 30 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-c-closure-pair

Choose two nearby points in the image closure, subtract their preimages, and rescale the difference.

Formal target: `Metric.mem_closure_iff; Set.mem_image; norm_sub_le`. Output: The half-error approximate preimage and its norm estimate. Source boundary: Banach.lean:114-153.
Budget: 54 substantive steps maximum; structured ledger: 3 recorded step(s).

### m0276-x-source

Map every material analytic node to an approved proof source with exact assumptions, correction, errata, and independent review.

Formal target: `node-specific primary-source crosswalk remains open`. Output: Human-source evidence without machine proof credit. Source boundary: source-statement-crosswalk.md; known printed Baire-cover gap.
Budget: 32 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-x-provenance

Bind the adapter, terminal body, helper bodies, immutable source hashes, licenses, declaration closure, and replay evidence without duplicate credit.

Formal target: `anchor-audit.json plus a future release provenance packet`. Output: Proof-body provenance without mathematical proof credit. Source boundary: anchor-audit.json; anchor-audit-receipt.json.
Budget: 36 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-x-trust

Audit imported compiled artifacts, executables, transitive declarations, unsafe/oracle boundaries, and independent replay.

Formal target: `Lean 4.29.0 and mathlib 8a178386 release trust closure`. Output: Release-grade trust evidence without proof credit. Source boundary: anchor-audit.json immutable_environment; release gate pending.
Budget: 38 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-x-readable

Provide a complete node-anchored reconstruction and independent functional-analysis review.

Formal target: `planned readable reconstruction`. Output: Readable coverage without machine proof credit. Source boundary: future readable proof surface.
Budget: 40 substantive steps maximum; structured ledger: 1 recorded step(s).

### m0276-x-workflow

Bind proof, validation, release, freshness, revocation, and independent verification tasks.

Formal target: `planned Stage1 workflow receipts`. Output: Dependency-legal workflow evidence without proof credit. Source boundary: task-dag.json and future accepted receipts.
Budget: 24 substantive steps maximum; structured ledger: 1 recorded step(s).

## Freeze boundary

All accepted machine obligations remain open at `M3`. Candidate `M0276-C01` is exact,
pinned, sorry-free, and locally checked at `M1/E2`, but it is not installed by this
obligation phase and has no accepted closure credit. The real and complex branches share
one generic terminal-body identity and cannot inflate distinct-body coverage. The printed
human-source Baire-cover gap, H0 and R0 independent reviews, complete provenance/TCB,
hermetic replay, independent verification, AUDIT-Z, and theorem completion remain open.
Any architectural or eligibility change requires a successor registry and append-only
delta.
