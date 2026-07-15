# THM-M-1200 proof-phase current-base blocker recheck

Item: `S56-M-1200-PROOF`. Execution rank: 394. Phase: `proof`.
Base revision: `bf6126986da025eabca097776ede0ba9484bbf71`.
Base tree: `98c8e9b005d8d255ee3e05a1c34a449daf02a5a5`.
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
analytic order `omega`, whereas a smooth compactly supported bump has order
`(infinity : WithTop ENat)`. Analytic uniqueness and compact support force every admissible `phi`
to be zero, so `InterfaceDefectVanishes` holds for every jump coefficient. Specializing the frozen
target to `f = 0`, `uL = 0`, `uR = 1`, and `s = 1` would then require the false equation `1 = 0`.

This refutes only the frozen analytic-test encoding, not the Rankine-Hugoniot theorem with smooth
compactly supported test functions. Replacing the regularity order in this proof worker would
change the frozen statement and invalidate its dependent audit and obligation artifacts. The
conditional composition theorem cannot close the root either: it assumes the now-refuted
`NonzeroTracePackage`.

The assigned item remains `[ ]`. No positive proof body, root closure, proof receipt, audit
completion, theorem completion, validation completion, release decision, or master acceptance is
claimed. `.stage1-worker-selftest.json` is deliberately absent because this requested positive
proof phase is not genuinely complete.

## Failed Gate And Retry

The prerequisite `S56-M-1200-OBLIGATION_TREE` is still provisional `[_]`, rather than accepted
`[x]`, so dependency-ordered proof acceptance is unavailable. Independently, the first semantic
failure is `S56-5.1-EXACT-TARGET-CONSISTENCY / M1200-S-BOUNDARIES`: the analytic compact-support
test class is trivial and makes the frozen universal target false. The minimal open root cut remains
`M1200-C-TEST`; the invalidated or open chain is `M1200-S-BOUNDARIES`, `M1200-C-TEST`, and
`M1200-ROOT`. This recheck proposes the blocker classification `[H5, M5, R3]` from the provisional
`[H3, M4, R3]`; it does not alter any authoritative state.

Positive proof work may resume only after an authorized statement-phase repair uses the smooth
order `(infinity : WithTop ENat)`, publishes a new statement fingerprint, and freshly freezes and
accepts the statement, anchor audit, obligation registry, and typed graphs in dependency order. The
other legal route is explicit scheduler redirection to the already checked counterexample or
barrier target.

The directory contained 36 preexisting `proof-recheck-*.json` records before this artifact; this is
the 37th, and the structured count is 38 when `proof-blocker.json` is included. File counts do not
establish private scheduler tick identity. The authoritative assignment reports `attempts: 0`, so
the master must reconcile actual attempts against the five-tick split rule instead of inferring
attempts from duplicated worker records. Regardless of that accounting, the checked refutation
forbids a positive proof attempt against the unchanged target.

## Validation

