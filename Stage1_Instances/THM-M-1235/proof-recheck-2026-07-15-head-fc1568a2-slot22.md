# THM-M-1235 proof-phase recheck at `fc1568a2`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Base tree: `635319193989301e577a430446e682952c51c538`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration
`Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness`
has exact type
`Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness`.
It was replayed from the current base with Lean `--trust=0 -t0`.

`Motion` stores conditions `(I)`--`(VIII)` as bare values of type `Prop`, not
as predicates applied to the five motion functions and not as proofs. Those
fields therefore constrain no function. Given an alleged unique motion,
`Proof.lean` changes `velocityX` pointwise to `velocityX + 1` while retaining
all other fields. The result is another `Motion`, but `SameMotion` would force
the two velocity functions to agree; evaluation at `(0, 0), 0` contradicts
that equality. `counterexampleData` discharges every explicit target premise.

This refutes only the frozen formal encoding. It does not refute Wolibner's
mathematical theorem. It also cannot count as a positive proof body or satisfy
the assigned item. The proof phase therefore remains `[ ]`, and no
`.stage1-worker-selftest.json` is written.

## Current-base delta

The current base integrated the preceding slot22 blocker packet but did not
change any core THM-M-1235 source, target fingerprint, registry, graph, or
dependency pin. Current SHA-256 values remain:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- canonical expression: `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- obligation denominator: `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`

The authoritative DAG still reports the predecessor
`S56-M-1235-OBLIGATION_TREE` as worker-provisional `[_]`, so master proof
acceptance is independently dependency-blocked. It reports this proof item as
`attempts=0` with no children despite 37 earlier structured recheck packets.
Under section 10.2, the master/scheduler must reconcile attempts and reopen or
split the invalid upstream statement task rather than schedule another
identical proof-only retry. This worker did not edit the DAG or checklist.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink reused the canonical pinned dependency
artifacts read-only. No update, build, clone, fetch, checkout, network use, or
dependency mutation was performed. Temporary Lean sources and objects were
removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Expression digest matched; all four structural mutations were killed; pinned toolchain/mathlib identity matched. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; root open M3; existence and uniqueness M4. |
| `cd Formalizations/Lean && timeout 300 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Isolated current-base replay below | 0 | Exact statement and both negative declarations elaborated at trust zero; axiom reports were exactly `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit; no prohibited proof construct. |
| Dependency revisions, environment hashes, and seven frozen input hashes | 0 | All values matched the current-base structured packet. |
| JSON syntax plus focused blocker assertions | 0 | Identity, base, negative outcome, unfinished state, and owned changed paths passed. |
| Diff checks for the owned path and both untracked artifacts | 0 | No whitespace diagnostics; only expected no-index content-difference statuses. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false completion self-test exists. |

Exact successful Lean replay from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-fc1568a2-slot22.XXXXXX)
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

The object hashes were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`. Pinned mathlib is
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; pinned `flt-regular` is
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` with tree
`32c9eace926573a9981787ae97643e520353c893`.

## Retry boundary

Reopen `S56-M-1235-STATEMENT`. Define conditions `(I)`--`(VIII)` as
predicates of the five functions and make `Motion` carry proofs of them. Scope
uniqueness to the source domain and `0 <= t <= T` unless the primary source
justifies global function equality. Then re-audit the source and publish a
versioned re-freeze of the canonical expression fingerprint, crosswalk,
obligation registry, typed graphs, and dependent evidence before resuming
proof execution.

`validation-specs.json` also retains legacy shell command strings rather than
the structured recipe schema required by section 10.5, and the intake README
and crosswalk remain unreconciled with later source pinpoints. Those are later
open gates; the exact-target truth failure is the first blocker.

## Status boundary

This artifact is current-base, nonrelease blocker evidence. It proposes no
`[_]` or `[x]`, adds no positive proof credit, and supports neither audit nor
theorem completion, validation, release, or master acceptance.
