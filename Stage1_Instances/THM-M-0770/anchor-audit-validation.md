# THM-M-0770 anchor-audit validation

Date: 2026-07-12  
Item: `S56-M-0770-ANCHOR_AUDIT`  
Base revision: `1c79616e19a84057db087026c82a5015599a2b18`

The audit searched the local target, the pinned mathlib checkout, and external
Lean repositories returned by GitHub's repository search. The exact candidate
is mathlib's `zorn_le_nonempty` at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `AnchorAudit.lean` specializes its
`Preorder` parameter to the canonical `PartialOrder` and checks the exact
nonempty-chain premise and `IsMax` conclusion. No dependency was fetched or
changed.

## Validation

From the repository root:

```text
$ python3 Stage1_Instances/THM-M-0770/check_anchor_audit.py
exit 0
{"axioms": ["propext", "Classical.choice", "Quot.sound"], "exact_wrapper": "Stage1Instances.THM_M_0770.AnchorAudit.canonical_of_pinned_mathlib", "item_id": "S56-M-0770-ANCHOR_AUDIT", "lean_exit_code": 0, "mathlib_revision": "8a178386ffc0f5fef0b77738bb5449d50efeea95", "mathlib_zorn_source_sha256": "706b55e103d64d65f1bb9668e3b0f821483c0536d6e87875a2717771410de14c"}

$ git diff --check -- Stage1_Instances/THM-M-0770
exit 0, no output
```

The validator also confirms that `lake-manifest.json` and the actual shared
mathlib checkout have the audited revision, hashes `Mathlib/Order/Zorn.lean`,
and invokes `lake env lean` on the narrow audit module. Lean reports only
`propext`, `Classical.choice`, and `Quot.sound` for both the upstream theorem
and wrapper; it does not report `sorryAx`.

## Boundary

`M0-L_candidate_pending_downstream_acceptance` is an anchor-audit result, not
accepted proof or theorem completion. Obligation-tree, proof, full validation,
human-source, readability, reproducibility, independent-runner, and release
gates remain outside this node.
