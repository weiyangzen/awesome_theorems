# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `3af3b6bc58d308bda7dc1cb164a9a258512b8c53`

Base tree: `65dce2e2ba00c806bf25b436c98caf996c1c56d2`

Recheck time: `2026-07-15T16:50:22+08:00`

## Verdict

`blocked`. The exact frozen Lean target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no proof receipt or root worker self-test is
emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is an arbitrary injective function `E -> X -> Complex`. It need not
preserve zero, addition, or complex scalar multiplication. Consequently `operator_eq_integral`
does not turn

```text
realize phi - lambda * realize (operator phi)
```

into `realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

The checked countermodel uses `X = PUnit`, `E = Complex`, the Dirac measure at the unique point,
constant kernel `1`, `T = id`, and the permitted injective affine realization
`realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly when `f = -1`, independently
of `phi`. The unique-solvability branch therefore fails for datum `-1`, while the second branch
fails because datum `0` has no homogeneous solution.

`CanonicalCounterexample.lean` transports this model field-for-field to the canonical declaration
and kernel-checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also kernel-checks `not_operator_normalization`. Both declarations report only `propext`,
`Classical.choice`, and `Quot.sound`. This refutes the overbroad formal encoding, not the classical
Fredholm alternative for a genuine complex-linear function realization.

The bounded pinned-mathlib audit found no exact integral-equation theorem that could replace a
positive proof. Its closest anchor, `IsCompactOperator.hasEigenvalue_or_mem_resolventSet`, is an
operator-spectral result and cannot repair the invalid pointwise/operator normalization.

The required predecessor `S56-M-1161-OBLIGATION_TREE` remains provisional `[_]`, not master
accepted. Dependency legality therefore prevents proof-node acceptance independently of the
mathematical counterexample.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was performed. The
automation-provided `.lake` symlink and its pinned package artifacts were reused read-only. The
untracked symlink makes this narrow replay nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | execution rank 364; lifecycle planned; theorem incomplete |
| DAG query for `S56-M-1161-PROOF` and its dependency | 0 | proof item is `[ ]`; obligation-tree dependency is provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; frozen root remains open at M4 |
| isolated pinned `lake env lean --trust=0` recipe below | 0 | exact statement, countermodel, and canonical adapter elaborated; printed axioms were only `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest is absent because the positive proof phase is blocked |

The isolated trust-level-zero recipe compiled temporary copies under the Lean package root and
removed all generated files:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-3af3b6bc-slot31.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
lean_path=$(cd "$lean_root" && timeout 180 lake env printenv LEAN_PATH)
(
  cd "$lean_root"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 \
      -o "$tmp/FredholmIntegralEquationStatement.olean" \
      "$tmp/FredholmIntegralEquationStatement.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 "$tmp/CanonicalCounterexample.lean"
)
printf '%s\n' 'ISOLATED_TRUST_ZERO_REPLAY=PASS'
```

The command exited zero with final marker `ISOLATED_TRUST_ZERO_REPLAY=PASS`. Pinned versions were
Lean `4.29.0` at `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
The `lake-manifest.json` SHA-256 was
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx)\b|^[[:space:]]*(?:axiom|unsafe|external)[[:space:]]|placeholder|fake result' \
  Stage1_Instances/THM-M-1161/Proof.lean \
  Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean
```

It exited `1` with no output, the expected `rg` result for zero matches.

## Escalation and retry condition

This is the thirty-fifth structured blocker record for the same invariant countermodel: one
original blocker and thirty-four rechecks, including this one. That exceeds the five-unresolved-
tick limit in section 10.2. The master must stop reassigning the unchanged positive-proof item and
split or redirect it to statement repair or a counterexample/barrier workflow node.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the necessary additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
desired branch is circular and is not a repair. Even after fixing realization linearity, a proof
must still establish the closed-range and adjoint-solvability bridge; the spectral anchor alone
does not close that analytic work.

The predecessor graph still records the root at `[H1, M4, R3]`, while intake and earlier blocker
prose use `H2`; this proof worker does not rewrite that authority and records only a proof-phase
`M5` diagnosis. The predecessor statement fingerprint is a source-file hash rather than a
serialized normalized kernel expression, required statement mutations are absent, most obligation
fingerprints remain planned, and no frozen obligation is closed or promoted here.

Because the requested positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
