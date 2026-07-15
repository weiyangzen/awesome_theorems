# THM-M-1235 current-base proof blocker

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `fd995645725ec3633e4da7e6d759deb14f530861`

Base tree: `5846121ab94ff0502b98217f643539881bc9c045`

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

This run also tested an independent pressure perturbation in a temporary file:
replacing `pressure` by `pressure + 1` gives the same contradiction through
the fifth `SameMotion` conjunct. Both negative witnesses elaborated with
`--trust=0` and reported exactly `[propext, Classical.choice, Quot.sound]`.
A legal positive proof of the frozen target cannot coexist with either
refutation in a consistent Lean environment. This refutes the formal encoding,
not Wolibner's mathematical theorem. A corrected, conditional, weaker, or
differently scoped proposition would be a forbidden proof-phase substitution.

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
| Isolated pinned-Lean replay of tracked `Statement.lean` and `Proof.lean` | 0 | Exact statement and both tracked negative declarations elaborated at trust zero; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| Isolated pinned-Lean replay of temporary independent pressure perturbation | 0 | Independent exact-target negation elaborated at trust zero with the same axiom report. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit; no prohibited proof construct was found. |
| Toolchain, dependency revision/tree, environment, and frozen-input hash checks | 0 | Lean 4.29.0 at `98dc76e3...`; mathlib `8a178386...`; flt-regular `56161b6e...`; all recorded hashes matched. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is deliberately absent. |

Exact tracked replay from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-fd995645-slot32.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
lean=$(timeout 120 lake env which lean)
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`. The independent pressure-refutation object digest was
`65ffc44b85c56857b9a60e011b33050f430112db3cfbb94ebd6d0c765715bfa2`.

## Retry boundary

Reopen `S56-M-1235-STATEMENT`. Define conditions `(I)`--`(VIII)` as
predicates of the five functions and make `Motion` carry their proofs. Scope
uniqueness to the source domain and `0 <= t <= T` unless the primary source
justifies global function equality. Then re-audit the source and version and
re-freeze the canonical expression fingerprint, crosswalk, obligation
registry, typed graphs, and dependent evidence before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so master proof
acceptance is independently dependency-blocked. Thirty-nine earlier structured
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
