# Statement-phase blocker

Item: `S56-M-1097-STATEMENT`  
Theorem: `THM-M-1097`  
Base revision: `888613d9a2a747d4f8fca16dc48f34cc88627ba4`

## Verdict

The exact Lean 4 statement gate is blocked. The source authority supplies only the named theory
"Meyn-Tweedie theory" and the gloss "stability of Markov chains". It does not identify a numbered
theorem or fix its premises and conclusion. The accepted intake consequently and correctly leaves
open whether the target concerns positive Harris recurrence, existence or uniqueness of an
invariant probability, total-variation convergence, or weighted geometric ergodicity.

These are materially different propositions. They also require different choices of discrete or
continuous time, irreducibility and aperiodicity assumptions, small versus petite sets, drift
inequality, accessibility, integrability, and boundary conventions. Selecting one during this
phase would broaden or substitute the source rather than elaborate its exact target. Therefore no
canonical human statement, Lean declaration/expression, normalized expression hash, checked
transport, or meaningful four-class mutation suite can truthfully be emitted.

The primary-source candidate in the intake is the 1993 first edition of Meyn and Tweedie's
*Markov Chains and Stochastic Stability*, but the dossier has no inspected theorem number, page,
definition chain, errata record, or independent statement crosswalk. This is the first failed gate:
canonical source-statement identity, before Lean target elaboration.

## Checked pinned boundary

`StatementProbe.lean` is deliberately not a target candidate. It establishes only that pinned
mathlib exposes kernels, Meyn-Tweedie-style `phi`-irreducibility, invariant measures, and the
reversible-kernel implication. Pinned mathlib documents `Kernel.IsIrreducible` as Meyn-Tweedie
Proposition 4.2.1(ii), page 89. That definition is not a stability theorem and cannot substitute
for this target. A scoped source search found no Markov-kernel definition or theorem for a petite
set, Foster-Lyapunov drift, positive Harris recurrence, or geometric ergodicity.

The environment is Lean `v4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The toolchain and Lake manifest SHA-256 digests are
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No dependency was updated, fetched, built, or otherwise mutated.

## Validation record

All commands ran from the worker clone root unless the command includes `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1097` | 0 | rank 537; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1097/StatementProbe.lean` | 0 | the four pinned substrate declarations elaborated; no target theorem was declared |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | the two digests recorded above |
| `rg -n -i 'petite set\|drift condition\|positive Harris\|Harris recurrent\|geometric ergod' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching Markov-chain stability API in pinned mathlib |
| `git diff --check -- Stage1_Instances/THM-M-1097` | 0 | no whitespace errors |

## Retry condition

An authorized reviewer must first select an exact numbered result from an immutable primary-source
edition and record its page, referenced definitions, all hypotheses and conclusions, errata, and
cross-edition differences. The retry must map that result premise-by-premise to a Lean expression,
minimize imports, serialize the elaborated expression and environment, check every credited
transport, and kill the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations required by rev-5.6.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is not genuinely
self-tested to its completion gate.
