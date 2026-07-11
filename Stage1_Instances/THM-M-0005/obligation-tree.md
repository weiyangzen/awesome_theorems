# THM-M-0005 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 18 canonical IDs before proof work observes closure. Fifteen are
root-relevant machine obligations; `X-ATLAS`, `X-SOURCE`, and `X-TCB` are separate provenance,
documentation, and trust overlays. No node is excluded or credited closed. Any correction, split,
merge, eligibility, or risk change requires registry version 2 and an append-only delta.

## Typed proof route

```text
ROOT -> ASSEMBLE
  |-> TOP-MAPS -> ALG-MAPS, ALG-ZERO, ALG-EXACT, DIRECT-SUM, EZ-EQUIV
  |-> COMPONENTS -> ALG-NAT, DIRECT-SUM
  `-> TOP-NAT -> ALG-NAT, EZ-NAT

ALG-MAPS, ALG-EXACT, ALG-NAT -> CHAIN-FREE
EZ-EQUIV, EZ-NAT -> EZ-MAP
```

## root

`M0005-ROOT` is exactly the frozen `KunnethFormula`, retaining PID coefficients, every degree,
the product of arbitrary spaces, the `Tor_1` term, component maps, and naturality in both spaces.

## scope

`M0005-SCOPE` prevents replacing the target by field coefficients, a pointwise existential, an
algebraic-only theorem, or an unnatural short exact sequence.

## chain-free

`M0005-CHAIN-FREE` owns the projectivity/freeness input needed to apply algebraic Kunneth to
singular chains. It may not be hidden in an instance search or imported wrapper.

## ez-map

`M0005-EZ-MAP` constructs the chain-level product comparison. Mathlib currently supplies no such
declaration; the audited external version is placeholder-bearing and receives no credit.

## ez-equiv

`M0005-EZ-EQUIV` proves the comparison is a chain homotopy equivalence and supplies the induced
homology isomorphism needed to reach `ProductHomology`.

## ez-nat

`M0005-EZ-NAT` proves the comparison commutes with a pair of continuous maps.

## alg-maps

`M0005-ALG-MAPS` constructs the algebraic tensor inclusion and Tor boundary maps.

## alg-zero

`M0005-ALG-ZERO` proves their composite is zero, yielding the short-complex datum.

## alg-exact

`M0005-ALG-EXACT` proves exactness over the PID. Its 100-step budget is a split threshold, not a
claim that an invocation of a deep theorem would be self-explanatory.

## alg-nat

`M0005-ALG-NAT` proves naturality of both algebraic maps in both complex variables.

## direct-sum

`M0005-DIRECT-SUM` owns the grading and reindexing transports to the exact `TensorDegrees` and
`TorDegrees` Sigma objects, including the `p + q + 1 = n` convention.

## top-maps

`M0005-TOP-MAPS` transports the algebraic sequence through Eilenberg-Zilber and supplies the
frozen inclusion, projection, zero composite, and short exactness fields.

## components

`M0005-COMPONENTS` proves that the selected tensor and Tor maps restrict on every summand to the
induced homology maps stated in the canonical structure.

## top-nat

`M0005-TOP-NAT` proves both naturality equations after all transports.

## assemble

`M0005-ASSEMBLE` is kernel-checked by `assemble_sequence` and `root_compose`. These declarations
consume all structure fields as premises; they do not establish any field unconditionally.

## x-atlas

`M0005-X-ATLAS` records the immutable external architectural lead and its placeholder boundary.

## x-source

`M0005-X-SOURCE` remains open for primary-source theorem/page/assumption/errata crosswalks and
independent review.

## x-tcb

`M0005-X-TCB` remains open for terminal-body, axiom, dependency, executable, and replay closure.

## Status boundary

All proof, refinement, provenance, evidence, trust, documentation, and workflow edges are stored
separately in `typed-graphs.json`. Budgets are at most 100, but are architecture estimates rather
than readable-proof or kernel evidence. The root remains `[H1, M3, R3]`; audit completion,
theorem completion, release, and master acceptance remain open.
