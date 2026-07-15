# THM-M-1235 current-base proof blocker

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `b8c0a0c119a82ef435e23f9ff85bfd783db95736`

Base tree: `831576eb7d1273d01e99653d36b616e99e85dc0f`

Recorded: `2026-07-15` (Asia/Shanghai)

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1235-S-DEFINITIONS` fails. The
frozen `Motion` structure stores conditions `(I)`--`(VIII)` as freely chosen
values of type `Prop`; it does not store predicates of the five functions or
proofs that those predicates hold. Its function fields are therefore
unconstrained, while `SameMotion` requires equality of all five globally
defined functions.

The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

changes an alleged unique motion's `velocityX` to `velocityX + 1` and retains
every other field. This yields another `Motion`; `SameMotion` would equate the
two velocity functions, but evaluation at `(0, 0), 0` gives the contradiction
`x + 1 = x`. The concrete `counterexampleData` discharges every explicit
premise at `T = 1`.

The trust-zero replay below checks this exact negation. A legal positive proof
of the frozen target cannot exist in the same consistent environment. This
refutes the formal encoding, not Wolibner's mathematical theorem. Proving a
corrected, weaker, conditional, or differently scoped proposition here would
be a forbidden target substitution. In particular,
`root_of_existence_and_uniqueness` assumes both analytic packages and is only
conditional composition; it supplies no root proof credit.

## Current-base validation

All completed checks ran in this worker clone and reused the
automation-provided untracked `Formalizations/Lean/.lake` symlink read-only.
No `lake update`, `lake build`, dependency clone, fetch, checkout, network
access, or `.lake` mutation was performed. Temporary Lean inputs and objects
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `timeout --foreground --kill-after=10s 600 python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression digest and pinned identities matched; all four structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness M4. |
| Isolated pinned-Lean trust-zero replay below | 0 | Exact statement and both negative declarations elaborated; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit; no prohibited proof construct was found. |
| `cd Formalizations/Lean && timeout 120 lake env lean --version && timeout 120 lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}; git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}; sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Both dependency revisions/trees and both environment hashes matched the structured packet. |
| `sha256sum Stage1_Instances/THM-M-1235/Statement.lean Stage1_Instances/THM-M-1235/Proof.lean Stage1_Instances/THM-M-1235/ObligationTree.lean Stage1_Instances/THM-M-1235/obligation-registry.json Stage1_Instances/THM-M-1235/typed-graphs.json Stage1_Instances/THM-M-1235/anchor-audit.json Stage1_Instances/THM-M-1235/validation-specs.json` | 0 | All seven frozen input hashes matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-b8c0a0c1-slot57.json` plus focused assertions | 0 | JSON syntax and blocker identity, base, state, and noncompletion flags passed. |
| `git diff --check -- Stage1_Instances/THM-M-1235`; `git diff --no-index --check /dev/null <new-artifact>` separately for both new files | 0 / 1 | The tracked diff check passed. Each no-index check returned only the expected added-file status 1 and emitted no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is deliberately absent. |

Exact successful replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1235
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1235-proof-b8c0a0c1-slot57.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
lean_path=$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)
lean_bin=$(cd "$lean_root" && timeout 120 lake env which lean)
cd "$lean_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`.

## Retry boundary

Reopen `S56-M-1235-STATEMENT`. Define conditions `(I)`--`(VIII)` as
predicates of the five functions and make `Motion` carry proofs. Scope
uniqueness to the source domain and `0 <= t <= T` unless the primary source
justifies global function equality. Re-audit the source and then version and
re-freeze the canonical expression fingerprint, source crosswalk, obligation
registry, typed graphs, and dependent evidence before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` remains only worker-provisional, so master proof
acceptance is independently dependency-blocked. Thirty-eight earlier
structured proof-recheck packets are already tracked while the authoritative
DAG still records `attempts=0` and no children. The master/scheduler must
reconcile that history and apply section 10.2's reopen/split rule instead of
scheduling another identical proof-only retry.

## Status boundary

Lifecycle remains `planned`. The intake manifest still records
`[H2, M4, R4]`, while the later frozen typed graph projects the root as
`[H3, M3, R4]`; this run changes neither provisional predecessor projection.
It proposes `[H5, M5, R4]` only as the diagnosis of the refuted formal target
for master reconciliation. This artifact adds negative, nonrelease blocker
evidence only. It adds no positive proof body, closed obligation, receipt,
provisional or accepted state, audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned proof phase
is not genuinely complete, `.stage1-worker-selftest.json` is not written.
