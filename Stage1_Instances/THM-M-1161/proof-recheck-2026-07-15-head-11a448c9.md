# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `11a448c97289d30fe7c8c05dbac5a283a9d00896`

Base tree: `a79f60552d328e98302026909ec6676cb6cd6ea2`

Recheck time: `2026-07-15T05:54:23+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no proof receipt or root worker self-test is
emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is an arbitrary injective function `E -> X -> Complex`; it need not
preserve zero, addition, or complex scalar multiplication. Consequently `operator_eq_integral`
does not turn the pointwise expression

```text
realize phi - lambda * realize (operator phi)
```

into `realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

The checked countermodel takes `X = PUnit`, `E = Complex`, the Dirac measure at the unique point,
constant kernel `1`, `T = id`, and the permitted injective affine realization
`realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly when `f = -1`, independently
of `phi`. Hence the first canonical branch fails uniqueness for datum `-1`, while the second
branch fails because the homogeneous datum `0` has no solution.

`CanonicalCounterexample.lean` transports that model field-for-field to the exact canonical
declaration and kernel-checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also kernel-checks `not_operator_normalization`. The checked negations report only `propext`,
`Classical.choice`, and `Quot.sound`. This refutes the overbroad Lean encoding, not the classical
Fredholm alternative for a genuine complex-linear function realization.

Pinned mathlib has no exact integral-equation theorem that could replace the missing proof. Its
closest audited anchor, `IsCompactOperator.hasEigenvalue_or_mem_resolventSet`, concerns the
associated compact operator and cannot repair the invalid pointwise/operator normalization.

## Validation

All Lean commands reused the existing pinned Lake closure read-only. No `lake update`, `lake build`,
clone, fetch, or dependency mutation was performed. Source copies and compiled outputs were confined
to a fresh temporary directory and removed afterward. The automation-provided `.lake` symlink is
untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | execution rank 364; lifecycle planned; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | exact assigned item found at `[ ]`, depending on `S56-M-1161-OBLIGATION_TREE` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; frozen root remains open at M4 |
| isolated pinned-Lean trust-zero recipe below | 0 | exact statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-11a448c9.json >/dev/null` | 0 | current-base blocker record is valid JSON |
| wrapped new-file `git diff --no-index --check` plus scoped `git diff --check` | 0 | both new artifacts and the scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-11a448c9.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
lean_path=$(cd "$lean_root" && timeout 180 lake env printenv LEAN_PATH)
(
  cd "$lean_root"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 -o "$tmp/FredholmIntegralEquationStatement.olean" \
      "$tmp/FredholmIntegralEquationStatement.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 "$tmp/CanonicalCounterexample.lean"
)
printf '%s\n' 'ISOLATED_TRUST_ZERO_REPLAY=PASS'
```

The recipe exited zero and printed `ISOLATED_TRUST_ZERO_REPLAY=PASS`. `#print axioms` reported
`[propext, Classical.choice, Quot.sound]` for `not_root_bad`, `not_canonical_target`, and
`not_operator_normalization`.

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx)\b|^[[:space:]]*(?:axiom|unsafe|external)[[:space:]]|placeholder|fake result' \
  Stage1_Instances/THM-M-1161/Proof.lean \
  Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Escalation and retry condition

This is the eleventh structured blocker or recheck for the same invariant countermodel, exceeding
the five-unresolved-tick limit in section 10.2. Reassigning the unchanged proof node cannot make
progress. The master must split or redirect the workflow to a statement-repair/barrier node rather
than issue another positive-proof retry against the same fingerprint.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
desired root branch is circular and is not a valid repair.

Several predecessor limitations also remain outside this proof worker's authority: the statement
fingerprint field records a source-file hash rather than a normalized kernel expression; the
required statement mutations are not recorded; most registry fingerprints remain planned; the
typed graph still records `[H1, M4, R3]` while intake and earlier blocker prose use `H2` and this
proof-phase evidence diagnoses `M5`; and the predecessor obligation-tree item has not received
master `[x]` acceptance. None is silently repaired or promoted here.

Because the positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
