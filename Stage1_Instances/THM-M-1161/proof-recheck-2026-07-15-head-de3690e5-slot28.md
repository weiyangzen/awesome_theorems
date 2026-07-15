# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `de3690e5c47324173be2cf28a18229b53290f989`

Base tree: `8a9cb34ea79069c40875230eafb677a50cc0405b`

Recheck time: `2026-07-15T22:37:54+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no positive proof receipt or root worker
self-test is emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is an arbitrary injective function `E -> X -> Complex`; it need not
preserve zero, addition, or complex scalar multiplication. Consequently `operator_eq_integral`
does not turn

```text
realize phi - lambda * realize (operator phi)
```

into `realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

The checked countermodel takes `X = PUnit`, `E = Complex`, the Dirac measure at the unique point,
constant kernel `1`, `T = id`, and the permitted injective affine realization
`realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly when `f = -1`, independently
of `phi`. The first branch therefore fails uniqueness for datum `-1`, while the second branch
fails because datum `0` has no homogeneous solution.

`CanonicalCounterexample.lean` transports the model field-for-field to the exact canonical
declaration and kernel-checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also checks `not_operator_normalization`. A fresh isolated trust-zero replay at the current base
reproduced both declaration types. The checked negations depend only on `propext`,
`Classical.choice`, and `Quot.sound`. Two independent read-only proof reviews reached the same
conclusion; one also independently replayed the modules at trust level zero. This refutes the
overbroad Lean encoding, not the classical Fredholm alternative for a genuine complex-linear
function realization.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, repair, or dependency mutation was run.
The automation-provided `.lake` symlink and existing pinned package oleans were reused read-only.
The target modules were copied to a fresh temporary directory under `Formalizations/Lean`,
elaborated by the pinned root `lake env lean`, and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; L0/rework-required; theorem incomplete |
| DAG JSON query for `S56-M-1161-PROOF` and `S56-M-1161-OBLIGATION_TREE` | 0 | proof item is `[ ]` with attempts 0; its dependency remains provisional `[_]` with attempts 1 |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; root remains open at M4 |
| isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and exact canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| JSON parse and blocker-invariant query | 0 | structured record and its item, base, verdict, completion, self-test, changed-path, and blocker invariants passed |
| new-file and scoped whitespace checks | 0 | both blocker artifacts and the complete scoped delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
flt_regular=$lean_root/.lake/packages/flt-regular
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-de3690e5-slot28.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
printf 'MATHLIB_HEAD=%s\n' "$(git -C "$mathlib" rev-parse HEAD)"
printf 'FLT_REGULAR_HEAD=%s\n' "$(git -C "$flt_regular" rev-parse HEAD)"
printf 'LEAN_PATH_SHA256=%s\n' \
  "$(printf '%s' "$lean_path" | sha256sum | cut -d' ' -f1)"
printf 'LEAN_PATH_DIRS=%s\n' \
  "$(printf '%s' "$lean_path" | awk -F: '{print NF}')"
(
  cd "$lean_root"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      -o "$tmp/FredholmIntegralEquationStatement.olean" \
      "$tmp/FredholmIntegralEquationStatement.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      -o "$tmp/Proof.olean" "$tmp/Proof.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      "$tmp/CanonicalCounterexample.lean"
  lake --version
  lake env lean --version
)
printf '%s\n' 'ROOT_LAKE_ENV_LEAN_TRUST_ZERO_REPLAY=PASS'
```

It exited zero. `MATHLIB_HEAD` was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `FLT_REGULAR_HEAD` was
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, `LEAN_PATH_SHA256` was
`459c7089eaa76eaf4a9d5d9cd3f4c3c1fecb19bccf0afddde18aae46e95df456`, and the path had 13
directories. Lake was `5.0.0-src+98dc76e`; Lean was `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M1161-N-OPERATOR`. The statement phase must
be reopened and `realize` replaced by, or accompanied by, a source-faithful complex-linear
compatibility law sufficient to prove

```text
realize (phi - lambda * operator phi) =
  realize phi - lambda * realize (operator phi).
```

The master must then accept a new statement fingerprint and obligation-registry version delta and
rerun statement mutation, anchor audit, obligation-tree construction, and proof execution. The
dossier now contains 56 blocker/recheck records including this one, well beyond the five-tick split
threshold, although the authoritative DAG still reports zero proof attempts. The master should
redirect this unchanged item to statement repair or a barrier/counterexample node instead of
reassigning it. Assuming the invalid normalization or either desired root branch is not a valid
repair.

Because the positive proof phase is blocked rather than completed, `.stage1-worker-selftest.json`
is deliberately absent.
