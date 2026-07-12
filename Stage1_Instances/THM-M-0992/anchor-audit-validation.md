# Anchor-audit validation record

Item: `S56-M-0992-ANCHOR_AUDIT`  
Base revision: `6607e765f4b1b664fa13d7035af8e18567eaf062`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact terminal
declaration `ProbabilityTheory.meas_ge_le_variance_div_sq`. Its event, expectation, variance,
second-moment premise, positive real threshold, and extended-nonnegative conclusion match the frozen
target. The only apparent premise difference is harmless and checked: the mathlib theorem requests
`IsFiniteMeasure`, which Lean obtains from the target's stronger `IsProbabilityMeasure` instance.
`AnchorAudit.lean` independently restates every material clause and elaborates the direct bridge.
The kernel reports only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

The immutable source body reduces the real-variance result to
`ProbabilityTheory.meas_ge_le_evariance_div_sq`; that supporting theorem is an alternate evariance
form, not a substituted root. The historical repository wrapper delegates to the same declaration
and receives no inherited rev-5.6 credit.

A bounded public Sourcegraph search returned 17 matches across mathlib4, historical mathlib3,
`lean-hansen-econometrics@b05e2b8...`, and `atlas-lean@34ffed3...`. The non-mathlib Lean 4 hits consume
the mathlib theorem in weak/strong-law or second-moment developments; they provide no independent
terminal body. Historical mathlib3 is not Lean 4 completion evidence. No external dependency should
be added.

The result is an exact `M0-W` candidate already in the pinned local closure. That candidate label is
pending all later proof-node, transitive provenance/trust, obligation, validation, and release gates;
this phase does not claim theorem proof or completion.

## Commands and results

All commands used the existing toolchain and pinned artifacts. No Lake update/build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0992` | 0 | rank 272, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Moments/Variance.lean` | 0 | immutable module SHA-256 `920c0220...72f0` |
| `rg` over repository-local and pinned dependency Lean sources | 0 | exact theorem and its upstream evariance dependency found; legacy wrappers and downstream consumers classified |
| Sourcegraph query recorded in `anchor-audit.json` | 0 | 17 matches in four repositories; response SHA-256 `befccb5d...081c` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0992/AnchorAudit.lean` | 0 | exact bridge and four declaration probes elaborated; axiom report has no `sorryAx` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0992/Statement.lean` | 0 | frozen target and statement mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-0992/check_anchor_audit.py` | 0 | pin, module hash, target clauses, status boundary, and five candidate classes agree |
| `python3 -m json.tool Stage1_Instances/THM-M-0992/anchor-audit.json >/dev/null` | 0 | audit ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0992 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The node is self-tested pending master acceptance. It supplies no accepted proof node, human-source
`H0`, full transitive trust closure, hermetic replay, independent receipt, or theorem-completion
credit.
