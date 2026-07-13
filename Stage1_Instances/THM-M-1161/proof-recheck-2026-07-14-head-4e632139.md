# THM-M-1161 proof phase: current-head blocker

Item: `S56-M-1161-PROOF`

Base revision: `4e632139f5060edf088cd107551caac63981263b`

Base tree: `7a87a6b3f6b71cfb0b2d98872327edc8fe8620e6`

Rechecked: `2026-07-14T02:34:52+08:00`

## Verdict

`blocked`: the exact frozen Lean target is false, so the requested positive
proof body cannot be truthfully implemented. The proof item remains `[ ]`;
no proof receipt, provisional item state, audit completion, validation,
release, theorem completion, or master acceptance is claimed.

`FredholmKernelModel.realize` is required to be injective, but it need not
preserve zero, addition, or complex scalar multiplication. Therefore
`operator_eq_integral` identifies the integral with `realize (T phi)`, but it
does not identify the pointwise left side with
`realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

The checked model in `Proof.lean` uses `X = PUnit`, `E = Complex`, Dirac
measure, constant kernel `1`, `T = I`, and the injective affine map
`realize z = z + 1`. At `lambda = 1`, Lean proves

```text
Solves phi f <-> f = -1.
```

This is independent of `phi`. Hence the first target branch fails because both
`0` and `1` solve datum `-1`, contradicting uniqueness. The second branch
fails because datum `0` has no homogeneous solution. The adapter in
`CanonicalCounterexample.lean` connects the local construction definitionally
to the exact canonical declaration and kernel-checks

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also kernel-checks `not_operator_normalization`, a direct refutation of the
universal normalization needed by `M1161-N-OPERATOR`. Both declarations report
only `[propext, Classical.choice, Quot.sound]`. This refutes the overbroad
formal encoding, not the classical Fredholm alternative for a genuinely
linear function realization.

Under the rev-5.6 debt definitions, this supports proposed `H5/M5` only for
the exact frozen proposition. The predecessor registry still records `H2/M4`,
and this worker does not rewrite that authority; reconciliation belongs to the
integration lane. The underlying classical theorem is not classified as
refuted.

## First failed gate

The first failed gate is exact-target consistency at `M1161-N-OPERATOR`.
Positive proof execution can resume only after the statement phase replaces
`realize` with a complex-linear realization or adds source-justified,
noncircular additive and scalar compatibility laws. The integration lane must
then accept a new statement fingerprint and obligation-registry version delta
and rerun statement mutations, anchor audit, obligation-tree construction,
and proof execution in dependency order.

The existing `root_compose` declaration is only conditional composition: it
assumes the dichotomy and both analytic branch packages. It cannot repair a
refuted normalization and supplies no positive root proof body.

## Scoped validation

All commands ran in this worker clone using the existing pinned Lake closure.
This worker performed no `lake update`, `lake build`, dependency clone/fetch,
or `.lake` mutation. Lean sources and output objects were copied to a fresh
`/tmp` directory, which was removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | Rank 364; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; predecessor root remains open at `M4`. |
| Isolated pinned Lean recipe below | 0 | Exact canonical target and both refutations elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Redundant replay using the long `--trust=0` spelling | 1 | `lake env` resolution stopped before the Lean source commands with external Git exit 128 while unrelated processes were active in the shared canonical cache. This bootstrap failure receives no source-validation credit. |
| Prohibited-token scan over `Proof.lean` and `CanonicalCounterexample.lean` | 1 | Expected ripgrep no-match result; no forbidden construct found. |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/proof-recheck-2026-07-14-head-4e632139.json >/dev/null` | 0 | Fresh structured blocker is valid JSON. |
| `git diff --no-index --check /dev/null <fresh-artifact>` wrapper, for each fresh artifact | 0 | The wrapper accepted Git's expected new-file exit `1` only with empty diagnostics; both new files have no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json` | 0 | No whitespace errors in tracked scoped deltas; fresh untracked files were checked separately above. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
tmp=$(mktemp -d /tmp/thm-m-1161-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean "$tmp/"
cp Stage1_Instances/THM-M-1161/Proof.lean "$tmp/"
cp Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean "$tmp/"
(
  cd "$tmp"
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -t0 -o \
    FredholmIntegralEquationStatement.olean \
    FredholmIntegralEquationStatement.lean
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -t0 -o Proof.olean Proof.lean
  LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" -t0 CanonicalCounterexample.lean
)
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
Here `-t0` is Lean's short form of `--trust=0`. The successful replay above is
the source result; the later shared-cache bootstrap failure is why this packet
is expressly nonrelease evidence.

Because the assigned positive proof phase is not genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent. This is actionable
blocker evidence, not proof completion.
