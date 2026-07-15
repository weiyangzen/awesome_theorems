# THM-M-1200 proof-phase current-base blocker recheck

Item: `S56-M-1200-PROOF`. Execution rank: 394. Phase: `proof`.
Base revision: `9ce5b15aaeafda7308c5b4d7b0eae998ab633650`.
Base tree: `74e115f8418e0cbb135a1b0be01fb72c63904ba4`.
Recorded on 2026-07-15 in the Stage1 rev-5.6 slot36 worker clone.

## Verdict

The exact frozen positive target cannot be proved. The existing placeholder-free declaration

```lean
Stage1Instances.THM_M_1200.Counterexample.not_rankineHugoniotTarget :
  Not Stage1Instances.THM_M_1200.RankineHugoniotTarget
```

kernel-checks at trust level zero against a freshly elaborated `Statement.olean`. The proof-phase
barrier also checks with the exact type

```lean
Stage1Instances.THM_M_1200.not_nonzeroTracePackage :
  Not Stage1Instances.THM_M_1200.NonzeroTracePackage
```

The statement requires `ContDiff Real top phi`. In the pinned calculus API, the outer `top` is the
analytic order `omega`, whereas a smooth compactly supported bump has the order denoted `infinity`
(the coercion of `top : ENat` into `WithTop ENat`). Analytic uniqueness and compact support force
every admissible `phi` to be zero, so `InterfaceDefectVanishes` holds for every jump coefficient.
Specializing the frozen target to `f = 0`, `uL = 0`, `uR = 1`, and `s = 1` would require the false
equation `1 = 0`.

This refutes only the frozen analytic-test encoding, not the Rankine-Hugoniot theorem with smooth
compactly supported test functions. Replacing the regularity order in this proof worker would
change the frozen statement and invalidate its dependent audit and obligation artifacts. The
conditional composition theorem cannot close the root either: it assumes the kernel-refuted
`NonzeroTracePackage`.

The assigned item remains `[ ]`. No positive proof body, root closure, proof receipt, audit
completion, theorem completion, validation completion, release decision, or master acceptance is
claimed. `.stage1-worker-selftest.json` is deliberately absent because this requested positive
proof phase is not genuinely complete.

## Failed Gate And Retry

The prerequisite `S56-M-1200-OBLIGATION_TREE` is still provisional `[_]`, rather than accepted
`[x]`, so dependency-ordered proof acceptance is unavailable. Independently, the first semantic
failure is rev-5.6 section 5.1 exact-target consistency at `M1200-S-BOUNDARIES`: the analytic
compact-support test class is trivial and makes the frozen universal target false. The minimal
root cut remains `M1200-C-TEST`; the invalidated or open chain is `M1200-S-BOUNDARIES`,
`M1200-C-TEST`, and `M1200-ROOT`. This recheck proposes blocker classification `[H5, M5, R3]`
from `[H3, M4, R3]`; it does not alter any authoritative state.

Positive proof work may resume only after an authorized statement-phase repair uses the smooth
order denoted `infinity`, publishes a new or transitive statement fingerprint and an
order-sensitive mutation, and freshly freezes and accepts the statement, anchor audit, obligation
registry, and typed graphs in dependency order. The other legal route is explicit scheduler
redirection to the already checked counterexample or barrier target.

There were 47 pre-existing `proof-recheck-*.json` records and 47 matching Markdown records, plus
`proof-blocker.json`. File counts do not establish private scheduler tick identity. The
authoritative assignment reports `attempts: 0`, so the master must reconcile actual attempts and
apply the five-unresolved-tick split rule. Regardless of that accounting, the checked refutation
forbids a positive proof attempt against the unchanged target.

## Validation

