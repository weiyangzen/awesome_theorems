# THM-M-1200 proof-phase blocker recheck

Item: `S56-M-1200-PROOF`. Base revision:
`62a4768eab1bedaed6d970d504e1788c021f47a9`. Base tree:
`fc154c2bea683094c1a662e67edba530547f5270`. Date: 2026-07-15.

## Verdict

`blocked`; state remains `[ ]`. No positive proof body was added. The exact
frozen declaration `Stage1Instances.THM_M_1200.RankineHugoniotTarget` has the
placeholder-free, kernel-checked negation

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

The frozen statement uses `ContDiff Real top phi`. In the pinned calculus API,
the outer `top : WithTop ENat` is analytic order `omega`, not smooth order
`(top : ENat)` coerced into `WithTop ENat`. Analytic uniqueness plus compact
support forces every admissible test function to zero. Thus the weak-defect
predicate holds for `f = 0`, `uL = 0`, `uR = 1`, and `s = 1`, while the jump
law would require `1 = 0`.

The obligation-tree composition theorem remains conditional on
`NonzeroTracePackage`. `ProofRefutation.lean` kernel-checks
`not_nonzeroTracePackage : Not NonzeroTracePackage`, so the premise cannot
close the root. These declarations refute only the frozen analytic-test
encoding, not the mathematical Rankine-Hugoniot theorem with smooth compactly
supported tests.

## Failed Gates And Repair

The first workflow gate fails because prerequisite
`S56-M-1200-OBLIGATION_TREE` remains provisional `[_]`, not master-accepted
`[x]`. Independently, the first semantic failure is rev-5.6 section 5.1 exact
target consistency / `M1200-S-BOUNDARIES`. The minimal root cut is
`M1200-C-TEST`; the invalidated or open chain is `M1200-S-BOUNDARIES`,
`M1200-C-TEST`, and `M1200-ROOT`. This supports proposed H5/M5 blocker status,
not M0 closure.

An authorized statement repair must use smooth `(top : ENat)`, coerced into
`WithTop ENat`, in both the test predicate and construction package. It must
then freshly audit and accept the statement, anchor audit, obligation registry,
and typed graphs in dependency order. The current validator hashes the printed
`RankineHugoniotTarget` body, which references `InterfaceDefectVanishes`
opaquely; changing that predicate's order can leave the reported
`b77d79ed...ca93` hash unchanged. A repair must therefore version the predicate
or fingerprint its unfolded transitive definition surface and add an
order-sensitive mutation test. The other legal route is explicit redirection
to the checked counterexample or barrier target.

There were 39 pre-existing `proof-recheck-*.json` records and 40 structured
blocker JSONs including `proof-blocker.json`; this is the fortieth recheck and
forty-first structured blocker record. File count does not prove scheduler tick
identity. The master must reconcile its tick ledger and apply the five-tick
split rule. This unchanged proof item should not be retried regardless of that
accounting.

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
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Reported expression SHA `b77d79ed...ca93`, pinned Lean/mathlib, and four structural mutation names. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations, 54 typed edges, denominator `9915c444...c54931`; root and construction remain open M4. |
| Isolated pinned direct Lean `--trust=0` recipe below | 0 | Statement, exact countermodel, conditional composition, and package refutation elaborated. Axiom reports contain exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| `lean --deps` with the credited path | 0 | Imports resolve to the fresh temporary `ObligationTree.olean` and `Counterexample.olean`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration in target Lean files. |
| `lake --offline env lean --version`; `lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| Pinned dependency revision checks | 0 | mathlib `8a178386...` / tree `bdc39a...`; flt-regular `56161b6e...` / tree `32c9eace...`. |
| Exact JSON/hash validation below | 0 | `PASS current-base blocker invariants and source hashes`. |
| Scoped and explicit untracked-file whitespace checks | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest correctly absent. |

The worker build directory contains a colliding stale root module named
`ObligationTree.olean`. Invoking `lake env lean` for the temporary module steps
prepends that directory and can import the wrong module; a diagnostic run
caught this and receives no credit. The credited recipe selects the pinned Lean
executable with `lake --offline env which lean`, removes only the worker build
directory from the pinned search path, invokes the selected executable directly,
and verifies import resolution with `--deps`:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-62a4768e-slot40.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1200/{Statement,Counterexample,ObligationTree,ProofRefutation}.lean "$tmp/"
cd Formalizations/Lean
lean=$(lake --offline env which lean)
raw_path=$(lake --offline env printenv LEAN_PATH)
base_path=''
IFS=: read -ra entries <<< "$raw_path"
for entry in "${entries[@]}"; do
  case "$entry" in
    "$repo/Formalizations/Lean/.lake/build/lib/lean") ;;
    *) base_path=${base_path:+$base_path:}$entry ;;
  esac
done
for module in Statement Counterexample ObligationTree ProofRefutation; do
  path=$base_path
  if [ "$module" != Statement ]; then path="$tmp:$base_path"; fi
  LEAN_NUM_THREADS=1 LEAN_PATH="$path" \
    timeout --foreground --kill-after=10s 600 \
    "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/$module.olean" \
    "$tmp/$module.lean" >"$tmp/$module.log" 2>&1
done
cat "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.log \
  >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp"/{Statement,Counterexample,ObligationTree,ProofRefutation}.olean \
  "$tmp/kernel.log"
LEAN_PATH="$tmp:$base_path" "$lean" --deps -R "$tmp" \
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

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The exact structured evidence check was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-62a4768e-slot40.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

p = Path(
    'Stage1_Instances/THM-M-1200/'
    'proof-recheck-2026-07-15-head-62a4768e-slot40.json'
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
assert d['retry_history']['preexisting_proof_recheck_json_records'] == 39
assert d['retry_history']['proof_recheck_json_records_including_this_one'] == 40
assert d['retry_history']['structured_blocker_records_including_this_one'] == 41
assert d['retry_history']['master_tick_reconciliation_required']
assert not Path('.stage1-worker-selftest.json').exists()
base = Path('Stage1_Instances/THM-M-1200')
for name, expected in d['source_hashes'].items():
    path = (Path('Formalizations/Lean') / name
            if name in {'lake-manifest.json', 'lean-toolchain'}
            else base / name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
assert len(list(base.glob('proof-recheck-*.json'))) == 40
print('PASS current-base blocker invariants and source hashes')
PY
```

This is durable blocker evidence, not a proof receipt. It changes no Lean
source, predecessor artifact, scheduler authority, dependency, or unrelated
target. `.stage1-worker-selftest.json` is deliberately absent because the
assigned positive proof phase is not genuinely complete.
