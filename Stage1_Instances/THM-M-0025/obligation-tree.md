# THM-M-0025 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 26 canonical obligations before proof-phase installation or acceptance.
The denominator is derived from stable obligation fields and bound to the exact statement and
anchor-audit inputs. The accepted proof set is empty and the root remains `[H1, M3, R3]`.

The audited wrapper and the registered polynomial-ring instance are aliases of the single pinned
`Polynomial.isNoetherianRing` terminal body. They do not create extra coverage.

## Typed proof route

```text
M0025-ROOT
`-- M0025-T-ROOT-COMPOSE
    `-- M0025-T-IDEAL-FG-COMPOSE
        `-- M0025-X-MATHLIB-BODY
            `-- M0025-N-IDEAL-FG
                `-- M0025-T-FG-COMPOSE
                    |-- M0025-L-GENERATOR-SPAN-SUBSET
                    |   `-- M0025-C-BOUNDED-GENERATORS
                    `-- M0025-L-STRONG-INDUCTION-SPAN
                        `-- M0025-B-DEGREE-SPLIT
                            |-- M0025-L-BOUNDED-SPAN
                            |   `-- M0025-C-BOUNDED-GENERATORS
                            `-- M0025-T-SPAN-COMPOSE
                                |-- M0025-L-BOUNDED-SPAN
                                `-- M0025-L-DEGREE-CANCELLATION
                                    |-- M0025-B-HIGH-DEGREE-NONTRIVIAL
                                    `-- M0025-C-LEADING-REPRESENTATIVE
                                        `-- M0025-L-MIN-DOMINATES
                                            `-- M0025-C-WF-MIN
```

Only the locally checked top-level parent-to-child requirements have reciprocal child-to-parent
`composes` edges. Relations internal to the pinned source body are open `logical_decomposition`
edges until exact conditional harnesses are built in a later phase. The local root and ideal-FG
compositions consume an explicit exact anchor and never invoke it. Provenance, evidence, trust,
documentation, and workflow edges are stored separately and cannot supply machine proof credit.

## m0025-root

The root is the exact universe-polymorphic proposition in `Statement.lean`: for any `CommRing R`
with `IsNoetherianRing R`, the ring `Polynomial R` is Noetherian. Its proof child is the terminal
finite-generation composition. No source, trust, or documentation edge can close it.

## m0025-s-interface

This interface preserves the implicit ring binder and the two typeclass assumptions. It forbids a
field, domain, characteristic, finiteness, or global `Nontrivial` restriction and retains the exact
univariate `Polynomial R` conclusion.

## m0025-s-fg-transport

The checked iff in `Statement.lean` relates the typeclass claim to finite generation of every
ideal. The transport owns no second Hilbert-basis proof body and inherits human-source coverage
from the root pending independent approval.

## m0025-s-zero-ring-boundary

The zero ring stays in scope. The statement module proves that a subsingleton coefficient ring
cannot supply `Nontrivial`, while `BoundaryProbe.lean` realizes the antecedent with `PUnit`. The
high-degree proof branch may derive a local `Nontrivial R`; that does not broaden the root.

## m0025-s-foundation

This node owns the final decision on `propext`, `Classical.choice`, `Quot.sound`, the Lean kernel,
the pinned imports, and the no-oracle computation policy. The candidate reports only those standard
principles, but transitive acceptance remains open.

## m0025-t-root-compose

`root_of_everyPolynomialIdealFG` consumes finite generation of every ideal of `Polynomial R` and
uses `isNoetherianRing_iff_ideal_fg` to yield the exact root. It is checked conditionally and does
not supply its child.

## m0025-t-ideal-fg-compose

`everyPolynomialIdealFG_of_exactPolynomialAnchor` consumes an exact polynomial Noetherian anchor
and exposes finite generation of each polynomial ideal. The reverse-direction composition back to
the root is checked independently.

## m0025-x-mathlib-body

This is the sole semantic obligation owning the pinned `Polynomial.isNoetherianRing` body at
mathlib revision `8a178386`. Anchor audit classified it as an `M0-W/E2` candidate. Architecture
freeze does not install it, accept it, or duplicate it through wrapper and instance names.

## m0025-n-ideal-fg

The visible body opens `isNoetherianRing_iff` and fixes an arbitrary ideal `I : Ideal R[X]`. Its
output is a finite set `s` with `Ideal.span s = I`; all subsequent constructions and induction are
scoped to this fixed ideal.

## m0025-c-wf-min

