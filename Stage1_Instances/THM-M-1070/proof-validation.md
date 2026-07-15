# THM-M-1070 proof execution

Item: `S56-M-1070-PROOF`
Date: `2026-07-15` (`Asia/Shanghai`)
Base revision: `111bbeb1a210ae4e8525a4342012921ab60e466f`

## Verdict

`no_state_change`: partial proof work is self-tested, but the frozen root remains blocked.
`Proof.lean` retains exact introduction and elimination bodies for the six-clause conjunction and
now proves two substantive boundary results. `isLevyProcess_zero` constructs the zero process on
any supplied probability space. Its proof establishes marginal measurability, almost-everywhere
zero, joint finite-family independence, stationary increments, and stochastic continuity rather
than assuming those clauses. `zeroMeasure_not_isLevyProcess` proves that no process over the zero
measure satisfies the predicate.

Neither new result closes a frozen obligation. The registered root is `IsLevyProcess P X` for
arbitrary `P` and `X`; all six registered leaves retain those arbitrary parameters. Specializing
to the zero process and requiring `IsProbabilityMeasure P` changes that target, while the checked
zero-measure result refutes any unconditional arbitrary-`P` interpretation. Thus zero frozen
obligations are provisionally or accepted closed, the root remains `M3`, and the assigned proof
phase is not complete. The worker manifest records only the self-tested partial contribution.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake artifacts read-only. No
update, build, dependency clone/fetch, network access, or `.lake` mutation was performed. Compiled
objects were created only under `/tmp` and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1070` | 0 | rank 512; lifecycle planned; hard-mathlib lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1070/check_obligation_tree.py` | 0 | 13 obligations and 26 typed edges passed; denominator `c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9`; root remains open M3 |
| `bash Stage1_Instances/THM-M-1070/check_proof.sh` | 0 | trust-zero isolated replay checked four local declarations; every axiom report was exactly `propext`, `Classical.choice`, and `Quot.sound` |
| prohibited-device scan over `Proof.lean` | 1, expected | no `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/opaque/extern escape, `implemented_by`, or `native_decide` |
| focused search in pinned mathlib | 1, expected | no exact Levy-process declaration or proof body |
| `python3 -m json.tool` on `proof-blocker.json` and `proof-receipt.json` | 0 | both proof evidence records are valid JSON |
| `python3 Stage1_Instances/THM-M-1070/check_proof.py` | 0 | hashes, pins, source hygiene, receipt boundary, blocker, manifest, and changed paths passed |
| `git diff --check -- Stage1_Instances/THM-M-1070 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Reopen condition

Reopen the statement and architecture to freeze a theorem about a specified process or an
existence proposition, then refreeze the statement-dependent registry and graphs before renewed
proof execution. An immutable exact compatible Lean result could instead be pinned and checked
after that repair. The audited LeanLevy near-match remains ineligible because its conventions and
dependency status do not match this target.

Status boundary: self-tested partial local proof evidence only. No frozen obligation, root,
validation phase, release gate, master acceptance, audit completion, or theorem completion is
claimed.
