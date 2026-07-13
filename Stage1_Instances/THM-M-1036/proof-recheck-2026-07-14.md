# THM-M-1036 proof-phase recheck

Item: `S56-M-1036-PROOF`

Date: `2026-07-14`

Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`

Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`

## Verdict

`blocked`. A fresh pinned-toolchain replay confirms that the exact frozen
target is false. This retry therefore adds no positive proof body and does not
satisfy the proof item.

`IntegralSemantics.standard_time_integral` and `standard_ito_integral` are bare
propositions with no laws connecting them to the supplied operations. The
target nevertheless quantifies over every such semantics and concludes strong
existence after receiving proofs of both propositions. `Counterexample.lean`
sets the propositions to `True`, chooses
`timeIntegral f _ omega = f 0 omega + 1`, and uses the integral equation at
`t = 0` to derive `x = x + 1` in coordinate zero.

The placeholder-free declaration
`Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget`
has type `Not SdeExistenceUniquenessTarget.{0}`. Any positive proof of the
universe-polymorphic target would specialize to this refuted universe-zero
instance, so no consistent positive proof body can be implemented for the
current statement.

The conditional theorem `root_of_existence_and_uniqueness` remains only a
composition certificate: it assumes complete `StrongExistencePackage` and
`PathwiseUniquenessPackage` values and supplies neither. The first failed gate
is exact-target consistency at `M1036-X-INTEGRAL-SEMANTICS`. The proposed root
classification remains `[H5, M5, R3]`, subject to master review; the root is
open and the theorem is not complete.

## Validation

All checks ran in this worker clone. The existing untracked link at
`Formalizations/Lean/.lake` was used only to read the canonical pinned
artifacts. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Lean output was confined to a
fresh `/tmp` directory and deleted by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS`: 18 obligations and 47 typed edges; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; the pre-countermodel projection remains open at M3. |
| Isolated pinned Lean recipe below | 0 | The exact statement and countermodel elaborated. Lean printed the negative declarations and axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`; `Statement.olean` SHA-256 `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`. |
| `rg -n '^\s*(sorry|admit|axiom)(\s|$)|sorryAx|^\s*unsafe\s' Stage1_Instances/THM-M-1036 -g '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token occurs in the owned Lean sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/proof-recheck-2026-07-14.json >/dev/null` plus scoped invariant assertions | 0 | The blocker JSON is valid; identity, current base, blocked `[ ]` state, false completion flags, kernel result, axiom list, and absent worker self-test agree. |
| `git diff --check -- Stage1_Instances/THM-M-1036` plus `git diff --no-index --check /dev/null <new-file>` for each new report | 0 for the scoped tracked check; 1 for each expected new-file difference | No whitespace diagnostics were emitted for either owned artifact. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The isolated Lean recipe was:

```bash
set -o pipefail
tmp=$(mktemp -d /tmp/thm-m-1036-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1036/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1036/Counterexample.lean "$tmp/Counterexample.lean"
{
  lake env lean --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
    lake env lean --root="$tmp" "$tmp/Counterexample.lean"
} 2>&1 | tee "$tmp/kernel-output.txt"
```

## Reopen Condition

Replace the two bare semantic flags with a source-faithful, law-bearing
standard time/Ito integral construction or exact sufficient laws. Then publish
a new statement fingerprint and freshly freeze and accept the statement,
anchor audit, obligation registry, and typed graphs before resuming positive
proof execution. Alternatively, redirect the task explicitly to the checked
counterexample target.

This report is durable blocker evidence, not a proof receipt. Because the
assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