All credited commands ran from the worker-clone repository root. They reused the automation-
provided symlink to the canonical pinned `.lake` artifacts without modifying it. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or other dependency mutation was run.
Lean outputs were confined to a fresh `/tmp` directory and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | JSON reports rank 394, lifecycle `planned`, baseline `L0`, `rework_required: true`, `legacy_artifacts_accepted: false`, and `theorem_complete: false`. |
| `git status --short` before this report | 0 | Exactly `?? Formalizations/Lean/.lake`; the owned target path and root self-test path were clean. |
| `python3 Stage1_Instances/THM-M-1200/check_obligation_tree.py` | 0 | `PASS THM-M-1200 obligation tree: 14 obligations, 54 typed edges`; denominator `9915c4444fa19015a1a5aa3413871c87dafe1aeafb0ef4ab8540cacc01c54931`; root and nonzero-trace construction remain open at M4. |
| Isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | Statement, countermodel, conditional composition, and proof-phase barrier elaborated. Every printed axiom set was exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-token scan below | 1 | Expected no-match: no prohibited proof device or declaration occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| Structured artifact check below | 0 | Printed `PASS current-base THM-M-1200 blocker invariants and source hashes`. |
| Scoped whitespace checks below | 0 | No whitespace errors in either new owned artifact or tracked scoped changes. |
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
tmp=$(mktemp -d /tmp/thm-m-1200-proof-head-bf612698-slot36.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
for module in Statement Counterexample ObligationTree ProofRefutation; do
  cp "$repo/Stage1_Instances/THM-M-1200/$module.lean" "$tmp/$module.lean"
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
  "$tmp/ObligationTree.olean" "$tmp/ProofRefutation.olean"
sha256sum "$tmp/kernel.log"
```

Output SHA-256 values:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `74f5f45b992141e003cee16879671aea16eb7e14174374070dd37062f35276b0` |
| `Counterexample.olean` | `3f4ccc8963bc2e801b8d2ed33909e9ed67d34503008f3b210ae96049791b6485` |
| `ObligationTree.olean` | `c3ab556b8209466f1dcbf67faeec45834fa5bd9d242dc797b05f1f221a844044` |
| `ProofRefutation.olean` | `1ae262cb2c3a2a9c6657721427154adb08f87bd9eac9ad9f0ffd571917cf8d08` |
| combined Lean output | `a91296be37b65fbe52ab3ec716c621079391b7ba096adb37d520cacf83b37aa0` |

The exact prohibited-token scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|unsafe|opaque|extern|external|constant)[[:space:]]' \
  Stage1_Instances/THM-M-1200 --glob '*.lean'
```

The structured check parsed the JSON, compared its base revision and tree to `HEAD`, verified all
negative/open-state invariants and exact source hashes, checked the 37/38 record counts, and required
the root self-test manifest to remain absent. The exact inline recipe was:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-bf612698-slot36.json \
  >/dev/null
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess

artifact = Path(
    "Stage1_Instances/THM-M-1200/"
    "proof-recheck-2026-07-15-head-bf612698-slot36.json"
)
data = json.loads(artifact.read_text(encoding="utf-8"))
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
tree = subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], text=True
).strip()
assert data["item_id"] == "S56-M-1200-PROOF"
assert data["theorem_id"] == "THM-M-1200"
assert data["execution_rank"] == 394
assert data["phase"] == "proof"
assert data["base_revision"] == head
assert data["base_tree"] == tree
assert data["verdict"] == "blocked" and data["state"] == "[ ]"
assert data["changed_paths"] == [str(artifact), str(artifact.with_suffix(".md"))]
assert data["exact_statements_added_or_changed"] == []
assert data["countermodel_exact_type"] == (
    "Not Stage1Instances.THM_M_1200.RankineHugoniotTarget"
)
assert data["proof_phase_barrier_exact_type"] == (
    "Not Stage1Instances.THM_M_1200.NonzeroTracePackage"
)
assert not data["proof_body_added"]
assert data["negative_barrier_body_present"]
assert not data["positive_root_proof_exists"]
assert not data["proof_phase_complete"]
assert not data["root_closed"]
assert not data["audit_complete"]
assert not data["theorem_complete"]
assert data["accepted_receipt_ids"] == []
assert data["content_addressed_recipe_ids"] == []
assert data["content_addressed_receipt_ids"] == []
assert not data["selftest_manifest_written"]
assert data["validation"]["worker_selftest_manifest_absent"]
assert not Path(".stage1-worker-selftest.json").exists()

base = Path("Stage1_Instances/THM-M-1200")
for name, expected in data["source_hashes"].items():
    path = (
        Path("Formalizations/Lean") / name
        if name in {"lake-manifest.json", "lean-toolchain"}
        else base / name
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected

rechecks = list(base.glob("proof-recheck-*.json"))
blockers = rechecks + [base / "proof-blocker.json"]
history = data["retry_history"]
assert len(rechecks) == history["proof_recheck_records_including_this_one"] == 37
assert len(blockers) == history["structured_blocker_records_including_this_one"] == 38
assert history["preexisting_proof_recheck_records"] == 36
assert history["preexisting_structured_blocker_records_including_proof_blocker_json"] == 37
assert history["authoritative_dag_attempts"] == 0
assert not history["record_count_proves_tick_count"]
assert history["master_tick_reconciliation_required"]
print("PASS current-base THM-M-1200 blocker invariants and source hashes")
PY
```

Because ordinary `git diff --check` ignores untracked files, the complete whitespace check was:

```bash
git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-bf612698-slot36.md \
  || test $? -eq 1
git diff --check --no-index /dev/null \
  Stage1_Instances/THM-M-1200/proof-recheck-2026-07-15-head-bf612698-slot36.json \
  || test $? -eq 1
```

This is durable blocker evidence, not a completion receipt. It changes no Lean source, frozen
predecessor artifact, scheduler authority, dependency artifact, or unrelated target.
