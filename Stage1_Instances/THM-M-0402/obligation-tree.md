# THM-M-0402 obligation tree

This freezes `THM-M-0402-OBLIGATIONS-v1` for item `S56-M-0402-OBLIGATION_TREE`.
It is architecture evidence, not proof evidence. The exact statement remains `M3`, every
mathematical proof node is open, and there are no composition certificates.

## Frozen proof route

```text
M0402-ROOT
`-- M0402-T-FINITENESS
    |-- M0402-L-SUNIT-FG
    `-- M0402-C-SPECIALIZATION
        |-- M0402-C-MULT-GROUP
        |-- M0402-L-NONDEGENERATE-UNIT-EQUATION
        `-- M0402-N-PROJECTIVE-NORMALIZATION
```

`M0402-S-DEFINITIONS`, `M0402-S-FOUNDATION`, and `M0402-X-PROVENANCE` are
root-relevant refinement, trust, and provenance obligations. Keeping them outside the proof graph
prevents source fidelity and release trust from being mistaken for mathematical premises.

## Node boundaries

### M0402-ROOT

The exact `EvertseSUnitStatement` from `Statement.lean`, with its ordered number-field, positive
dimension, finite-support binders. It consumes only `M0402-T-FINITENESS`.

### M0402-S-DEFINITIONS

Audit the S-unit tuple, coercion, coordinate sum, normalization, full-sum equation, and every
nonempty proper-subsum condition against equations (6)-(8) in the primary source.

### M0402-S-FOUNDATION

Own the eventual transitive axiom and pinned-TCB report. It cannot close before a terminal proof.

### M0402-L-SUNIT-FG

Establish finite generation of mathlib's `S.unit K` for finite `S`, including the bridge from the
paper's set of places to mathlib's finite-prime convention. The audited mathlib module only defines
S-units and explicitly lacks this theorem, so the obligation remains critical and open.

### M0402-C-MULT-GROUP

Package the tuple coordinates in the finitely generated multiplicative-group interface demanded by
the core theorem, preserving total sums and all partial sums through coercions.

### M0402-L-NONDEGENERATE-UNIT-EQUATION

The central Evertse/Subspace-Theorem package: fixed-arity nondegenerate linear equations in a
finitely generated multiplicative group have finitely many projective solutions. No audited pinned
Lean dependency supplies it. It is required, not assumed or excluded because it is unavailable.

### M0402-N-PROJECTIVE-NORMALIZATION

Construct and prove uniqueness of the representative with `x_0 = 1`, and transport the total-sum
and nondegeneracy predicates. S-unit nonzeroness must be checked rather than silently used.

### M0402-C-SPECIALIZATION

Specialize all coefficients to one and `(c,d)=(1,0)`, then prove exact agreement between the core
predicate and `NormalizedNondegenerateSolutions`.

### M0402-T-FINITENESS

For fixed `n` and `S`, compose finite generation, the core theorem, the group adapter, and projective
normalization into the exact `Set.Finite` conclusion. No child-to-parent certificate exists yet.

### M0402-X-PROVENANCE

Content-address every eventual proof body, wrapper, import, transitive axiom, and TCB boundary.
This cannot close while terminal proof bodies are absent.

## Status boundary

There are 10 inventory and required-machine obligations, 7 source-review obligations, and 10
readability obligations. Zero are claimed machine-closed. The architectural cut set highlights
finite generation and the nondegenerate unit-equation core, but closing them alone would not waive
the remaining adapters, composition, trust, provenance, or review gates.
