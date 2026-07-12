# Statement validation record

Base revision: `c03519b15d342c7ab9b4fab75bfaa01ed0015c8e`.

Pinned environment:

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256 `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Environment fingerprint SHA-256 `cec5b3566157a30c0adf598fe6fbf307453e7e141d0e8074c95d98c1c6d6c78e` binds the toolchain, mathlib revision, three imports, options, and foundation profile listed in `intake.json`.

Run Lean commands from `Formalizations/Lean`. The clone's `.lake` is a link to the canonical pinned
artifacts; no dependency update or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 1546 uniform-L0 Lean 4 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1520` | 0 | rank 189; planned; L0/rework-required; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1520/Statement.lean` | 0 | target elaborated; `#check` reports `LiouvilleStatement : Prop`; `pp.all` expression output SHA-256 is `547fe7d61d57e7ea242aaff7a97763a769275f0c6f1c64d03ca5db45e82a012b` |
| `lake env lean --deps ../../Stage1_Instances/THM-M-1520/Statement.lean` | 0 | direct compiled imports are exactly the three modules declared in `Statement.lean`; output SHA-256 `e3cb135960df0a13df88977882bfefd2242859848ffd66c60274c25ed1571f8a` |
| `lake env lean -R ../../ ../../Stage1_Instances/THM-M-1520/Statement.lean -o ../../Stage1_Instances/THM-M-1520/Statement.olean; P=$(lake env printenv LEAN_PATH); for f in MutationRemovedHypothesis MutationChangedDomain MutationChangedBinderScope MutationExcludedBoundary; do LEAN_PATH="../..:$P" lean "../../Stage1_Instances/THM-M-1520/$f.lean"; done; rm ../../Stage1_Instances/THM-M-1520/Statement.olean` | statement 0; mutation 1 each | each deliberately false `rfl` identity is rejected: removed `C2 H`, fixed domain `n = 1`, moved time binder, and excluded `n = 0` are not definitionally the canonical target |
| `python3 -m json.tool Stage1_Instances/THM-M-1520/intake.json >/dev/null` | 0 | structured statement record is valid JSON |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1520; test $? -eq 1` | 0 | no forbidden proof devices or axiom declarations |
| `git diff --check -- Stage1_Instances/THM-M-1520 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Boundary

This receipt validates statement elaboration only. The target specializes the intake's geometric
formulation to canonical coordinates and complete flows because pinned mathlib has no manifold
symplectic-form/local-flow API sufficient to express the stronger form without inventing an opaque
interface. A checked manifold-to-coordinate transport is not credited. There is no proof of
`LiouvilleStatement`; machine status is `M3`, theorem completion is false, and master acceptance is
pending.
