# THM-M-1235 current-base proof blocker

Item: `S56-M-1235-PROOF`

Intent: `prove`

Verdict: `blocked`

Base revision: `9d50d838c8132b2aaf005a4863baeb5385e52a97`

Base tree: `ef268baf236c1fe55806a57847c7f78ed6587b9d`

Recorded: `2026-07-15` (Asia/Shanghai)

## First failed gate

`S56-5.1-EXACT-TARGET-CONSISTENCY / M1235-S-DEFINITIONS` fails. The
frozen `Motion` structure stores conditions `(I)`--`(VIII)` as values of type
`Prop`; it does not store predicates of the five functions or proofs of those
predicates. Its five function fields are therefore unconstrained, while
`SameMotion` requires equality of all five globally defined functions.

The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

changes an alleged unique motion's `velocityX` to `velocityX + 1` and retains
every other field. This yields another `Motion`; `SameMotion` would equate the
two velocity functions, but evaluation at `(0, 0), 0` gives the contradiction
`x + 1 = x`. The concrete `counterexampleData` discharges all six explicit
premises at `T = 1`.

The trust-zero replay below checks this exact negation. Thus a legal positive
proof of the frozen target cannot exist in the same consistent environment.
This refutes the formal encoding, not Wolibner's mathematical theorem. Proving
a corrected, weaker, conditional, or differently scoped proposition here
would be a forbidden target substitution. In particular,
`root_of_existence_and_uniqueness` assumes both analytic packages and is only
conditional composition; it supplies no root proof credit.

## Current-base validation

All checks ran in this worker clone and reused the automation-provided
untracked `Formalizations/Lean/.lake` symlink read-only. No `lake update`,
`lake build`, dependency clone, fetch, checkout, network access, or `.lake`
mutation was performed. Temporary Lean inputs and objects were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Four structural mutations were killed; canonical expression digest `77aec2f5...`; pinned mathlib matched. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root remains open M3. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | Exact statement and both negative declarations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit; no prohibited proof construct was found. |
| Environment and seven frozen-input identity checks | 0 | Toolchain/dependency revisions, trees, manifest hashes, and all target input hashes matched the structured packet. |
| JSON parse, focused packet assertions, and whitespace checks | 0 | The blocker packet is valid, its identity/noncompletion flags passed, and no whitespace errors were found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-9d50d838-slot37.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Frozen input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The temporary object digests were
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
acceptance is independently dependency-blocked. Thirty-four earlier structured
proof-recheck JSON packets are already tracked while the authoritative DAG
still records `attempts=0` and no children. The master/scheduler must reconcile
that history and apply rev-5.6 section 10.2's reopen/split rule instead of
scheduling another identical proof-only retry.

## Status boundary

Lifecycle remains `planned`; the accepted root vector remains
`[H3, M3, R4]`, with `[H5, M5, R4]` proposed only as the diagnosis of this
refuted formal target. This artifact adds negative, nonrelease blocker evidence
only. It adds no positive proof body, closed obligation, composition
certificate, receipt, provisional/accepted state, audit completion, theorem
completion, validation, release, or master acceptance. Because the assigned
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is not
written.
