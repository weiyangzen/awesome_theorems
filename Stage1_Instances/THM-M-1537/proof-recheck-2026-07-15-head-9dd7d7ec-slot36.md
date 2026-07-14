# THM-M-1537 proof-phase recheck at 9dd7d7ec (slot36)

Item: `S56-M-1537-PROOF`

Intent: `prove`

Base revision: `9dd7d7ec7d399cdac6abb2a51d3ea55ed5f4b8ca`

Base tree: `af8d932b6def693afe67a997e2be4c6e813036f2`

Recheck date: 2026-07-15 (Asia/Shanghai)

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
premise, not prove the exact target. Merely excluding zero-area horizons would not repair the model:
`thermodynamicEntropy` remains independent at positive area.

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
renewed statement, anchor-audit, and obligation-tree gates.

The prerequisite `S56-M-1537-OBLIGATION_TREE` is also only worker-provisional `[_]`, not
master-accepted `[x]`. The proof item stays `[ ]`. No audit-completion, theorem-completion,
validation, release, receipt acceptance, scheduler transition, or master-acceptance claim is made.
Because the assigned positive phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The automation-provided
untracked `Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 0 | Canonical expression SHA-256 `0294eb7c...7cc8`; all four structural mutations had distinct hashes. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | Exact statement, six pinned mathlib probes, the partial Physlib candidate, and the `M4` boundary agree. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; denominator `8c57fc2c...c19`; root remains refuted at `M5`. |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | Both invocations exited 0. The exact statement, conditional composition, and countermodel refutation elaborated; both printed declarations report only `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `21763c76...c4224`; statement output SHA-256: `ff89d33c...61fb`; obligation output SHA-256: `a3249e7c...e802b`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1537/Statement.lean Stage1_Instances/THM-M-1537/ObligationTree.lean` | 1 | Expected no-match result: no prohibited construct in the checked Lean sources. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1537/proof-recheck-2026-07-15-head-9dd7d7ec-slot36.json` | 0 | Fresh structured blocker record is valid JSON. |
| scoped Python proof-blocker invariant check | 0 | Item, theorem, base revision/tree, source hashes, blocked state, negative-evidence booleans, changed paths, and self-test absence agree. |
| `git diff --no-index --check /dev/null <artifact>` for each fresh artifact | 0 wrapper | Each comparison returned the expected new-file difference status `1` and emitted zero whitespace-diagnostic bytes. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
TMP=$(mktemp -d /tmp/thm-m-1537-slot36-9dd7d7ec.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(lake env which lean)
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
cp ../../Stage1_Instances/THM-M-1537/Statement.lean "$TMP/Statement.lean"
cp ../../Stage1_Instances/THM-M-1537/ObligationTree.lean "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" timeout 300 \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout 300 \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Exact bound source hashes, output hashes, commands,
failed gate, retry condition, and changed paths are recorded in
`proof-recheck-2026-07-15-head-9dd7d7ec-slot36.json`.

This is fresh, target-specific negative kernel evidence. It is not a proof receipt and does not
satisfy `S56-M-1537-PROOF`.
