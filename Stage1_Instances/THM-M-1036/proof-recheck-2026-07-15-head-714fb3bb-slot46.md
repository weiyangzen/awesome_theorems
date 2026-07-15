# THM-M-1036 proof-phase recheck at `714fb3bb` (slot46)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`.

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`.

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

This directory already contained 27 `proof-recheck-*.json` records and 28
structured blockers when `proof-blocker.json` was included, while the DAG
still records proof `attempts: 0` and no children. File counts do not prove
distinct scheduler ticks, but the master must reconcile them and apply the
five-tick split rule. Another unchanged positive-proof retry is not useful.

## Validation

All checks ran from this worker clone. This worker reused the
automation-provided untracked `Formalizations/Lean/.lake` symlink read-only and
issued no `lake update`, `lake build`, dependency clone/fetch, or direct network
command. The root `lake env` probe did attempt dependency resolution before its
timeout, so it is recorded only as a failed probe and receives no pinned
validation credit. Other workers concurrently mutated the shared canonical
cache while this packet was prepared. Generated output from the credited
mathlib-scoped replay stayed under `/tmp` and was removed. This is nonrelease
evidence and makes no clean-cache claim.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | 18 obligations and 47 typed edges passed; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `cd Formalizations/Lean && timeout --foreground 30 ~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake env lean --version` | 124 | In the recorded run, the root-project probe produced no output before the timeout and attempted dependency resolution, so it receives no pinned validation credit. This shared-cache-state-sensitive result is not claimed as a stable reproducer. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | Read-only inspection confirmed that the canonical pinned checkout has no resolvable `HEAD`. This worker did not fetch or repair it. |
| From the pinned mathlib project, run `lake env lean --version` with `LEAN_PATH` restricted to existing compiled package paths | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Isolated trust-zero `lake env lean` replay from the pinned mathlib project | 0 | `Statement.lean` and `Counterexample.lean` elaborated using only existing artifacts. Both negative declarations reported exactly `[propext, Classical.choice, Quot.sound]`; output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom)(?:\s|$)|^\s*(?:unsafe|opaque|extern)\b|\bsorryAx\b|\bimplemented_by\b|\bnative_decide\b' Stage1_Instances/THM-M-1036 --glob '*.lean'` | 1 | Expected no-match exit: no prohibited proof escape was found. |
| `python3 -m json.tool` plus packet invariant assertions | 0 | Structured blocker JSON parsed and all identity, hash, state, axiom, completion, and self-test-absence invariants agreed. |
| Scoped `git diff --check` and new-file no-index checks | 0 | No whitespace error in either owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion-only self-test manifest is absent. |

The root project's ordinary `lake env lean` route is unavailable because the
pre-existing pinned `flt-regular` artifact cannot resolve `HEAD`; this worker
did not repair or fetch it. The smallest real kernel replay therefore invoked
`lake env lean` from the pinned mathlib project, with `LEAN_PATH` restricted to
the pre-existing compiled dependency paths:

```bash
set -uo pipefail
root=$(git rev-parse --show-toplevel)
target="$root/Stage1_Instances/THM-M-1036"
cache="$root/Formalizations/Lean/.lake"
mathlib="$cache/packages/mathlib"
lake="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
tmp=$(mktemp -d /tmp/thm-m-1036-proof-head-714fb3bb-slot46.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
lean_path="$cache/packages/Cli/.lake/build/lib/lean:$cache/packages/batteries/.lake/build/lib/lean:$cache/packages/Qq/.lake/build/lib/lean:$cache/packages/aesop/.lake/build/lib/lean:$cache/packages/proofwidgets/.lake/build/lib/lean:$cache/packages/importGraph/.lake/build/lib/lean:$cache/packages/LeanSearchClient/.lake/build/lib/lean:$cache/packages/plausible/.lake/build/lib/lean:$mathlib/.lake/build/lib/lean"
cd "$mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300 \
  "$lake" env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.out" 2>&1
s1=$?
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 300 \
  "$lake" env lean --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.out" 2>&1
s2=$?
cat "$tmp/statement.out" "$tmp/counterexample.out" >"$tmp/kernel-output.txt"
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/statement.out" "$tmp/counterexample.out" \
  "$tmp/kernel-output.txt" "$tmp/Statement.olean"
exit $((s1 != 0 || s2 != 0))
```

The invoked Lean was version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; its binary SHA-256 was
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`.
The statement and counterexample output hashes were respectively
`052c267144c1dc46129f5c40f97db91627a3025fea97d86a001e8ee1bd004673`
and `e5e5d6a071019cdb10d072baefb1e7f05d0da040dcd61a457458decb0d897cfe`.
`Statement.olean` hashed
`a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`.
The paired JSON packet binds all source, environment, object, and output
hashes.

## Status Boundary

This current-base packet is durable blocker evidence, not a proof receipt. It
does not satisfy `S56-M-1036-PROOF` or support any completion claim. Because
the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
