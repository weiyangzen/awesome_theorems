# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `51c2828e82ffb19860830f78b771f80e13ad7dff`

Base tree: `4655b8b40829513de6fb5661344b33fc7cd17cd1`

Recheck time: `2026-07-15T16:11:05+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no proof receipt or root worker self-test is
emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is assumed injective but not complex-linear. Consequently
`operator_eq_integral` does not identify the pointwise expression

```text
realize phi - lambda * realize (operator phi)
```

with `realize ((I - lambda T) phi)`. The frozen normalization obligation
`M1161-N-OPERATOR` is invalid.

The kernel-checked countermodel takes `X = PUnit`, `E = Complex`, the Dirac measure at the unique
point, constant kernel `1`, identity operator `T`, and the permitted affine injection
`realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly when `f = -1`, independently
of `phi`. The first branch fails because both `0` and `1` solve datum `-1`; the second branch fails
because datum `0` has no homogeneous solution.

`CanonicalCounterexample.lean` transports the model field-for-field to the exact canonical
statement and checks:

```text
AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target :
  Not (FredholmSecondKindAlternative (Measure.dirac PUnit.unit) ... 1)
```

It also checks `not_operator_normalization`. Both declarations report only `propext`,
`Classical.choice`, and `Quot.sound`. Three independent worker inspections agreed that the model,
adapter, and contradiction match the frozen target. This refutes the overbroad Lean encoding, not
the classical Fredholm alternative for a genuine complex-linear function realization.

The required predecessor `S56-M-1161-OBLIGATION_TREE` remains provisional `[_]`, independently
preventing dependency-ordered proof-node acceptance.

## Current-base validation

No `lake update`, `lake build`, dependency clone/fetch, repair, or dependency mutation was run. The
automation-provided `.lake` symlink and existing pinned package oleans were reused read-only. The
three target modules were copied into an ignored temporary directory beneath `Formalizations/Lean`,
elaborated using root `lake env lean`, and removed by a trap.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD && git rev-parse HEAD^{tree} && git status --short` | 0 | base `51c2828e82ffb19860830f78b771f80e13ad7dff`; tree `4655b8b40829513de6fb5661344b33fc7cd17cd1`; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before worker changes |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; L0/rework-required; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF" or .id == "S56-M-1161-OBLIGATION_TREE")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | proof item is `[ ]`; its obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; root remains open at M4 |
| root pinned `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool` plus the `jq -e` blocker-invariant query | 0 | structured blocker parses and its item, base, verdict, completion, self-test, changed-path, dependency, and escalation invariants pass |
| new-file `git diff --no-index --check` wrappers plus scoped `git diff --check` | 0 | both new artifacts and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-51c2828e-slot40.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
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
printf '%s\n' 'ROOT_LAKE_ENV_LEAN_TRUST_ZERO_REPLAY=PASS'
```

It exited zero. `MATHLIB_HEAD` was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `FLT_REGULAR_HEAD` was
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, and `LEAN_PATH_SHA256` was
`c8dd1960a4ac15907ad2e1f13db33a8627927d16c49bafc019ebf39e05e733e7`. Lean was
`4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake was
`5.0.0-src+98dc76e`. The final pass marker was printed.

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx)\b|^[[:space:]]*(?:axiom|unsafe|external)[[:space:]]|placeholder|fake result' \
  Stage1_Instances/THM-M-1161/Proof.lean \
  Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean
```

## Escalation and retry condition

This is the thirty-fourth structured blocker artifact for the same invariant countermodel: one
original `proof-blocker` plus thirty-three `proof-recheck` artifacts, including this one. That
exceeds the five-unresolved-tick limit. This is an artifact count, not an authoritative scheduler
attempt count; the DAG still records `attempts: 0`, which only the master may reconcile.
Reassigning the unchanged proof node cannot make progress. The master must split or redirect the
workflow to a statement-repair or barrier/counterexample node.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply additive and scalar compatibility. Then accept a new statement fingerprint, publish an
append-only obligation-registry version delta, and rerun statement mutation, anchor audit,
obligation-tree construction, and proof execution. Assuming the normalization or either desired
root branch would be circular and is not a valid repair.

Even after repairing realization linearity, substantive analytic obligations remain: bijectivity
of `I - lambda T` in the trivial-kernel case, closed range, range/adjoint-kernel orthogonality, and
transport back to the pointwise equation. The pinned spectral and adjoint declarations are
supporting anchors, not exact proof bodies for those obligations.

## Status boundary

This is fresh current-base negative kernel evidence only. It does not complete
`S56-M-1161-PROOF`, change authoritative debt, establish `AUDIT-Z` or `THEOREM-Z`, or authorize
validation, release, checklist promotion, or master acceptance. Because the assigned positive
proof phase is not genuinely self-tested, `.stage1-worker-selftest.json` is deliberately absent.
