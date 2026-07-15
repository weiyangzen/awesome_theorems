# THM-M-1200 proof-phase recheck at `443b8bbc` (slot49)

Item: `S56-M-1200-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No positive Lean proof can inhabit the exact frozen target. The
tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-checks at trust level zero against a freshly elaborated
`Statement.olean`.

The statement requires `ContDiff Real top phi`. In the pinned calculus API,
that outer `top` is the analytic order `omega`; smooth bump functions instead
have order `(infinity : WithTop ENat)`. Analytic uniqueness and compact support
force every admissible `phi` to be zero. Hence `InterfaceDefectVanishes` holds
for every jump coefficient. Specializing the target to `f = 0`, `uL = 0`,
`uR = 1`, and `s = 1` would require the false jump law `1 = 0`.

This refutes only the frozen analytic-test encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Replacing the
outer `top` with smooth `(infinity : WithTop ENat)` would substitute a repaired
statement and is outside this proof-phase worker's authority. The conditional
composition theorem cannot close the root because its `NonzeroTracePackage`
premise is impossible for the frozen test class.

The assigned item remains `[ ]`. No positive proof body or receipt, state
transition, audit completion, theorem completion, validation completion,
release, or master acceptance is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the requested proof phase is not genuinely
complete.

## Failed Gate And Retry

The first semantic failure is the rev-5.6 section 5.1 Lean 4 statement gate at
`M1200-S-BOUNDARIES`. Separately, prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`, so it also blocks dependency-ordered acceptance of this parent. The
frozen minimal root cut remains `M1200-C-TEST`; the invalidated/open chain is
`M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`. The tracked registry
remains open at M4; this recheck proposes H5/M5 blocker evidence without
altering predecessor state.

This is the twenty-third `proof-recheck-*.json` record and the twenty-fourth
structured blocker record when `proof-blocker.json` is included. These files
do not establish twenty-three distinct execution ticks; the authoritative DAG
still records `attempts: 0`. The master must reconcile the records with its
private tick ledger and split after five actual unresolved ticks.

Positive proof work may resume only after an authorized statement-phase repair
replaces analytic outer `top` with smooth `(infinity : WithTop ENat)`, publishes
a new statement fingerprint, and freshly freezes and accepts statement,
anchor-audit, and obligation-tree artifacts in dependency order. The other
legal route is explicit redirection to the checked counterexample target.

## Validation

The credited Lean check used the existing pinned Lean 4.29.0 toolchain,
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, and only existing
package build directories. Its outputs stayed under `/tmp` and were removed.
No `lake update`, `lake build`, or explicit dependency clone/fetch command was
run by this worker.

There is an important validation failure to preserve: the prescribed
`check_statement.py` internally invokes top-level `lake env lean`. On this
worker base, Lake attempted to materialize absent package `flt-regular` and ran
`git fetch --tags --force origin` in the canonical shared `.lake` cache. The
worker terminated that process and removed the temporary `tmp*.lean` copy from
the owned path. That validator receives no credit. The interrupted operation
nevertheless left an incomplete `flt-regular/.git` directory with fetched
remote refs. Therefore this record is nonrelease evidence and does not claim a
read-only-cache run. The cache owner must reconcile it before release work.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only automation-provided `?? Formalizations/Lean/.lake` was present; the owned target was clean. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | terminated, uncredited | Its internal Lake invocation attempted a moving dependency fetch. The process was stopped, its owned-path temporary copy was removed, and it supplies no statement-mutation evidence. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction remain open at M4. |
| Isolated pinned Lean `--trust=0` recipe below | 0 | Exact statement and refutation elaborated. `not_rankineHugoniotTarget` has type `Not RankineHugoniotTarget`; all three countermodel declarations report exactly `[propext, Classical.choice, Quot.sound]`. `Statement.olean` SHA-256 is `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0`; combined output SHA-256 is `cda1655d57dbdc79af3a7dda5753057d0510596fa63b23ceb0c84ded1e627ef4`. |
| Exact prohibited-token scan below | 1 | Expected no-match result: no prohibited declaration token occurs in owned Lean sources. |
| Exact JSON/hash validation recipe below | 0 | Prints `PASS current-base blocker invariants and source hashes`. |
| Scoped whitespace checks below | 0 | No whitespace error in the two new owned artifacts. |
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
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-443b8bbc-slot49.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1200/Counterexample.lean" "$tmp/Counterexample.lean"
cd "$mathlib"
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.log" 2>&1
cat "$tmp/statement.log" "$tmp/counterexample.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/kernel.log"
```

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The exact structured evidence check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-443b8bbc-slot49.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-443b8bbc-slot49.json'
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
assert d['accepted_receipt_ids'] == [] and not d['selftest_manifest_written']
assert d['environment']['unintended_dependency_fetch_observed']
assert d['retry_history']['structured_blocker_records_including_this_one'] == 24
assert d['retry_history']['master_tick_reconciliation_required']
assert not Path('.stage1-worker-selftest.json').exists()
base = Path('Stage1_Instances/THM-M-1200')
for name, expected in d['source_hashes'].items():
    path = (Path('Formalizations/Lean') / name
            if name in {'lake-manifest.json', 'lean-toolchain'}
            else base / name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
print('PASS current-base blocker invariants and source hashes')
PY
```

Because ordinary `git diff --check` omits untracked files, the scoped checks
were:

```bash
git diff --check -- Stage1_Instances/THM-M-1200 \
  .stage1-worker-selftest.json
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-443b8bbc-slot49.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-443b8bbc-slot49.json \
  || test $? -eq 1
```

Checked input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `8e1650b86f9f8ab1917c326d938859bace727cf445182d3ae614d2eb48ae5ee7` |
| `Counterexample.lean` | `532c2f0d11e2a5b547b6bf55da3b5feee6a0ecb1bf2c5f32ad337abdfced4d95` |
| `ObligationTree.lean` | `c4eef89fd1e79a37b1733724709162544057743ff0b37f25716c2b1273c71598` |
| `obligation-registry.json` | `88f89866d3780610b8992be9d65651b3d922871fe6a571cfe957fa1e2fed2b91` |
| `typed-graphs.json` | `079f92a507df6b0330c3cdcc5629037db719e6d8b53fd674933a7429430717dc` |
| `anchor-audit.json` | `7ea5d8d3ccc31b3268381917ecd7d47ac2187c30edacf732c9acd17f8c0f402c` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable blocker evidence, not a proof receipt. It changes no Lean
source, frozen predecessor artifact, scheduler authority, dependency artifact,
or unrelated target.
