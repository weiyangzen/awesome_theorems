# THM-M-0476 obligation-tree validation

Item: `S56-M-0476-OBLIGATION_TREE`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen Result

Registry version 1 freezes 26 unique semantic obligations before proof-phase installation. The
canonical ten-field projection has SHA-256
`9375f9b987132465572c04a019d70b32638823c1279dd91a7935007f108fe62b`. The registry content
SHA-256 is `032993303cc2c963a4b3256c95a03989cf24cd0462baed03cbfe16055c58fbbf`. The bundle contains
114 typed edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. The proof relation has reciprocal requirement/composition edges; imported-body
expansions are also non-crediting provenance relations. Every semantic ledger contains stable,
premise-specific steps; every budget is a split threshold rather than an R0 claim. The static task
contract projection excludes mutable cursor state and hashes to
`56954b5bd91ba62533ce09b1cf1194a13b342c07b3ed5fd8ebc500aa324c3f6b`.

The `L-WILSON` and `L-UNITS-PRODUCT` certificates are same-typed local expansion interfaces. They
do not invoke or certify identity with the two pinned candidate bodies; proof-phase admission and
terminal dependency inspection remain open.

Validation uses only the existing manifest-pinned Lake artifacts. It performs no `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation. The exact commands and outcomes are
are recorded below.

## Commands And Results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0; PASS, 1546 targets and 10822 typed DAG items

python3 scripts/stage1_target.py check
  exit 0; target manifest/order and generated projection agree

python3 scripts/stage1_target.py show THM-M-0476
  exit 0; execution rank 1357, obligation-tree authoritative state [ ]

python3 -B Stage1_Instances/THM-M-0476/build_obligation_artifacts.py --check
  exit 0; deterministic 26-obligation, 114-edge artifacts

python3 -B Stage1_Instances/THM-M-0476/check_obligation_tree.py
  exit 0; structure, graph, receipt, source, and stored Lean evidence pass

lake env lean scoped Statement.lean and ObligationTree.lean elaboration
  both exit 0; ObligationTree stdout SHA-256 344e0d6a...ade4cc

JSON, Python, prohibited-marker, deterministic-regeneration, and whitespace checks
  exit 0; exact commands are listed in the provisional receipt and root self-test
```

The structural checker validates target and item identity, dependency state, immutable statement
and anchor hashes, registry content/denominator hashes, substantive ledger flow, all required node
fields, node/obligation bijection, graph-specific edge types, adjacency, endpoint policy, acyclicity,
reciprocal proof edges, root reachability, exact-child composition certificates, static task contract
and task-obligation links, recipe coverage, source pins and markers, open closure, receipt, owned
inventory, and worker handoff.

## Historical Validator Boundary

The earlier intake and statement checkers bind authoritative blueprint or execution-DAG hashes
that changed during integration. The anchor checker additionally binds its historical base commit
and its own phase-specific root handoff. Their receipts remain historical evidence; this successor
does not rewrite or misreport them as fresh. Instead it checks the unchanged exact statement,
expression fingerprint, anchor inventory, candidate identity, source hashes, toolchain, manifest,
and mathlib pin directly.

## Status Boundary

`ObligationTree.lean` validates only conditional child-to-parent composition. It never invokes
`ZMod.wilsons_lemma` to construct the root. Accepted closed obligations remain empty and the root
remains `[H1, M3, R4]`. H0, accepted M0, R0, full provenance/trust, hermetic replay, independent
verification, validation, AUDIT-Z, release, and theorem completion remain open. Master acceptance
is still required.
