# THM-M-1200 proof-phase blocker recheck

Item: `S56-M-1200-PROOF`. Base revision:
`fafb52c91501fd02290f6e2aa8dbf6af59184135`. Base tree:
`368a5490da1afb0cfd49518532085ec2146ce1e6`. Date: 2026-07-15.

## Verdict

`blocked`; state remains `[ ]`. No positive proof body was added. The exact
frozen declaration `Stage1Instances.THM_M_1200.RankineHugoniotTarget` has the
placeholder-free, kernel-checked negation

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

The frozen statement uses `ContDiff Real top phi`. Its order type is
`WithTop ENat`; the outer `top` is analytic order `omega`, while smooth order
is `(top : ENat)` coerced into `WithTop ENat`. Analytic uniqueness and compact
support force every admissible test function to zero. The weak-defect predicate
therefore holds for `f = 0`, `uL = 0`, `uR = 1`, and `s = 1`, while the jump
law would require `1 = 0`.

The obligation-tree composition theorem is conditional on
`NonzeroTracePackage`. `ProofRefutation.lean` kernel-checks
`not_nonzeroTracePackage : Not NonzeroTracePackage`, so that premise cannot
close the root. These declarations refute only the frozen analytic-test
encoding, not the mathematical Rankine-Hugoniot theorem with smooth compactly
supported tests.

## Failed Gates And Repair

The first workflow gate fails because prerequisite
`S56-M-1200-OBLIGATION_TREE` is provisional `[_]`, not master-accepted `[x]`.
Independently, the first semantic failure is rev-5.6 section 5.1 exact-target
consistency at `M1200-S-BOUNDARIES`. The minimal root cut is `M1200-C-TEST`;
the invalidated or open chain is `M1200-S-BOUNDARIES`, `M1200-C-TEST`, and
`M1200-ROOT`. This supports proposed H5/M5 blocker status, not M0 closure.

An authorized statement repair must use smooth `(top : ENat)`, coerced into
`WithTop ENat`, in both the test predicate and construction package. It must
then freshly freeze and accept the statement, anchor audit, obligation
registry, and typed graphs in dependency order. The current statement checker
hashes the printed root body, which references `InterfaceDefectVanishes`
opaquely; a repair must version that predicate or fingerprint its unfolded
transitive definition surface and add an order-sensitive mutation. The other
legal route is explicit redirection to the checked counterexample or barrier
target.

There were 40 pre-existing `proof-recheck-*.json` records and 41 structured
blocker JSONs including `proof-blocker.json`; this is the forty-first recheck
and forty-second structured blocker record. File count does not prove scheduler
tick identity. The master must reconcile its private tick ledger and apply the
five-unresolved-tick split rule. This unchanged proof item should not be
retried regardless of that accounting.

## Validation

All credited checks ran in this worker clone against existing pinned sources
and compiled dependencies. No `lake update`, `lake build`, dependency
clone/fetch, network action, or other `.lake` mutation was run. Lean output was
confined to a fresh directory under `/tmp` and removed. The automation-provided
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA `b77d79ed...ca93`, pinned Lean/mathlib, and four killed structural mutations. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c444...c54931`; root and construction remain M4. |
| Isolated pinned `lake --offline env lean --trust=0` recipe below | 0 | Statement, exact countermodel, conditional composition, and package refutation elaborated. Axiom reports contain exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| Direct pinned Lean `--deps` with the temporary-first path | 0 | Imports resolve to the fresh temporary `ObligationTree.olean` and `Counterexample.olean`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration in target Lean files. |
| Direct pinned Lean and Lake version checks | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| Pinned dependency revision checks | 0 | mathlib `8a178386...` / tree `bdc39a...`; flt-regular `56161b6e...` / tree `32c9eace...`. |
| Exact JSON/hash validation below | 0 | `PASS current-base blocker invariants and source hashes`. |
| Scoped and explicit new-file whitespace checks | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent. |

The isolated Lean recipe was:

```bash
set -euo pipefail
canonical=$(readlink -f Formalizations/Lean/.lake)
packages=$canonical/packages
mathlib=$packages/mathlib
toolchain=$(tr -d '\n' < Formalizations/Lean/lean-toolchain)
lean_bin=$(ELAN_TOOLCHAIN="$toolchain" elan which lean)
toolchain_lib=$(realpath "$(dirname "$lean_bin")/../lib/lean")
base_path=$toolchain_lib
for package in "$packages"/*; do
  if [ -d "$package/.lake/build/lib/lean" ]; then
    base_path="$base_path:$package/.lake/build/lib/lean"
  fi
done
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-fafb52c9-slot12.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1200/{Statement,Counterexample,ObligationTree,ProofRefutation}.lean "$tmp/"
cd "$mathlib"
for module in Statement Counterexample ObligationTree ProofRefutation; do
  path=$base_path
  if [ "$module" != Statement ]; then path="$tmp:$base_path"; fi
  LEAN_NUM_THREADS=1 LEAN_PATH="$path" \
    timeout --foreground --kill-after=10s 600 \
    lake --offline env lean --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" \
      >"$tmp/$module.log" 2>&1
done
cat "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.log \
  >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.olean \
  "$tmp/kernel.log"
LEAN_PATH="$tmp:$base_path" "$lean_bin" --deps -R "$tmp" \
  "$tmp/ProofRefutation.lean"
```

Fresh output hashes:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |
| Combined kernel log | `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0` |

The prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The exact structured evidence check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-fafb52c9-slot12.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-fafb52c9-slot12.json'
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
assert d['retry_history']['preexisting_proof_recheck_json_records'] == 40
assert d['retry_history']['proof_recheck_json_records_including_this_one'] == 41
assert d['retry_history']['structured_blocker_records_including_this_one'] == 42
assert d['retry_history']['master_tick_reconciliation_required']
assert not Path('.stage1-worker-selftest.json').exists()
base = Path('Stage1_Instances/THM-M-1200')
for name, expected in d['source_hashes'].items():
    path = (Path('Formalizations/Lean') / name
            if name in {'lake-manifest.json', 'lean-toolchain'}
            else base / name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
assert len(list(base.glob('proof-recheck-*.json'))) == 41
assert len(list(base.glob('proof-recheck-*.md'))) == 41
print('PASS current-base blocker invariants and source hashes')
PY
```

Because ordinary `git diff --check` omits untracked files, both new files were
also checked explicitly:

```bash
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-fafb52c9-slot12.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-fafb52c9-slot12.json \
  || test $? -eq 1
```

This is durable blocker evidence, not a proof receipt. It changes no Lean
source, predecessor artifact, scheduler authority, dependency, or unrelated
target. `.stage1-worker-selftest.json` is deliberately absent because the
assigned positive proof phase is not genuinely complete.
