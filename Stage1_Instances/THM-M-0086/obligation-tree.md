# THM-M-0086 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 19 semantic obligations before proof-phase closure credit. Sixteen are
root-relevant machine obligations; the upstream, human-source, and TCB nodes are informational
overlays. No obligation is excluded merely because the pinned library exposes a likely proof.
Every correction, split, merge, eligibility change, or risk change requires version 2 and an
append-only delta.

## Typed proof route

```text
M0086-ROOT [open M1]
`-- M0086-T-ASSEMBLE  checked conditional conjunction
    |-- M0086-L-EMBED
    |   |-- M0086-B-EMBED
    |   `-- M0086-C-EMBED-FUNCTOR
    |-- M0086-L-INJECTIVE
    |   |-- M0086-B-INJECTIVE
    |   `-- M0086-C-INJECTIVE
    `-- M0086-L-PROJECTIVE
        |-- M0086-B-PROJECTIVE
        `-- M0086-C-OPPOSITE
```

## root

`M0086-ROOT` is the exact frozen conjunction for every abelian category. It does not identify the
three claims as one historical theorem; that human-source package identity remains open.

## s-exact

`M0086-S-EXACT` owns universes, typeclass binders, conjunction association, branch-local
hypotheses, and the module universe `max u v`.

## s-boundary

`M0086-S-BOUNDARY` records that the target adds no `Nonempty` or nontriviality assumption. The
statement mutation probe distinguishes such an added hypothesis.

## s-transport

`M0086-S-TRANSPORT` is the checked `canonicalStatement_iff_unfolded` equivalence. It is a transport,
not a second semantic obligation or duplicate proof credit.

## s-foundation

`M0086-S-FOUNDATION` owns the logical and trust boundary. Narrow probes report `propext`,
`Classical.choice`, and `Quot.sound`; complete transitive trust closure remains open.

## n-conj

`M0086-N-CONJ` normalizes the right-associated conjunction into three independent branches without
moving completeness, enough-object, separator, or coseparator hypotheses across branches.

## b-embed

`M0086-B-EMBED` requires one ring and module-valued functor that is simultaneously full, faithful,
finite-limit preserving, and finite-colimit preserving.

## b-injective

`M0086-B-INJECTIVE` quantifies over completeness and enough injectives before the separator witness,
and produces an object carrying both injectivity and coseparator witnesses.

## b-projective

`M0086-B-PROJECTIVE` is independently quantified under cocompleteness and enough projectives. It
starts from a coseparator and produces a projective separator.

## c-embed-functor

`M0086-C-EMBED-FUNCTOR` isolates the imported Freyd-Mitchell ring and functor construction and its
four structural instances. Its substantial upstream body requires later provenance expansion.

## c-injective

`M0086-C-INJECTIVE` isolates the imported injective-coseparator construction, including the limits
and enough-injectives boundary hidden by a terminal invocation.

## c-opposite

`M0086-C-OPPOSITE` isolates the opposite-category dualization used for the projective branch. This
crosses representations and cannot be silently counted as the injective branch a second time.

## l-embed

`M0086-L-EMBED` packages `CategoryTheory.Abelian.freyd_mitchell` into the exact embedding branch.

## l-injective

`M0086-L-INJECTIVE` packages `has_injective_coseparator` into the exact universally quantified
injective branch.

## l-projective

`M0086-L-PROJECTIVE` packages `has_projective_separator` into the exact universally quantified dual
branch.

## t-assemble

`M0086-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It consumes all three branch
families without invoking their terminal theorems. Thus it proves no unconditional root here.

## x-upstream

`M0086-X-UPSTREAM` records pinned mathlib revision `8a178386`, the two source modules, and distinct
terminal declaration/body identities. Wrapper and body provenance remain separate.

## x-source

`M0086-X-SOURCE` remains `H2`: exact primary editions, pages, assumptions, errata, package identity,
and independent review are not accepted.

## x-tcb

`M0086-X-TCB` remains open for full transitive declaration, compiled artifact, executable, axiom,
and reproducibility closure.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow relations remain separate graphs. The frozen root cut set is
`M0086-L-EMBED`, `M0086-L-INJECTIVE`, and `M0086-L-PROJECTIVE`. This architecture marks no node
closed and claims no H0, M0, R0, audit completion, theorem completion, or master acceptance.
