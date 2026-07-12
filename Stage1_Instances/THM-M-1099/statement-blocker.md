# Statement-phase blocker

Item: `S56-M-1099-STATEMENT`  
Theorem: `THM-M-1099`  
Base revision: `d83bcd9bb91558d5f3e2cd99f964cc161d7a0cc5`

## Verdict

The exact Lean 4 statement gate is blocked. The repository authority provides only the topic label
"petite set", the gloss "small sets and ergodicity", the attribution Meyn/Tweedie, and the year
1993. It provides no numbered result, page, exact premises, or conclusion. In particular, it does
not decide among the definition of a petite set, the implication from small to petite, a theorem
about petite sets for an irreducible or T-chain, or an ergodicity criterion involving a petite set.
Those are different propositions, not alternate spellings of one proposition.

The accepted intake also leaves open the state-space hypotheses, transition-kernel iteration and
sampling conventions, minorizing measure, irreducibility/aperiodicity/recurrence assumptions, and
the meaning of ergodicity. Selecting those choices here would invent or substitute mathematics.
Consequently there is no truthful canonical human statement from which to produce an exact Lean
expression, normalized expression hash, checked transports, or the four required semantic mutation
tests. The first failed gate is canonical source-statement identity, before Lean elaboration.

The primary-source candidate is the 1993 first edition of Meyn and Tweedie's *Markov Chains and
Stochastic Stability*, but the owned dossier contains no inspected theorem number, definition
chain, page, errata record, or independent statement crosswalk. The source's existence cannot fill
in those missing choices.

## Checked pinned boundary

`StatementProbe.lean` is deliberately not a target candidate. It checks only that the pinned Lean
environment exposes a Markov-kernel type, its Markov typeclass, kernel composition, and the
Meyn-Tweedie-style irreducibility predicate. A scoped search found no Markov-chain declaration
named for petite sets, sampled-kernel minorization, positive Harris recurrence, or geometric
ergodicity in pinned mathlib. Matches for `smallSets` belong to the unrelated order-filter notion.

The environment is Lean `v4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The toolchain and Lake manifest SHA-256 digests are
recorded in the validation table below. No dependency was updated, fetched, built, or modified.

## Validation record

All commands ran from the worker clone root unless the command includes `cd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1099` | 0 | rank 539; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1099/StatementProbe.lean` | 0 | four pinned substrate declarations elaborated; no target theorem was declared |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; manifest `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `rg -n -i 'petite|minorization|minorisation|sampled kernel|positive Harris|Harris recurrent|geometric ergod' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability --glob '*.lean'` | 1 | no matches in the pinned probability library |
| `git diff --check -- Stage1_Instances/THM-M-1099` | 0 | no whitespace errors |

## Retry condition

An authorized source reviewer must select and inspect an exact numbered result in an immutable
edition, recording its page, referenced definitions, all hypotheses and conclusion, errata, and
cross-edition differences. A retry can then map it premise-by-premise to Lean, minimize imports,
serialize the elaborated expression and environment, check credited transports, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This artifact does not complete the statement node, accept a receipt, or claim theorem completion.
No `.stage1-worker-selftest.json` is emitted because the assigned statement phase cannot genuinely
pass its completion gate without an exact source proposition.
