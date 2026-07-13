# THM-M-0487 proof-phase attempt

Item: `S56-M-0487-PROOF`

Date: `2026-07-13T23:45:55+08:00`

Base revision: `4a10a7a4ddff88e302d5a303b16dd687d9468f63`

## Verdict

`blocked`: no eligible proof body for the exact weak Goldbach target exists in the repository or
pinned dependency closure. The frozen minimal open root cut is
`M0487-T-ANALYTIC` together with `M0487-T-FINITE-UPPER`. The first package is the complete
analytic proof for odd inputs at and above `10^27`; the second is the exact finite theorem through
`8875694145621773516800000000000`, including the prime-ladder data, primality certificates,
finite binary Goldbach verification, exhaustive coverage, and a sound replay checker.

`ObligationTree.lean` contains genuine unconditional bodies for the cutoff split and endpoint
arithmetic, plus checked conditional restriction and root-composition theorems. The latter consume
`AnalyticRangePackage` and `FiniteUpperBoundPackage`; they construct neither package. Returning one
of those conditional theorems as the result would substitute an assumed implication for the
canonical target.

The prerequisite immutable audit found no valid import route. Pinned mathlib has supporting prime
distribution APIs but no terminal three-primes theorem. Formal Conjectures has the exact pointwise
type with a literal `by sorry`; PrimeNumberTheoremAnd is bounded and has placeholder ancestry;
foolishair/Goldbach supplies an equivalent statement, conditional scaffolding, and small finite
checks only; goldbach_tm concerns binary Goldbach. No candidate may be wrapped or credited.

No proof body, axiom, placeholder, unsafe declaration, weakened theorem, or dependency was added.
The root remains `[H1, M3, R3]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned proof phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing canonical pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok`; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0487` | 0 | rank 1366; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0487/Statement.lean` | 0 | The exact canonical target and transports elaborated; the four intentional `#check_failure` mutation diagnostics appeared as expected |
| Isolated `Statement.olean` followed by `ObligationTree.lean` using the pinned Lean binary and `LEAN_PATH` | 0 | Cutoff, endpoint coverage, conditional finite restriction, conditional root composition, and exact decomposition elaborated; the printed axiom reports contain only `propext` |
| `rg -n -i 'weak.?goldbach\|ternary.?goldbach\|three.?prime\|sum.{0,30}three.{0,30}prime\|goldbach' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only an unrelated Fermat-number docstring matched; no terminal weak/ternary Goldbach proof was found in the pinned Lean sources |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0487 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited declaration or proof escape occurs in the owned Lean modules |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `sha256sum` on `Statement.lean`, `ObligationTree.lean`, `obligation-registry.json`, and `anchor-audit.json` | 0 | `9d020004...090b0d`; `296af729...338f8`; `6fc1d3df...6052f`; `569ce7bc...99f36` |
| `python3 Stage1_Instances/THM-M-0487/check_obligation_tree.py` | 1 | The prior phase validator has a stale hardcoded expectation that its own authoritative DAG item is `[ ]` with zero attempts; the integrated DAG now records `S56-M-0487-OBLIGATION_TREE` as `[_]` with one attempt. This is a validator freshness failure, not proof evidence or a mathematical failure. |

Exact isolated elaboration recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0487
tmp=$(mktemp -d /tmp/thm-m-0487-proof-attempt.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" ObligationTree.lean
```

The pre-existing untracked `Formalizations/Lean/.lake` entry is the automation-provided symlink to
the canonical artifacts and was reused read-only.

## Reopen condition

Resume only after placeholder-free implementations of `M0487-T-ANALYTIC` and
`M0487-T-FINITE-UPPER` with their frozen dependencies, or discovery of an immutable compatible
Lean 4 proof that can be pinned, transported to the exact target, and checked for terminal-body
provenance, transitive axioms and TCB, computation coverage, and exact composition.
