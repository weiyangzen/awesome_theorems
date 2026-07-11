# THM-M-0106 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 18 semantic obligations before the proof phase
assigns closure credit. Fifteen are root-relevant machine obligations; the
three `X-*` nodes are informational source, provenance, and trust overlays.
All 18 require readable coverage. The exact root fingerprint is inherited
from the statement artifact; planned child fingerprints bind their human
statement and proposed formal target. A correction, split, merge, exclusion,
eligibility change, or risk change requires version 2 with an append-only
old/new ID delta.

The canonical denominator SHA-256 is
`c0bea0cca56af925922c0bf56a324e7a6fbfe82459ee7f303d3676a11fcc12ce`.
No obligation is excluded because its proof is difficult. Eligibility follows
the mathematical architecture, not the already discovered mathlib status.

## Typed proof route

```text
M0106-ROOT  exact algebraic-plus-affine target [open M2]
`-- M0106-T-ASSEMBLE  checked conditional root composition
    |-- M0106-S-EXACT
    |   |-- M0106-S-BOUNDARY
    |   |-- M0106-S-TRANSPORT
    |   `-- M0106-S-FOUNDATION
    |-- M0106-L-FINITE  integral-to-finite upgrade [root cut set]
    |   `-- M0106-L-INTEGRAL-FG
    |       |-- M0106-N-PRESENT  finite-type polynomial presentation
    |       `-- M0106-B-QUOTIENT  induction on variable count
    |           |-- M0106-B-ZERO
    |           `-- M0106-B-SUCC
    |               |-- M0106-C-NAGATA  triangular coordinate change
    |               `-- M0106-C-HOM2  integral quotient map
    `-- M0106-L-SPEC  finite Spec map and affine-space isomorphism
```

### root

`M0106-ROOT` is exactly `NoetherNormalizationTarget`, not the weaker
coordinate-only form and not a claim about arbitrary non-affine varieties.

### s-exact

`M0106-S-EXACT` fixes the universe, field, nonzero commutative algebra,
finite-type hypothesis, `Fin s` indexing, injectivity, `AlgHom.Finite`, and
the explicit affine-space morphism equation.

### s-boundary

`M0106-S-BOUNDARY` includes `s = 0`, excludes the zero ring through
`Nontrivial R`, and adds no reducedness, irreducibility, dimension, or
algebraic-closedness hypothesis.

### s-transport

`M0106-S-TRANSPORT` is the already checked equivalence with the historical
affine-Spec encoding. It is a transport, not another proof body.

### s-foundation

`M0106-S-FOUNDATION` owns classical choice, quotient soundness,
propositional extensionality, and the still-open transitive TCB audit.

### n-present

`M0106-N-PRESENT` extracts a surjective map from a finite-variable polynomial
ring and uses the quotient by its kernel as the canonical normalized input.

### b-quotient

`M0106-B-QUOTIENT` is the central induction producing an integral injective
map into a proper polynomial quotient. Its two induction branches are
separate obligations rather than hidden inside the upstream theorem call.

### b-zero

`M0106-B-ZERO` treats the zero-variable polynomial ring. Properness of the
ideal makes the quotient map injective; surjectivity supplies integrality.

### b-succ

`M0106-B-SUCC` splits on whether the ideal is zero. The zero-ideal branch uses
the quotient equivalence directly. The nonzero branch chooses a nonzero
polynomial, lowers the variable count through `hom2`, applies induction to
its kernel, and composes the injective integral maps.

### c-nagata

`M0106-C-NAGATA` owns the substantive coordinate construction: powers large
enough to separate monomial degrees define a triangular automorphism, after
which the selected nonzero polynomial has unit leading coefficient.

### c-hom2

`M0106-C-HOM2` owns the quotient and coordinate equivalences, the lower-variable
map, and the proof that this map is integral. Its 58-step semantic budget is
below the split threshold but must be revised if readable reconstruction
reveals a hidden package.

### l-integral-fg

`M0106-L-INTEGRAL-FG` applies quotient normalization to the kernel of the
finite-type presentation and transfers injectivity and integrality across the
quotient equivalence.

### l-finite

`M0106-L-FINITE` upgrades integrality to module finiteness. It first checks
the scalar-tower algebra-map identity, obtains finite type over the embedded
polynomial algebra, and invokes `IsIntegral.to_finite`. This is the single
root cut-set node: supplying its exact package permits final assembly.

### l-spec

`M0106-L-SPEC` uses `IsFinite.SpecMap_iff`, postcomposition stability under
the affine-space `SpecIso`, and the inverse/hom simplification. It shares the
same algebra map and is not an independently counted normalization proof.

### t-assemble

`M0106-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It
consumes an exact `AlgebraicCore` premise and derives the complete root. The
premise remains open here, so the composition certificate proves no
unconditional Noether-normalization theorem.

### x-upstream

`M0106-X-UPSTREAM` records mathlib commit `8a178386` and the terminal body
chain. Private declarations such as `T_leadingcoeff_isUnit` and `hom2_isIntegral`
remain provenance boundaries, not independently importable public APIs.

### x-source

`M0106-X-SOURCE` remains H4. Stacks tag `00OW` is only a source lead until an
edition/tag/assumption/proof/errata crosswalk and independent review exist.

### x-tcb

`M0106-X-TCB` remains open for full transitive declaration and trust closure,
fresh replay, and release review. The narrow composition probe reports only
`propext`, `Classical.choice`, and `Quot.sound`.

## Graph and status boundary

Proof edges have explicit reciprocal `composes` edges. Statement refinement,
body/source provenance, evidence, trust, documentation, and workflow are
separate graphs and cannot masquerade as proof premises. Every listed leaf
has a substantive budget at most 100; those budgets are architecture bounds,
not R0 or proof-completion evidence.

The registry records no closed obligations. The root stays M2 and the frozen
root cut set is `M0106-L-FINITE`. This phase does not claim accepted upstream
proof credit, H0, R0, transitive trust closure, audit completion, theorem
completion, release readiness, or master acceptance.
