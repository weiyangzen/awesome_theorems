# THM-M-1036 proof-phase recheck at `506796f9`

Item: `S56-M-1036-PROOF`

Date: `2026-07-15`

Base revision: `506796f90c31097a0d170410e431f83da4b1853c`

Base tree: `32c911b35ce53ab8fd2ad6bfd6a34bdc603ef50d`

## Verdict

`blocked`: no consistent proof body can inhabit the exact frozen target. The
target quantifies over every `IntegralSemantics`, but
`standard_time_integral` and `standard_ito_integral` are bare propositions and
impose no laws on the supplied operations. The tracked, placeholder-free
`Counterexample.lean` sets both propositions to `True` and chooses
`timeIntegral f _ omega = f 0 omega + 1`. At time zero, any purported strong
solution would therefore satisfy `x = x + 1` in coordinate zero.

The kernel-checked declaration
`Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget`
proves `Not SdeExistenceUniquenessTarget.{0}`. This refutes the current abstract
encoding, not the classical SDE theorem. It is negative evidence only: no
positive proof body was added, the proof item remains `[ ]`, and neither proof-
phase nor theorem completion is claimed.

The prerequisite `S56-M-1036-OBLIGATION_TREE` is also still provisional `[_]`
rather than master-accepted. Because this proof phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was used
read only. No `lake update`, `lake build`, dependency fetch/clone, network
operation, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; baseline `L0`; `rework_required=true`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS THM-M-1036 obligation tree: 18 obligations, 47 typed edges`; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| Copy `Statement.lean` and `Counterexample.lean` to a fresh `/tmp` directory; resolve the executable and `LEAN_PATH` with `lake env`; run each file with `LEAN_NUM_THREADS=1 nice -n 15 timeout 900 ... lean --trust=0 -t0`, compiling `Statement.lean` to a temporary `Statement.olean`; remove the directory on exit | 0 | The exact statement and countermodel elaborated. Lean printed the two negative declarations and axioms exactly `[propext, Classical.choice, Quot.sound]`. Combined output SHA-256: `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`. Temporary `Statement.olean` SHA-256: `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`. |
| Run `rg` over owned `*.lean` files for line-leading `sorry`, `admit`, `axiom`, or `unsafe`, and for `sorryAx`; require the no-match exit | 0 | No prohibited declaration token in the owned Lean sources. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion-only worker self-test manifest is absent. |

Lean was `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. Source hashes were:

- `Statement.lean`: `4942287dad0600f98aa6379a6e541e50452e4c3d7cfd97e6f45fb1a7105a91dc`
- `Counterexample.lean`: `199ef928d35fe42bdcbadaac9b8e464d77b7ddb72dd782b381395aa7d8e24a18`
- `ObligationTree.lean`: `3a601fd16850b39a0416b4bf2dbe71a3e018773d1c9c79baec342c19c472891a`
- `obligation-registry.json`: `2e3678b818e758c5dd9ea74969b6f27e3c7196695f4a416e7634d947c60102a3`
- `typed-graphs.json`: `29af0cb8d4d8075b9e6b396b97c9409b7f6e9102d2259bdd8ac1dafaff18456e`

## Reopen condition

Replace the two semantic flags with a source-faithful, law-bearing standard
time/Ito integral construction, or constrain the operations by exact sufficient
laws. Then version and re-fingerprint the statement and freshly freeze and
master-accept the statement, anchor audit, obligation registry, and typed
graphs before proof execution resumes. Until then, the first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`, and the
decisive remaining cut is `M1036-X-INTEGRAL-SEMANTICS`,
`M1036-T-EXISTENCE`, and `M1036-ROOT`.
