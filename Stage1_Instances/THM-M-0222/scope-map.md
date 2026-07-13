# Scope map

## Preserved theorem family

The intake preserves the classical Cauchy integral formula family named by the catalog: values of
a holomorphic complex function inside a positively oriented boundary are recovered by integrating
its boundary values against the Cauchy kernel. This is a scope description, not the frozen
canonical proposition.

NIST DLMF 1.9.E30 gives the familiar scalar simple-closed-contour version. Pinned mathlib instead
offers source-plausible circle versions, including Banach-valued functions and a weakened
off-countable differentiability hypothesis. A later statement phase may select a source-reviewed
variant or a checked equivalent encoding, but intake does not silently choose among them.

## Decisions required at statement freeze

An exact source-reviewed statement must decide all of the following:

1. Whether `f` is complex-valued or takes values in a complete normed complex vector space, and
   which universes and typeclass assumptions are quantified.
2. Whether the boundary is a circle, a piecewise smooth simple closed contour, an arbitrary closed
   path with winding number, or the boundary of a source-defined domain.
3. Whether `f` is defined globally on `Complex` or only on a neighborhood of the closure, and
   whether regularity is expressed by holomorphicity, differentiability, `DiffContOnCl`, or
   continuity on the closure plus differentiability inside.
4. Whether exceptional countable sets are admitted or everywhere interior differentiability is
   required.
5. Whether the root is the value formula only or also includes the formulas for higher
   derivatives.
6. Whether the formula is normalized as `f w = (2 * pi * I)^-1` times the integral or left in the
   equivalent unnormalized form with the integral equal to `(2 * pi * I) * f w`.
7. The kernel orientation (`f z / (z - w)` versus an equivalent scalar-action encoding), contour
   parametrization, positive orientation, and any winding-number multiplier.
8. The exact ordered binders, hypotheses, conclusion, all alternate encodings and checked
   transports, foundation profile, and boundary conventions.

These choices change the proposition or proof boundary. They are a resolution ledger, not a
canonical statement.

## Degenerate and boundary cases

Source review must explicitly resolve zero and negative circle radii; an evaluation point at the
center, elsewhere in the interior, on the boundary, or outside it; constant and zero functions;
empty or degenerate contours; reversed orientation; non-simple closed contours; zero and nonunit
winding number; functions failing boundary continuity; countable exceptional sets containing the
evaluation point; and the scalar specialization of a Banach-valued formula. No case is excluded at
intake.

## Excluded substitutions

- The Cauchy-Goursat theorem that a holomorphic contour integral vanishes is the neighboring
  theorem `THM-M-0221`, not the representation formula itself.
- The residue theorem (`THM-M-0223`), Liouville theorem (`THM-M-0224`), maximum modulus principle
  (`THM-M-0225`), Cauchy estimates (`THM-M-1145`), and power-series analyticity consequences are
  downstream or related results, not substitutes for the formula.
- A formula only at the center, only for polynomials, only for constant functions, or only for a
  fixed unit circle cannot replace a source-selected general target.
- The derivative formula cannot silently replace the value formula, nor may a general-contour
  target be narrowed to a circle without a reviewed source decision and checked transport.
- A theorem name, `#check`, axiom report, legacy wrapper, or the untrusted `已验证` label supplies no
  source identity or proof credit.
- A structure or hypothesis that stores the desired integral equality does not prove it.

## Neighbor target boundaries

`THM-M-0221` separately owns Cauchy's integral theorem, `THM-M-0223` the residue theorem,
`THM-M-0224` Liouville's theorem, and `THM-M-1145` Cauchy estimates. Their future artifacts may
become explicit dependencies only after exact statement and obligation freezes. The legacy
`THM-M-1559` Riemann-Hilbert module contains a checked Cauchy-formula wrapper, but ownership and
status do not transfer across targets.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the candidate module provides normalized and
unnormalized circle formulas for Banach-valued functions, `DiffContOnCl` and closed-ball
differentiability wrappers, an off-countable variant, and a scalar division form. The narrow probe
checks representative declarations and their current axioms. This is real feasibility evidence
supporting provisional `M3`, not an exact source match, an anchor/body audit, or `M0` proof credit.
