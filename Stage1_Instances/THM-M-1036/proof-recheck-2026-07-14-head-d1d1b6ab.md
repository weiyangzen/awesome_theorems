# THM-M-1036 proof-phase recheck at `d1d1b6ab`

Item: `S56-M-1036-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `d1d1b6abb3bf227c43ebb3ce0513779bc96d6294`

Base tree: `c8009994d3b72ece76326dd39eaf0262255cb6a1`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks against the current pinned environment. The frozen
`IntegralSemantics` gives arbitrary `timeIntegral` and `itoIntegral` operations
and only bare proposition fields named `standard_time_integral` and
`standard_ito_integral`; those fields impose no laws on either operation. The
target nevertheless quantifies over every such semantics and concludes strong
existence when the two propositions hold.

`Counterexample.lean` sets both propositions to `True`, takes the sample space
to be `Unit` with its Dirac probability measure, uses state dimension one and
noise dimension zero, and defines
`timeIntegral f _ omega = f 0 omega + 1`. The required integral equation at
`t = 0` then yields `x = x + 1` in coordinate zero. Thus any positive proof of
the universe-polymorphic target would contradict the checked universe-zero
specialization.

This refutes the frozen formal encoding, not the mathematical SDE
existence-and-uniqueness theorem. Proving a repaired, strengthened, or narrower
statement would be a forbidden substitution in this proof item. The conditional
`root_of_existence_and_uniqueness` theorem supplies no proof body because it
assumes complete existence and uniqueness packages.

The assigned item remains `[ ]`. No positive proof receipt, state transition,
audit completion, theorem completion, validation completion, release, or
master-acceptance claim is made. No `.stage1-worker-selftest.json` is written
because the requested proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. Replace the two
bare semantic flags with a source-faithful law-bearing time/Ito integral
construction or exact sufficient laws. Then publish a new statement
fingerprint and freshly freeze and accept the statement, anchor audit,
obligation registry, and typed graphs before resuming positive proof work.
Alternatively, redirect the item explicitly to the checked counterexample
target.

The decisive invalid/open root cut is `M1036-X-INTEGRAL-SEMANTICS`,
`M1036-T-EXISTENCE`, and `M1036-ROOT`. The prior registry projection remains
open at M3; this recheck supplies M5 exact-target blocker evidence without
altering predecessor state. The prerequisite obligation-tree item is still
provisional rather than master-accepted.

## Validation

All checks ran in this worker clone using the existing symlink to canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, or `.lake` mutation was performed. Lean output was confined to
`/tmp` and removed after hashes and exact results were recorded.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present; this makes the evidence nonrelease. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS`: 18 obligations and 47 typed edges; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| Isolated `lake env lean` recipe below | 0 | Statement and countermodel both exited 0. Lean printed both negative declarations with axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`; `Statement.olean` SHA-256 `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx\|^\s*unsafe\s' Stage1_Instances/THM-M-1036 -g '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The isolated Lean recipe, run from `Formalizations/Lean`, was:

```bash
tmp=$(mktemp -d /tmp/thm-m-1036-proof-recheck-headd1d1b6ab.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1036/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1036/Counterexample.lean "$tmp/Counterexample.lean"
lake env lean --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/kernel-output.txt" 2>&1
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean --root="$tmp" "$tmp/Counterexample.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
```

Input SHA-256 values at this base are:

- `Statement.lean`: `4942287dad0600f98aa6379a6e541e50452e4c3d7cfd97e6f45fb1a7105a91dc`
- `Counterexample.lean`: `199ef928d35fe42bdcbadaac9b8e464d77b7ddb72dd782b381395aa7d8e24a18`
- `ObligationTree.lean`: `3a601fd16850b39a0416b4bf2dbe71a3e018773d1c9c79baec342c19c472891a`
- `obligation-registry.json`: `2e3678b818e758c5dd9ea74969b6f27e3c7196695f4a416e7634d947c60102a3`
- `typed-graphs.json`: `29af0cb8d4d8075b9e6b396b97c9409b7f6e9102d2259bdd8ac1dafaff18456e`
- `anchor-audit.json`: `b257e870b8076cdb6e4514e4636bf280111b1be741de0bedc9f25a400f84cd96`
- `lean-toolchain`: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
- `lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

This report is durable blocker evidence, not a proof receipt. Because the
assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.
