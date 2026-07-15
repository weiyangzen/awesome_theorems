# THM-M-1036 proof-phase blocker at `3a3be423` (slot45)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3a3be4230e6a57856a9a6701d4b7261ccea3c915`.

Base tree: `bd887a80b81681181d9fece91ae697e54f0c83f4`.

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

The first workflow gate is `S56-M-1036-OBLIGATION_TREE` master acceptance:
the required predecessor remains provisional `[_]`. Independently, the
decisive mathematical gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. The minimal
root cut is `M1036-X-INTEGRAL-SEMANTICS`; its invalidated/open chain continues
through `M1036-T-EXISTENCE` to `M1036-ROOT`.

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

This directory already contained 51 paired `proof-recheck-*.json/.md` records
and 52 structured blocker records when `proof-blocker.json` was included. File
counts do not prove distinct scheduler ticks, but the master must reconcile
them and apply the five-tick split rule. Another unchanged positive-proof retry
is not useful.

## Validation

All checks ran from this worker clone. This worker reused the
automation-provided untracked `Formalizations/Lean/.lake` symlink read only and
issued no `lake update`, `lake build`, dependency clone/fetch, network command,
or deliberate `.lake` mutation. Generated output stayed under `/tmp` and was
removed. This is nonrelease evidence and makes no clean-cache claim.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | Statement elaborated; all three mutations differed; fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | 18 obligations and 47 typed edges passed; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` plus read-only package revision inspection | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; exact pinned mathlib and flt-regular revisions present. |
| Isolated trust-zero `lake env lean` replay from `Formalizations/Lean` | 0 | `Statement.lean` and `Counterexample.lean` elaborated. Both negative declarations reported exactly `[propext, Classical.choice, Quot.sound]`; output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom)(?:\s|$)|^\s*(?:unsafe|opaque|extern)\b|\bsorryAx\b|\bimplemented_by\b|\bnative_decide\b' Stage1_Instances/THM-M-1036 --glob '*.lean'` | 1 | Expected no-match exit: no prohibited proof escape was found. |
| `python3 -m json.tool` plus packet invariant assertions | 0 | Structured blocker JSON parsed and all identity, hash, state, axiom, completion, and self-test-absence invariants agreed. |
| Scoped `git diff --check` and new-file no-index checks | 0 | No whitespace error in either owned artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion-only self-test manifest is absent. |

The smallest real kernel replay used this recipe:

```bash
set -uo pipefail
root=$(git rev-parse --show-toplevel)
target="$root/Stage1_Instances/THM-M-1036"
leanroot="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1036-proof-head-3a3be423-slot45.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
cd "$leanroot"
LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.out" 2>&1
s1=$?
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.out" 2>&1
s2=$?
cat "$tmp/statement.out" "$tmp/counterexample.out" \
  >"$tmp/kernel-output.txt"
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/statement.out" "$tmp/counterexample.out" \
  "$tmp/kernel-output.txt" "$tmp/Statement.olean"
exit $((s1 != 0 || s2 != 0))
```

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
