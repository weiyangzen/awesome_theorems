# Canonical statement record

## Frozen interpretation

`Statement.lean` fixes the canonical target as the classical unforced Leray whole-space theorem in
three spatial dimensions. Space and velocity are `Fin 3 -> Real`; time is `Real`, restricted to
`[0, infinity)` by the measure or quantifier in each condition; viscosity is strictly positive.
The datum is square-integrable and distributionally divergence-free.

The witnesses are a velocity `u` and its distributional spatial gradient `g`. The predicate
`IsLerayHopfSolution` explicitly requires the weak gradient identity, spatial square integrability
of `u` and `g`, distributional incompressibility, the solenoidal-test weak momentum identity,
strong attainment of the initial datum from the right, and the global energy inequality. Pressure
is eliminated by divergence-free test velocities. There is no external force and no boundary.

The canonical expression is `Stage1.THM_M_1227.lerayHopfExistenceTarget`. It is deliberately a
`def : Prop`, not a theorem declaration: this phase elaborates the exact target and gives it no
proof credit. In particular, none of the conditions is supplied as a field of an input structure.

## Binder and boundary decisions

Binders are ordered `nu`, `u0`, positivity, finite energy, component integrability for the weak
divergence pairing, distributional divergence freedom, then existential `u` and `g`. Zero datum is
included, zero viscosity is excluded, and dimension two is not part of this canonical target. A
future two-dimensional or bounded-domain Hopf formulation must be a separately checked theorem or
transport, not a silent replacement.

`ContDiff Real top` plus compact support describes test functions. The additional test-velocity
condition makes them vanish at negative time. The initial trace uses convergence of the squared
`L2` distance as `t -> 0+`. The energy inequality is stated from initial time zero for every
nonnegative `t`.

## Fidelity boundary

This statement resolves the intake ambiguity by choosing the Leray whole-space member of the
Leray-Hopf theorem family. The repository source phrase itself does not determine these choices.
Primary-source theorem/page and assumption-by-assumption review remains `H2`; this statement-phase
artifact does not promote source fidelity to `H0`, prove equivalence with Leray's original
notation, or claim an inspected errata record. Such review belongs to the downstream source and
anchor audits. The machine state advances only from “no exact expression” to an elaborated open
target; it remains `M4` because no proof body or exact external closure is present.

## Import and environment record

The checked import surface is:

```lean
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
```

These imports provide smoothness/Fréchet derivatives, Bochner integration, and the Lebesgue/Haar
measure instance for finite-dimensional real function spaces. Validation uses the repository's
pinned `lean-toolchain`, `lake-manifest.json`, and pre-existing canonical `.lake` artifacts; it does
not update dependencies.
