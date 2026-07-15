# THM-M-0673 release reconciliation

Item `S56-M-0673-RELEASE` is **blocked**. The lifecycle remains `planned`,
the accepted root vector remains `[H1, M3, R4]`, and both `audit_complete`
and `theorem_complete` are false. This is a self-tested negative release
decision, not release evidence or master acceptance.

## Evidence reconciliation

The predecessor validation receipt records a real trust-zero,
network-isolated warm-cache replay of the exact statement, frozen composition,
local wrappers, and a separately written same-worker adapter. The exact root is
inhabited through pinned mathlib, every checked declaration reports only
`propext`, `Classical.choice`, and `Quot.sound`, and the traversed proof and
validation closures contain no bodyless nonaxiom or unsafe declaration.

Those observations are provisional. `S56-M-0673-VALIDATION` is only `[_]`;
its receipt is blocked, unaccepted, and non-release-grade. The planned instance
and typed graph remain authoritative at `H1/M3/R4`, with `root_closed=false`
and no accepted proof state, obligation, or receipt. Fifteen deeper nodes are
source-mapped into the pinned bounded-formula body rather than individually
accepted. The first release failure is therefore validation dependency
acceptance. The first intrinsic release failure is immutable clean input.

The root release cut also retains the historical recipe freshness migration,
accepted foundation and complete provenance/TCB/SBOM/license records, a
primary-source H0 crosswalk and independent review, a unique R0 reconstruction
and review, cold empty-cache network-denied reproduction and offline restore,
two signed independent clean-runner attestations, an independently implemented
minimal verifier, protected CI/mutation gates, a deterministic bundle, and
master reconciliation.

## Commands and results

Run from the repository root without dependency update, build, clone, or fetch:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and exactly 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0673
  exit 0: rank 717, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0673/check_proof.sh
  exit 0: exact pinned root and frozen composition replayed with trust zero

python3 -B Stage1_Instances/THM-M-0673/check_obligation_tree.py
  exit 1 as expected: historical immutable base-revision binding rejects current HEAD

python3 -I -B Stage1_Instances/THM-M-0673/check_release.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0: negative decision, authority, dependency, hashes, cut set, and handoff agree

python3 -m json.tool Stage1_Instances/THM-M-0673/release-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0673/release-decision.json
python3 -m json.tool Stage1_Instances/THM-M-0673/release-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all structured artifacts parsed

git diff --check -- Stage1_Instances/THM-M-0673 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The checker does not replay the stale validation checker as a current pass: it
is immutably bound to its earlier validation snapshot. The narrow Lean proof
replay above is fresh current-worker evidence, but the shared warm `.lake`
cache and untracked link make it explicitly nonrelease evidence.

