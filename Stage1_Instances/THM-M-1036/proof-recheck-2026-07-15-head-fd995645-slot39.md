# THM-M-1036 proof-phase recheck at `fd995645` (slot39)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fd995645725ec3633e4da7e6d759deb14f530861`.

Base tree: `5846121ab94ff0502b98217f643539881bc9c045`.

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks at trust level zero. `IntegralSemantics` supplies arbitrary
`timeIntegral` and `itoIntegral` operations, while `standard_time_integral`
and `standard_ito_integral` are bare propositions imposing no laws on either
operation. The target nevertheless quantifies over every such semantics and
concludes strong existence after receiving proofs of those propositions.

`Counterexample.lean` sets both propositions to `True`, uses `Unit` with its
Dirac probability measure, state dimension one and noise dimension zero, and
defines `timeIntegral f _ omega = f 0 omega + 1`. At `t = 0`, the required
integral equation yields `x = x + 1` in coordinate zero. Hence any positive
proof of the universe-polymorphic target would contradict its checked
universe-zero specialization.

This refutes the frozen Lean encoding, not the classical SDE theorem. Proving a
repaired, strengthened, or narrower statement would be a forbidden theorem
substitution in this item. The existing `root_of_existence_and_uniqueness`
declaration is only conditional assembly: it assumes complete existence and
uniqueness packages and supplies neither.

The item remains `[ ]`. No proof body, proof receipt, provisional state, audit
completion, validation completion, release, theorem completion, or master
acceptance is claimed. Its prerequisite obligation-tree item is still `[_]`,
not master-accepted `[x]`.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. The minimal
decisive root cut is `M1036-X-INTEGRAL-SEMANTICS`; its invalidated/open chain
continues through `M1036-T-EXISTENCE` to `M1036-ROOT`.

The frozen registry projects `[H2, M3, R3]`. This recheck proposes machine
classification `M5`, so `[H2, M3, R3] -> [H2, M5, R3]`, without changing
accepted state. `H2` stays unchanged because the countermodel diagnoses the
backend encoding, not the human mathematical theorem.

Replace the bare semantic flags with a source-faithful, law-bearing standard
time/Ito integral construction or exact sufficient laws. Then publish a new
statement fingerprint and freshly freeze and master-accept the statement,
anchor audit, obligation registry, and typed graphs before resuming proof
work. An explicit redirect to the checked counterexample/barrier target is the
other legal route.

This directory already contained 36 `proof-recheck-*.json` records and 37
structured blockers when `proof-blocker.json` was included, while the DAG
still records proof `attempts: 0` and no children. File counts do not prove
distinct scheduler ticks, but the master must reconcile them and apply the
five-tick split rule. Another unchanged positive-proof retry is inappropriate.

## Validation

All checks ran from this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read only. No `lake update`, `lake build`, dependency clone/fetch, or network
operation was run. The manifest-pinned mathlib and `flt-regular` revisions were
present, and ordinary `lake env lean` was available. Generated output from the
credited replay stayed under `/tmp` and was removed by a shell trap. The warm
shared cache and untracked symlink make this nonrelease evidence; no cold-cache,
immutable-input, or independent-runner claim is made.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | Statement elaborated; all three mutations differed; fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; pinned mathlib revision matched. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | 18 obligations and 47 typed edges passed; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `cd Formalizations/Lean && timeout --foreground 60 lake env lean --version && timeout --foreground 60 lake --version && timeout --foreground 60 lake env which lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; exact pinned toolchain path. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; tree `32c9eace926573a9981787ae97643e520353c893`. |
| Isolated trust-zero `lake env lean` replay from `Formalizations/Lean` | 0 | `Statement.lean` and `Counterexample.lean` elaborated. Both negative declarations reported exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|^\s*(?:unsafe\|opaque\|extern)\b\|\bsorryAx\b\|\bimplemented_by\b\|\bnative_decide\b' Stage1_Instances/THM-M-1036 --glob '*.lean'` | 1 | Expected no-match exit: no prohibited proof escape was found. |
| `python3 -m json.tool` plus packet invariant assertions | 0 | Structured blocker JSON parsed and identity, base, source hashes, environment, kernel evidence, exact axiom list, blocker state, empty receipts, and self-test absence agreed. |
| Scoped `git diff --check`, then `git diff --no-index --check /dev/null <file>` for each new artifact with a wrapper requiring expected difference exit 1 and empty diagnostics | 0 | No whitespace error in either owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion-only worker self-test manifest is absent. |

The smallest real proof-phase replay was:

```bash
set -uo pipefail
root=$PWD
target="$root/Stage1_Instances/THM-M-1036"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1036-proof-head-fd995645-slot39.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
cd "$lean_dir"
LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.out" 2>&1
statement_exit=$?
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  lake env lean --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.out" 2>&1
counterexample_exit=$?
cat "$tmp/statement.out" "$tmp/counterexample.out" >"$tmp/kernel-output.txt"
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/statement.out" "$tmp/counterexample.out" \
  "$tmp/kernel-output.txt" "$tmp/Statement.olean"
exit $((statement_exit != 0 || counterexample_exit != 0))
```

It ran from `2026-07-15T17:05:46+08:00` through
`2026-07-15T17:07:12+08:00`. Statement and counterexample outputs hashed
`052c267144c1dc46129f5c40f97db91627a3025fea97d86a001e8ee1bd004673`
and `e5e5d6a071019cdb10d072baefb1e7f05d0da040dcd61a457458decb0d897cfe`.
The generated `Statement.olean` hashed
`a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`.
The paired JSON packet binds these values and the source/environment hashes.
The JSON parser, target-specific invariant assertions, scoped whitespace
checks, and self-test absence check were rerun successfully after both packet
files were written.

## Status Boundary

This current-base packet is durable blocker evidence, not a proof receipt. It
does not satisfy `S56-M-1036-PROOF` or support any completion claim. Because
the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
