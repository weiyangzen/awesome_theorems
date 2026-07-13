# THM-M-1140 proof-phase recheck at 8c4a58ee

Item: `S56-M-1140-PROOF`  
Intent: `prove`  
Base revision: `8c4a58ee73da7fa8dce7a9f9bfcc0ec5fd713588`  
Base tree: `3fa6104e948efe18f95dcfc23e9d2bf7f3dad150`  
Recorded at: `2026-07-14T03:10:29+08:00`

## Verdict

`blocked`. The exact proof phase remains open at the arbitrary-dimensional
`InteriorLocalRigidity` package. No placeholder-free local proof or eligible pinned import was found,
so the root remains `[H2, M3, R3]` and this item remains `[ ]`. This artifact is blocker evidence,
not a proof receipt, audit-completion claim, theorem-completion claim, or master acceptance.

The target quantifies over every `n : Nat`: a real-valued `HarmonicOnNhd` function on a nonempty,
connected, open subset of `EuclideanSpace Real (Fin n)` which attains a maximum at a domain point is
constant throughout the domain. A complex-plane specialization, a positive-dimension restriction,
or a supplied local-rigidity premise would not close this frozen proposition.

## Closed Support And Open Cut

`Proof.lean` genuinely proves `ConnectedLevelPropagation`: the maximum-level set is nonempty,
closed by continuity, open by the supplied local-rigidity neighborhoods, and therefore all of the
connected domain subtype. `ObligationTree.lean` genuinely composes that result and a supplied
`InteriorLocalRigidity` into the exact root. Neither declaration constructs the analytic package.

The remaining root cut is:

1. `M1140-L-MEAN-VALUE`: an analytic local-equality mechanism.
2. `M1140-T-LOCAL-PACKAGE`: an inhabitant of `InteriorLocalRigidity`.
3. `M1140-ROOT`: exact composition after the local package closes.

Pinned mathlib supplies arbitrary-dimensional harmonic definitions, `C^2` regularity, continuity,
and algebraic closure, but not a matching general mean-value theorem, harmonic analyticity, unique
continuation, local rigidity, or strong maximum theorem. `HarmonicOnNhd.circleAverage_eq` and
`HarmonicAt.analyticAt` are specialized to `Complex -> Real`.

The adjacent `THM-M-1138` strict-subharmonic perturbation does prove a general weak maximum
principle on bounded balls. A fresh attempted upgrade was rejected rather than recorded as a proof:
the weak principle yields `u z <= u y` on each concentric sphere, which is the already-known
direction and not the reverse inequality required for local constancy. Closing that route still
requires a mean-value, Harnack, unique-continuation, or full Hopf-barrier argument. The immutable
Atlas candidate remains ineligible because its harmonic-to-mean-value chain contains unproved
bodies and opaque analytic objects.

## Validation

All successful Lean checks used existing pinned compiled artifacts. Source copies and generated
oleans were confined to `/tmp` and removed. The manual `LEAN_PATH` replay was used because the
shared canonical `flt-regular` checkout was incomplete when validation ran; no dependency fetch,
update, build, or `.lake` repair was performed by this worker.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; lifecycle `planned`; theorem incomplete |
| isolated direct Lean 4.29.0 `--trust=0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` with the existing Lake artifact paths | 0 | All three modules elaborated; the two checked proof declarations use only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | 16 obligations and 36 typed edges passed; denominator `355cbcf...0bee`; frozen root open at `M3` |
| `rg -n '^\\s*(sorry\\|admit\\|axiom\\|unsafe)\\b\\|\\bsorryAx\\b'` over the three Lean modules | 1 | Expected clean no-match |
| `$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent |

The isolated replay was equivalent to the prescribed `lake env lean` check but invoked the pinned
Lean binary directly and assembled `LEAN_PATH` from the already-built project, mathlib, Batteries,
Qq, Aesop, ProofWidgets, ImportGraph, LeanSearchClient, and Plausible artifact directories. It used
`--trust=0` on each module and did not include the incomplete `flt-regular` checkout because the
target's import closure does not depend on it.

Pinned environment: Lean commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Resume positive proof work only with a placeholder-free arbitrary-dimensional harmonic
local-rigidity implementation, or an immutable compatible Lean 4 theorem whose transitive proof
closure can be pinned, exact-type transported, provenance-audited, and kernel-checked without
changing the target. Because the assigned phase is not complete, no
`.stage1-worker-selftest.json` is written.
