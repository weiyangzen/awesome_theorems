# Statement validation record

Item: `S56-M-0110-STATEMENT`  
Base revision: `705caafffbcdaf43757a4468b018716da692307d`

## Frozen target

`Stage1Instances.THMM0110.KodairaVanishingTarget` states the intake-selected
algebraic form: for an integral scheme smooth and projective over a
characteristic-zero field, and an ample invertible sheaf `L`, every positive
degree of the concrete pinned `Sheaf.H` cohomology of `omega_X tensor L` is
subsingleton. The universe, ordered binders, hypotheses, degree range, and
encoding boundary are recorded in `statement.json`.

The pinned snapshot lacks native combined definitions for projective scheme
morphisms, canonical or dualizing sheaves, ample invertible sheaves, and their
tensor product. These are explicit semantic predicates over actual mathlib
`Scheme` and `Scheme.Modules` carriers. The cohomology family is not an opaque
interface: `KodairaVanishingData.Cohomology` reduces to `Sheaf.H` of the
underlying abelian sheaf. No data field contains the vanishing conclusion.

## Import minimization

The module has five direct imports and no aggregate `Mathlib` import:

- `Mathlib.AlgebraicGeometry.Modules.Sheaf` supplies `Scheme.Modules` and
  `SheafOfModules.toSheaf`.
- `Mathlib.AlgebraicGeometry.Morphisms.Smooth` supplies the concrete smoothness
  and integral-scheme surface.
- `Mathlib.CategoryTheory.Sites.SheafCohomology.Basic` supplies `Sheaf.H`.
- `Mathlib.Topology.Sheaves.Abelian` and
  `Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt` jointly provide
  the concrete `HasExt` instance needed to elaborate `H` at the pinned default
  heartbeat limit. Removing either leaves that typeclass obligation unresolved.

## Mutation evidence

Four independently elaborated propositions change one required statement
dimension: removing ampleness, removing characteristic zero, moving and
weakening the degree binder, and including degree zero. Lean rejects each
mutation as a term of the canonical target using `#check_failure`, and
`check_statement.py` additionally requires every fully explicit expression to
differ from the canonical expression.

## Commands and results

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard/manifest projection passed for 1546 uniform-L0 targets |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| repository root | `python3 scripts/stage1_target.py show THM-M-0110` | 0 | Rank 34, planned, legacy artifacts unaccepted, theorem incomplete |
| `Formalizations/Lean` | `lake env lean ../../Stage1_Instances/THM-M-0110/Statement.lean` | 0 | Canonical target, expansion, four mutation rejections, explicit print, and axiom print elaborated |
| repository root | `python3 Stage1_Instances/THM-M-0110/check_statement.py` | 0 | Imports, DAG identity, five explicit expressions, mutation distinctions, and three fingerprints reconciled |
| repository root | `python3 -m json.tool Stage1_Instances/THM-M-0110/statement.json >/dev/null` | 0 | Valid JSON; `statement-receipt.json` passed separately |
| repository root | forbidden Lean-source token scan recorded in `statement-receipt.json` | 1 | No matches; `rg` exit 1 means no match |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0110 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The canonical explicit expression SHA-256 is
`d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6`;
the statement source SHA-256 is
`81e89341fc571e588c47c8984d71779fd4b90b2cd55ae70c3392c742655574dd`;
the complete canonical Lean-output SHA-256 is
`f68a44c380be94e6e3db98da208c0058b98a5013fabde12dd7ca207974301842`.

The structured checker independently re-elaborates the canonical target and
all four mutations, checks the authoritative item identity and ownership,
pins direct imports and environment metadata, and reconciles source, explicit
expression, and complete Lean-output SHA-256 fingerprints.

## Status boundary

This phase can propose only a self-tested statement node. It provides no
Kodaira proof body or proof credit. Source fidelity remains `H1`, machine debt
remains `M3`, readability remains `R3`, and `audit_complete` and
`theorem_complete` are both false. The provisional intake dependency, this
node, and all downstream nodes still require dependency-ordered master
acceptance or execution.
