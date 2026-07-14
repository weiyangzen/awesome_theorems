# THM-M-1036 proof-phase recheck at `3b741f76`

Item: `S56-M-1036-PROOF`

Date: `2026-07-15` (Asia/Shanghai)

Base revision: `3b741f76df83670ba151a8f6ad6257bb8b6f6ead`

Base tree: `021c27ee3fae960d30f31e7f932f29401412edb0`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks against the pinned environment. `IntegralSemantics` supplies
arbitrary `timeIntegral` and `itoIntegral` operations, while
`standard_time_integral` and `standard_ito_integral` are bare propositions
that impose no laws on either operation. The root nevertheless quantifies over
every such semantics and concludes strong existence after receiving proofs of
those propositions.

`Counterexample.lean` sets both propositions to `True`, uses `Unit` with its
Dirac probability measure, state dimension one and noise dimension zero, and
defines `timeIntegral f _ omega = f 0 omega + 1`. The required integral
equation at `t = 0` then yields `x = x + 1` in coordinate zero. Consequently,
any positive proof of the universe-polymorphic target would contradict its
checked universe-zero specialization.

This refutes the frozen formal encoding, not the classical SDE theorem.
Proving a repaired, strengthened, or narrower statement would be a forbidden
substitution in this proof item. The conditional
`root_of_existence_and_uniqueness` declaration is not closure: it assumes the
complete existence and uniqueness packages and supplies neither one.

The item remains `[ ]`. No positive proof receipt, provisional state, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. The prerequisite obligation-tree item is also still
provisional `[_]`, not master-accepted. Because this proof phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M1036-X-INTEGRAL-SEMANTICS`. Replace the two
bare semantic flags with a source-faithful, law-bearing standard time/Ito
integral construction or exact sufficient laws. Then publish a new statement
fingerprint and freshly freeze and master-accept the statement, anchor audit,
obligation registry, and typed graphs before resuming proof work. Alternatively,
redirect this item explicitly to the checked counterexample target.

The decisive invalid/open root cut is `M1036-X-INTEGRAL-SEMANTICS`,
`M1036-T-EXISTENCE`, and `M1036-ROOT`. The frozen registry projection remains
open at M3; this recheck proposes `[H2, M3, R3] -> [H2, M5, R3]` blocker
classification without altering predecessor state. H2 is unchanged because
the Lean countermodel refutes the backend encoding rather than the classical
human theorem.

## Validation

All checks ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation occurred. Lean output was confined to fresh
directories under `/tmp` and removed after the runs. The dirty symlink makes
this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS THM-M-1036 obligation tree: 18 obligations, 47 typed edges`; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| `python3 Stage1_Instances/THM-M-1036/check_statement.py` | 0 | Canonical statement fingerprint `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; all three structural mutations killed; toolchain and mathlib pin matched the frozen statement packet. |
| Isolated `lake env`-pinned Lean recipe below | 0 | The exact statement and countermodel elaborated. Lean printed both negative declarations with axioms exactly `[propext, Classical.choice, Quot.sound]`; combined output SHA-256 `4b11faa31e8ad2a6401448d63176322e46bf814ff423c23016d4c7bfea426a55`; `Statement.olean` SHA-256 `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`, 624664 bytes. |
| `rg -n '^\s*(sorry|admit|axiom)(\s|$)|sorryAx|^\s*unsafe\s' Stage1_Instances/THM-M-1036 -g '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in the owned Lean sources. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-3b741f76.json >/dev/null` plus the invariant assertions described below | 0 | JSON parsed; item/base identity, open state, exact fingerprint, input hashes, negative kernel result, axiom list, empty receipt IDs, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1036` | 0 | No scoped tracked-diff whitespace diagnostic. |
| `git diff --no-index --check /dev/null <new-file>` for each new artifact | 1 each | Expected content-difference exits with empty diagnostic output; a wrapper asserted both exits were exactly 1 and returned 0. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion-only worker self-test manifest is absent. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1036
tmp=$(mktemp -d /tmp/thm-m-1036-proof-recheck-head3b741f76.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Counterexample.lean" "$tmp/Counterexample.lean"
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 nice -n 15 timeout 900 env LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/kernel-output.txt" 2>&1
LEAN_NUM_THREADS=1 nice -n 15 timeout 900 env LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean" \
  >>"$tmp/kernel-output.txt" 2>&1
cat "$tmp/kernel-output.txt"
sha256sum "$tmp/kernel-output.txt" "$tmp/Statement.olean"
```

The invariant check parses the packet and asserts its item ID, theorem ID,
HEAD and tree identities, `[ ]`/`blocked` state, statement fingerprint, every
listed input SHA-256, zero-exit kernel result, exact axiom list, false root and
terminal flags, empty receipt ID lists, recorded validation exits, and absent
worker self-test manifest.

Input SHA-256 values at this base are:

- `Statement.lean`: `4942287dad0600f98aa6379a6e541e50452e4c3d7cfd97e6f45fb1a7105a91dc`
- `Counterexample.lean`: `199ef928d35fe42bdcbadaac9b8e464d77b7ddb72dd782b381395aa7d8e24a18`
- `ObligationTree.lean`: `3a601fd16850b39a0416b4bf2dbe71a3e018773d1c9c79baec342c19c472891a`
- `statement.json`: `0ff7770a14df8bfa9c8b327a7ecf8508458cfd00a6df8a9ee67c85480b2fc18f`
- `obligation-registry.json`: `2e3678b818e758c5dd9ea74969b6f27e3c7196695f4a416e7634d947c60102a3`
- `typed-graphs.json`: `29af0cb8d4d8075b9e6b396b97c9409b7f6e9102d2259bdd8ac1dafaff18456e`
- `anchor-audit.json`: `b257e870b8076cdb6e4514e4636bf280111b1be741de0bedc9f25a400f84cd96`
- `validation-specs.json`: `2b1500e69c336a977ecc0c3c60dbd7c77f35c4d7f0f0d514aa0a5e2797789dd6`
- `lean-toolchain`: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
- `lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

This packet is durable blocker evidence, not a proof receipt. It supports no
state transition and deliberately leaves the completion-only worker self-test
manifest absent.
