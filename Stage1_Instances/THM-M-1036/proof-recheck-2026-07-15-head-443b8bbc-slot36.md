# THM-M-1036 proof-phase recheck at `443b8bbc`

Item: `S56-M-1036-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THM_M_1036.Counterexample.not_sdeExistenceUniquenessTarget :
  Not Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget.{0}
```

kernel-checks with the pinned Lean 4.29.0 executable and existing mathlib
artifacts. `IntegralSemantics` supplies arbitrary `timeIntegral` and
`itoIntegral` operations, while `standard_time_integral` and
`standard_ito_integral` are bare propositions that impose no laws on either
operation. The root nevertheless quantifies over every such semantics and
concludes strong existence after receiving proofs of those propositions.

`Counterexample.lean` sets both propositions to `True`, uses `Unit` with its
Dirac probability measure, state dimension one and noise dimension zero, and
defines `timeIntegral f _ omega = f 0 omega + 1`. The required integral
equation at `t = 0` yields `x = x + 1` in coordinate zero. Consequently, any
positive proof of the universe-polymorphic target would contradict its checked
universe-zero specialization.

This refutes the frozen formal encoding, not the classical SDE theorem.
Proving a repaired, strengthened, or narrower statement would be a forbidden
substitution in this proof item. The conditional
`root_of_existence_and_uniqueness` declaration is not closure: it assumes the
complete existence and uniqueness packages and supplies neither one.

The assigned item remains `[ ]`. No positive proof receipt, provisional state,
audit completion, theorem completion, validation completion, release, or
master acceptance is claimed. Its obligation-tree prerequisite is also still
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

The minimal decisive invalid root cut is `M1036-X-INTEGRAL-SEMANTICS`; its
invalidated/open chain continues through `M1036-T-EXISTENCE` to `M1036-ROOT`.
The frozen registry projection remains open at M3; this recheck proposes
`[H2, M3, R3] -> [H2, M5, R3]` blocker classification without altering
predecessor state. H2 is unchanged because the Lean countermodel refutes the
backend encoding rather than the classical human theorem.

There were 23 pre-existing `proof-recheck-*.json` records and 24 structured
blocker records when `proof-blocker.json` was included; this packet raises
those counts to 24 and 25. File counts include rejected or duplicate work and
do not prove distinct scheduler tick identity. The master must reconcile
actual unresolved ticks against the five-tick split rule. In all cases, another
unchanged positive-proof retry is inappropriate: repair and re-freeze the
target, or redirect it to the checked counterexample/barrier.

## Validation

Repository and target structural checks passed. Direct isolated Lean replay
also passed without invoking Lake dependency resolution. The direct replay
used the pinned Lean executable and explicitly listed only the pre-existing
standard library and package build paths; its output stayed under `/tmp` and
was removed after the run.

An ordinary `lake env` validation was also attempted. Because the canonical
cache lacked the manifest-pinned `flt-regular` artifact, Lake unexpectedly
started materializing that dependency through the automation-provided `.lake`
symlink. The operation was stopped; no cleanup, checkout, update, build, or
repair followed. The resulting partial `flt-regular` checkout has
`HEAD = refs/heads/.invalid` and does not resolve a commit. This is a separate
validation-environment blocker and makes this evidence nonrelease. It does not
affect the direct countermodel elaboration, which does not import
`flt-regular`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | Rank 229; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before this report | 0 | Only the automation-provided `?? Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-1036/check_obligation_tree.py` | 0 | `PASS THM-M-1036 obligation tree: 18 obligations, 47 typed edges`; denominator `7e425556f1efaf61324a9d453d76aa833189110b116824aaf32c2f390b328e69`; root open at M3. |
| Ordinary `lake env` statement validation | not accepted | The missing `flt-regular` package triggered Lake dependency materialization; the partial package does not resolve `HEAD`. The operation was stopped and no fetch or repair was intentionally continued. |
| Direct isolated Lean recipe below | 0 | The exact statement and countermodel elaborated with `--trust=0 -t0`. Lean printed both negative declarations with axioms exactly `[propext, Classical.choice, Quot.sound]`; statement-output SHA-256 `052c267144c1dc46129f5c40f97db91627a3025fea97d86a001e8ee1bd004673`; counterexample-output SHA-256 `e5e5d6a071019cdb10d072baefb1e7f05d0da040dcd61a457458decb0d897cfe`; `Statement.olean` SHA-256 `a3ec6b23bd506207b3cd0aff4175153a56fc3aa87f37cfc0466d3fe46a4812e4`. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx\|^\s*unsafe\s' Stage1_Instances/THM-M-1036 -g '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in the owned Lean sources. |
| Direct pinned `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | The partial cache artifact has no resolvable `HEAD`; expected manifest revision is `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/proof-recheck-2026-07-15-head-443b8bbc-slot36.json >/dev/null` plus scoped invariant assertions | 0 | JSON parsed; item/base identity, open state, source hashes, prerequisite and registry identity, direct kernel results, exact axiom list, empty receipts, false completion flags, and deliberate self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1036` | 0 | No scoped tracked-diff whitespace diagnostic. |
| `git diff --no-index --check /dev/null <new-file>` for both artifacts | 1 each | Expected content-difference exits with empty diagnostics; a wrapper required both exits to equal 1. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion-only worker self-test manifest is absent. |

The direct Lean recipe was:

```bash
set -uo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-1036-root-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1036/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1036/Counterexample.lean "$tmp/Counterexample.lean"
base="$root/Formalizations/Lean/.lake/packages"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean:$base/mathlib/.lake/build/lib/lean:$base/batteries/.lake/build/lib/lean:$base/Qq/.lake/build/lib/lean:$base/aesop/.lake/build/lib/lean:$base/proofwidgets/.lake/build/lib/lean:$base/LeanSearchClient/.lake/build/lib/lean:$base/plausible/.lake/build/lib/lean:$base/importGraph/.lake/build/lib/lean:$base/Cli/.lake/build/lib/lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  >"$tmp/statement.log" 2>&1
s1=$?
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" "$tmp/Counterexample.lean" \
  >"$tmp/counterexample.log" 2>&1
s2=$?
cat "$tmp/statement.log"
cat "$tmp/counterexample.log"
sha256sum "$tmp/statement.log" "$tmp/counterexample.log" "$tmp/Statement.olean"
exit $((s1 != 0 || s2 != 0))
```

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