All credited commands ran from the worker-clone repository root. They reused the automation-
provided link to canonical pinned `.lake` artifacts without modifying it. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or other dependency mutation was run.
Lean outputs were confined to a fresh `/tmp` directory and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | Rank 394, lifecycle `planned`, baseline `L0`, `rework_required: true`, and `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1200/check_statement.py` | 0 | Expression SHA `b77d79ed...ca93`, pinned Lean/mathlib, and four killed structural mutations. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS`: 14 obligations and 54 typed edges; denominator `9915c444...c54931`; root and construction remain M4. |
| Isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | Statement, countermodel, conditional composition, and proof-phase barrier elaborated. Every printed axiom set was exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration occurs in the owned Lean sources. |
| `cd Formalizations/Lean/.lake/packages/mathlib && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386...`, tree `bdc39a31...`. |
| Structured artifact check below | 0 | `PASS current-base THM-M-1200 blocker invariants and source hashes`. |
| Scoped whitespace checks below | 0 | No whitespace errors in either new artifact or tracked scoped changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
target="$repo/Stage1_Instances/THM-M-1200"
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
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-9ce5b15a-slot36.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for module in Statement Counterexample ObligationTree ProofRefutation; do
  cp "$target/$module.lean" "$tmp/$module.lean"
done
cd "$mathlib"
for module in Statement Counterexample ObligationTree ProofRefutation; do
  if [ "$module" = Statement ]; then
    module_path="$base_path"
  else
    module_path="$tmp:$base_path"
  fi
  LEAN_PATH="$module_path" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 600 \
    lake env lean --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" \
      >"$tmp/$module.log" 2>&1
done
cat "$tmp/Statement.log" "$tmp/Counterexample.log" \
  "$tmp/ObligationTree.log" "$tmp/ProofRefutation.log" >"$tmp/kernel.log"
cat "$tmp/kernel.log"
sha256sum "$tmp/Statement.olean" "$tmp/Counterexample.olean" \
  "$tmp/ObligationTree.olean" "$tmp/ProofRefutation.olean" "$tmp/kernel.log"
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

The structured check parses the JSON, binds it to `HEAD` and `HEAD^{tree}`, verifies the negative
and open-state invariants, compares all recorded source hashes, checks the 48/49 record counts, and
requires the root self-test manifest to remain absent.

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9ce5b15a-slot36.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

artifact = Path(
    "Stage1_Instances/THM-M-1200/"
    "proof-recheck-2026-07-15-head-9ce5b15a-slot36.json"
)
data = json.loads(artifact.read_text(encoding="utf-8"))
base = Path("Stage1_Instances/THM-M-1200")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip()

assert data["item_id"] == "S56-M-1200-PROOF"
assert data["theorem_id"] == "THM-M-1200"
assert data["base_revision"] == head and data["base_tree"] == tree
assert data["verdict"] == "blocked" and data["state"] == "[ ]"
assert data["changed_paths"] == [str(artifact), str(artifact.with_suffix(".md"))]
assert data["countermodel_exact_type"] == (
    "Not Stage1Instances.THM_M_1200.RankineHugoniotTarget"
)
assert data["proof_phase_barrier_exact_type"] == (
    "Not Stage1Instances.THM_M_1200.NonzeroTracePackage"
)
for key in (
    "proof_body_added", "positive_root_proof_exists", "proof_phase_complete",
    "root_closed", "audit_complete", "theorem_complete", "selftest_manifest_written",
):
    assert data[key] is False
assert data["negative_barrier_body_present"] is True
assert data["accepted_receipt_ids"] == []
assert data["content_addressed_recipe_ids"] == []
assert data["content_addressed_receipt_ids"] == []
assert not Path(".stage1-worker-selftest.json").exists()

for name, expected in data["source_hashes"].items():
    path = (
        Path("Formalizations/Lean") / name
        if name in {"lean-toolchain", "lake-manifest.json"}
        else base / name
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected

history = data["retry_history"]
recheck_json = list(base.glob("proof-recheck-*.json"))
recheck_md = list(base.glob("proof-recheck-*.md"))
assert len(recheck_json) == history["proof_recheck_json_records_including_this_one"] == 48
assert len(recheck_md) == history["proof_recheck_markdown_records_including_this_one"] == 48
assert len(recheck_json) + 1 == history["structured_blocker_records_including_this_one"] == 49
assert history["authoritative_dag_attempts"] == 0
assert not history["record_count_proves_tick_count"]
assert history["master_tick_reconciliation_required"]
print("PASS current-base THM-M-1200 blocker invariants and source hashes")
PY
```

Because ordinary `git diff --check` ignores untracked files, the complete whitespace check is:

```bash
git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9ce5b15a-slot36.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-9ce5b15a-slot36.json \
  || test $? -eq 1
```

This is durable blocker evidence, not a completion receipt. It changes no Lean source, frozen
predecessor artifact, scheduler authority, dependency artifact, or unrelated target.
