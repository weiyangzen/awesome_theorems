# THM-M-1235 proof-phase recheck at `cff518b49`

Item: `S56-M-1235-PROOF`

Intent: `prove`

Recheck date: `2026-07-16T01:02:46+08:00`

Base revision: `cff518b49c10dc043854d984bb38a0748aa4f3a0`

Base tree: `751ce4527826593f7fccac18160af616cf18b8cf`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target. Two independent,
tracked, placeholder-free declarations freshly elaborate at Lean trust level zero:

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness

Stage1Instances.THMM1235.independently_not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values of type `Prop`. They
are not proofs of predicates constraining the five motion functions. The primary refutation changes
an alleged unique motion's `velocityX` to `velocityX + 1`; the independent refutation changes its
`pressure` to `pressure + 1`. Both structure updates preserve the frozen `Motion` type. `SameMotion`
would equate the changed function to the original, but evaluation at `(0, 0), 0` reduces that
equality to the contradiction `x + 1 = x`. Concrete source data discharge every explicit premise
because the domain and regularity fields are likewise freely chosen propositions.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem. Proving a corrected,
weaker, specialized, or conditional proposition in this item would be forbidden target substitution.
The conditional `root_of_existence_and_uniqueness` in `ObligationTree.lean` assumes the substantive
existence and uniqueness packages and therefore supplies no positive root proof credit. The pinned
candidate audit still identifies no positive exact Wolibner proof anchor.

The item remains `[ ]`. No proof receipt, closed obligation, accepted state, audit completion,
theorem completion, validation completion, or release is claimed. No
`.stage1-worker-selftest.json` is written because the requested positive proof phase is not
genuinely complete or self-tested. The frozen graph remains `[H3, M3, R4]`; this run proposes only
an `H5/M5/R4` exact-target diagnosis for master reconciliation.

## Failed Gate And Retry

The first failed gate is rev-5.6 section 5.1 exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`; replace semantic proposition placeholders with
actual predicates of the five functions and make `Motion` carry proofs of conditions `(I)`-`(VIII)`.
Re-audit uniqueness over the source domain and `0 <= t <= T` against the primary source. Then
publish a versioned re-freeze of the canonical expression fingerprint, source crosswalk, obligation
registry, typed graphs, and dependent evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` is still worker-provisional (`[_]`) rather than
master-accepted, so proof acceptance is independently dependency-blocked. Later gates also remain
open: `validation-specs.json` uses legacy shell-command strings rather than the structured recipe
schema required by rev-5.6 section 10.5, and the intake README, crosswalk, and local task DAG have
not been reconciled with the later source pinpoints and checked refutation. None changes the earlier
truth blocker.

Fifty-six earlier structured proof-recheck JSON packets were already present while the
authoritative DAG still records `attempts=0` and no children. The master/scheduler should reconcile
the execution history and reopen or split the invalid upstream statement work under section 10.2
instead of issuing another identical proof-only retry. This worker did not edit authoritative
state.

## Validation

All checks ran inside this worker clone and reused the automation-provided untracked
`Formalizations/Lean/.lake` symlink read-only. No `lake update`, `lake build`, dependency
clone/fetch/checkout, network access, or `.lake` mutation was performed. Temporary Lean sources and
objects were removed. The shared dependency-cache symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Expression digest `77aec2f5...` and pins matched; all four structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff35...`; root open M3, existence and uniqueness M4. |
| Isolated pinned-Lean replay below | 0 | The exact statement and both tracked negative modules elaborated with `--trust=0 -t0`; all four negative axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scans over both negative modules | 0 | Both scans produced the required no-match result; neither module contains `sorry`, `admit`, bodyless declarations, unsafe/oracle constructs, or `native_decide`. |
| Toolchain, dependency revision/tree, and frozen-input hash checks | 0 | Lean 4.29.0 at `98dc76e3...`; mathlib `8a178386...`; flt-regular `56161b6e...`; all recorded hashes matched and both dependency worktrees were clean. |
| Existing-packet boundary audit | 0 | All 56 predecessor JSON packets remain `[ ]`, root-open, and theorem-incomplete. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists for this blocked proof phase. |
| Blocker JSON parse and boundary assertions | 0 | Item/base identity, `blocked` `[ ]` state, checked refutation, open root, incomplete proof/theorem, changed paths, and absent self-test claim matched. |
| New-file whitespace checks | 0 | Both artifacts differ from `/dev/null`, contain no whitespace errors, and end with a newline. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-cff518b49-slot11.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cp "$target/IndependentRefutation.lean" "$tmp/IndependentRefutation.lean"
cd "$lean_root"
base_path=$(env -u LEAN_PATH timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/IndependentRefutation.olean" \
  "$tmp/IndependentRefutation.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/IndependentRefutation.olean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular revision/tree
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

Temporary object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d` for
`Statement.olean`,
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169` for
`Proof.olean`, and
`a06c3ab25b0a901364d85a3ac1b2993452810f88edf013f3458545d6622b4b5d` for
`IndependentRefutation.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does not satisfy
`S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or theorem completion. The retry must
begin with statement correction and a versioned re-freeze; repeating proof search against this
exact encoding cannot close the item.
