# THM-M-1029 proof-phase execution

Item: `S56-M-1029-PROOF`

Date: `2026-07-14`

Base revision: `dd9bc71d70586d022d87833d780fbe15959b89b0`

## Result

`Proof.lean` supplies 23 placeholder-free local theorem bodies. They establish the deterministic-
time compensation normalization; adaptedness and L2/integrability consequences; conditional
increment mean zero and second moment `t-s`; coordinate mean, second moment, and variance; the
zero-elapsed increment law and independence case; Gaussian identification from an exact
characteristic function; and conditional package-composition interfaces.

These bodies are genuine partial proof work, but they do not prove Levy's characterization. In
particular, `GaussianIncrementLawPackage`, `IncrementIndependencePackage`, and
`StrictIncrementLawPackage` are proposition definitions, not proof bodies. The terminal declaration
`root_of_assumedIncrementComponents` still takes the exact missing Gaussian-law and independence
packages as premises. No whole frozen obligation is claimed closed because most relevant registry
targets have only planned fingerprints and the strict-positive analytic bridge is absent.

The exact root therefore remains `H2/M3/R4`, with immediate proof cut `M1029-T-INCREMENTS`.
Conditional first and second moments do not characterize Gaussianity. The missing route requires a
continuous quadratic-variation or equivalent stochastic-calculus bridge, an exponential martingale,
the conditional characteristic function, Gaussian-law identification, and independence from the
past. Pinned mathlib has the endpoints used here but no such bridge or Levy converse.

## Validation

The proof replay copies `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` to a temporary
directory, then invokes the pinned Lean 4.29.0 binary with `--trust=0`. Pinned mathlib's own
`lake env` selects the executable, while the import path contains only existing compiled artifact
directories. This avoids traversal of the unrelated top-level `flt-regular` package, whose shared
checkout was concurrently left at an invalid symbolic HEAD with no worktree. No dependency was
updated, built, cloned, fetched, checked out, or otherwise modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1029` | 0 | rank 222; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1029/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `f5ba78d2...cf0fb4`; root open M3 |
| `bash Stage1_Instances/THM-M-1029/check_proof.sh` | 0 | isolated statement/tree/proof replay passed at trust zero; one frozen composition plus 23 proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 -B Stage1_Instances/THM-M-1029/check_proof.py` | 0 | target, frozen hashes/graph, source hygiene, mathlib pin, receipt, blocker, and handoff consistency passed |
| JSON syntax checks for blocker, receipt, and worker packet | 0 | all structured evidence parsed |
| prohibited-device scan over the three Lean sources | 1 | expected no-match exit; no placeholder, declared axiom, unsafe/oracle, or native shortcut |
| scoped `git diff --check` | 0 | no whitespace errors |

## Status Boundary

This is self-tested partial proof execution and proposes only worker state `[_]` pending integration.
It does not change the accepted instance vector, freeze new obligation signatures, close
`IncrementLawPackage`, or claim the root. Foundation/provenance closure, source and readable review,
downstream validation/release, hermetic cold replay, independent verification, audit completion,
theorem completion, and master acceptance remain open.
