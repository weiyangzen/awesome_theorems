# THM-M-0914 statement validation

Item: `S56-M-0914-STATEMENT`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a` (tree
`fdfff18dea4c6798c5b322b6088dfe556109c134`)

## Frozen target

`Stage1Instances.THM_M_0914.PigeonholeTarget` says that for every `n : Nat` and total placement
`f : Fin (n + 1) -> Fin n`, there are distinct `x` and `y` with `f x = f y`. This is the literal
catalog family, not the broader arbitrary-finite-type theorem. The checked iff
`pigeonholeTarget_iff_boxWitnessTarget` names the shared box explicitly.

The target, transport, mutations, and boundaries require no direct imports: they elaborate from
the Init prelude of the pinned Lean 4.29.0 toolchain. No mathlib pigeonhole theorem is imported or
invoked. The `n = 0` case remains included and vacuous because no function `Fin 1 -> Fin 0`
exists. The `n = 1` boundary is the first inhabited collision case.

## Commands and results

All commands ran inside this worker clone. The automation-provided canonical `.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0914` | 0 | rank 1456, planned, no legacy slot, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...ea95`, tree `bdc39a31...5c2b` |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0914/Statement.lean)` | 0 | exact target, checked iff, four expected mutation type rejections, two boundary witnesses, axiom reports, and explicit expression elaborated |
| `(cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0914/check_statement.py --worker-packet ../../.stage1-worker-selftest.json)` | 0 | expression SHA-256 `faef4a7f...ae3b`; source `953cf5ba...33db`; all four mutations differed; empty import set, packet, inventories, and pins agreed |
| `python3 -c` exact JSON parse over the root packet and every owned `*.json` | 0 | validated 6 JSON files |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0914-pycache python3 -m py_compile Stage1_Instances/THM-M-0914/check_statement.py` | 0 | validator compiled without generated files under the owned path |
| scoped prohibited-construct scan over `Statement.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom/bodyless/opaque/unsafe declaration, TODO, FIXME, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0914 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The historical `check_intake.py` replay is intentionally superseded because statement freeze
changes the mutable dossier projection; it now exits nonzero with that explicit status. Current
replay authority is `check_statement.py` plus `statement-receipt.json`; the original intake
observations remain historical and unaccepted.

## Mutation and boundary policy

The target has no antecedent to remove. The removed-contract mutation therefore drops the required
distinctness conjunct. The domain mutation changes `n + 1` objects to `n + 2`, the binder-scope
mutation selects the object pair before the placement, and the boundary mutation adds `0 < n`.
Each mutation is rejected at the canonical exact type and has a distinct fully explicit expression.

The checked shared-box transport reports no axioms. The two boundary witnesses report only
`propext`. These are statement-level observations, not proof-body or transitive trust closure.

## Status boundary

This is provisional statement evidence pending master acceptance. The source-of-record and H0
review, formal anchor and terminal-body provenance audit, obligation freeze, proof, composition,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, release,
audit completion, and theorem completion remain open.
