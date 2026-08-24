# Erdős Problem 1128 — distilled study

<a id="U0-statement"></a>

## U0 — exact statement reduction

The frozen statement asks whether every two-colouring of a product of three
sets of cardinality `aleph 1` contains a monochromatic product of three
countably infinite subsets. Its registered answer is false.

The logical reduction is exact: after unfolding the answer wrapper, the root
is `False ↔ P`, hence equivalent to `¬ P`.

<a id="U1-counterexample"></a>

## U1 — counterexample unit

A Prikry--Mills colouring supplies a single witness refuting `P`. Applying `P`
to that colouring would produce subsets with all three cardinality hypotheses
and a constant colour on their box; this is precisely the output forbidden by
the counterexample.

The exceptional issue is provenance trust. The pinned FormalConjectures source
contains a placeholder in the counterexample lemma used by its headline proof.
Consequently the source is statement authority only. The claim-owned Lean
surface expands the local definitions and uses Mathlib alone. It exposes the
counterexample as a typed hypothesis so no provider oracle is smuggled into the
composition. Canonical acceptance requires an independently closed body for
that unit and a trust-zero Master replay.

<a id="U2-composition"></a>

## U2 — contradiction composition

Instantiate the universal positive property at the counterexample type three
times and at its colouring. Destruct the promised box, preserving each of its
three cardinality equalities, then apply the counterexample's negated constancy
result. This closes the reverse implication; the forward implication is false
elimination.

<a id="U3-audit"></a>

## U3 — transport and trust audit

Downstream, the root settles the Stage6 alias `S6-CLM-00007173` /
`S6-VAR-00004401`. No exceptional finite or empty-set case is lost: cardinality
equalities to `aleph 0` are passed unchanged to the counterexample, and all
three type and colouring quantifiers are preserved.
