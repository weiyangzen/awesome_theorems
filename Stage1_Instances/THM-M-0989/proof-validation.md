# THM-M-0989 proof-phase validation

Item: `S56-M-0989-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`. Intent: `prove`.

## Implemented proof

The exact frozen theorem now has a repo-local, placeholder-free body:

```text
Stage1Instances.THM_M_0989.lindebergFeller_exact :
  Stage1Instances.THM_M_0989.Statement
```

`Proof.lean` supplies row measurability, characteristic-function
factorization, normalization, and truncation support. `CharFunBound.lean`
supplies the complex-exponential estimates, `ProdExp.lean` supplies the
finite-product limit, and `LindebergArray.lean` proves infinitesimality, the
summed Lindeberg remainder bound, the row-law characteristic-function limit,
and the exact root through the frozen Levy composition.

The analytic route is a repo-local adaptation of `patrickrd/CLT-lindeberg` at
commit `82249ccfc05c0d97b86f33fce2582f0bf4ff9c06`, not an imported wrapper of
its different global-sequence theorem. Immutable upstream paths, hashes, tree,
and Apache-2.0 license hash are recorded in `proof-receipt.json`.

## Proof boundary

The proof worker proposes repo-local `M0-L` kernel closure for the exact root
and the frozen machine proof route. It does not claim master acceptance or
theorem completion. `M0989-S-FOUNDATION`, full provenance/trust, H0, R0,
validation, hermetic cold/offline replay, independent verification, release,
`AUDIT-Z`, and `THEOREM-Z` remain downstream gates. The frozen obligation
registry and denominator were not changed.

## Validation commands

Commands ran from the worker repository root and reused the canonical pinned
Lake artifacts without update, build, clone, fetch, or mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups; 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0989
  exit 0
  rank 269; planned; L0/rework_required; theorem_complete=false

python3 Stage1_Instances/THM-M-0989/check_obligation_tree.py
  exit 0
  15 frozen obligations, 32 typed edges, denominator
  c5d0b41c35c0759e11055611925021d6c2e38fc251da666e8f3afe238eccdc15
  The reported M3/open cut is the intentionally frozen pre-proof snapshot.

bash Stage1_Instances/THM-M-0989/check_proof.sh
  exit 0
  Isolated Statement, ObligationTree, Proof, ProdExp, CharFunBound, and
  LindebergArray elaboration with --trust=0; all 20 declaration-specific axiom
  reports are exactly [propext, Classical.choice, Quot.sound].

python3 -B Stage1_Instances/THM-M-0989/check_proof.py
  exit 0
  Source, receipt, provenance, registry denominator, hashes, pinned environment,
  changed paths, and worker self-test packet agree.

python3 -m json.tool Stage1_Instances/THM-M-0989/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each; both structured artifacts parse

rg -n --glob '*.lean' '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern)\b' \
  Stage1_Instances/THM-M-0989
  exit 1 (expected no-match result)

git diff --check -- Stage1_Instances/THM-M-0989 .stage1-worker-selftest.json
  exit 0; no whitespace diagnostics
```

The exact hashes and complete provisional declaration inventory are in
`proof-receipt.json`. This is a self-tested proof-phase proposal `[_]`, not an
accepted receipt or a theorem-completion verdict.
