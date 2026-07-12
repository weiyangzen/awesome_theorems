# Statement validation record

Item: `S56-M-0509-STATEMENT`  
Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`

## Frozen target

`Stage1Instances.THM_M_0509.ChenTheoremTarget` freezes the intake-selected classical `P + P2`
claim over natural numbers. One existential threshold precedes the universal even number. The
representation is `N = p + a`, where `p` is prime and `a` is either prime or the product of two
primes. The product witnesses may coincide. Thus the convention counts one or two prime factors
with multiplicity, admits primes and prime squares, and excludes zero and one.

The sole direct import is `Mathlib.Data.Nat.Prime.Basic`. `PinnedSourceShape` directly expands the
chosen target, and `chenTheoremTarget_iff_pinnedSourceShape` checks the expansion. This gate freezes
the exact mathematical target but does not claim that the later source audit has supplied and
independently accepted a primary-source page-level crosswalk.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned Lake environment; no dependency update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0509/Statement.lean` | 0 | target, direct-expansion iff, four mutations, and four boundary theorems elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0509/check_statement.py` | 0 | expression SHA-256 `e2c8d3782d80648aa229dab05f90a84506ed5b6f213fa3083e312674aa6c64f7`; all four mutations distinguished; mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0509/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `fe4685...76a9`, `651c8a...1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0509` | 0 | rank 883, planned, legacy artifacts unaccepted, theorem incomplete |

## Mutation and boundary policy

The validator compares elaborated explicit expressions and rejects removal of evenness, requiring
exactly two prime factors instead of at most two, changing `Nat` to `Int`, and moving the threshold
inside the universal number binder. Kernel-checked boundary theorems admit a prime and a repeated
prime factor while excluding zero and one.

This is statement-only evidence pending master acceptance. It does not prove Chen's theorem or
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
