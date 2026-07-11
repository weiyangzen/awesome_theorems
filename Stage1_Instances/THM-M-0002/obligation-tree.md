# THM-M-0002 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 canonical obligations before the proof phase assigns closure credit.
Eleven are root-relevant machine obligations; `X-UPSTREAM`, `X-SOURCE`, and `X-TCB` are separate
provenance, human-source, and trust overlays. All 14 require readable coverage. Any correction,
split, merge, exclusion, eligibility, or risk change requires registry version 2 and an append-only
old/new ID delta. No node is excluded merely because pinned mathlib supplies a likely closure.

## Typed proof route

```text
M0002-ROOT  exact frozen five-lemma target [open M1]
`-- M0002-T-ASSEMBLE  middle Mono + Epi imply IsIso
    |-- M0002-B-MONO
    |   |-- M0002-C-LEFT-TRUNC  delta-last exact rows
    |   `-- M0002-L-FOUR-MONO  mono four lemma
    `-- M0002-B-EPI
        |-- M0002-C-RIGHT-TRUNC  delta-zero exact rows
        `-- M0002-L-FOUR-EPI  epi four lemma
```

## root

`M0002-ROOT` is exactly `FiveLemmaTarget`: arbitrary exact five-object rows in an abelian category,
with epi/iso/iso/mono vertical hypotheses and an isomorphism conclusion at component 2.

## s-exact

`M0002-S-EXACT` owns the two `ComposableArrows C 4` rows, their morphism, and both `Exact`
hypotheses. It does not specialize to modules or elementwise functions.

## s-hypotheses

`M0002-S-HYPOTHESES` keeps the asymmetric endpoint assumptions exactly as frozen. In particular,
component 0 is not strengthened from epi and component 4 is not strengthened from mono.

## s-transport

`M0002-S-TRANSPORT` is the checked definitional equivalence with the pinned candidate source shape.
It is statement transport, not independent proof credit.

## b-mono

`M0002-B-MONO` owns the derivation of `Mono (app' phi 2)` from the left four-object window.

## b-epi

`M0002-B-EPI` owns the derivation of `Epi (app' phi 2)` from the right four-object window.

## c-left-trunc

`M0002-C-LEFT-TRUNC` isolates `deltaLastFunctor.map phi` and the two exactness transports needed by
the mono four lemma. Truncation is a material bridge, not hidden inside the theorem invocation.

## c-right-trunc

`M0002-C-RIGHT-TRUNC` similarly isolates `deltaZeroFunctor.map phi` and the exactness transports
needed by the epi four lemma.

## l-four-mono

`M0002-L-FOUR-MONO` anchors the left branch to
`CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono`. The two isomorphism hypotheses supply the
required mono interfaces by typeclass inference.

## l-four-epi

`M0002-L-FOUR-EPI` anchors the right branch to
`CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono`. The two isomorphism hypotheses supply the
required epi interfaces.

## t-assemble

`M0002-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It consumes explicit
`MiddleMono` and `MiddleEpi` premises and uses only `isIso_of_mono_of_epi`; it invokes neither four
lemma and therefore proves no unconditional five lemma in this phase.

## x-upstream

`M0002-X-UPSTREAM` records pinned mathlib revision `8a178386`, the exact diagram-lemmas module, both
four-lemma declarations, the five-lemma body, and the distinction between wrappers and terminals.

## x-source

`M0002-X-SOURCE` remains `H2`: pinpoint primary-source theorem/page/assumption/errata mapping and an
independent review have not been accepted.

## x-tcb

`M0002-X-TCB` remains open for transitive declarations, compiled artifacts, executables, axioms,
and reproducibility closure.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow are separate typed graphs. Every substantive step budget is at most
100. The frozen proof-phase root cut set is `M0002-B-MONO` and `M0002-B-EPI`.

This architecture claims no closed obligation, proof-node acceptance, primary-source review,
readable reconstruction review, transitive trust closure, audit completion, theorem completion,
release readiness, or master acceptance.
