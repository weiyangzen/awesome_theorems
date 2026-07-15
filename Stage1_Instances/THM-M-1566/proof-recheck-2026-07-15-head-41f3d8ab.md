# THM-M-1566 proof-phase recheck at current base

Item: `S56-M-1566-PROOF`

Recorded at: `2026-07-15T08:52:15+08:00`

Base revision: `41f3d8abe3a5500190c3f5db50e05104ceeeeb8b`

Base tree: `3ddb4e8f36082a5a71e32c731390fef8207a6987`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM1566.not_GIPCorollary59Target :
  Not (Stage1Instances.THMM1566.GIPCorollary59Target.{0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`.
A universe-polymorphic proof of the positive target would specialize to
universe zero and contradict this declaration.

The frozen target quantifies over every `GIPCorollary59API`, but the API has no
adequacy condition tying its fields to the source mathematics and no
nonemptiness condition on `Solution`. The checked countermodel takes
`Omega := Unit`, the Dirac probability measure, `Unit` for every non-solution
carrier, and `Empty` for `Solution`. Its data assumptions are inhabited at
`alpha = beta = 3/4`. Applying the claimed target produces an inhabitant of
`Empty`. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
the refutation.

This refutes the frozen abstract encoding, not Gubinelli--Imkeller--Perkowski
Corollary 5.9. Merely requiring `Nonempty api.Solution` would also be
insufficient because the API may interpret `solvesLimitEquation` as `False`.
A repair needs concrete analytic semantics or substantive noncircular adequacy
laws. Adding either during this phase would change the frozen statement and
invalidate its downstream fingerprints. The conditional theorem
`root_of_existence_and_uniqueness` remains valid, but it consumes the open
existence and uniqueness packages and cannot close the root.

No positive proof body, proof receipt, or frozen obligation was added or
closed. The proof item remains `[ ]`; the recorded dossier vector remains
`[H1, M4, R3]`, with `[H1, M5, R3]` only the proposed diagnosis for the
refutable encoding. Proof-phase completion, root closure, audit completion,
validation, release, theorem completion, and master acceptance are all false.
Because the assigned phase is not complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Failed Gate And Retry

The first failed gate in this phase is the positive kernel-closure gate for
`S56-M-1566-PROOF` / `M1566-ROOT`. The section 5.1 statement elaboration and
mutation checks pass; the checked refutation shows that their frozen output
cannot receive a positive proof body. The defect originates in the unconstrained
interface modeled by `M1566-S-INTERFACE`, which must be repaired and refrozen.
The predecessor graph records `M1566-T-EXISTENCE` and
`M1566-T-UNIQUENESS` as the root cut. Existence cannot hold for the empty-
solution API; uniqueness is vacuous in that particular model and remains open
in the predecessor registry. The actionable repair cut therefore starts at
`S56-M-1566-STATEMENT`, `M1566-S-INTERFACE`, and `M1566-ROOT`.

Resume only after an authorized statement revision replaces the universal
unconstrained API with a fixed source-faithful implementation or adds
noncircular adequacy hypotheses that entail the analytic semantics and an
appropriate solution type. Accept a new exact expression fingerprint, refreeze
the anchor audit and obligation registry, and rerun all downstream phases
before attempting a positive proof.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network access, or `.lake` mutation was performed. Temporary Lean objects were
created under `/tmp` and removed by a shell trap. The pre-edit worktree was
already non-clean solely because of that automation symlink; the final status
also contains the two untracked owned artifacts. This evidence is nonrelease.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | Rank 182; planned lifecycle; theorem incomplete. |
| `timeout --foreground 300s python3 Stage1_Instances/THM-M-1566/check_statement.py` | 0 | Canonical expression SHA-256 `70ee4869...473a`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | Four candidates, four search records, five pinned Lean support probes, and the M4 boundary agreed. |
| `python3 Stage1_Instances/THM-M-1566/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `7ae15c07...3fe640`; the predecessor graph still records the root as open M4. |
| `timeout --foreground 300s python3 Stage1_Instances/THM-M-1566/validate_obligation_tree.py` | 0 | The exact statement and conditional composition elaborated; the composition reports `[propext, Classical.choice, Quot.sound]`. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement and refutation elaborated; `not_GIPCorollary59Target` has the exact type above and reports `[propext, Classical.choice, Quot.sound]`. Object hashes were `1e1c07...2793` and `611605...62f3`; the temporary directory was removed. |
| `rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|opaque|constant|unsafe|external)[[:space:]]' Stage1_Instances/THM-M-1566 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-41f3d8ab.json` | 0 | The current-base structured blocker record is valid JSON. |
| Inline Python assertion recipe below | 0 | Item/base identity, exact input hashes, open-root flags, empty proof credit, `[ ]` state, changed paths, and absent self-test all agreed. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1566/proof-recheck-2026-07-15-head-41f3d8ab.json` and the same command for the Markdown artifact | 1, 1 | Expected added-file status with empty diagnostic output; no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1566` | 0 | No whitespace errors in tracked owned-path changes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-1566-proof-recheck-41f3d8ab.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$repo/Stage1_Instances/THM-M-1566/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-1566/ProofCountermodel.lean" "$tmp/ProofCountermodel.lean"
lean=$(cd "$repo/Formalizations/Lean" && lake env which lean)
lean_path=$(cd "$repo/Formalizations/Lean" && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
sha256sum Statement.olean
LEAN_NUM_THREADS=1 LEAN_PATH=.:"$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" -o ProofCountermodel.olean ProofCountermodel.lean
sha256sum ProofCountermodel.olean
```

The inline invariant check parsed the paired JSON, compared `base_revision`
and `base_tree` with `git rev-parse HEAD` and `git rev-parse HEAD^{tree}`, and
asserted the recorded state booleans, empty receipt list, absent self-test, exact
changed-path list, and SHA-256 values of all eight files under `source_hashes`.
The assertions are replayable from the repository root with:

```bash
python3 - <<'PY'
import hashlib, json, subprocess
from pathlib import Path

root = Path.cwd()
rel = Path("Stage1_Instances/THM-M-1566")
name = "proof-recheck-2026-07-15-head-41f3d8ab.json"
d = json.loads((root / rel / name).read_text())
assert d["item_id"] == "S56-M-1566-PROOF"
assert d["base_revision"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True).strip()
assert d["base_tree"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], text=True).strip()
assert d["state"] == "[ ]" and d["verdict"] == "blocked"
assert d["canonical_target_refuted"] and not d["proof_phase_complete"]
assert not d["root_closed"] and not d["audit_complete"]
assert not d["theorem_complete"] and d["accepted_receipt_ids"] == []
assert not (root / ".stage1-worker-selftest.json").exists()
assert d["changed_paths"] == [str(rel / name), str(rel / name.replace(".json", ".md"))]
for file_name, expected in d["source_hashes"].items():
    assert hashlib.sha256((root / rel / file_name).read_bytes()).hexdigest() == expected
print("PASS current-base blocker invariants and hashes")
PY
```

The bound input hashes and environment fingerprint are recorded in the paired
JSON artifact. This is durable blocker evidence, not a proof receipt.
