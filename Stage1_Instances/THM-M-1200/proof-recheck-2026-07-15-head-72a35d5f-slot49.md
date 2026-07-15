# THM-M-1200 proof-phase recheck at `72a35d5f` (slot49)

Item: `S56-M-1200-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `72a35d5f64e32233c0bc77a57e47bd078475ad74`

Base tree: `a80eb91ed5629dee62d031e78bc87b509cf8e6eb`

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
force every admissible `phi` to be zero. Hence `InterfaceDefectVanishes` is
true for every jump coefficient. Specializing the target to `f = 0`, `uL = 0`,
`uR = 1`, and `s = 1` would require the false jump law `1 = 0`.

This refutes only the frozen analytic-test encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Replacing the
outer `top` with smooth `(infinity : WithTop ENat)` would substitute a repaired
statement and is outside the assigned proof phase. The conditional composition
theorem cannot close the root because its `NonzeroTracePackage` premise is
impossible for the frozen test class.

The assigned item remains `[ ]`. No positive proof body or receipt, state
transition, audit completion, theorem completion, validation completion,
release, or master acceptance is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the requested proof phase is not genuinely
complete.

## Failed Gate And Retry

The first semantic failure is the rev-5.6 section 5.1 Lean 4 statement gate at
`M1200-S-BOUNDARIES`. Separately, the prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`, so it would also block dependency-ordered acceptance of this parent.
The frozen minimal root cut remains `M1200-C-TEST`; the invalidated/open chain
is `M1200-S-BOUNDARIES`, `M1200-C-TEST`, and `M1200-ROOT`. The tracked registry
remains open at M4; this recheck proposes H5/M5 blocker evidence without
altering predecessor state. The provisional anchor audit and obligation
architecture are stale as positive support because they rely on the impossible
bump candidate; their hashes in the JSON record identify invalidated inputs,
not accepted proof evidence.

This is the eighteenth `proof-recheck-*.json` record and the nineteenth
structured blocker record when `proof-blocker.json` is included. These files
establish eighteen unresolved proof-recheck records, but not eighteen distinct
executions or their identity with private scheduler ticks; the authoritative
DAG still records `attempts: 0`. The master must reconcile the records against
its tick ledger and split after five actual unresolved ticks. Independently of
that accounting, the checked refutation requires redirecting positive work to
an authorized statement repair or a checked counterexample/barrier target.

Positive proof work may resume only after an authorized statement-phase repair
replaces the analytic outer `top` with smooth `(infinity : WithTop ENat)`,
publishes a new statement fingerprint, and freshly freezes and accepts the
statement, anchor audit, obligation registry, and typed graphs in dependency
order. The other legal route is an explicit redirection to the checked
counterexample target.

## Validation

All credited checks ran in this worker clone against the existing canonical
pinned sources and compiled artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or other `.lake` mutation command was
run. Lean output was confined to a fresh directory under `/tmp` and removed
after the check. The automation-provided untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; the owned target path was clean. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 130 | Not credited: the optional check was interrupted after taking longer than expected. It left no target artifact; the separately isolated exact statement check below passed. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction open at M4. |
| Isolated pinned Lean `--trust=0` recipe below | 0 | The exact statement and checked refutation elaborated. `not_rankineHugoniotTarget` has type `Not RankineHugoniotTarget`; all three countermodel declarations reported axioms exactly `[propext, Classical.choice, Quot.sound]`. `Statement.olean` SHA-256 was `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0`; combined output SHA-256 was `cda1655d57dbdc79af3a7dda5753057d0510596fa63b23ceb0c84ded1e627ef4`. |
| Exact prohibited-token scan below | 1 | Expected no-match result: no prohibited declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Exact JSON validation recipe below | 0 | Prints `PASS current-base blocker invariants and source hashes`. |
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
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-72a35d5f-slot49.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1200/Counterexample.lean" \
  "$tmp/Counterexample.lean"
cd "$mathlib"
LEAN_PATH="$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout 600 lake env lean \
  --trust=0 -R "$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.log" 2>&1
cat "$tmp/statement.log" "$tmp/counterexample.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
printf 'STATEMENT_OLEAN_SHA256='
sha256sum "$tmp/Statement.olean" | cut -d' ' -f1
printf 'KERNEL_OUTPUT_SHA256='
sha256sum "$tmp/kernel.log" | cut -d' ' -f1
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
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-72a35d5f-slot49.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-72a35d5f-slot49.json'
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
assert d['retry_history']['structured_blocker_records_including_this_one'] == 19
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
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-72a35d5f-slot49.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-72a35d5f-slot49.json \
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
