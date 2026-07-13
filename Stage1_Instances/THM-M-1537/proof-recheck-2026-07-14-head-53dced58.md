# THM-M-1537 proof-phase recheck at 53dced58

Item: `S56-M-1537-PROOF`

Intent: `prove`

Base revision: `53dced5833f17a55f667239e756fc93c99810c44`

Base tree: `f0c4bdb31a84f0b4221b8392c9c95be1441914dc`

Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. In
`SemiclassicalBlackHole`, `thermodynamicEntropy` is an independent real field; the stationary,
Einstein-gravity, semiclassical, area, and constant premises do not relate it to `entropyFromArea`.

The placeholder-free declaration

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

kernel-checks at trust level zero. Its admissible record has horizon area zero, entropy one, all
four constants one, and all three regime propositions true. Every premise holds, while
`entropyFromArea` reduces to zero, contradicting the required equality `1 = 0`.

This refutes the frozen formal encoding, not the physical Bekenstein-Hawking law. The checked local
theorem `areaLaw_of_bridge` consumes `AreaLawBridge`, which is definitionally the same universal
equality as the root. Historical `S1_M_200` declarations consume models or predicates already
carrying an area-law relation. Importing either route would hide the missing conclusion as a
premise, not prove the exact target. Excluding the zero-area boundary alone would not repair the
model: entropy remains independent even at positive area.

The frozen upstream registry records `[H2, M5, R3]`, and this proof-only worker does not mutate that
authoritative vector. The exact formal proposition's checked refutation warrants `H5` under
rev-5.6 section 3.1, while the distinct physical Bekenstein-Hawking law is not refuted. A repaired
statement phase must reconcile that classification boundary. The minimal open cut remains
`M1537-B-PHYSICS`. No proof source, axiom, placeholder, unsafe declaration, weakened statement,
substituted theorem, or unpinned dependency was added.

## Failed Gate

The first failed gate is `M1537-B-PHYSICS` / exact-target consistency. Positive proof work can
resume only after an authorized statement-phase repair gives the physical regime substantive
entropy-area semantics, followed by accepted replacement statement and registry versions and
renewed anchor-audit and obligation-tree gates.

The proof item stays `[ ]`. No audit-completion, theorem-completion, validation, release, receipt
acceptance, scheduler transition, or master-acceptance claim is made. Because the assigned positive
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` remains absent.

## Validation

The final scoped kernel replay used the pinned Lean 4.29.0 binary directly with an explicit
`LEAN_PATH` over already-built canonical package artifacts. This deliberately avoided Lake
dependency resolution. It ran with `--trust=0 -t0`, used temporary source copies, and removed the
temporary directory. The exact statement and negative proof both exited zero. The two printed
declarations report only `[propext, Classical.choice, Quot.sound]`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 0 | Canonical expression SHA-256 `0294eb7c...7cc8`; all four structural mutations had distinct hashes. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | Exact statement, six pinned mathlib probes, the partial Physlib candidate, and the `M4` boundary agree. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; denominator `8c57fc2c...c19`; root remains refuted at `M5`. |
| direct pinned `lean --trust=0 -t0` replay described below | 0 | Exact statement, conditional composition, and countermodel refutation elaborated without Lake dependency resolution. Statement olean SHA-256: `21763c76...c4224`; obligation output SHA-256: `a3249e7c...02b`. |
| isolated `lake env lean --trust=0 -t0` replay after the manifest-pinned closure became available | 0 | Reproduced the direct replay's statement olean and output hashes; both printed declarations reported only `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1537/Statement.lean Stage1_Instances/THM-M-1537/ObligationTree.lean` | 1 | Expected no-match result: no prohibited construct in the checked Lean sources. |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1537/proof-recheck-2026-07-14-head-53dced58.json` | 0 | Fresh structured blocker record is valid JSON. |
| `git diff --no-index --check /dev/null <artifact>` for both fresh artifacts, with raw-exit and empty-output assertions | 0 aggregate | Both raw exits were the expected new-file difference code 1; neither command emitted whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |

The direct replay used these steps from the worker root, with `LEAN_PATH_BASE` formed from the
existing pinned build roots for batteries, Qq, aesop, proofwidgets, importGraph, LeanSearchClient,
plausible, and mathlib:

```bash
TMP=$(mktemp -d /tmp/thm-m-1537-direct-capture.XXXXXX)
cp Stage1_Instances/THM-M-1537/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-1537/ObligationTree.lean "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" timeout 240 \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean" \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout 240 \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean" \
  --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
rm -rf "$TMP"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with clean tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Initial attempts through `lake env` were not accepted as evidence. The automation-provided shared
`.lake` closure exposed an incomplete `flt-regular` checkout and Lake began restoring its
manifest-pinned revision. Those attempts were stopped. Concurrent workers later completed the
shared checkout at pinned revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; this shared cache
change is not an owned-path change or worker deliverable. The final replay above did not invoke
Lake, fetch, build, or any network-capable dependency operation.

The initially affected `check_statement.py` and required isolated `lake env lean` recipes were both
rerun successfully once the manifest-pinned closure became available. The `lake env` replay
reproduced the direct replay's three hashes exactly. Exact source hashes, commands, output hashes,
failed gate, retry condition, and limitations are recorded in the paired JSON artifact.

This is fresh, target-specific negative kernel evidence. It is not a proof receipt and does not
satisfy `S56-M-1537-PROOF`.
