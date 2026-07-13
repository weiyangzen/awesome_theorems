# THM-M-1036 proof-phase attempt

Item: `S56-M-1036-PROOF`

Date: `2026-07-14`

Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`: the exact frozen target is false, not merely absent from the pinned
library. `IntegralSemantics.standard_time_integral` and
`standard_ito_integral` are bare propositions with no laws connecting them to
the two supplied operations. The frozen target nevertheless quantifies over
every such semantics and concludes strong existence after receiving proofs of
those two propositions.

The tracked `Counterexample.lean` chooses both propositions to be `True` while
making `timeIntegral f` equal to `f 0 + 1`. At `t = 0`, any purported strong
solution would then satisfy `x = x + 1` in coordinate zero. The placeholder-free
declaration
`Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget`
kernel-checks at the exact universe-zero specialization and proves
`Not SdeExistenceUniquenessTarget.{0}`. Therefore no consistent positive Lean
proof body can inhabit the current universal target.

The first failed gate is exact-target consistency at
`M1036-X-INTEGRAL-SEMANTICS`. The conditional composition in
`ObligationTree.lean` still consumes `StrongExistencePackage` and
`PathwiseUniquenessPackage` as hypotheses; it supplies neither package and
cannot bypass the countermodel. This attempt proposes reclassification from
`[H2, M3, R3]` to `[H5, M5, R3]`, subject to master review. It claims no
positive proof credit and no theorem completion.

Because the assigned proof phase is not self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused read
only. No Lake update/build, dependency clone/fetch, network operation, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | The frozen dependency has 18 obligations and 47 typed edges; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; its pre-countermodel projection reports an open M3 root. |
| From `Formalizations/Lean`, copy `Statement.lean` and `Counterexample.lean` to a fresh `mktemp` directory, run `lake env lean --root=<tmp> -o <tmp>/Statement.olean <tmp>/Statement.lean`, then run `LEAN_PATH=<tmp>:$(lake env printenv LEAN_PATH) lake env lean --root=<tmp> <tmp>/Counterexample.lean`; remove the directory by shell trap | 0 | Exact target and countermodel elaborated. Lean printed `not_sdeExistenceUniquenessTarget : Not SdeExistenceUniquenessTarget` with axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1036 -g '*.lean'` | 1 | Expected no-match exit: no prohibited Lean declaration token in the owned sources. |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/proof-blocker.json >/dev/null` | 0 | Structured blocker is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1036` | 0 | No scoped whitespace diagnostics. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1036/proof-blocker.json` and the same command for `proof-validation.md` | 1 each | Expected new-file difference exits with no whitespace diagnostics; unlike the tracked-diff check, these commands cover both untracked deliverables. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

Statement SHA-256:
`4942287dad0600f98aa6379a6e541e50452e4c3d7cfd97e6f45fb1a7105a91dc`.
Counterexample source SHA-256:
`199ef928d35fe42bdcbadaac9b8e464d77b7ddb72dd782b381395aa7d8e24a18`.

## Reopen condition

Replace the two bare semantic flags with a source-faithful, law-bearing
standard time/Ito integral construction or with hypotheses that constrain the
operations by all required laws. Then version and re-fingerprint the statement
and freshly freeze the anchor audit, obligation registry, and typed graphs
before proof work resumes. Until that happens, `M1036-X-INTEGRAL-SEMANTICS`,
`M1036-T-EXISTENCE`, and `M1036-ROOT` form the decisive open/invalid cut, and
this proof item cannot truthfully receive `[_]` or theorem-completion credit.
