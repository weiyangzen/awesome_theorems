# THM-M-1235 proof-phase recheck at `f53223e6`

Item: `S56-M-1235-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T18:05:08+08:00`

Base revision: `f53223e6746df4856b00068d3e8723264dfd044a`

Base tree: `bb293e5342b6501791d40c7464d150820aafe441`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

freshly kernel-checks at trust level zero against the current pinned
environment. `Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`, not proofs of predicates constraining the five motion
functions. Updating an alleged unique motion's `velocityX` to `velocityX + 1`
therefore preserves the `Motion` type. `SameMotion` would equate the original
and updated velocity functions, but evaluation at `(0, 0), 0` yields the
contradiction `x + 1 = x`. The concrete `counterexampleData` discharges every
explicit premise of the target.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, conditional, or otherwise substituted proposition
would violate the assigned exact-target gate. `root_of_existence_and_uniqueness`
assumes both substantive packages and provides only conditional composition; it
does not supply a positive root proof. The bounded pinned-mathlib recheck also
found no exact positive anchor.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. No `.stage1-worker-selftest.json` is written because the
requested positive proof phase is not genuinely complete. The planned instance
record remains `[H2, M4, R4]`, and the later worker-provisional graph remains
`[H3, M3, R4]`; this packet proposes `[H5, M5, R4]` only as a diagnosis for
master reconciliation.

## Failed gate and retry

The first failed gate is the rev-5.6 section 5.1 exact-statement/encoding gate
at `M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the primary source justifies equality of globally
defined functions. Re-audit the source and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, structured validation recipes, and dependent evidence before
proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` is only worker-provisional, so master proof
acceptance is independently dependency-blocked. Forty-two earlier structured
proof-recheck JSON packets were present at this base while the authoritative
DAG still records `attempts=0` and no child nodes. The master/scheduler must
reconcile that history. Section 10.2 requires reopening or splitting the
invalid upstream work after five unresolved execution ticks rather than
scheduling another identical proof-only retry. This worker did not edit the
DAG or generated checklist.

## Validation

All checks reused the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network access, or `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence. Temporary Lean sources and objects were
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root remains open M3. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression digest `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four structural mutations were killed; pins matched. |
| Isolated trust-zero pinned-Lean recipe below | 0 | Exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| Bounded pinned-mathlib source search for Wolibner, Euler, vorticity, Biot-Savart, perfect fluid, and ideal fluid terms | 1 | Expected no-match: no positive Wolibner/fluid-PDE anchor was found. |
| Environment revision, clean-status, and frozen-input hash commands | 0 | Lean 4.29.0, Lake 5.0.0, dependency revisions/trees, clean dependency states, and all frozen input hashes matched the JSON packet. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-f53223e6-slot22.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`. Frozen input SHA-256 values are recorded in the paired JSON
artifact.

## Status boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
