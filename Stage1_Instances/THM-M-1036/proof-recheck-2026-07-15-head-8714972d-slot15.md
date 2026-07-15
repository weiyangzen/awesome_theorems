# THM-M-1036 proof-phase recheck at `8714972d` (slot15)

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `8714972d4cf7ae256a92b9e35032c9df1bf5745c`.

Base tree: `080d14e14102a733c6992aa0644e3c65d755e91b`.

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

again elaborated at Lean trust level zero. Its only reported axioms are
`propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx`, placeholder,
unsafe declaration, opaque escape, or native computation escape occurs.

The obstruction is in the frozen encoding, not the classical SDE theorem.
`IntegralSemantics.standard_time_integral` and `standard_ito_integral` are bare
propositions with no laws connecting them to the supplied operations. Since the
root quantifies over every `IntegralSemantics`, an implementation cannot repair
this by constructing one good standard semantics: the adversarial instance is
still among the universally quantified inputs.

That instance uses the Dirac probability space on `Unit`, state dimension one,
noise dimension zero, and both semantic flags equal to `True`. Its
`timeIntegral` returns `f 0 + 1`. At `t = 0`, any purported strong solution
would satisfy `x = x + 1` in coordinate zero. Thus the required existence
conjunct is false.

The first failed gate is exact-target consistency at
`M1036-X-INTEGRAL-SEMANTICS`. The downstream invalid chain is
`M1036-X-INTEGRAL-SEMANTICS`, `M1036-T-EXISTENCE`, `M1036-ROOT`. The
conditional composition in `ObligationTree.lean` assumes a complete existence
package and therefore cannot bypass the countermodel.

The prerequisite `S56-M-1036-OBLIGATION_TREE` also remains provisional `[_]`,
not master-accepted `[x]`. The proof item remains `[ ]` with lifecycle
`planned`; it earns no receipt, proof credit, or theorem-completion claim.
Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was reused
read only. No Lake update/build, dependency clone/fetch, network operation, or
deliberate `.lake` mutation occurred. Generated Lean output stayed in a fresh
`/tmp` directory removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS`: 18 obligations, 47 typed edges, denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | After one interrupted no-output attempt under transient shared-cache contention, the retry completed in 27 seconds: all three mutations differed; fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `cd Formalizations/Lean && timeout --foreground 60 lake env lean --version && timeout --foreground 60 lake --version && timeout --foreground 60 lake env which lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0; pinned toolchain binary located. |
| Fresh-`/tmp` `lake env lean --trust=0 -t0` replay of `Statement.lean`, then `Counterexample.lean` with the temporary `Statement.olean` prepended to pinned `LEAN_PATH` | 0 | Both modules elaborated. Both negative declarations reported axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|^\s*(?:unsafe\|opaque\|extern)\b\|\bsorryAx\b\|\bimplemented_by\b\|\bnative_decide\b' Stage1_Instances/THM-M-1036 --glob '*.lean'` | 1 | Expected no-match exit; no prohibited proof escape found. |
| Current blocker JSON parse plus target-specific invariant assertions | 0 | Identity, base, hashes, environment, negative evidence, axiom list, blocker state, empty receipts, and self-test absence agree. |
| Scoped tracked and new-file whitespace checks | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion-only self-test manifest absent. |

The trust-zero replay ran from `Formalizations/Lean` with
`LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and `--root` set to the target. It
compiled `Statement.lean` to a fresh `/tmp/Statement.olean`, prepended that
directory to the pinned `LEAN_PATH`, and then elaborated
`Counterexample.lean`. Exact replay timestamps were
`2026-07-15T15:04:46+08:00` through `2026-07-15T15:05:29+08:00`.

Evidence digests:

```text
Statement.lean             4942287dad0600f98aa6379a6e541e50452e4c3d7cfd97e6f45fb1a7105a91dc
Counterexample.lean        199ef928d35fe42bdcbadaac9b8e464d77b7ddb72dd782b381395aa7d8e24a18
Statement output           052c267144c1dc46129f5c40f97db91627a3025fea97d86a001e8ee1bd004673
Counterexample output      e5e5d6a071019cdb10d072baefb1e7f05d0da040dcd61a457458decb0d897cfe
Combined kernel output     4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55
Temporary Statement.olean  a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4
```

## Retry boundary

Do not retry the unchanged positive-proof item. Replace the bare flags with a
source-faithful law-bearing integral structure or exact sufficient predicates,
or quantify only over a canonical constrained semantics. Then version and
re-fingerprint the statement and freshly freeze and accept the statement,
anchor audit, obligation registry, and typed graphs before proof execution.
Alternatively, the master may explicitly redirect this item to the checked
counterexample/barrier theorem.

There were 30 pre-existing structured recheck files (31 structured blocker
files including `proof-blocker.json`) before this packet. File count does not
prove scheduler tick identity, but if these are distinct unresolved proof ticks
the master must reconcile them and apply the five-tick split rule. This packet
is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-1036-PROOF`, complete the audit, or complete the theorem.
