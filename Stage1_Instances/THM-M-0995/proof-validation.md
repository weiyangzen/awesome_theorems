# THM-M-0995 proof-phase validation

Item: `S56-M-0995-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented proof

`Proof.lean` proves the exact frozen one-sided Bernstein inequality without placeholders. It proves
the scalar exponential-series bound, integrates it into the individual MGF estimate, factors the
finite independent-prefix MGF, applies the variance budget and Chernoff bound, verifies the
positive-variance optimizer, and closes the zero-variance case by proving the sum is almost
everywhere zero. The terminal declaration is
`Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2 : StatementShape`.

Proof execution exposed a genuine defect in frozen registry v1: its optimizer admitted `v = 0`
while requiring the strict domain `s*b < 3`. The theorem
`Proof.not_optimizeExponentPackage` refutes that interface at `v = 0`, `b = 1`, `t = 1`.
Registry v2 therefore preserves v1 history and publishes an append-only semantic delta: it retires
the false optimizer, adds positive-variance and zero-variance nodes, replaces the assembly node,
and checks every corrected child-to-parent composition. This is a proof-architecture correction,
not a statement substitution.

## Validation

Validation ran in the worker clone on 2026-07-14. It reused the canonical pinned Lake artifacts;
no update, build, fetch, clone, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0995/check_proof.sh
  exit 0
  Statement.lean, ObligationTree.lean, and Proof.lean elaborated using temporary oleans.
  The exact root and all registry-v2 composition declarations report only:
  [propext, Classical.choice, Quot.sound].

python3 Stage1_Instances/THM-M-0995/build_obligation_artifacts.py
  exit 0: wrote registry v2 with 21 obligations and 39 typed edges;
  retained registry-v1 denominator 40ec266a8614befd347bb0f00848703182aac04f6446a113a6a2e6b1a0348794;
  v2 denominator 29fa162b68c22ecc1c0b1edb83306a411eb8ddea7a4b546fbeb082270a425b18.

python3 Stage1_Instances/THM-M-0995/check_obligation_tree.py
  exit 0: append-only delta, hashes, denominators, IDs, typed edges, reciprocity,
  acyclicity, reachability, composition certificates, recipes, closure boundary,
  budgets, and source hygiene passed.
```

The remaining commands and exact outcomes are recorded in `proof-receipt.json`. This proof-phase
receipt proposes exact-root `M0-L` machine closure pending master acceptance. It does not claim H0,
R0, audit completion, hermetic validation, independent replay, release, or theorem completion.
