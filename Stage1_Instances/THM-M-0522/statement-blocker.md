# Exact-statement gate: blocked

Item: `S56-M-0522-STATEMENT`  
Theorem: `THM-M-0522`  
Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`

## Decision

The inherited provisional intake dossier fixes the intended human claim: for every elliptic curve
`E/Q`, analytic rank
at most one implies equality of analytic and Mordell-Weil ranks and finiteness of `Sha(E/Q)`. The
first failed gate is not theorem-name selection but availability of native Lean objects for that
claim.

The pinned mathlib closure provides `WeierstrassCurve`, the additive group `E⟮ℚ⟯`, generic
complex `LSeries` and derivative infrastructure, and a Dedekind-domain Selmer group. It does not
provide the elliptic-curve Hasse-Weil L-function and its analytic order at `s = 1`, or the
Tate-Shafarevich group defined through the required global-to-local Galois cohomology. Nor is there
a curve-specific Mordell-Weil finite-generation/rank package connecting `E⟮ℚ⟯` to the intended
natural-valued algebraic rank.

The generic `LSeries` is not canonically attached to `E`, and
`IsDedekindDomain.selmerGroup` is not the Galois-cohomological Selmer or Tate-Shafarevich group in
the theorem. The legacy `S1_M_091` file states that its analytic-rank, Mordell-Weil-rank, and Sha
components are abstract data or proposition fields. Importing those fields would violate the
owned intake's requirement that these objects be native and explicit. A Heegner-point conditional
or the rank-one branch alone would instead weaken the selected root.

It is therefore impossible in this pinned closure to form the exact proposition without first
implementing substantial missing definitions or pinning a proof ecosystem that supplies them.
`StatementProbe.lean` checks only the available adjacent vocabulary and deliberately declares no
canonical target. Since there is no target expression, there can be no expression fingerprint,
checked alternate transport, or meaningful removed-hypothesis, changed-domain, changed-scope, and
rank-zero/one/two boundary mutations. Machine state remains `M3`; statement acceptance, audit
completion, and theorem completion are false.

## Environment

- Validation date: 2026-07-12 (Asia/Shanghai).
- Repository state: nonrelease evidence; the automation clone began with the untracked canonical
  `.lake` symlink.
- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
  Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Statement probe SHA-256:
  `b9f873c84a4347391b2c93ff9316fac21e829df531159bdaec873463dd2e428e`.
- The existing `.lake` artifacts were used read-only. No update, build, clone, fetch, or other
  dependency mutation was run.

## Validation evidence

Commands ran from the worker repository root unless the command begins with `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0522` | 0 | rank 894, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0522/StatementProbe.lean` | 0 | rational-point `AddCommGroup` and generic `LSeries`/`iteratedDeriv` substrate checks elaborated |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions match the fingerprint above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision matches the pin above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0522/StatementProbe.lean` | 0 | all three hashes match the fingerprint above |
| `rg -n -i 'Kolyvagin\|Gross.?Zagier\|Tate.?Shafarevich\|Shafarevich\|Hasse.?Weil\|analyticRank\|analytic_rank' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching theorem-specific or native analytic/Sha vocabulary in pinned mathlib; exit 1 is `rg` no-match |
| `rg -n -i 'Mordell.?Weil' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only two prose lines in `GroupTheory/Descent.lean`; no elliptic-curve rank declaration |
| `rg -n '\b(sorry\|axiom\|admit\|unsafe)\b' Stage1_Instances/THM-M-0522/StatementProbe.lean` | 1 | no prohibited Lean token; exit 1 is `rg` no-match |

## Retry condition

Implement or pin immutable Lean 4 definitions for the elliptic Hasse-Weil L-function and its order
at one, the Mordell-Weil rank bridge, and the Tate-Shafarevich group, with the intake's normalization
and all-elliptic-curves-over-`ℚ` scope. A later statement run can then elaborate and serialize the
exact expression, compile checked transports, and execute all four required mutation classes.

This is a truthful blocker, not completion of this node or a later node. The assigned phase is not
genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
