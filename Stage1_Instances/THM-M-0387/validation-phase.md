# S56-M-0387-VALIDATION worker evidence

Date: `2026-07-12`. Base revision: `2e3a5d5130638c6983d4febfd040ca94571e2f68`.

The structured recipes in `validation-spec.json` re-elaborate the frozen target and every proof body
admitted by the proof phase. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
those declarations. Source hygiene has no `sorry`, `admit`, `sorryAx`, `axiom`, or `unsafe` match.
The local mathlib and flt-regular revisions are respectively
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, and both dependency worktrees are clean.

This validation fails closed at the exact root. `target_of_odd_prime_exponents` is conditional;
`M0387-WTW` has no eligible proof body, so the root remains `M2`. A release-grade hermetic check was
not run: this clone uses the canonical warm `.lake` through a symlink, rather than a fresh empty
cache. Independent validation also cannot pass because there is only this worker, this checkout, and
the shared writable cache. The separately implemented `check_validation.py` checks the evidence
shape and open-root decision, but it is not a distinct independently provisioned runner.

## Commands and results

All commands were run from the repository root unless the command contains an explicit subshell.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok` with 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1; planned; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e...` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Statement.lean)` | 0 | exact target elaborated |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0387/Proof.lean)` | 0 | five declarations elaborated; axiom lists recorded in `validation-receipt.json` |
| `python3 Stage1_Instances/THM-M-0387/check_statement.py` | 0 | four mutations killed; expression hash `8e0d406e...13c1` |
| `python3 Stage1_Instances/THM-M-0387/check_obligation_tree.py` | 0 | 132 obligations, 140 edges, root open M2 |
| hygiene `rg` over `Statement.lean` and `Proof.lean` | 1 | expected no-match result |
| `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 0 | handoff consistent; open root and failed release gates preserved |

The network-dependent anchor checker was attempted with a 90-second bound but did not produce a
successful receipt; remote provenance is therefore not claimed by this phase. The locally pinned
source and declaration checks remain the only provenance result admitted here.

First failed theorem gate: `proof.root_kernel_closure`. Additional release failures are
`hermetic.cold_empty_cache` and `independent.distinct_runner`. No theorem completion is claimed.
