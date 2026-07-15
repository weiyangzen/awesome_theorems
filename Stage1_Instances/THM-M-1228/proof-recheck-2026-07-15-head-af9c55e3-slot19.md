# THM-M-1228 proof-phase recheck at `af9c55e3` (slot 19)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `af9c55e3e17639cd0c13bfd85bfb4bf30554785a`

Base tree: `4e842676a2087338f5582d16e365c51c87763af0`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the frozen target
interface. The canonical declaration is a family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

whose three predicate fields have no laws relating suitability, regularity,
or parabolic measure. The tracked, placeholder-free `ProofBlocker.lean`
chooses a permitted semantics in which suitability is true, regularity is
false, and the measure-zero predicate is false. The pinned Lean kernel checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. This is a countermodel to uniform closure of the formal
interface, not a refutation of the mathematical Caffarelli-Kohn-Nirenberg
theorem. Choosing favorable semantics, adding the desired conclusion as a
premise or structure field, using ambient Hausdorff measure, or proving a
smooth, two-dimensional, or global-regularity statement would substitute a
different theorem and was not done.

The prerequisite `S56-M-1228-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted `[x]`. Its registry records no closed obligation, and
`ObligationTree.root_compose` only consumes the still-open per-solution
analytic result. The minimal open machine cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib supplies only adjacent distribution, smoothness, Lp, and
ambient Hausdorff APIs. The immutable candidate audit found no exact eligible
CKN terminal body to pin or import. The proof-relevant inputs are unchanged
from commit `c45f3c709`, where the checked blocker and obligation artifacts
entered history.

Before this packet, 38 JSON and 38 Markdown recheck packets already existed,
although the authoritative DAG still records `attempts: 0` and `children: []`.
This exceeds the five-tick split threshold in section 10.2. Only the master
may reconcile that state and create dependency-legal child items; scheduling
the unchanged monolithic proof task cannot close it.

The lifecycle stays `planned`, the vector stays `H1/M4/R4`, and the assigned
item stays `[ ]`. No positive proof body, closed obligation, receipt, audit
completion, theorem completion, or master acceptance is claimed.

## Validation

All commands ran in this automation clone. The untracked
`Formalizations/Lean/.lake` symlink was supplied by automation and points to
the canonical pinned artifacts. It was used read-only. No Lake update/build,
dependency clone/fetch, network action, or `.lake` mutation was performed.
Lean outputs were written only to an isolated `/tmp` directory and removed by
the validation trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; four mutations reported killed. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable external-tree receipts agree. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | Passed 15 obligations and 31 typed edges; denominator `25704bee...66f41e`; root remains M4 with a four-obligation cut. |
| Isolated pinned `lake env` resolution and `lean --trust=0 -t0` replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated. The blocker and conditional composer report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, bodyless `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token was found. |
| `git diff --exit-code c45f3c709..HEAD -- <proof-relevant inputs>` | 0 | Statement, blocker, composition, registry, graphs, anchor audit, and validation specs are unchanged. |
| `python3 -m json.tool <this JSON packet>` and blocker invariant assertions | 0 | JSON parsed; identity, base, `[ ]` state, unchanged vector, cut set, changed paths, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `git diff --no-index --check /dev/null <each new packet>` | 1 expected each | Both commands produced empty output; exit 1 records content differences, not whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact successful replay core was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d /tmp/thm-m-1228-proof-af9c55e3.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" \
  "$TARGET/ObligationTree.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- blocker stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- composition stdout: `c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
- every stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

## Retry Condition

The master must first reconcile the repeated attempts and predecessor state.
Then reopen and version the statement around fixed, source-faithful analytic
definitions; repair the statement-mutation and node-specific validation
coverage; freeze a corrected, split registry; and implement locally or
immutably pin exact compatible proof bodies for every cut obligation with
checked transport, composition, trust, and terminal-body provenance.

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.
