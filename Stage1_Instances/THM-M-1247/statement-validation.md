# Statement validation record

Item: `S56-M-1247-STATEMENT`  
Base revision: `c370639c4481be6bdcec40b9aa3553046d6f7572`.

## Frozen target

`Stage1Instances.THM_M_1247.RellichInequalityTarget` fixes the sharp classical `L2` inequality on
`Fin n -> Real`, with `5 <= n`, product Lebesgue volume, smooth compactly supported test functions,
and support avoiding zero. The Laplacian is the standard-coordinate trace of the second Frechet
derivative. `rellichInequalityTarget_iff_expandedTarget` checks the expanded spelling by definitional
equality. This node does not prove the inequality.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned environment. No dependency
update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1247/Statement.lean` | 0 | target, definitions, definitional transport, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1247/check_statement.py` | 0 | expression SHA-256 `4697dbba...5c90e`; all four structural mutations distinguished |
| remove each direct import in turn and pipe the result to `lake env lean /dev/stdin` | 1 each | removing `ContDiff.Defs` loses `fderiv`; removing `Bochner.Basic` loses integral syntax; removing `Lebesgue.Basic` loses the measure-space instance |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-1247/Statement.lean lean-toolchain lake-manifest.json` | 0 | `0fb5f4dd...bf266`, `651c8acc...b1d2`, `321626c8...2d81` |

The mutations remove a hypothesis, change the domain, change binder scope, or include the excluded
dimension-four boundary. Their explicit kernel renderings are distinct from the canonical target.
This is statement-only evidence pending master acceptance; source, anchor, proof, validation, and
release gates remain open.
