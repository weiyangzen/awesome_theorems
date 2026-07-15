# THM-M-1161 current-base proof recheck

Item: `S56-M-1161-PROOF`

Intent: `prove`

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

Recheck time: `2026-07-15T15:15:37+08:00`

## Verdict

`blocked`. The exact frozen formal target is false, so no placeholder-free positive proof can
truthfully inhabit it. The proof item remains `[ ]`; no positive proof receipt or root worker
self-test is emitted, and no audit, theorem, validation, release, or master acceptance is claimed.

`FredholmKernelModel.realize` is assumed injective but not complex-linear. Therefore
`operator_eq_integral` does not justify rewriting the pointwise equation as
`(ContinuousLinearMap.id Complex E - lambda • M.operator) phi = f`. The checked countermodel uses
`X = PUnit`, `E = Complex`, Dirac measure, constant kernel `1`, identity operator, and the injective
affine realization `realize z = z + 1`. At `lambda = 1`, `Solves phi f` holds exactly when
`f = -1`, independently of `phi`. Unique solvability fails for datum `-1`, while datum `0` has no
homogeneous solution, so both branches of the canonical target fail.

The exact canonical negation is checked by
`AwesomeTheorems.Stage1.THM_M_1161.not_canonical_target`; the separate declaration
`not_operator_normalization` refutes the frozen normalization itself. This evidence refutes only
the current overbroad Lean encoding, not the classical Fredholm alternative for genuine linear
function realizations.

## Current-base validation

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD && git rev-parse HEAD^{tree}` | 0 | base revision `350285c48208616b6e3ad74154d9183d16523cfa`; tree `c4edebc115ec954e4940ed5faaa3ffacd4e56091` |
| `git status --short` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before worker changes |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364; lifecycle planned; L0/rework-required; theorem incomplete |
| `jq '.items[] \| select(.id == "S56-M-1161-PROOF" or .id == "S56-M-1161-OBLIGATION_TREE")' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | proof item is `[ ]`; its obligation-tree dependency remains provisional `[_]` |
| `python3 Stage1_Instances/THM-M-1161/check_obligation_tree.py` | 0 | 19 obligations and 65 typed edges passed; denominator `8a07bd14994ae4988b608e465665fd5360bb659474ed5915bbef01b2ae60533a`; root remains open at M4 |
| root pinned `lake env lean --trust=0 -t0` recipe below | 0 | statement, countermodel, and canonical adapter elaborated; all printed counterexample axioms were `propext`, `Classical.choice`, and `Quot.sound` |
| scoped prohibited-construct scan below | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, declaration-level `axiom`/`unsafe`/`external`, placeholder, or fake result |
| `python3 -m json.tool` plus the `jq -e` blocker-invariant query on the JSON artifact | 0 | structured blocker parses and its item, base, verdict, completion, self-test, changed-path, and escalation invariants pass |
| new-file `git diff --no-index --check` wrappers plus `git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json` | 0 | each raw new-file check returned its expected difference exit 1 with empty diagnostics; the wrappers and complete scoped delta passed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no proof-completion manifest was emitted |

The exact structured-artifact checks were:

```bash
python3 -m json.tool \
  Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-350285c4-slot30.json \
  >/dev/null
jq -e \
  --arg head "$(git rev-parse HEAD)" \
  --arg tree "$(git rev-parse HEAD^{tree})" \
  '.item_id == "S56-M-1161-PROOF"
   and .theorem_id == "THM-M-1161"
   and .base_revision == $head
   and .base_tree == $tree
   and .verdict == "blocked"
   and .state == "[ ]"
   and (.positive_proof_body_added | not)
   and (.proof_phase_complete | not)
   and (.root_closed | not)
   and (.audit_complete | not)
   and (.theorem_complete | not)
   and (.selftest_manifest_written | not)
   and (.accepted_receipt_ids | length == 0)
   and (.changed_paths | length == 2)
   and .unresolved_tick_escalation.structured_blocker_records_including_this_one == 31
   and .unresolved_tick_escalation.limit == 5' \
  Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-350285c4-slot30.json \
  >/dev/null
set -euo pipefail
for f in \
  Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-350285c4-slot30.json \
  Stage1_Instances/THM-M-1161/proof-recheck-2026-07-15-head-350285c4-slot30.md
do
  set +e
  out=$(git diff --no-index --check /dev/null "$f" 2>&1)
  status=$?
  set -e
  test "$status" -eq 1
  test -z "$out"
done
git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json
```

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-1161
lean_root=$root/Formalizations/Lean
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
tmp=$(mktemp -d "$lean_root/.thm-m-1161-proof-350285c4-slot30.XXXXXX")
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
`1d6eb1c08fe405c7444bca9765452c4b58e2409103d1223e21540dc4a975cb58`.
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
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Escalation and retry condition

This is the thirty-first structured blocker artifact for the same invariant countermodel: one
original `proof-blocker` plus thirty `proof-recheck` artifacts, including this one. That exceeds
the five-unresolved-tick limit in section 10.2. This count is an artifact count, not an authoritative
scheduler-attempt count; the DAG still records `attempts: 0`, which only the master may reconcile.
Reassigning the unchanged proof node cannot make progress. The master must split or redirect the
workflow to a statement-repair or barrier/counterexample node.

Reopen the statement phase and require a complex-linear realization, or source-faithful laws that
imply the needed additive and scalar compatibility. Then accept a new statement fingerprint,
publish an append-only obligation-registry version delta, and rerun statement mutation, anchor
audit, obligation-tree construction, and proof execution. Assuming the normalization or either
root branch would be circular and is not a valid repair.

Assuming the normalization defect is repaired, substantial analytic obligations still remain:
bijectivity of `I - lambda T` under the trivial-kernel case, closed range,
range/adjoint-kernel orthogonality, and transport back to the pointwise equation. The pinned spectral
and adjoint declarations are supporting anchors, not exact proof bodies for those obligations. The
audited external candidate is self-adjoint-only and likewise cannot close the current general target.

The obligation-tree prerequisite remains provisional `[_]`, independently blocking a
dependency-ordered acceptance of this proof item.

## Status boundary

This is fresh current-base negative kernel evidence only. It does not complete
`S56-M-1161-PROOF`, change an authoritative debt vector, establish `AUDIT-Z` or `THEOREM-Z`, or
authorize validation, release, checklist promotion, or master acceptance. Because the assigned
positive proof phase is not genuinely self-tested, `.stage1-worker-selftest.json` is deliberately
absent.
