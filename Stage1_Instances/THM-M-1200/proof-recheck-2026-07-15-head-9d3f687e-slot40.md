# THM-M-1200 proof-phase recheck at 9d3f687e (slot40)

Item: `S56-M-1200-PROOF`. Date: 2026-07-15. Base revision:
`9d3f687e9bf0fe3120397744332e909472c52dfd`; base tree:
`558507d70ac5e5e38486f214a3e0ce7b33f7ae9b`.

## Verdict

`blocked`; state remains `[ ]`. No positive proof body was added. The exact
frozen target is kernel-refuted by the tracked placeholder-free declaration

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

The statement requires `ContDiff Real top phi`. In the pinned calculus API,
that outer `top` is analytic order `omega`, while smooth compactly supported
bumps have order `(infinity : WithTop ENat)`. Analytic uniqueness plus compact
support therefore forces every admissible test function to be zero. Taking
`f = 0`, `uL = 0`, `uR = 1`, and `s = 1` makes the defect predicate true but
the requested jump law false.

This refutes only the frozen Lean encoding, not the mathematical
Rankine-Hugoniot theorem with smooth compactly supported tests. Replacing
outer `top` here would substitute a repaired theorem and is outside this proof
worker's authority.

## Failed Gate And Retry

The first failed semantic gate is rev-5.6 section 5.1 / `M1200-S-BOUNDARIES`.
The minimal frozen root cut is `M1200-C-TEST`: the required
`NonzeroTracePackage` is impossible. A fresh trust-zero temporary module
directly proved `Not NonzeroTracePackage` from the tracked analytic
compact-support lemma. The checked theorem
`rankineHugoniotTarget_of_nonzeroTracePackage` remains conditional and earns no
positive closure.

The authoritative prerequisite `S56-M-1200-OBLIGATION_TREE` remains
provisional `[_]`, independently blocking dependency-ordered acceptance of
this parent. The DAG reports zero proof attempts, while 32 older proof-recheck
JSON records exist. File count is not scheduler-tick evidence; the master must
reconcile actual ticks and split or redirect after five unresolved executions.

Do not retry the unchanged proof item. An authorized statement-phase repair
must use smooth `(infinity : WithTop ENat)`, publish a new statement
fingerprint, and then freshly audit and accept its obligation architecture.
Alternatively, the master may redirect to a checked counterexample or barrier
target.

## Validation

No command updated, built, cloned, fetched, or otherwise mutated `.lake`.
Credited Lean commands only read the automation-provided symlink to canonical
pinned artifacts and wrote generated files to a fresh directory under `/tmp`,
which was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | JSON reported statement expression SHA `b77d79ed...ca93`, pinned mathlib `8a178386...`, Lean 4.29.0, and all four named structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c444...c54931`; root and nonzero-trace construction remain M4/open. |
| Fresh isolated pinned `lake --offline env` / direct Lean `--trust=0` recipe below | 0 | Exact statement, countermodel, conditional composition, and direct negation of `NonzeroTracePackage` elaborated. All reported axioms were exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| Prohibited-token scan below | 1 | Expected no-match result: no prohibited proof device or declaration in target Lean files. |
| `Lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `lake --version` | 0 | Lake `5.0.0-src+98dc76e` (Lean 4.29.0). |
| Pinned dependency revision checks | 0 | mathlib `8a178386...` / tree `bdc39a...`; flt-regular `56161b6e...` / tree `32c9eace...`. |
| Exact JSON/hash validation recipe below | 0 | Prints `PASS current-base blocker invariants and source hashes`. |
| Scoped whitespace checks below | 0 | No whitespace error in either new owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1200-slot40-evidence.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$root/Stage1_Instances/THM-M-1200/Statement.lean" "$tmp/Statement.lean"
cp "$root/Stage1_Instances/THM-M-1200/Counterexample.lean" "$tmp/Counterexample.lean"
cp "$root/Stage1_Instances/THM-M-1200/ObligationTree.lean" "$tmp/ObligationTree.lean"
cat >"$tmp/ConstructionRefutation.lean" <<'EOF'
import ObligationTree
import Counterexample
namespace Stage1Instances.THM_M_1200
theorem not_nonzeroTracePackage : Not NonzeroTracePackage := by
  intro package
  obtain ⟨phi, smooth, compact, integral_ne⟩ := package 0
  rw [Counterexample.analytic_compactSupport_eq_zero phi smooth compact] at integral_ne
  simp at integral_ne
#check not_nonzeroTracePackage
#print axioms not_nonzeroTracePackage
end Stage1Instances.THM_M_1200
EOF
cd "$root/Formalizations/Lean"
lean=$(lake --offline env which lean)
base_lean_path=$(lake --offline env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Counterexample.olean" \
  "$tmp/Counterexample.lean" >"$tmp/counterexample.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ConstructionRefutation.lean" \
  >"$tmp/construction.log" 2>&1
cat "$tmp/statement.log" "$tmp/counterexample.log" \
  "$tmp/obligation.log" "$tmp/construction.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/kernel.log"
```

The fresh result hashes were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| Combined kernel log | `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0` |

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The exact structured evidence check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9d3f687e-slot40.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-9d3f687e-slot40.json'
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
assert d['retry_history']['structured_blocker_records_including_this_one'] == 34
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

Because ordinary `git diff --check` omits untracked files, both new files were
checked explicitly:

```bash
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9d3f687e-slot40.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9d3f687e-slot40.json \
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

This is durable blocker evidence, not a proof receipt. It changes no tracked
Lean source, frozen predecessor artifact, scheduler authority, dependency, or
unrelated target. `.stage1-worker-selftest.json` is deliberately absent because
the assigned proof phase is not genuinely complete.
