# THM-M-1006 proof-phase blocker, 2026-07-14

Item: `S56-M-1006-PROOF`

Base revision: `a7c34044268bf5745e40c011134b447dd1e7cd0f`

## Verdict

`blocked`: the exact frozen target is mathematically false. `StatementShape` asks for a finite
constant, uniform in the horizon and martingale, in the discrete square-function comparison for
every `p > 0`. At `p = 1 / 2`, the stopped rare-jump family developed in
`counterexample-analysis.md` has

```text
E[M_N^(1/2)] >= (1/2) N^(1/2),
E[Q_N^(1/4)] <= N^(1/4) + 2^(1/4).
```

Their ratio is unbounded. This contradicts the uniform finite upper constant quantified in
`StatementShape`. It refutes the frozen unrestricted discrete-jump encoding, not the classical
continuous-martingale BDG theorem.

`Counterexample.lean` checks eight supporting algebraic and asymptotic declarations under the pinned
Lean environment. It does not formalize the complete finite probability spaces, filtration,
martingale witness, moment calculations, or `Not (StatementShape (1 / 2))`. Thus the result supports
a proposed human classification of `H5`, subject to master review, while the machine classification
truthfully remains `M3`. No positive proof body, full kernel refutation, proof receipt, or root credit
is claimed.

The first failed gate is exact-target mathematical truth at `M1006-B-P-RANGE`. Because the assigned
positive proof phase is not complete, `.stage1-worker-selftest.json` is deliberately absent and the
workflow item remains `[ ]`.

## Validation Evidence

All Lean commands used the existing automation-provided pinned `.lake` symlink read only. No network
operation, dependency update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1006` | 0 | Rank 286, baseline L0, planned, rework required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py` | 0 | The frozen pre-refutation projection structurally passes with 18 obligations, 49 typed edges, denominator `12818dc1f1f77555b23c3fea780e482518d1d5c196dc1390c8175d00914dac6f`, and its stale open M3 root. |
| Isolated temporary elaboration of `Statement.lean`, followed by `Counterexample.lean` with `lake env lean` and only the temporary statement module added to `LEAN_PATH` | 0 | The exact statement and all eight supporting declarations elaborate. Printed axiom sets are subsets of `[propext, Classical.choice, Quot.sound]`; no `sorryAx`. |
| The same isolated temporary elaboration of `Proof.lean` | 0 | The five pre-existing local leaf declarations elaborate; their printed axiom set is `[propext, Classical.choice, Quot.sound]`. They do not close the root. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx\|^\s*unsafe\s' Stage1_Instances/THM-M-1006 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| Structured blocker identity/hash/state assertions run with an inline read-only Python checker | 0 | Exact item metadata, `[ ]` state, source hashes, denominator, open-root booleans, no receipts, explicit kernel boundary, and absent self-test all passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-1006/proof-blocker-2026-07-14-slot64.json` | 0 | The blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1006` plus `git diff --no-index --check /dev/null <each new artifact>` | 0 / 1 | No whitespace diagnostics; exit 1 from each no-index invocation records only the expected new-file difference. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The exact commands were rerun after final artifact assembly; the table records their results rather
than claiming a hermetic release or independent verification.

### Exact Narrow Recipes

The isolated Lean elaboration command was:

```bash
cd Formalizations/Lean
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1006-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1006/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1006/Counterexample.lean "$tmp/Counterexample.lean"
cp ../../Stage1_Instances/THM-M-1006/Proof.lean "$tmp/Proof.lean"
lake env lean --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
pinned_lean_path=$(lake env printenv LEAN_PATH)
LEAN_PATH="$tmp:$pinned_lean_path" lake env lean --root="$tmp" "$tmp/Counterexample.lean"
LEAN_PATH="$tmp:$pinned_lean_path" lake env lean --root="$tmp" "$tmp/Proof.lean"
```

It exited `0`. `Statement.lean` printed the three frozen declaration types, and the other two
modules elaborated without diagnostics. Their own `#print axioms` commands were replayed in the
same pinned environment; every report was a subset of `[propext, Classical.choice, Quot.sound]` and
none contained `sorryAx`.

The remaining exact commands corresponding to the earlier table rows were:

```bash
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1006
python3 Stage1_Instances/THM-M-1006/check_obligation_tree.py
rg -n '^\s*(sorry|admit|axiom)(\s|$)|sorryAx|^\s*unsafe\s' \
  Stage1_Instances/THM-M-1006 -g '*.lean'
python3 -m json.tool \
  Stage1_Instances/THM-M-1006/proof-blocker-2026-07-14-slot64.json >/dev/null
cd Formalizations/Lean && lake env lean --version
git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
```

Their exits, in order, were `0`, `0`, `0`, `0`, `1`, `0`, `0`, and `0`; the exact results are in
the table above. The `rg` exit `1` is the expected clean no-match result.

The final read-only structured assertion command was:

```bash
python3 - <<'PY'
import hashlib, json, pathlib, subprocess

root = pathlib.Path.cwd()
here = root / "Stage1_Instances/THM-M-1006"
packet = json.loads((here / "proof-blocker-2026-07-14-slot64.json").read_text())
registry = json.loads((here / "obligation-registry.json").read_text())
dag = json.loads((root / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
sha = lambda name: hashlib.sha256((here / name).read_bytes()).hexdigest()

assert packet["item_id"] == "S56-M-1006-PROOF"
assert packet["theorem_id"] == "THM-M-1006"
assert packet["base_revision"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True
).strip()
item = next(row for row in dag["items"] if row["id"] == packet["item_id"])
assert item["state"] == "[ ]"
assert item["owned_paths"] == ["Stage1_Instances/THM-M-1006"]
for key, name in {
    "statement_sha256": "Statement.lean",
    "proof_source_sha256": "Proof.lean",
    "counterexample_source_sha256": "Counterexample.lean",
    "counterexample_analysis_sha256": "counterexample-analysis.md",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
}.items():
    assert packet[key] == sha(name)
assert packet["obligation_registry_denominator_sha256"] == registry["denominator_sha256"]
for key in ("root_closed", "proof_phase_complete", "audit_complete", "theorem_complete"):
    assert packet[key] is False
assert packet["accepted_receipt_ids"] == []
assert packet["full_kernel_refutation_present"] is False
assert not (root / ".stage1-worker-selftest.json").exists()
print("PASS: THM-M-1006 blocker packet is internally consistent; proof state remains [ ]")
PY
```

It exited `0` with the single `PASS` line shown in the command. Final whitespace checks were run
literally as follows:

```bash
git diff --check -- Stage1_Instances/THM-M-1006
git diff --no-index --check /dev/null Stage1_Instances/THM-M-1006/counterexample-analysis.md
git diff --no-index --check /dev/null Stage1_Instances/THM-M-1006/proof-attempt-2026-07-14-slot64.md
git diff --no-index --check /dev/null Stage1_Instances/THM-M-1006/proof-blocker-2026-07-14-slot64.json
```

The first command exited `0`; each no-index command exited `1`, denoting only the expected new-file
difference, and emitted no whitespace diagnostic.

## Retry Condition

Reopen the statement phase and choose a valid, source-faithful formulation: for example, an exponent
range where the discrete square-function comparison holds, sufficient jump control, or the intended
continuous-martingale theorem. A changed statement requires a new fingerprint and fresh acceptance
of the dependent audit, registry, and typed graphs. Alternatively, redirect the item explicitly to
a full kernel-checked counterexample target.

Until then, the authoritative vector remains `[H2, M3, R3]`; this evidence proposes
`[H5, M3, R3]` for master reconciliation. Proof-phase, audit, and theorem completion are all false.
