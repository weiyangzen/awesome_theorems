# THM-M-1161 proof-phase blocker

Item: `S56-M-1161-PROOF`  
Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`  
Validation date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`: the exact frozen Lean target is false. The assigned positive proof
deliverable therefore cannot be truthfully completed. The item remains `[ ]`;
no proof receipt or worker self-test manifest is emitted, and no audit,
theorem, validation, release, or master acceptance is claimed.

The model field

```lean
realize : E -> X -> Complex
```

is required only to be injective. It is not required to preserve zero,
addition, or scalar multiplication. Consequently `operator_eq_integral`
identifies the integral with `realize (T phi)`, but does not turn
`realize phi - lambda * realize (T phi)` into
`realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

`Proof.lean` instantiates `X = PUnit`, `E = Complex`, the Dirac measure at the
unique point, constant kernel `1`, operator `T = I`, and
`realize z = z + 1`. All frozen model fields hold: the domain is compact, the
kernel is continuous, `realize` is injective, the integrand is integrable, the
identity is compact in finite dimension, and the Dirac integral equals
`realize (T z)`.

At `lambda = 1`, the pointwise equation reduces to

```text
(phi + 1) - (phi + 1) = f + 1,
```

so `Solves phi f` holds exactly when `f = -1`, independently of `phi`. The
first alternative cannot hold because both `0` and `1` solve the datum `-1`,
contradicting uniqueness. The second cannot hold because the homogeneous
datum `0` has no solution. Thus the checked declaration

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

refutes the exact canonical proposition. Its axiom report is
`[propext, Classical.choice, Quot.sound]`, with no added axiom or admission.
`not_operator_normalization` separately refutes the universal normalization
claimed by `M1161-N-OPERATOR`.

This countermodel refutes only the overbroad frozen formal encoding. It does
not refute the classical Fredholm alternative for a genuine linear function
realization.

## First Failed Gate

The first failed gate is exact-target consistency at `M1161-N-OPERATOR`. The
statement phase must be reopened and `realize` replaced by, or accompanied by,
a complex-linear compatibility law sufficient to prove

```text
realize (phi - lambda • operator phi) =
  realize phi - lambda • realize (operator phi).
```

The integration lane must then accept a new statement fingerprint, publish a
registry-version delta, and rerun statement mutation, anchor audit, obligation
tree, and proof execution. Assuming the normalization or either root branch
would be circular and is not a valid repair.

## Scoped Validation

All checks used the existing pinned Lake closure. No update, build, clone,
fetch, or dependency mutation was performed. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to the canonical pinned cache and
makes this nonrelease evidence.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1161
  exit 0: execution rank 364; lifecycle planned; theorem_complete false

python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py
  exit 0: 19 obligations and 65 typed edges passed; denominator
  8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a
```

The exact isolated Lean recipe compiles the canonical statement, local
countermodel, and definitional adapter into a temporary directory, then
removes all generated files:

```bash
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
tmp=$(mktemp -d /tmp/thm-m-1161-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean "$tmp/"
cp Stage1_Instances/THM-M-1161/Proof.lean "$tmp/"
cp Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean "$tmp/"
(cd "$tmp" &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -t0 -o FredholmIntegralEquationStatement.olean \
    FredholmIntegralEquationStatement.lean &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -t0 -o Proof.olean Proof.lean &&
  LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" -t0 CanonicalCounterexample.lean)
```

The trust-level-zero recipe exits `0`; both negation declarations report only `propext`,
`Classical.choice`, and `Quot.sound`.

```text
rg -n '(\bsorry\b|\badmit\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b|placeholder|fake result)' \
  Stage1_Instances/THM-M-1161/Proof.lean \
  Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean
  exit 1 with empty output: pass; `rg` uses exit 1 for no matches

python3 -m json.tool Stage1_Instances/THM-M-1161/proof-blocker.json >/dev/null
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json
  exit 0: no whitespace errors

test ! -e .stage1-worker-selftest.json
  exit 0: no worker completion manifest was emitted
```

Because the positive proof phase is blocked rather than completed, root closure
remains false and `.stage1-worker-selftest.json` is deliberately absent.
