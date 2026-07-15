# THM-M-1200 proof-phase blocker recheck

Item: `S56-M-1200-PROOF`. Base revision:
`af9c55e3e17639cd0c13bfd85bfb4bf30554785a`. Base tree:
`4e842676a2087338f5582d16e365c51c87763af0`. Date: 2026-07-15.

## Verdict

The assigned proof phase is blocked. The exact frozen declaration
`Stage1Instances.THM_M_1200.RankineHugoniotTarget` has a placeholder-free,
kernel-checked negation:
`Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget`.

The frozen statement uses `ContDiff Real top phi`. In the pinned calculus API,
the outer `top : WithTop ENat` is analytic order `omega`, not smooth order
`infinity`. Analytic uniqueness and compact support force every admissible
test function to be zero. Hence `InterfaceDefectVanishes` holds for every
coefficient, but the specialization `f = 0`, `uL = 0`, `uR = 1`, `s = 1`
would require `1 = 0`.

The obligation-tree composition theorem is only conditional on
`NonzeroTracePackage`. The checked declaration
`Stage1Instances.THM_M_1200.not_nonzeroTracePackage` proves that exact package
cannot exist. Replacing `top` with smooth `(infinity : WithTop ENat)` here
would substitute a repaired theorem and is outside this proof worker's owned
phase.

The assigned item remains `[ ]`. No positive proof body, proof receipt, state
transition, audit completion, theorem completion, validation completion,
release, or master acceptance is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the requested proof phase is not genuinely
self-tested.

## Failed Gates And Repair

The first workflow gate fails because prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`. Independently, the first semantic failure is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1200-S-BOUNDARIES`. The minimal root cut
is `M1200-C-TEST`; the invalidated or open chain is
`M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`. The checked result
supports proposed H5/M5 blocker evidence, not M0 closure.

Positive proof work may resume only after an authorized statement-phase
repair uses smooth `(infinity : WithTop ENat)`, versions and re-fingerprints
the statement, and freshly freezes and accepts the statement, anchor audit,
obligation registry, and typed graphs in dependency order. The other legal
route is explicit redirection to the checked counterexample or barrier target.

There were 38 pre-existing `proof-recheck-*.json` records and 39 structured
blocker records including `proof-blocker.json`; this file is the fortieth
structured blocker record. File count does not prove private scheduler tick
identity. The master must reconcile that ledger and apply the five-tick split
rule. This unchanged proof item should not be retried regardless of that
accounting.

## Validation

All credited checks ran in this worker clone against the existing canonical
pinned sources and compiled artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or other `.lake` mutation command was
run. Lean output was confined to a fresh directory under `/tmp` and removed.
The automation-provided untracked `.lake` symlink makes this nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction open at M4. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | The statement, countermodel, conditional composition, and package refutation elaborated. The countermodel proves `Not RankineHugoniotTarget`; the refutation proves `Not NonzeroTracePackage`. All printed reports contain exactly `[propext, Classical.choice, Quot.sound]`. Combined kernel-log SHA-256 was `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0`. |
| `rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|constant)[[:space:]]' Stage1_Instances/THM-M-1200 --glob '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Exact JSON invariant and source-hash check | 0 | `PASS current-base blocker invariants and source hashes`. |
| `git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json`; then for each new file capture `git diff --check --no-index /dev/null <file>`, require its normal diff exit 1, and require empty output | 0 | The wrapper passed; no whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
canonical=$(readlink -f Formalizations/Lean/.lake)
packages=$canonical/packages
mathlib=$packages/mathlib
lean_bin=$(cd "$mathlib" && timeout 90 lake env which lean)
toolchain_lib=$(realpath "$(dirname "$lean_bin")/../lib/lean")
base_path=$toolchain_lib
for package in "$packages"/*; do
  if [ -d "$package/.lake/build/lib/lean" ]; then
    base_path="$base_path:$package/.lake/build/lib/lean"
  fi
done
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-af9c55e3.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1200/Counterexample.lean" "$tmp/Counterexample.lean"
cp "$repo/Stage1_Instances/THM-M-1200/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$repo/Stage1_Instances/THM-M-1200/ProofRefutation.lean" "$tmp/ProofRefutation.lean"
cd "$mathlib"
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" -o "$tmp/Counterexample.olean" \
  "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" "$tmp/ProofRefutation.lean" \
  >"$tmp/refutation.log" 2>&1
cat "$tmp/statement.log" "$tmp/counterexample.log" \
  "$tmp/obligation.log" "$tmp/refutation.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/kernel.log"
```

Checked input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8e1650b86f9f8ab1917c326d938859bace727cf445182d3ae614d2eb48ae5ee7` |
| `Counterexample.lean` | `532c2f0d11e2a5b547b6bf55da3b5feee6a0ecb1bf2c5f32ad337abdfced4d95` |
| `ObligationTree.lean` | `c4eef89fd1e79a37b1733724709162544057743ff0b37f25716c2b1273c71598` |
| `ProofRefutation.lean` | `ef349a99041aef294fb51cbae34ef292b7aef02add3860353569365bb91b695d` |
| `obligation-registry.json` | `88f89866d3780610b8992be9d65651b3d922871fe6a571cfe957fa1e2fed2b91` |
| `typed-graphs.json` | `079f92a507df6b0330c3cdcc5629037db719e6d8b53fd674933a7429430717dc` |
| `anchor-audit.json` | `7ea5d8d3ccc31b3268381917ecd7d47ac2187c30edacf732c9acd17f8c0f402c` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

The exact structured evidence check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-af9c55e3-slot31.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-af9c55e3-slot31.json'
)
d = json.loads(p.read_text())
assert d['item_id'] == 'S56-M-1200-PROOF'
assert d['theorem_id'] == 'THM-M-1200'
assert d['base_revision'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD'], text=True).strip()
assert d['base_tree'] == subprocess.check_output(
    ['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
assert d['verdict'] == 'blocked' and d['state'] == '[ ]'
assert not d['proof_body_added'] and not d['positive_root_proof_exists']
assert not d['proof_phase_complete'] and not d['root_closed']
assert not d['audit_complete'] and not d['theorem_complete']
assert d['accepted_receipt_ids'] == []
assert not d['selftest_manifest_written']
assert d['retry_history']['preexisting_proof_recheck_records'] == 38
assert d['retry_history'][
    'preexisting_structured_blocker_records_including_proof_blocker_json'
] == 39
assert d['retry_history'][
    'structured_blocker_records_including_this_one'
] == 40
assert d['retry_history']['master_tick_reconciliation_required']
assert not Path('.stage1-worker-selftest.json').exists()
base = Path('Stage1_Instances/THM-M-1200')
for name, expected in d['source_hashes'].items():
    path = (Path('Formalizations/Lean') / name
            if name in {'lake-manifest.json', 'lean-toolchain'}
            else base / name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
assert len(list(base.glob('proof-recheck-*.json'))) == 39
print('PASS current-base blocker invariants and source hashes')
PY
```

This is durable blocker evidence, not a proof receipt. It changes no Lean
source, frozen predecessor artifact, scheduler authority, dependency artifact,
or unrelated target.
