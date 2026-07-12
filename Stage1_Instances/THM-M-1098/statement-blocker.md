# Statement-phase blocker

Item: `S56-M-1098-STATEMENT`

Theorem: `THM-M-1098`

Base revision: `e7fc1469ef5eb468d13c2ccc07a94982bc51ab75`

## Verdict

The exact Lean 4 statement gate is blocked. The repository authority gives only the title "drift
condition", the attribution Meyn/Tweedie (1993), and the gloss "a stability condition for Markov
chains". It does not identify a numbered theorem or fix its hypotheses and conclusion. The intake
therefore correctly records a theorem family rather than a proposition.

Additive Foster-Lyapunov drift, geometric drift, and subgeometric drift are not interchangeable.
Their possible conclusions include recurrence, positive Harris recurrence, existence of an
invariant probability, moment bounds, and different convergence rates. They require materially
different choices of state-space model, small versus petite set, irreducibility, aperiodicity,
accessibility, integrability, constants, and boundary cases. Choosing one here would substitute an
invented target for the source record. Consequently no canonical human statement, exact Lean
declaration or expression, normalized expression hash, checked alternate transport, or meaningful
four-class mutation suite can truthfully be emitted.

The intake names the 1993 first edition of Meyn and Tweedie's *Markov Chains and Stochastic
Stability* as a primary-source candidate, but it contains no inspected theorem number, page,
definition chain, errata record, or independent statement crosswalk. Canonical source-statement
identity is therefore the first failed gate, before target elaboration.

## Checked pinned boundary

`StatementProbe.lean` is deliberately not a target candidate. It checks only that the pinned
environment exposes Markov kernels, Meyn-Tweedie-style `phi`-irreducibility, invariant measures,
and kernel integration needed to encode possible drift inequalities. None of these declarations is
the missing stability implication. A scoped search found no Markov-kernel definition or theorem
for a petite set, Foster-Lyapunov drift condition, positive Harris recurrence, or geometric
ergodicity.

The environment is Lean `v4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The SHA-256 digests of
`Formalizations/Lean/lean-toolchain` and `Formalizations/Lean/lake-manifest.json` are recorded in
the validation table below. No dependency was updated, fetched, built, or otherwise mutated. The
pre-existing untracked `Formalizations/Lean/.lake` symlink was reused without modification.

## Validation record

All commands ran from the worker clone root unless the command includes `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1098` | 0 | rank 538; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1098/StatementProbe.lean` | 0 | the four pinned substrate declarations elaborated; no target theorem was declared |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `rg -n -i 'petite set\|drift condition\|Foster.Lyapunov\|positive Harris\|Harris recurrent\|geometric ergod' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching Markov-chain stability API in pinned mathlib |
| `git diff --check -- Stage1_Instances/THM-M-1098` | 0 | no whitespace errors |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1098/StatementProbe.lean` | 1 | expected content-difference status; no whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1098/statement-blocker.md` | 1 | expected content-difference status; no whitespace diagnostics |

## Retry condition

An authorized source reviewer must first select an exact numbered result from an immutable primary
source edition and record its page, referenced definitions, complete premises and conclusion,
errata, and cross-edition differences. A retry must map that result premise-by-premise to Lean,
minimize imports, serialize the elaborated expression and environment, check every credited
transport, and kill the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations required by rev-5.6.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned statement phase cannot be
genuinely self-tested to its completion gate without an exact source statement.
