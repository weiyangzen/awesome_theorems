# THM-M-1015 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 canonical obligations before proof execution assigns closure credit.
Fourteen are root-relevant machine obligations; `X-UPSTREAM`, `X-SOURCE`, and `X-TCB` are
informational overlays. The exact statement and anchor-audit file hashes bind the freeze. A split,
merge, correction, eligibility change, exclusion, or risk change requires registry version 2 and an
append-only delta.

No obligation is marked closed. In particular, the three available mathlib branches do not conceal
the absent quotient branch or upgrade the exact four-branch root.

## Typed proof route

```text
M1015-ROOT [open M1]
`-- M1015-T-ASSEMBLE  checked conditional composition
    |-- M1015-B-PAIR
    |   `-- M1015-L-PAIR-ANCHOR
    |-- M1015-B-ADD
    |   `-- M1015-L-CONT-ANCHOR
    |-- M1015-B-MUL
    |   `-- M1015-L-CONT-ANCHOR
    `-- M1015-B-QUOT
        `-- M1015-L-QUOT-LOCAL [open M3]
```

## root

`M1015-ROOT` is the elaborated `Statement`: arbitrary countably generated index filter, common
source probability space, possibly different limit probability space, real-valued variables,
distribution convergence of `X`, convergence in measure of `Y` to `c`, and explicit a.e.
measurability of every `Y n`.

## s-exact

`M1015-S-EXACT` owns the exact universes, ordered binders, typeclass assumptions, hypotheses, and
complete conclusion package. The historical three-branch wrapper is not an alternate exact target.

## s-boundary

`M1015-S-BOUNDARY` retains `c = 0` in pair, addition, and multiplication. Only quotient convergence
is guarded by `c != 0`; moving that guard or demanding division at zero changes the theorem.

## s-transport

`M1015-S-TRANSPORT` is the checked definitional equivalence with the binder-expanded encoding. It
is one transport obligation, not another semantic theorem or proof-body credit.

## s-foundation

`M1015-S-FOUNDATION` owns the future complete axiom and trust decision. Narrow anchor probes report
`propext`, `Classical.choice`, and `Quot.sound`; transitive release-grade trust remains open.

## n-branches

`M1015-N-BRANCHES` normalizes the nested conjunction into pair, addition, multiplication, and
conditional quotient interfaces without changing scope or duplicating credit.

## b-pair

`M1015-B-PAIR` supplies convergence of `(X_n,Y_n)` to `(Z,c)`. Its pinned bridge is
`prodMk_of_tendstoInMeasure_const`.

## b-add

`M1015-B-ADD` supplies convergence of `X_n + Y_n` to `Z + c`. It specializes the pinned continuous
mapping bridge; the dedicated mathlib addition declaration is equivalent discovery evidence.

## b-mul

`M1015-B-MUL` supplies convergence of `X_n * Y_n` to `Z * c` by the globally continuous
multiplication map.

## b-quot

`M1015-B-QUOT` supplies convergence of `X_n / Y_n` to `Z / c` under `c != 0`. It cannot be closed by
the global continuous-map bridge because division on `Real x Real` is discontinuous at denominator
zero.

## l-pair-anchor

`M1015-L-PAIR-ANCHOR` models the material imported proof body for the pair branch. Its wrapper,
terminal declaration, immutable mathlib revision, and source body remain separate provenance facts.

## l-cont-anchor

`M1015-L-CONT-ANCHOR` models the continuous-function Slutsky engine shared by addition and
multiplication. Sharing this proof body prevents duplicate distinct-body credit.

## l-quot-local

`M1015-L-QUOT-LOCAL` is the critical open proof package: localize the denominator around nonzero
`c`, control the exceptional set using convergence in measure, and apply a mapping argument valid
on the localized region. Its step budget is 80; it must split if execution reveals hidden major
lemmas or exceeds 100 substantive steps.

## t-assemble

`M1015-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It consumes all four branch
premises and returns the exact conjunction. Since those premises are abstract, this is not an
unconditional Slutsky proof.

## x-upstream

`M1015-X-UPSTREAM` records mathlib revision `8a178386`, the convergence-in-distribution module, and
the terminal pair/continuous-map bodies. Full body-level dependency and trust closure remains open.

## x-source

`M1015-X-SOURCE` remains `H1`: no primary edition, theorem/page locator, assumption and errata map,
or independent source-review receipt has been accepted.

## x-tcb

`M1015-X-TCB` remains open for compiled-artifact, executable, transitive declaration, axiom,
reproducibility, and independent-replay closure.

## Graph and status boundary

Proof requirements have reciprocal `composes` edges. Refinement, provenance, evidence, trust,
documentation, and workflow are separate typed graphs. Every node has a structured validation
recipe and a step budget no larger than 100, but this does not establish `R0`.

The frozen proof cut set is `M1015-L-PAIR-ANCHOR`, `M1015-L-CONT-ANCHOR`, and
`M1015-L-QUOT-LOCAL`. The first two have pinned candidates but receive no closure credit in this
phase; the quotient package remains `M3`. No proof-node acceptance, `H0`, `R0`, trust closure,
`AUDIT-Z`, `THEOREM-Z`, release readiness, or master acceptance is claimed.
