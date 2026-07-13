# THM-M-0028 release reconciliation

Item: `S56-M-0028-RELEASE`. Base revision:
`75ab5edd624df749325d391b41b669f8d72774b2`; base tree:
`26562e2b8168d91a92a8164c9d8f0fc55178836e`.

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`; the accepted root vector remains
`[H1, M3, R3]`; `AUDIT-Z` and `THEOREM-Z` are both false; and `accepted_receipt_ids` remains empty.
The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is
provisional `[_]` worker evidence, not master-accepted `[x]` evidence. The first release-specific
failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact modern-unital ascending-chain target has substantive provisional kernel evidence. A
fresh temporary-module replay checks the direct exact root, the frozen child composition, and the
separately written differential root through pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The finite-generation terminal reports `propext` and
`Quot.sound`; the chain terminal and exact roots additionally report `Classical.choice`. All
scoped declarations are sorry-free. This is a kernel-closed wrapper candidate that could classify
as `M0-W` only after accepted `E1` evidence; it is not a legal accepted `M0-W/E1` state now.

The structured authority remains `planned`, `[H1, M3, R3]`, `root_closed=false`,
`audit_complete=false`, and `theorem_complete=false`, with no accepted receipt or obligation. The
human-source record lacks a pinpoint independently reviewed `H0` packet, and no node-specific
independently reviewed `R0` reconstruction exists. Full transitive provenance, foundation, axiom
policy, and TCB acceptance are also absent, so `AUDIT-Z` fails independently of machine closure.

The integrated validation receipt is `accepted=false` and `release_grade=false`. Its recorded
recipe is not replayable at this release snapshot: `check_validation.py` binds historical base
`a16267e7165144d202080fb647261658fa75ceb2`, an ephemeral validation-worker self-test packet, and
the validation-only worktree shape. The release checker therefore performs fresh narrow Lean
replays while recording, rather than concealing, that stale-recipe gate.

This worker reused the automation-provided shared warm `.lake` artifacts read-only. It did not
create an immutable clean checkout, empty caches, a network-denied cold build, or an offline
restoration archive. There is no complete SBOM/license closure, two signed attestations from
independently provisioned runners, independently implemented minimal release verifier, protected
adversarial CI record, or deterministic signed content-addressed bundle. Same-workspace
differential elaboration is not independent release verification.

## Commands and results

All commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0028
  exit 0: rank 1073, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0028/check_proof.sh
  exit 0: both pinned terminals and all four exact proof declarations are sorry-free; finite
  generation reports propext/Quot.sound and the chain/root declarations additionally report
  Classical.choice

set -euo pipefail; tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT;
cp Stage1_Instances/THM-M-0028/{Statement,Validation}.lean "$tmp/";
cd Formalizations/Lean; lean_bin=$(lake env which lean);
lean_path=$(lake env printenv LEAN_PATH); cd "$tmp";
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean;
LEAN_PATH=".:$lean_path" "$lean_bin" Validation.lean
  exit 0: three declarations are sorry-free; the differential exact root reports exactly propext,
  Classical.choice, and Quot.sound

python3 -B Stage1_Instances/THM-M-0028/check_release.py
  exit 0: hashes, authority boundary, dependency failure, terminal decisions, open release gates,
  and both fresh narrow Lean replays agree; verdict blocked

python3 -m json.tool Stage1_Instances/THM-M-0028/release-decision.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

## Retry boundary

The integration lane must first accept the dependency chain in topological order and reconcile the
instance, local DAG, typed graph, and replayable validation recipe. A separate release lane must
then close independent `H0/R0`, complete provenance/TCB and supply-chain records, reproduce the
immutable snapshot from empty caches with network denied and offline restoration, obtain two
qualifying signed attestations, and verify a deterministic bundle with an independently implemented
minimal verifier. Only the master may advance authoritative state.

## Status boundary

This is a self-tested negative release reconciliation. It grants no accepted receipt, lifecycle or
debt transition, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
