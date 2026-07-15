# THM-M-1036 proof-phase recheck at `c887c8e5` (slot29)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `c887c8e5d7afe589d4b90386654421a60e998f51`

Base tree: `7a1298612a32286e2a542ffc410cf4de9bb1fabd`

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
integral equation yields `x = x + 1` in coordinate zero. Thus any positive
proof of the universe-polymorphic target would contradict its checked
universe-zero specialization.

This refutes the frozen Lean encoding, not the classical SDE theorem. Proving a
repaired, strengthened, or narrower statement would be a forbidden theorem
substitution in this proof item. The existing
`root_of_existence_and_uniqueness` declaration is conditional assembly: it
assumes complete existence and uniqueness packages and supplies neither.

The item remains `[ ]`. No positive proof body, proof receipt, provisional
state, audit completion, validation completion, release, theorem completion,
or master acceptance is claimed. Its prerequisite obligation-tree item is
still `[_]`, not master-accepted `[x]`.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. The minimal
decisive root cut is `M1036-X-INTEGRAL-SEMANTICS`; its invalidated/open chain
continues through `M1036-C-LIMIT-SOLUTION`, `M1036-T-EXISTENCE`, and
`M1036-T-ASSEMBLE` to `M1036-ROOT`.

The frozen registry projects `[H2, M3, R3]`. This recheck proposes machine
classification `M5`, yielding `[H2, M3, R3] -> [H2, M5, R3]`, without changing
accepted state. `H2` stays unchanged because the countermodel diagnoses the
backend encoding, not the human mathematical theorem.

Replace the bare semantic flags with a source-faithful law-bearing standard
time/Ito integral construction or exact sufficient laws. Then publish a new
statement fingerprint and freshly freeze and master-accept the statement,
anchor audit, obligation registry, and typed graphs before resuming proof
work. An explicit redirect to the checked counterexample/barrier target is the
other legal route.

This directory already contained 40 `proof-recheck-*.json` records, while the
DAG still records proof `attempts: 0` and no children. File counts do not prove
distinct scheduler ticks, but the master must reconcile the repeated blocker
history and apply the five-tick split rule. Another unchanged positive-proof
retry is inappropriate.

## Validation

All checks ran from this worker clone. The scheduler-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read only. No `lake update`, `lake build`, dependency clone/fetch, or network
operation was run. Generated output from the credited replay stayed under
`/tmp` and was removed by a shell trap. The warm shared cache and untracked
symlink make this nonrelease evidence; no cold-cache, immutable-input, or
independent-runner claim is made.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | Statement elaborated; all three mutations differed; fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; pinned mathlib revision matched. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | 18 obligations and 47 typed edges passed; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `cd Formalizations/Lean && lake env lean --version` plus read-only pinned dependency probes | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular` `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| Isolated trust-zero `lake env lean` replay from `Formalizations/Lean` | 0 | `Statement.lean` and `Counterexample.lean` elaborated. Both negative declarations reported exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`; `Statement.olean` SHA-256 `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`. |
| Scoped prohibited-token scan over `*.lean` | 1 | Expected no-match exit: no `sorry`, `admit`, axiom declaration, unsafe/opaque/extern escape, `sorryAx`, `implemented_by`, or `native_decide` was found. |
| Final JSON parse, target-specific invariant assertions, scoped whitespace checks, and `test ! -e .stage1-worker-selftest.json` | 0 | Packet identity/base/hashes/evidence agreed, no whitespace error occurred, and the completion-only self-test manifest is absent. |

The smallest real proof-phase replay was:

```bash
set -euo pipefail
root=$PWD
target="$root/Stage1_Instances/THM-M-1036"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1036-proof-recheck-head-c887c8e5-slot29.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
cd "$lean_dir"
LEAN_NUM_THREADS=1 nice -n 15 timeout --foreground 900 \
  lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" nice -n 15 \
  timeout --foreground 900 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/Counterexample.lean"
```

The paired JSON packet binds the source hashes, pinned environment, exact
axiom list, kernel output digest, and open-state boundary.

## Status Boundary

This current-base packet is durable blocker evidence, not a proof receipt. It
does not satisfy `S56-M-1036-PROOF` or support any completion claim. Because
the assigned proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
