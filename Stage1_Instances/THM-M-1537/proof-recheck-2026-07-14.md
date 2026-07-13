# THM-M-1537 proof-phase recheck

Item: `S56-M-1537-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `309f58b7a54d36653b3483a543c6378eea53882c`

Base tree: `1051ab77fe56d6e32ba26761bbcfd3ad8a258743`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. In
`SemiclassicalBlackHole`, `thermodynamicEntropy` is an independent real field;
the stationary, Einstein-gravity, semiclassical, area, and constant premises
do not relate it to `entropyFromArea`.

The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

kernel-checks at trust level zero. Its admissible record has horizon area zero,
entropy one, all four constants one, and all three regime propositions true.
Every premise holds, while `entropyFromArea` reduces to zero, contradicting the
claimed equality `1 = 0`.

This refutes only the frozen formal encoding, not the physical
Bekenstein-Hawking law. The local `areaLaw_of_bridge` theorem is conditional on
`AreaLawBridge`, which is definitionally the same universal equality as the
root. Historical `S1_M_200` declarations consume a model or predicate already
carrying an area-law boundary. Neither is a proof of the unconstrained target,
and importing either would hide the missing conclusion as a premise.

The exact root therefore remains `[H2, M5, R3]`; the minimal open root cut is
`M1537-B-PHYSICS`. No proof source, axiom, placeholder, unsafe declaration,
weakened statement, substituted theorem, or unpinned dependency was added.

## Failed Gate And Retry

The first failed gate is `M1537-B-PHYSICS` / exact-target consistency. Positive
proof work can resume only after an authorized statement-phase repair gives
the physical regime substantive entropy-area semantics, followed by new
accepted statement and obligation-registry versions and renewed anchor-audit
and obligation-tree gates.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 0 | canonical expression SHA-256 `0294eb7c5af32d8a7dfc2abf6ff5ac0431343f4eeab5fe4d331217a398d07cc8`; all four required mutations had distinct hashes |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | nine obligations and 16 typed edges passed; denominator `8c57fc2c6fdba40bd4293e06ca656fbe2cc371cbe00d7ac34528108b2fb13c19`; root remains refuted at M5 |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | exact statement, conditional composition, and countermodel refutation elaborated; both printed declarations report only `[propext, Classical.choice, Quot.sound]` |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe\|implemented_by\|native_decide' Stage1_Instances/THM-M-1537/Statement.lean Stage1_Instances/THM-M-1537/ObligationTree.lean` | 1 | expected no-match result: no prohibited construct in the checked Lean sources |
| `python3 -m json.tool Stage1_Instances/THM-M-1537/proof-recheck-2026-07-14.json` | 0 | fresh structured blocker record is valid JSON |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1537/proof-recheck-2026-07-14.json` and the same command for the Markdown record | 1 each | expected new-file difference exits; neither command printed a whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
TMP=$(mktemp -d ./proof-recheck.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp ../../Stage1_Instances/THM-M-1537/Statement.lean "$TMP/Statement.lean"
cp ../../Stage1_Instances/THM-M-1537/ObligationTree.lean "$TMP/ObligationTree.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
lake env lean --trust=0 -t0 \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" \
  lake env lean --trust=0 -t0 "$TMP/ObligationTree.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Bound source SHA-256 values are
recorded in `proof-recheck-2026-07-14.json`.

This is real negative kernel evidence and an actionable blocker, not a proof
receipt. It does not satisfy the assigned positive proof item or claim audit
completion, theorem completion, validation, release, or master acceptance.
Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
