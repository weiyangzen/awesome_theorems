# Exact-statement gate: blocked

Item: `S56-M-0177-STATEMENT`

## Decision

The exact Grothendieck-Riemann-Roch target selected by the accepted intake cannot be truthfully
elaborated in the pinned Lean environment. The intended formula is

`ch(f_! E) * td(T_Y) = f_*(ch(E) * td(T_X))`

for a proper morphism of smooth quasi-projective schemes. Expressing this formula requires all of
the following as compatible, typed constructions:

- the relevant Grothendieck group of vector bundles or coherent sheaves and its proper pushforward;
- rational Chow groups/rings and their proper pushforward;
- the Chern character into the chosen rational Chow theory;
- tangent classes and the Todd class, including grading or completion conventions;
- a precise quasi-projectivity predicate and the base-scheme/field convention.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides schemes and the
`AlgebraicGeometry.IsProper` and `AlgebraicGeometry.Smooth` morphism predicates. Repository and
pinned-mathlib searches found no algebraic-geometric Chow-group/ring, Chern-character, Todd-class,
or K-theoretic proper-pushforward API with which to type the equation. They also found no
quasi-projective scheme predicate fixing the intake wording. The generic commutative-monoid
`Algebra.GrothendieckGroup` is not the K-theory of vector bundles or coherent sheaves and cannot be
substituted.

Introducing uninterpreted types and arbitrary functions for these missing constructions would
only encode an abstract equality supplied by the model, not the stated theorem about schemes.
Likewise, reducing to Hirzebruch-Riemann-Roch, a curve case, an analytic index theorem, or the two
available morphism predicates would narrow or replace the intake target. Those routes are
therefore rejected rather than presented as an exact elaboration.

## Lean boundary checked

`StatementProbe.lean` uses only:

```lean
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
```

It checks `Scheme`, `IsProper`, and `Smooth`, and elaborates
`SchemeMorphismBoundary X Y f := IsProper f ∧ Smooth f`. This is deliberately a substrate probe,
not the canonical target and not proof evidence for GRR.

The check ran with Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, through the existing canonical Lake environment. No
dependency update, fetch, or `.lake` mutation was performed.

## Validation record

Base revision: `6ba79369e24bfba400ebdfd7dbacd4fd64e18d2c`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0177/StatementProbe.lean` (from `Formalizations/Lean`) | 0 | Scheme, properness, smoothness, and the boundary conjunction elaborated |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg` searches for the required APIs in pinned mathlib and the repository | 1 for the exact API search | No algebraic-geometric Chow/Chern/Todd/K-theory pushforward or quasi-projective target API found; exit 1 means no match |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure passed for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-0177` | 0 | Rank 121, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0177` | 0 | No whitespace errors |

## Gate result and retry condition

First failed gate: section 5 exact canonical Lean target. Machine status remains `M4`; no formal
target, expression hash, checked transport, or meaningful statement mutations can be frozen.
Retry after compatible pinned APIs define the K/G-theory and rational Chow objects, characteristic
classes, both pushforwards, quasi-projectivity, and the conventions required to state the intake
formula, or after an approved pinned external Lean dependency supplies that exact object model.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked, not
self-tested complete. This record does not advance later anchor-audit, obligation-tree, proof,
validation, or release nodes, and it makes no theorem-completion claim.
