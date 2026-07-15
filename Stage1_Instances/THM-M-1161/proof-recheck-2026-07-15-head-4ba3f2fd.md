# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `4ba3f2fd1e609b5958f24e0415eef9300da16924`

Base tree: `6abc1f64758c17a59dad8c80ac44f238983dc720`

Recheck time: `2026-07-15T08:22:26+08:00`

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

The elaborated canonical declaration has another statement-fidelity defect: it does not quantify
`CompactSpace X` or `IsFiniteMeasure mu`. Lean drops those surrounding instances because neither
occurs in the resulting structure or proposition type, although the prose and `statement.json`
describe them as assumptions. The countermodel does not rely on this defect; its explicit
`compact_domain` and integrability fields satisfy the actual target.

The bounded pinned-mathlib audit found no exact integral-equation theorem that could replace the
missing proof. Its operator-level anchors include
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet`,
`ContinuousLinearMap.orthogonal_range`, and `ContinuousLinearMap.orthogonal_ker`. They cannot
repair the invalid pointwise normalization. Even after a linear-realization repair, the adjoint
solvability equivalence still needs a separate closed-range proof.

## Validation

All Lean commands reused the existing pinned Lake closure read-only. No `lake update`, `lake build`,
clone, fetch, or dependency mutation was performed. Source copies and compiled outputs were confined
to a fresh temporary directory under `Formalizations/Lean` and removed afterward. The
automation-provided `.lake` symlink is untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | execution rank 364; lifecycle planned; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | exact assigned item found at `[ ]`; obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; frozen root remains open at M4 |
| isolated pinned-Lean trust-zero recipe below | 0 | exact statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-4ba3f2fd.json >/dev/null` | 0 | current-base blocker record is valid JSON |
| `jq -e` blocker invariant check | 0 | item/base/verdict/state/completion/self-test/changed-path/count invariants passed |
| wrapped new-file `git diff --no-index --check` plus scoped `git diff --check` | 0 | both new artifacts and the scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-4ba3f2fd.XXXXXX")
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

This is the nineteenth structured blocker record for the same invariant countermodel: one original
`proof-blocker` plus eighteen `proof-recheck` records, including this one. That exceeds the
five-unresolved-tick limit in section 10.2. Reassigning the unchanged proof node cannot make
progress. The master must split or redirect the workflow to a statement-repair or barrier node
rather than issue another positive-proof retry against the same fingerprint.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Ensure the intended compactness and finite-
measure assumptions survive in the elaborated signature. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
desired root branch is circular and is not a valid repair. A repaired statement will still require
real proof of the closed-range and adjoint-solvability bridge; the pinned spectral anchor alone does
not close that analytic work.

Several predecessor limitations remain outside this proof worker's authority: the statement
fingerprint field records a source-file hash rather than a normalized kernel expression; required
statement mutations are not recorded; most registry fingerprints remain planned; the typed graph
still records `[H1, M4, R3]` while intake and earlier blocker prose use `H2` and this proof-phase
evidence diagnoses `M5`; and the predecessor obligation-tree item is only provisional `[_]`, not
master accepted. No frozen obligation is closed. Its recorded analytic cut set remains
`M1161-B-DICHOTOMY`, `M1161-L-BIJECTIVE`, `M1161-L-CLOSED-RANGE`, and
`M1161-L-ORTHOGONAL`. None is silently repaired or promoted here.

Because the positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
