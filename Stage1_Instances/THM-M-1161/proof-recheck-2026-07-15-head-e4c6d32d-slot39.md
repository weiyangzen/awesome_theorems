# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `e4c6d32d1eb44bab8a06b606e6f2274e442d7f45`

Base tree: `c987baeda5c9641649fa79fa00eb4ec435472142`

Recheck time: `2026-07-15T12:28:08+08:00`

## Verdict

`blocked`. The universal closure of the exact frozen formal target is false, so no
placeholder-free positive proof can truthfully inhabit it. The proof item remains `[ ]`; no proof
receipt or worker self-test is emitted, and no audit, theorem, validation, release, or master
acceptance is claimed.

`FredholmKernelModel.realize` is an arbitrary injective function `E -> X -> Complex`; it need not
preserve zero, addition, or complex scalar multiplication. Thus `operator_eq_integral` does not
turn the pointwise expression

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

`CanonicalCounterexample.lean` transports the model field-for-field to the canonical declaration
and kernel-checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also checks `not_operator_normalization`. Both independent source inspection and a second Lean
replay found no defect in the adapter or countermodel. The negation declarations report only
`propext`, `Classical.choice`, and `Quot.sound`. This refutes the overbroad Lean encoding, not the
classical Fredholm alternative for a genuine complex-linear function realization.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, repair, or dependency mutation was run.
The automation-provided `.lake` symlink and existing pinned package oleans were reused read-only.
The root project's cached `flt-regular` checkout has no resolvable `HEAD`, so root-project
`lake env` failed closed. The narrow check instead used `lake env lean` from the intact pinned
mathlib subproject, with `LEAN_PATH` restricted to existing package build directories plus fresh
temporary copies of the three target modules. The temporary directory was removed afterward.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF" or .id == "S56-M-1161-OBLIGATION_TREE")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | proof item is `[ ]`; its obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; frozen root remains open at M4 |
| `cd Formalizations/Lean && timeout 60 lake env printenv LEAN_PATH` | 1 | Lake reported that cached `flt-regular` cannot resolve `HEAD`; no dependency mutation was attempted |
| isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-e4c6d32d-slot39.json >/dev/null` | 0 | current-base blocker record is valid JSON |
| `jq -e` blocker invariant check | 0 | item, base, verdict, state, completion, self-test, changed-path, and tick invariants passed |
| new-file and scoped `git diff --check` commands | 0 | both blocker artifacts and the scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd:)
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-e4c6d32d-slot39.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
(
  cd "$mathlib"
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
)
printf '%s\n' 'PINNED_MATHLIB_LAKE_ENV_LEAN_TRUST_ZERO_REPLAY=PASS'
```

It exited zero. `MATHLIB_HEAD` was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and `#print axioms` reported
`[propext, Classical.choice, Quot.sound]` for `not_root_bad`, `not_canonical_target`, and
`not_operator_normalization`. The final pass marker was printed.

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

This is the twenty-fourth structured blocker record for the same invariant countermodel: one
original `proof-blocker` plus twenty-three `proof-recheck` records, including this one. That
exceeds the five-unresolved-tick limit in section 10.2. Reassigning the unchanged proof node cannot
make progress. The master must split or redirect the workflow to a statement-repair or barrier node
rather than issue another positive-proof retry against the same fingerprint.

This count is an artifact count, not an authoritative scheduler-attempt count. The DAG still says
`attempts: 0`; only the master may reconcile that authority. The repeated records nevertheless
demonstrate far more than five unresolved assignments of the unchanged work surface.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
desired root branch is circular and is not a valid repair. A repaired statement will still need a
real closed-range and adjoint-solvability proof; the pinned spectral anchor alone does not close
that analytic work.

The obligation-tree prerequisite is provisional rather than master accepted. Other predecessor
limitations also remain outside this proof worker's authority: the statement fingerprint is a
source-file hash rather than a serialized normalized kernel expression, required mutation evidence
is absent, most obligation fingerprints remain planned, and predecessor artifacts disagree on
human debt while the proof-phase counterexample diagnoses machine status M5. No frozen obligation
is closed or promoted here.

Because the requested positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
