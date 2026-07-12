# Statement elaboration receipt

Item: `S56-M-0464-STATEMENT`  
Base revision: `9a198a2d8ff0981d17df1c1b8d4b11e4babaf7ed`

## Source freeze

The canonical root is Pila-Wilkie (2006), Theorem 1.8, **first version**, not the family-uniform
Theorems 1.9 or 1.10. A source copy was retrieved from the University of Manchester repository at
`https://eprints.maths.manchester.ac.uk/942/1/The_rational_points.pdf`; its SHA-256 is
`81071938707150caedbcc640cdd426ca8f2ca98bc016aac2dde054d9d45f4d2f`.

The checked source wording fixes `T >= 1`, the affine height `H(a/b) = max(|a|, b)` for a reduced
fraction, coordinatewise maximum height on `Q^n`, `X^alg` as the union of connected
positive-dimensional semialgebraic subsets, and the binder order `X`, `epsilon > 0`, `exists c`,
then the height cutoff. The source merely says "a constant"; the Lean target therefore does not
silently strengthen it to `c > 0`. The target also asserts finiteness before applying `Set.ncard`,
preventing the library's zero value for the cardinality of an infinite set from weakening the claim.

## Validation

Commands were run from the worker clone. The Lean commands used `Formalizations/Lean` as `cwd` so
Lake selected the checked-in toolchain and the existing canonical pinned `.lake` artifacts.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310; planned; L0/rework-required; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0464/Statement.lean` | 0 | `PilaWilkieStatement : Prop`, followed by the fully elaborated `#print`; output SHA-256 `5f467e148ffd7fe060f55e1371cf8be5ce9aee16770c53cb868b6dcf427ecd92` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This receipt supports statement elaboration only. `PilaWilkieStatement` is a definition whose value
is a proposition, not a theorem with a proof. The representation-equivalence obligation for
"positive-dimensional" versus connected non-subsingleton semialgebraic sets, statement mutation
tests, anchor audit, obligation graphs, proof, trust closure, and release evidence remain open.
Accordingly the machine classification advances only from `M4` to `M3`; theorem completion is
false and master acceptance is still required.
