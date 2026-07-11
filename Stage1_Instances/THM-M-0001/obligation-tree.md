# THM-M-0001 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 canonical obligations before the proof phase assigns closure credit.
Fourteen are root-relevant machine obligations; `X-UPSTREAM`, `X-SOURCE`, and `X-TCB` are
informational provenance, human-source, and trust overlays. All 17 require readable coverage. The
root fingerprint is inherited from the elaborated statement; planned child fingerprints bind their
human statement and proposed formal target. Any correction, split, merge, exclusion, eligibility,
or risk change requires registry version 2 with an append-only old/new ID delta.

No node is excluded because mathlib already supplies a likely proof. The registry records no closed
obligations, so this architecture cannot itself upgrade the anchor audit's `M1` root classification.

## Typed proof route

```text
M0001-ROOT  exact continuing long-sequence target [open M1]
`-- M0001-T-ASSEMBLE  checked conditional composition
    |-- M0001-L-EXACT2  same-degree H(f), H(g) exactness
    |   `-- M0001-B-DEGREE  every degree, including endpoints
    |-- M0001-L-EXACT3  H(g), delta exactness
    |   |-- M0001-B-RELATED  every c.Rel i j
    |   |-- M0001-C-DELTA  connecting morphism construction
    |   `-- M0001-C-ZERO  comp_delta zero witness
    `-- M0001-L-EXACT1  delta, H(f) exactness
        |-- M0001-B-RELATED
        |-- M0001-C-DELTA
        `-- M0001-C-ZERO  delta_comp zero witness
```

## root

`M0001-ROOT` is exactly the universally quantified, degree-indexed target from `Statement.lean`.
It is not the legacy six-term window and does not assume boundedness or a successor-total shape.

## s-exact

`M0001-S-EXACT` fixes the arbitrary abelian category, complex shape, short complex, and
`ShortExact` witness. The category, degree, and shape universes remain independent.

## s-boundary

`M0001-S-BOUNDARY` retains `L-EXACT2` at every degree, including one with no outgoing `Rel` edge.
The two connecting families are required exactly for related degree pairs.

## s-transport

`M0001-S-TRANSPORT` is the checked equivalence with the three-family grouped encoding. It is a
statement transport, not a second proof obligation or proof-body credit.

## s-foundation

`M0001-S-FOUNDATION` owns the foundation and trust decision. Narrow probes observed `propext`,
`Classical.choice`, and `Quot.sound`; the full transitive TCB audit remains open.

## n-repeat

`M0001-N-REPEAT` normalizes the continuing sequence into one same-degree and two connecting-map
families. This is the repeating architecture, not a finite truncation.

## b-degree

`M0001-B-DEGREE` quantifies the `H(f)`-then-`H(g)` exactness interface over every degree.

## b-related

`M0001-B-RELATED` quantifies both sides of the connecting morphism over each `c.Rel i j`. The
single relation hypothesis supplies both positions, preventing either side from being hidden.

## c-delta

`M0001-C-DELTA` isolates mathlib's connecting-morphism construction. Its internal snake-lemma
construction is a material imported boundary and must receive provenance and readable expansion.

## c-zero

`M0001-C-ZERO` owns `comp_δ` and `δ_comp`, which make the two connecting positions valid short
complexes. Their zero composites are not silently folded into the exactness nodes.

## l-exact2

`M0001-L-EXACT2` is the same-degree exactness package, anchored to `homology_exact₂`. The endpoint
branch in its terminal body remains part of the future provenance/readability audit.

## l-exact3

`M0001-L-EXACT3` is exactness of `H(g)` followed by `δ`, anchored to `homology_exact₃`.

## l-exact1

`M0001-L-EXACT1` is exactness of `δ` followed by `H(f)`, anchored to `homology_exact₁`.

## t-assemble

`M0001-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It consumes all three
family premises and yields the nested canonical root without invoking an exactness theorem. The
premises remain open here, so this certificate proves no unconditional long exact sequence.

## x-upstream

`M0001-X-UPSTREAM` records pinned mathlib revision `8a178386`, the exact module, and the terminal
declaration family. Wrapper credit and terminal body provenance remain separate.

## x-source

`M0001-X-SOURCE` remains `H1`: a primary-source edition/theorem/page/assumption/errata crosswalk and
independent review have not yet been accepted.

## x-tcb

`M0001-X-TCB` remains open for full transitive declaration, compiled-artifact, executable, axiom,
and reproducibility closure.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Statement refinement, formal/human
provenance, evidence, trust, documentation, and workflow are separate graphs. Every budget is at
most 100 substantive steps, but these architecture estimates are neither `R0` nor proof evidence.

The frozen root cut set is `M0001-L-EXACT1`, `M0001-L-EXACT2`, and `M0001-L-EXACT3`. This phase
claims no accepted proof node, primary-source review, readable reconstruction review, transitive
trust closure, audit completion, theorem completion, release readiness, or master acceptance.
