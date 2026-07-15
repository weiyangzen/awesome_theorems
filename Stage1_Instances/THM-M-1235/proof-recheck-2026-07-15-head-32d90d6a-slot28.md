# THM-M-1235 current-base proof blocker

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `32d90d6afe5c1ba9d60738ca106ee0ee0f29409f`

Base tree: `7768f7f323b0dc6d23410eb8ea6898f6d0c908dd`

Recorded: `2026-07-15` (Asia/Shanghai)

## First failed gate

The rev-5.6 section 5.1 exact-target consistency gate fails at
`M1235-S-DEFINITIONS`. The frozen `Motion` structure stores conditions
`(I)`--`(VIII)` as freely chosen values of type `Prop`; it does not store
predicates of the five motion functions or proofs that those predicates hold.
Its functions are therefore unconstrained while `SameMotion` demands global
equality of all five functions.

The tracked placeholder-free theorem

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

changes an alleged unique motion's `velocityX` to `velocityX + 1`. It remains
a `Motion`, but `SameMotion` would equate the changed and original velocity
functions; evaluation at `(0, 0), 0` gives the contradiction `x + 1 = x`.
`counterexampleData` discharges all explicit target premises at `T = 1`.

The tracked `IndependentRefutation.lean` separately changes `pressure` by
`+1` and derives the same contradiction through a different `SameMotion`
conjunct. Both exact negations elaborated with `--trust=0` and reported exactly
`[propext, Classical.choice, Quot.sound]`. A legal positive proof cannot coexist
with either refutation in a consistent Lean environment. This refutes the
frozen formal encoding, not Wolibner's mathematical theorem. Proving a
corrected, weaker, conditional, or differently scoped proposition would be a
forbidden proof-phase substitution. In particular,
`root_of_existence_and_uniqueness` is conditional composition only.

## Current-base validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone, fetch, checkout, network access, or `.lake`
mutation was performed. Temporary Lean files and objects were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Expression digest `77aec2f5...` and pinned identities matched; all four structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff35...`; root open M3, existence and uniqueness M4. |
| Isolated pinned-Lean replay of `Statement.lean`, `Proof.lean`, and `IndependentRefutation.lean` | 0 | The statement and both independently implemented exact negations elaborated at trust zero; all axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan of both negative Lean modules | 1 | Expected no-match exit; no prohibited proof construct was found. |
| Pinned mathlib search for Wolibner and global two-dimensional Euler anchors | 1 | Expected no-match exit; no plausible terminal theorem was found in the pinned snapshot. |
| Toolchain, dependency revision/tree, environment, and frozen-input hash checks | 0 | Lean 4.29.0 at `98dc76e3...`; mathlib `8a178386...`; flt-regular `56161b6e...`; all recorded hashes matched. |
| Structured JSON and focused invariant checks | 0 | JSON syntax, identity, base, blocker flags, state, evidence count, prior-packet count, and changed paths passed. |
| Scoped and no-index whitespace checks | 0 | No whitespace diagnostics; no-index checks returned only the expected new-file difference status. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is deliberately absent. |

Exact tracked replay from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-32d90d6a-slot28.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cp "$target/IndependentRefutation.lean" "$tmp/IndependentRefutation.lean"
cd "$lean_root"
lean=$(timeout 120 lake env which lean)
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/IndependentRefutation.olean" \
  "$tmp/IndependentRefutation.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/IndependentRefutation.olean"
```

The object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean`,
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`, and
`a06c3ab25b0a901364d85a3ac1b2993452810f88edf013f3458545d6622b4b5d`
for `IndependentRefutation.olean`.

## Retry boundary

Reopen `S56-M-1235-STATEMENT`. Define conditions `(I)`--`(VIII)` as
predicates of the five functions and make `Motion` carry their proofs. Scope
uniqueness to the source domain and `0 <= t <= T` unless the primary source
justifies global function equality. Then re-audit the source and version and
re-freeze the canonical expression fingerprint, crosswalk, obligation
registry, typed graphs, and dependent evidence before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so master proof
acceptance is independently dependency-blocked. Forty-eight earlier structured
proof-recheck packets are already tracked while the authoritative DAG still
records `attempts=0` and no children. The master/scheduler must reconcile the
history and apply section 10.2's reopen/split rule rather than schedule another
identical proof-only retry.

## Status boundary

Lifecycle remains `planned`. The intake manifest remains `[H2, M4, R4]`; the
later provisional typed graph remains `[H3, M3, R4]`. This run changes neither
and proposes `[H5, M5, R4]` only as a diagnosis for master reconciliation. It
adds negative nonrelease blocker evidence, not a positive proof body, closed
obligation, receipt, provisional or accepted state, audit completion, theorem
completion, validation, release, or master acceptance. Because the assigned
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is not
written.
