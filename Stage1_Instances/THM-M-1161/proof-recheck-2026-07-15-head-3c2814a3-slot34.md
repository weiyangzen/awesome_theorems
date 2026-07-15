# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

Recheck time: `2026-07-15T15:52:40+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no proof receipt or root worker self-test is
emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is assumed injective but not complex-linear. Therefore
`operator_eq_integral` does not justify rewriting the pointwise equation as
`(ContinuousLinearMap.id Complex E - lambda • M.operator) phi = f`. The checked countermodel uses
`X = PUnit`, `E = Complex`, Dirac measure, constant kernel `1`, identity operator, and the permitted
injective affine realization `realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly
when `f = -1`, independently of `phi`. Unique solvability fails for datum `-1`, while datum `0` has
no homogeneous solution, so both branches of the canonical target fail.

The exact canonical negation is checked by
`AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target`; the separate declaration
`not_operator_normalization` refutes the frozen normalization itself. The declarations depend only
on `propext`, `Classical.choice`, and `Quot.sound`. This evidence refutes only the overbroad Lean
encoding, not the classical Fredholm alternative for genuine linear function realizations.

The pinned mathlib anchors are operator-level support only. In particular,
`IsCompactOperator.hasEigenvalue_or_mem_resolventSet` and
`ContinuousLinearMap.orthogonal_range` cannot repair the invalid pointwise/operator bridge. The
required predecessor `S56-M-1161-OBLIGATION_TREE` also remains provisional `[_]`, independently
preventing dependency-ordered proof-node acceptance.

## Current-base validation

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | base revision `3c2814a370c2fee02158ca79aa44a48e411c4d18`; tree `e1bd7e27bd922b779322c089410a471b6a1535f0` |
| `git status --short` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before worker changes |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; L0/rework-required; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF" or .id == "S56-M-1161-OBLIGATION_TREE")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | proof item is `[ ]`; its obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; root remains open at M4 |
| first `/tmp` isolated replay with explicit root | 1 | Lean rejected the source before elaboration because it was outside `Formalizations/Lean`; no dependency or repository artifact changed |
| second `/tmp` isolated replay with inferred root | 1 | Lean rejected the source before elaboration because it was outside mathlib's inferred root; no dependency or repository artifact changed |
| corrected isolated pinned-mathlib `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool` plus the `jq -e` blocker-invariant query | 0 | structured blocker parses and its item, base, verdict, completion, self-test, changed-path, dependency, and escalation invariants pass |
| new-file `git diff --no-index --check` wrappers plus scoped `git diff --check` | 0 | both new artifacts and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

The two preliminary attempts used the variable definitions and three source copies shown in the
successful recipe below, but placed `tmp` under `/tmp`. With `set -euo pipefail`, each stopped at
its first Lean invocation. The first used these exact changed lines:

```bash
tmp=$(mktemp -d /tmp/thm-m-1161-proof-3c2814a-slot34.XXXXXX)
(
  cd "$mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --root="$lean_root" --trust=0 -t0 \
      -o "$tmp/FredholmIntegralEquationStatement.olean" \
      "$tmp/FredholmIntegralEquationStatement.lean"
)
```

It exited `1` with:

```text
input file '/tmp/thm-m-1161-proof-3c2814a-slot34.<mktemp>/FredholmIntegralEquationStatement.lean'
must be contained in root directory (<worker-root>/Formalizations/Lean/)
```

The second retained the `/tmp` placement and removed only the explicit root argument:

```bash
(
  cd "$mathlib"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
    lake env lean --trust=0 -t0 \
      -o "$tmp/FredholmIntegralEquationStatement.olean" \
      "$tmp/FredholmIntegralEquationStatement.lean"
)
```

It exited `1` with the same containment error against mathlib's inferred root. Neither attempt
reached elaboration. Both traps removed their temporary sources, and neither mutated `.lake`.

The successful isolated elaboration recipe, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd:)
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-3c2814a-slot34.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
cp "$target/FredholmIntegralEquationStatement.lean" "$tmp/"
cp "$target/Proof.lean" "$tmp/"
cp "$target/CanonicalCounterexample.lean" "$tmp/"
printf 'MATHLIB_HEAD=%s\n' "$(git -C "$mathlib" rev-parse HEAD)"
printf 'LEAN_PATH_DIRS=%s\n' \
  "$(printf '%s' "$lean_path" | awk -F: '{print NF}')"
printf 'LEAN_PATH_SHA256=%s\n' \
  "$(printf '%s' "$lean_path" | sha256sum | cut -d' ' -f1)"
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
  lake --version
  lean --version
)
printf '%s\n' 'PINNED_MATHLIB_LAKE_ENV_LEAN_TRUST_ZERO_REPLAY=PASS'
```

It exited zero. `MATHLIB_HEAD` was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `LEAN_PATH_DIRS` was `8`, and the
`LEAN_PATH` SHA-256 was `66bec89efe93fe099f9810c21e2a29266f96ff4502b0769cc8c1ea9aa3879ae3`.
`#print axioms` reported `[propext, Classical.choice, Quot.sound]` for `not_root_bad`,
`not_canonical_target`, and `not_operator_normalization`. The final pass marker was printed.

Scoped prohibited-construct scan:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx)\b|^[[:space:]]*(?:axiom|unsafe|external)[[:space:]]|placeholder|fake result' \
  Stage1_Instances/THM-M-1161/Proof.lean \
  Stage1_Instances/THM-M-1161/CanonicalCounterexample.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; flt-regular
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No `lake update`, `lake build`, clone, fetch, or dependency mutation was performed. Both failed
preliminary recipes copied sources only into `/tmp` and failed before elaboration; their traps
removed those copies. The successful recipe used an ignored temporary directory under
`Formalizations/Lean`, and its trap removed that directory and generated oleans.

## Escalation and retry condition

This is the thirty-third structured blocker artifact for the same invariant countermodel: one
original `proof-blocker` plus thirty-two `proof-recheck` artifacts, including this one. That exceeds
the five-unresolved-tick limit. This count is an artifact count, not an authoritative scheduler
attempt count; the DAG still records `attempts: 0`, which only the master may reconcile. Reassigning
the unchanged proof node cannot make progress. The master must split or redirect the workflow to a
statement-repair or barrier/counterexample node.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
root branch would be circular and is not a valid repair.

Even after repairing realization linearity, substantive analytic obligations remain: bijectivity
of `I - lambda T` in the trivial-kernel case, closed range, range/adjoint-kernel orthogonality, and
transport back to the pointwise equation. The pinned spectral and adjoint declarations are
supporting anchors, not exact proof bodies for those obligations.

## Status boundary

This is fresh current-base negative kernel evidence only. It does not complete
`S56-M-1161-PROOF`, change an authoritative debt vector, establish `AUDIT-Z` or `THEOREM-Z`, or
authorize validation, release, checklist promotion, or master acceptance. Because the assigned
positive proof phase is not genuinely self-tested, `.stage1-worker-selftest.json` is deliberately
absent.