Noetherianity of `R` supplies a well-founded strict order on its ideals. The proof takes the
well-founded minimum of `Set.range I.leadingCoeffNth`, proves it belongs to that range, and chooses
an index `N` identifying the minimum.

## m0025-l-min-dominates

For `k <= N`, monotonicity of `leadingCoeffNth` gives containment directly. For `N < k`, strict
containment would contradict `WellFounded.not_lt_min`; equality is handled separately. Thus every
leading-coefficient ideal at index `k` lies below the selected minimum.

## m0025-c-bounded-generators

`Ideal.is_fg_degreeLE I N` is a material imported bridge, not a routine one-line primitive. It uses
Noetherianity of `R` and finite generation of the degree-bounded ambient polynomial submodule to
obtain a finite generator set for `I.degreeLE N`.

## m0025-l-bounded-span

The equality supplied by bounded generation is converted into membership in `Ideal.span s`.
`Submodule.span_induction` checks preservation under zero, addition, and scalar multiplication;
the final scalar action is reconciled with ideal multiplication.

## m0025-l-generator-span-subset

Every chosen generator belongs to `I.degreeLE N`, hence to `I`. Applying `Ideal.span_le` to those
members supplies the inclusion `Ideal.span s <= I`. This is kept separate from bounded-span and
strong-induction work, which prove the reverse inclusion.

## m0025-l-strong-induction-span

For arbitrary `p` in `I`, the body generalizes `p.natDegree = k` and performs strong induction on
`k`. The induction hypothesis is available only for remainders of strictly smaller degree and
retains the premise that the remainder belongs to `I`.

## m0025-b-degree-split

The induction step uses `le_or_gt k N`. The low-degree side is discharged through the bounded-span
ledger. The high-degree side must perform leading-term cancellation and cannot silently reuse the
bounded result.

## m0025-b-high-degree-nontrivial

High degree first proves `p != 0`. If `0 = 1` in `R`, coefficient extensionality forces `p = 0`, a
contradiction; hence this branch may construct a local `Nontrivial R` instance for degree and
leading-coefficient lemmas.

## m0025-c-leading-representative

Domination puts `p.leadingCoeff` in `I.leadingCoeffNth N`. The checked membership characterization
selects `q` in `I` with degree at most `N` and leading coefficient equal to that of `p`.

## m0025-l-degree-cancellation

Shift `q` by `X^(k - q.natDegree)`. The degree and leading coefficient then match those of `p`.
`Polynomial.degree_sub_lt` makes the remainder strictly smaller, allowing the strong induction
hypothesis to apply.

## m0025-t-span-compose

The high-degree composition applies the induction hypothesis to the smaller remainder, places the
bounded-degree representative `q` in the span, and uses ideal-span closure under multiplication
and addition together with the subtraction identity to reconstruct `p`. This terminal node keeps
the child-to-parent composition distinct from the degree-descent lemma that only supplies its key
strict inequality.

## m0025-t-fg-compose

The final finite-generation assembly consumes both inclusions: generator containment supplies
`Ideal.span s <= I`, while strong induction supplies `I <= Ideal.span s`. Antisymmetry identifies
the ideal with the span of the finite set. This source-body relation remains an open logical
decomposition in this phase, not a checked local composition certificate.

## m0025-x-source

The source boundary remains `H1`. A pinpoint historical statement, definition alignment, proof
crosswalk, errata check, and independent review are all open.

## m0025-x-provenance

The pinned file blob, body slice, import origins, aliases, license, and historical lineage are
partially inventoried. Complete transitive declaration and artifact provenance remains a release
gate and supplies no proof credit.

## m0025-x-trust

Executable, compiled-artifact, axiom, TCB, offline replay, and supply-chain closure remain open.
The warm shared cache used for this phase is explicitly nonrelease evidence.

## m0025-x-readable

This architecture ledger is not an independently reviewed mathematical reconstruction. A complete
reader-facing proof of the leading-coefficient induction, including the zero-ring branch and the
bounded-generation bridge, remains required for `R0`.

## m0025-x-workflow

This node binds later proof, validation, freshness, revocation, independent-verification, and
release receipts. It is not a mathematical premise and cannot close the root.

## Status boundary

The registry, typed graphs, and conditional compositions are self-tested worker artifacts pending
master acceptance. No proof is installed, no obligation is accepted closed, and no H0, accepted
M0, R0, transitive trust closure, audit completion, theorem completion, release, or master
acceptance is claimed.
