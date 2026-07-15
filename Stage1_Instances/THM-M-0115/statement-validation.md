# Statement validation record

Item: `S56-M-0115-STATEMENT`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

## Frozen target

`Stage1Instances.THMM0115.GrothendieckRiemannRochExpandedTarget` freezes the
intake-selected classical form: for every proper morphism `f : X -> Y` of
nonsingular quasi-projective varieties over a field and every class
`alpha in K_0(X)`,

`ch(f_* alpha) cap td(T_Y) = f_*(ch(alpha) cap td(T_X))`

in rational Chow homology of `Y`. The field, scheme and morphism carriers,
structure maps, smoothness hypotheses, and properness hypothesis use pinned
mathlib objects. Typed families and semantic compatibility hypotheses represent
the unavailable `K_0`, rational Chow, characteristic-class, tangent, and cap
surfaces. No input field contains or implies the equality.

`GrothendieckRiemannRochTarget` is a public definitional alias, and
`grothendieckRiemannRochTarget_iff_expanded` checks that alias against the fully
expanded expression by `Iff.rfl`. This is an `M3` statement/interface boundary,
not a proof.

## Import minimization

The module has two direct imports and no aggregate `Mathlib` import:

- `Mathlib.AlgebraicGeometry.Morphisms.Proper` supplies schemes, `Spec`,
  categorical composition, `IsProper`, and the group substrate for typed
  `K_0` and rational Chow families.
- `Mathlib.AlgebraicGeometry.Morphisms.Smooth` supplies the concrete `Smooth`
  predicate used to encode nonsingularity through the structure morphisms.

Replacing `Smooth` by its weaker `RingHomProperties` dependency makes that
predicate unavailable. Replacing `Proper` by its weaker `Separated` dependency
makes `IsProper` unavailable. The structured checker recreates both negative
probes, so both direct imports are required by this module in the pinned snapshot.

## Mutation evidence

Four separately elaborated propositions change one required statement
dimension: properness is removed; nonsingularity and the common-base condition
are removed from the domain; the universally quantified datum and class become
existential; and the class binder is restricted to zero. Lean rejects each as
a term of the canonical target using `#check_failure`. The structured checker
also requires all five fully explicit expressions to be distinct.

## Validation

Commands run from the worker clone unless another directory is shown:

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard and manifest projection passed for 1546 uniform-L0 targets |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| repository root | `python3 scripts/stage1_target.py show THM-M-0115` | 0 | Rank 23, planned, legacy artifacts unaccepted, theorem incomplete |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0115/Statement.lean` | 0 | Canonical target, definitional transport, four mutation rejections, explicit print, and axiom print elaborated |
| repository root | `LC_ALL=C TZ=UTC python3 Stage1_Instances/THM-M-0115/check_statement.py` | 0 | Imports, DAG identity, five explicit expressions, mutation distinctions, and source/expression/output fingerprints reconciled |
| repository root | `python3 -m json.tool` on `statement.json`, `statement-receipt.json`, and the worker self-test | 0 | All structured records parsed |
| repository root | prohibited-token scan over the new Lean source | 1 | Expected no-match exit: no proof escape or unsafe declaration token; the checker enforces the same scan |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0115 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics |

The canonical expression SHA-256 is
`eada246ab2968c378c5b6c31c2ffd84c10873d9206b499457c451ae3848c160e`;
the statement source SHA-256 is
`26648a8514a0a9240c831132918c9ad0f735eb7accce33f2287a45961394d538`;
and the complete canonical Lean-output SHA-256 is
`bfff4eb71b922d3feaf598391d55b7e404d8fe5ebbd7c8a5691ce128288a52cf`.
They are recorded in `statement.json` and `statement-receipt.json` and are
independently recomputed by `check_statement.py`. The existing canonical pinned `.lake` symlink was used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Status boundary

This phase proposes only a self-tested statement node and a machine-debt change
from `M5` to `M3`. Human-source debt remains `H4` and readability debt remains
`R4`. The intake's rational-Chow-ring slogan versus rational-Chow-homology
conclusion and its cap/fundamental-class convention remain source-audit debt.
No GRR proof body, anchor audit, obligation tree, proof, validation, release,
audit completion, theorem completion, or master acceptance is claimed.
