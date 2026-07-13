# Scope map

## Preserved theorem family

The intake preserves a recursion-theoretic theorem about the range of a jump operator on degrees of
unsolvability. The catalog fixes the Chinese title `跳跃反演定理` and gloss `跳跃算子的像`; it gives
neither a formula nor a source capable of selecting an exact proposition.

The conventional Friedberg shape is a candidate, not the adopted statement:

> Every Turing degree `a` above the jump `0'` of the computable degree is itself a jump: there is a
> Turing degree `b` with `b' = a`.

An inspected Encyclopedia of Mathematics revision states this shape. It is secondary evidence and
does not resolve whether the terse catalog intended that exact theorem or a relative, iterated,
computably-enumerable, or other degree-theoretic variant.

## Decisions required at statement freeze

An approved source and target-identity review must freeze all of the following:

1. The primary edition, theorem locator, incorporated definitions, proof boundary, correction and
   errata status, and independent review.
2. The degree structure: Turing degrees of sets, total functions, or partial functions; or a
   different reducibility whose result must not be substituted here.
3. Representatives, oracle-computation convention, equivalence relation, order, and least degree.
4. The jump operator on representatives and the proof that it descends to degrees independently of
   representatives.
5. Whether the theorem is the ordinary Friedberg inversion result, a relative uniform form, an
   iterated/higher form, or a restriction such as computably enumerable degrees.
6. The exact binder order and image characterization: `0' <= a` as a hypothesis and existence of
   `b` with `b' = a`, or another source-backed proposition.
7. Whether equality is degree equality, equivalence of representatives, or mutually checked
   reducibility, together with every required transport direction.
8. Boundary cases at `a = 0'`, degrees below `0'`, and any relativized base degree.
9. The exact foundation, quotient, classical-choice, TCB, and computation profiles.

## Neighbor and variant boundaries

- `THM-M-0752` separately names the jump operator. Its future definition and well-definedness proof
  may be dependencies, but its statement or evidence cannot count as this target's inversion root.
- `THM-M-0751` separately concerns upper bounds in Turing degrees. Semilattice/order facts are only
  substrate here.
- `THM-M-0754` separately concerns the arithmetic hierarchy. Iterated-jump connections do not turn
  a hierarchy theorem into jump inversion.
- Results called jump inversion for enumeration degrees, truth-table degrees, structures, spectra,
  or higher effective hierarchies are distinct candidates unless a checked source crosswalk proves
  the intended relationship.

## Explicit exclusions and boundaries

The target is not merely existence of Turing degrees, definition or monotonicity of a jump, Post's
problem, a non-inversion theorem, or a surjectivity claim onto degrees below `0'`. No conclusion may
be installed as a structure field or assumption. The source label `已验证`, the secondary statement,
and a passing substrate probe are not proof evidence.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` defines
`TuringReducible`, `TuringEquivalent`, `TuringDegree`, and a partial order in
`Mathlib.Computability.TuringDegree`. The inspected module ends after the order instance and has no
jump operator. A bounded search found no named jump-inversion target elsewhere in pinned
`Mathlib/Computability` or repo-local Lean. These are discovery observations only, not an exhaustive
anchor audit or a global absence claim.

## Formal boundary

No canonical proposition, Lean declaration, expression fingerprint, environment fingerprint,
transport, mutation test, obligation registry, graph, proof body, or accepted receipt exists at
intake. The next phase must first obtain source authority and freeze the exact statement. Later
phases then own formal-candidate audit, proof architecture, proof work, validation, and release.
