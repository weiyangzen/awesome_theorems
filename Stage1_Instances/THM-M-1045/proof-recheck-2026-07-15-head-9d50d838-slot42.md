# THM-M-1045 proof phase: current-base blocker

Item: `S56-M-1045-PROOF`

Intent: `prove`

Base revision: `9d50d838c8132b2aaf005a4863baeb5385e52a97`

Base tree: `ef268baf236c1fe55806a57847c7f78ed6587b9d`

Rechecked: `2026-07-15T15:21:05+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible positive proof body can establish the exact frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`. The proof item remains `[ ]`, and no root
`.stage1-worker-selftest.json` is written.

The root quantifies over every `WienerData`, but `WienerData.paleyWienerIntegral` is constrained
only by measurability. The checked `ProofBlockerCurrent.lean` preserves every Wiener-law field,
replaces only that field by the measurable constant-one pairing, and proves:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At `h = 0` and `g = 0`, the frozen density branch makes the self Radon-Nikodym derivative equal
`ENNReal.ofReal (Real.exp 1)` almost everywhere, while `Measure.rnDeriv_self` makes it equal one.
The checked exact characterization is:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

The blocker does not independently prove `WienerData` inhabited. Its reverse characterization
branch is empty elimination, a vacuous interface-emptiness result rather than a proof of the
Cameron-Martin theorem. It is ineligible under the exact-target and no-substitution gates. The
frozen repo-local and pinned-package candidate inventory contains no exact positive proof or import.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`, invalidating
`M1045-L-PALEY-WIENER` and blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
The fail-closed vector proposed for master reconciliation is `[H1, M3, R3] -> [H1, M5, R3]`.
Separately, predecessor `S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`.

Two other statement risks remain. The path measurable-space encoding comaps `top`, producing the
top/discrete measurable space on `WienerPath` rather than the advertised cylinder/Borel
sigma-algebra. The selected `timeMeasure` pushes all real volume through `Real.toNNReal`, sending
the negative half-line to zero and giving the singleton zero infinite mass rather than ordinary
volume on `NNReal`.

Positive proof work can resume only after a source-justified statement revision constructs or
constrains the Paley-Wiener integral without assuming the desired conclusion, corrects or justifies
the measure encodings, publishes a fresh target fingerprint, and refreezes the dependent anchor
audit and a version-2 obligation registry and typed graphs.

Eleven prior dated blocker/recheck JSON-plus-Markdown packet pairs predate this run (not counting
the standalone `proof-blocker.md`), but the authoritative DAG still records zero proof attempts and
no children. Packet count alone does not establish five scheduler execution ticks. This worker did
not edit that authority. Because the failed node is the predecessor statement rather than a
divisible proof leaf, the master should reopen the statement dependency and stop scheduling
unchanged proof-root retries.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation ran. The narrow proof replay used stdin and wrote no
Lean object output.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, legacy artifacts unaccepted, theorem incomplete. |
| `timeout --foreground 600 python3 -B Stage1_Instances/THM-M-1045/check_statement.py` | 0 | Target fingerprint `e1b35bb7...5cea` agreed and all four recorded mutations were distinguished. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, ten Lean probes, candidate inventory, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open at M3. |
| `timeout --foreground --kill-after=2s 30s env ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake --dir Formalizations/Lean env lean --version` | 0 | Pinned Lean 4.29.0 commit `98dc76e3...fab16740`. |
| Narrow pinned `lake env lean` stdin replay below | 0 | Statement, blocker, and characterization elaborated with `--trust=0 -t0`; both proof declarations depend exactly on `[propext, Classical.choice, Quot.sound]`; `PIPESTATUS=0 0`. |
| Prohibited-construct scan | 1 expected | No prohibited construct occurs in the three checked proof-related sources. |
| Exact material-delta command from `e89fe5cc` to current HEAD | 0 | No material target source, registry, graph, validation-spec, lockfile, or toolchain delta. |
| `python3 -m json.tool Stage1_Instances/THM-M-1045/proof-recheck-2026-07-15-head-9d50d838-slot42.json` | 0 | Structured blocker packet parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-1045` | 0 | No tracked-diff whitespace diagnostics. |
| Two `git diff --no-index --check /dev/null <new-file>` commands | 1 expected each | Each file differs from `/dev/null`; empty diagnostics confirm no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

Exact narrow Lean recipe:

```bash
set -o pipefail
{
  sed -n '1,$p' Stage1_Instances/THM-M-1045/Statement.lean
  sed '1{/^import Statement$/d;}' \
    Stage1_Instances/THM-M-1045/ProofBlockerCurrent.lean
  sed '1{/^import ProofBlockerCurrent$/d;}' \
    Stage1_Instances/THM-M-1045/ProofBlockerCharacterizationHead443b8bbcSlot38.lean
} | (
  cd Formalizations/Lean
  timeout --foreground 600 lake env lean --trust=0 -t0 --stdin
)
printf 'PIPESTATUS=%s\n' "${PIPESTATUS[*]}"
```

Exact substantive output:

```text
'Stage1Instances.THM_M_1045.no_target_of_wienerData' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1045.target_iff_isEmpty_wienerData' depends on axioms: [propext, Classical.choice, Quot.sound]
PIPESTATUS=0 0
```

Pinned identities are Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib
commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is fresh target-scoped nonrelease blocker evidence. It supplies no positive root proof credit,
does not satisfy `S56-M-1045-PROOF`, and makes no provisional-state, audit-completion, validation,
release, theorem-completion, or master-acceptance claim.
