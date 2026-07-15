# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `e57cfb0904e8a827b17320aba51bd41b96109c7c`

Base tree: `79ab3544eee575a45c51d85923144ed20f607f9e`

Recheck time: `2026-07-15T20:04:03+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no positive proof receipt or root worker
self-test is emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

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
of `phi`. The first branch therefore fails uniqueness for datum `-1`, while the second branch
fails because datum `0` has no homogeneous solution.

`CanonicalCounterexample.lean` transports the model field-for-field to the exact canonical
declaration and kernel-checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also checks `not_operator_normalization`. A fresh isolated trust-zero replay at the current base
reproduced these declaration types. The checked negations depend only on `propext`,
`Classical.choice`, and `Quot.sound`. This refutes the overbroad Lean encoding, not the classical
Fredholm alternative for a genuine complex-linear function realization.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, repair, or dependency mutation was run.
The automation-provided `.lake` symlink and existing pinned package oleans were reused read-only.
The three target modules were copied to a fresh temporary directory under `Formalizations/Lean`,
elaborated by the pinned root `lake env lean`, and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; L0/rework-required; theorem incomplete |
| DAG query for `S56-M-1161-PROOF` and `S56-M-1161-OBLIGATION_TREE` | 0 | proof item is `[ ]`; its obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; root remains open at M4 |
| isolated pinned `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| JSON parse and blocker-invariant query on the sibling record | 0 | structured blocker and its item, base, verdict, completion, self-test, changed-path, and escalation invariants passed |
| new-file and scoped whitespace checks | 0 | both blocker artifacts and the complete scoped delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-e57cfb09-slot41.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
lean_path=$(cd "$lean_root" && timeout 180 lake env printenv LEAN_PATH)
printf 'MATHLIB_HEAD=%s\n' \
  "$(git -C "$lean_root/.lake/packages/mathlib" rev-parse HEAD)"
printf 'FLT_REGULAR_HEAD=%s\n' \
  "$(git -C "$lean_root/.lake/packages/flt-regular" rev-parse HEAD)"
printf 'LEAN_PATH_SHA256=%s\n' \
  "$(printf '%s' "$lean_path" | sha256sum | cut -d' ' -f1)"
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
  lean --version
)
printf '%s\n' 'LAKE_ENV_LEAN_TRUST_ZERO_REPLAY=PASS'
```

It exited zero. `MATHLIB_HEAD` was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `FLT_REGULAR_HEAD` was
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, and `LEAN_PATH_SHA256` was
`ddb0ad4cf4c921543a069cc532b0ba93ec6745349bf75e2338855a6b7f8dda05`.
`#print axioms` reported `[propext, Classical.choice, Quot.sound]` for `not_root_bad`,
`not_canonical_target`, and `not_operator_normalization`. The final pass marker was printed.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Escalation and retry condition

This is the forty-ninth structured blocker artifact for the same invariant countermodel: one
original `proof-blocker` plus forty-eight `proof-recheck` artifacts, including this one. That
exceeds the five-unresolved-tick limit in section 10.2. This count is an artifact count, not an
authoritative scheduler-attempt count; the DAG still records `attempts: 0`, which only the master
may reconcile. Reassigning the unchanged proof node cannot make progress. The master must split or
redirect the workflow to a statement-repair or barrier/counterexample node.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
desired root branch is circular and is not a valid repair. A corrected statement will still need a
real bijectivity/closed-range and adjoint-solvability proof; the pinned spectral anchors alone do
not close that analytic work.

The obligation-tree prerequisite is provisional rather than master accepted. Other predecessor
limitations also remain outside this proof worker's authority: the statement fingerprint is a
source-file hash rather than a serialized normalized kernel expression, required mutation evidence
is absent, most obligation fingerprints remain planned, and predecessor artifacts disagree on
human debt while this proof-phase counterexample diagnoses machine status M5. No frozen obligation
is closed or promoted here.

Because the requested positive proof phase is blocked rather than self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
