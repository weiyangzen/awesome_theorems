# THM-M-0729 proof recheck at `30228d98` (slot74)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:07:46+08:00`

Base revision: `30228d98c98c401cb60a3dfa09eec01bb904053f`

Base tree: `773a33c6344fb9787649fbc5edea99092ea68856`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`; the
root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked `root_of_directionalPackage` declaration is conditional composition. Its premise
already contains both missing inclusions, so it constructs neither one. The immediate root cut is:

- `M0729-D-NP-PCP`: verifier normalization, a constant-gap robustness theorem, PCP composition,
  logarithmic-randomness and constant-query accounting, perfect completeness, and exact
  soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive enumeration of logarithmically many
  coin strings with a bundled polynomial-time proof, and the finite below-threshold branch.

Assuming `DirectionalPackage`, adding an axiom or bodyless declaration, or reporting the conditional
composer as the proof would be a placeholder or theorem substitution. None was done. Pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies only deterministic Turing-machine,
finite-cardinality, polynomial, and logarithm infrastructure. It has no NP/PCP development or PCP
theorem; even `Turing.TM2ComputableInPolyTime.comp` remains a non-retained `proof_wanted` marker.
The prerequisite bounded immutable audit found no compatible external terminal proof to pin. It did
not have authenticated GitHub code search, so this packet makes no global-absence claim.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch/checkout, network request, or `.lake` mutation was performed. Temporary Lean
outputs were removed.

The canonical `flt-regular` package is an empty worktree whose `HEAD` cannot resolve. Consequently,
the normal `lake env` statement check fails before target elaboration. The exact target, conditional
composition, and blocker probe were separately replayed with the immutable Lean 4.29.0 executable
against existing pinned package oleans at trust level zero. That fallback passed but is nonrelease
evidence only; the dependency defect was not repaired in this worker.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `30228d98...053f`, tree `773a33c6...856`; only the canonical `.lake` symlink was initially untracked. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 1 | Normal Lake validation stopped because the unrelated `flt-regular` checkout cannot resolve `HEAD`; no repair was attempted. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact PCP root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Isolated immutable Lean 4.29.0 `--trust=0 -t0` replay against existing pinned oleans | 0 | The exact statement, conditional assembly, and blocker probe elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; the polynomial-time-composition application failed as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Exact PCP declarations were confined to this dossier; no terminal inclusion or root body was found. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded source marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Hash all frozen proof inputs and pins | 0 | Hashes matched the paired structured artifact. |
| Scoped diff from original blocker integration `9864b47f` | 0 | No statement, registry, graph, audit, validation specification, pin, target manifest, or execution-skill input changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is incomplete. |

The trust-zero replay used disposable copies and this command shape from the worker root:

```bash
set -euo pipefail
root=$(pwd)
tmp=$(mktemp -d /tmp/thm-m-0729-slot74.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0729/{Statement,ObligationTree,ProofBlockerProbe}.lean "$tmp/"
lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path=$(find "$root/Formalizations/Lean/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
lean_path="$root/Formalizations/Lean/.lake/build/lib/lean:$lean_path"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" ProofBlockerProbe.lean
```

## Reopen Condition

Resume after placeholder-free implementations of both frozen directional packages and their
reduction, resource, certificate, enumeration, and boundary dependencies exist. Alternatively,
integrate an immutable compatible Lean 4 terminal proof of the exact target with full dependency and
license evidence. The canonical `flt-regular` checkout must also be repaired outside this worker
before normal `lake env lean` replay.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
