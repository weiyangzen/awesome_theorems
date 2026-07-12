# Anchor audit

## Scope and outcome

At the `2026-07-12T11:41:10Z` cutoff, the bounded search found no exact Lean 4 proof of
`Stage1Instances.THM_M_0347.FejerTheoremTarget`. The target therefore remains `M3`: its exact
statement elaborates, while no repo-local, pinned-mathlib, or immutable external candidate closes
it. This document completes only `S56-M-0347-ANCHOR_AUDIT`; it gives no theorem-completion credit.

Search order followed rev-5.6 section 7.2: repo-local sources, pinned mathlib, official/public Lean
projects, then public project registries. Queries included `Fejer`, `Fejer`, `Cesaro`, `Cesaro`,
`Fourier`, `fejerKernel`, declaration-name variants, and translated repository metadata. GitHub
code search required authentication and grep.app became rate-limited, so this is reproducible
bounded negative evidence, not an exhaustive-discovery claim. GitLab returned no project.

## Pinned mathlib candidates

Mathlib is fixed at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

| Candidate | Exact comparison | Decision |
|---|---|---|
| `hasSum_fourier_series_of_summable`, `Mathlib/Analysis/Fourier/AddCircle.lean` | Requires `Summable (fourierCoeff f)` and proves a bilateral `HasSum`. The canonical target permits every continuous `f` and asks for symmetric Cesaro means. | Related API only; no M0/M1 credit. |
| `Filter.Tendsto.cesaro_smul`, `Mathlib/Analysis/Asymptotics/SpecificAsymptotics.lean` | Requires the sequence being averaged already to converge. That premise cannot be assumed for the Fourier partial sums in Fejer's theorem. | Generic bridge only; no M0/M1 credit. |

`AnchorAudit.lean` checks both exact declaration types, typed uses, and their axiom profiles. Both
wrappers report only `propext`, `Classical.choice`, and `Quot.sound`. A source-tree alias search
found no declaration or documentation named Fejer/Fejer in pinned mathlib.

## External candidate

GitHub repository search returned `BryceT233/L1-convergence-of-Fejer-sum`. It was inspected without
cloning at verified commit `2718c05d5ab6beca24f7f5df2e86f673a0550e1f`, tree
`83db828a8bb2bd6fbeab1d5c0bd483af3f5db873`, Apache-2.0. Its sole Lean source is
`fejer_L1.lean`, blob `e0fc7960bfcf2533ab0eee9983840ceffad125b3`, SHA-256
`c856b60abe160bc73a95e8a735e786c17526c4a51df594c1688d6f61615a18b7`.

Its main `Fejer_L1` theorem is not the canonical target: it fixes `AddCircle (2 * pi)`, assumes an
integrable function, expresses Fejer means through convolution, and concludes L1 convergence to
`(2 * pi) • hf.toL1`, not uniform convergence to a continuous function for arbitrary positive
period. More decisively, its `aux_cmul` declaration is explicitly sorry-backed. A direct check of
the immutable source against the pinned environment exited 1 with multiple elaboration failures
and `warning: declaration uses sorry` at upstream line 345. It is therefore a different,
unchecked target and not a dependency or integration candidate.

## Validation ledger

All commands ran from repository base `cc46a50150dae27c90dca0938294d8da17db9109`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0347/AnchorAudit.lean` | 0 | Both pinned candidate types and wrappers elaborated; axiom profiles printed. |
| `curl .../fejer_L1.lean -o /tmp/THM-M-0347-fejer_L1-2718c05.lean && cd Formalizations/Lean && timeout 120 lake env lean /tmp/THM-M-0347-fejer_L1-2718c05.lean` | 1 | Immutable upstream source failed elaboration and exposed a sorry-backed declaration. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure OK: 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest OK: 1546 unique targets, ranks 1..1546. |

Machine debt remains `M3`; human debt remains `H1`; readability remains `R4`. The next proof phase
must build the Fejer-kernel/approximate-identity route locally or identify a new exact,
placeholder-free immutable closure. No `repo_local_integration_debt` is created because no exact
external closure was found.

