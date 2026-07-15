# Statement validation record

Item: `S56-M-0122-STATEMENT`
Base revision: `6ee4e043011799c8a8d6f7f5a2b68dd5fb819679`

## Frozen target

`Stage1Instances.THMM0122.FaltingsTarget` states the intake-selected Mordell
form: for every number field, the rational-section type of every smooth,
projective, geometrically connected relative curve whose geometric genus is
greater than one is finite. Smoothness and relative dimension, geometric
connectedness, scheme morphisms, closed immersions, projective space,
structure-sheaf cohomology, and the rational-section type are concrete pinned
mathlib surfaces.

Projectivity is defined by existence of a closed immersion into a finite
projective space whose composite is the curve's structure morphism. Genus is
derived from the actual scheme: `StructureSheafH1 X` is the concrete pinned
`H^1(X, O_X)` type, and `HasGeometricGenus K X n` requires an additive
equivalence between it and `K^n`. Over a number field, additive maps are
rational-linear; finite rational dimensions make `n` the expected
`K`-dimension when cohomology carries its standard scalar action.

The pin does not expose that K-linear cohomology action, its finrank, or a
native geometric-genus declaration. The comparison is therefore disclosed M3
normalization debt. Unlike the historical free natural slot, however, the
condition is a proposition about the actual structure-sheaf cohomology and
cannot be made true by choosing an unconstrained field of the curve datum. No
data field contains or assumes rational-point finiteness.

The dated `statement-blocker.md` correctly records the absent native genus
API, but its stronger conclusion is superseded by this concrete cohomological
representation. This is still H4/M3/R3 statement evidence, not native-genus
closure, proof closure, or master acceptance.

## Import minimization

The module has eight direct imports and no aggregate `Mathlib` import:

- `Mathlib.AlgebraicGeometry.Geometrically.Basic` supplies `geometrically`.
- `Mathlib.AlgebraicGeometry.Modules.Sheaf` supplies the structure-sheaf
  module and its underlying abelian sheaf.
- `Mathlib.AlgebraicGeometry.Morphisms.Smooth` supplies
  `SmoothOfRelativeDimension` and the homogeneous-polynomial surface needed
  by the projective-space construction at this pin.
- `Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic` supplies `Proj`,
  `Proj.toSpecZero`, and transitively the closed-immersion and Over-category
  surfaces.
- `Mathlib.CategoryTheory.Sites.SheafCohomology.Basic` supplies `Sheaf.H`.
- `Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt` and
  `Mathlib.Topology.Sheaves.Abelian` jointly provide the concrete `HasExt`
  instance needed to elaborate `H`.
- `Mathlib.NumberTheory.NumberField.Basic` supplies `NumberField`.

Temporary probes removing any one of these eight imports exited 1 with a
missing identifier or unresolved cohomology instance. Initial explicit imports
of `Morphisms.ClosedImmersion`, `Comma.Over.Basic`, and
`MvPolynomial.Homogeneous` were each removable and were deleted. Every
temporary probe was outside the repository or unlinked, and no dependency
artifact was changed.

## Mutation evidence

Four independently elaborated propositions change one required statement
dimension: removing the concrete H1-genus hypothesis, dropping the number-field
domain, changing the curve binder from universal to existential scope, and
weakening the cohomological genus bound from `1 < n` to `0 < n` so genus
one is included. Lean rejects each mutation as a term of the canonical target
using `#check_failure`. `check_statement.py` additionally requires all five
fully explicit expressions to be pairwise distinct.

## Commands and results

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard/manifest projection passed for 1546 uniform-L0 targets |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| repository root | `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned, legacy artifacts unaccepted, theorem incomplete |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0122/Statement.lean` | 0 | Canonical target, expansion, point transport, four mutation rejections, explicit print, and axiom prints elaborated |
| repository root | `python3 Stage1_Instances/THM-M-0122/check_statement.py` | 0 | Imports, DAG identity, five explicit expressions, mutation distinctions, transports, and three fingerprints reconciled |
| repository root | `python3 -m json.tool Stage1_Instances/THM-M-0122/statement.json >/dev/null` | 0 | Valid JSON; `statement-receipt.json` passed separately |
| repository root | prohibited Lean-source token scan recorded in `statement-receipt.json` | 1 | No matches; `rg` exit 1 means no match |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0122 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The canonical explicit expression SHA-256 is
`f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac`;
the statement source SHA-256 is
`824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8`;
the complete canonical Lean-output SHA-256 is
`82b09c5ebb5b8a560f76cc37361d67faf46d8ca8555ce1b4fe5d730f0fb7271b`.

The checker independently re-elaborates the canonical target and all four
mutations with `LC_ALL=C` and `TZ=UTC`, checks the authoritative item
identity and ownership, pins direct imports and environment metadata, requires
all checked transports, unlinks every temporary source, and reconciles source,
explicit-expression, and complete Lean-output fingerprints.

## Status boundary

This phase proposes only a worker-self-tested statement node. It supplies no
proof of `FaltingsTarget`; the K-linear/native-genus comparison remains an
open normalization obligation. Human debt remains H4, machine debt moves only
from M4 to proposed M3, and readability moves only from R4 to proposed R3. The
provisional intake dependency, this node, and all downstream nodes still
require dependency-ordered master acceptance or execution;
`audit_complete` and `theorem_complete` are false.
