# THM-M-1108 proof-phase attempt

Item: `S56-M-1108-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `d021f11112bde0e0efd8eac22cc92f1e7d610f13`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `Stage1Instances.THM_M_1108.CanonicalStatement` re-elaborates in the pinned Lean
environment. The existing theorem
`canonicalStatement_of_poissonized_depoissonized` is a real checked composition body, but it
accepts `PoissonizedAsymptotics` and `DePoissonizationTransfer` as explicit premises. It proves
neither premise and therefore does not close the root.

The first unavailable frozen mathematical package is `M1108-C-RSK`: the pinned closure has no
checked Robinson-Schensted correspondence with the required LIS/first-row identity. Every later
analytic package is also absent, including the Toeplitz determinant representation,
Riemann-Hilbert steepest descent, Hastings-McLeod identification, uniform edge estimates, and the
fixed-size de-Poissonization bounds. The prerequisite anchor audit found no eligible external Lean
4 proof to pin. The immediate root cut remains `M1108-T-POISSONIZED` plus
`M1108-T-DEPOISSONIZE`.

Introducing either terminal package as an axiom or unproved theorem, or reporting the conditional
composition as the BDJ theorem, would be a placeholder or substituted theorem. The frozen root
therefore remains `M3`, with `root_closed=false` and `theorem_complete=false`. Because the assigned
proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All checks ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1108` | 0 | rank 548; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1108/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `2defff91...0322c8e`; root open M3 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1108/Statement.lean` | 0 | exact target and unfolded transport elaborated; all four negative mutation probes were rejected as expected |
| Compile `Statement.lean` to a temporary local `Statement.olean`, then elaborate `ObligationTree.lean` with `lake env which lean` and the pinned `LEAN_PATH`; remove the temporary olean | 0 | conditional composition elaborated; its axiom report was `[propext, Classical.choice, Quot.sound]`, with no custom analytic axiom |
| `rg -n -i '\\b(baik\|deift\|johansson\|tracy.?widom\|painleve\|hastings.?mcleod\|longest increasing subsequence\|riemann.?hilbert\|robinson.?schensted)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned-mathlib source declaration |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Statement.lean ObligationTree.lean obligation-registry.json` in the owned directory | 0 | `f298aca2...46cc`; `9e8413ff...b5a0`; `308c7cb9...2c16` |

The `sorry` text printed while elaborating `Statement.lean` is Lean's diagnostic rendering for
terms inside `#check_failure`; it is not source syntax or an admitted proof. The scoped source scan
of owned Lean files contains no `sorry`, `admit`, axiom declaration, or unsafe declaration.

## Reopen condition

Resume after implementing the frozen combinatorial and analytic packages without placeholders, or
after locating an immutable compatible Lean 4 BDJ proof whose exact type, terminal bodies,
dependencies, axioms, license, and provenance can all be validated in the pinned environment.
