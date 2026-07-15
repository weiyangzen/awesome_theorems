# THM-M-1228 proof phase blocked at 6bf9ee93

Item: `S56-M-1228-PROOF`

Intent: `prove`

Recorded: `2026-07-16T04:51:20+08:00`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen target.
The lifecycle remains `planned`, the root remains `H1/M4/R4`, and the assigned
phase remains `[ ]`. This packet is blocker evidence, not a proof receipt.

The required v2 dependency inspection was completed first. The current node has
no direct hard parent, transitive hard ancestor, hard edge, reuse hint, or shared
group. `dependency-reuse-ledger.json` records that empty audited closure with
schema `stage1-dependency-reuse-ledger/1.1`, observed graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The graph still says `unknown_not_independent_proof_claim`; an empty closure is
not evidence that the mathematical proof is independent.

## First Failed Gate

`M1228-S-CONCRETE / exact-target executability` fails. The declaration is a
family

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

whose suitability, regularity, and parabolic-measure predicates have no laws.
Consequently a premise-free proof with an arbitrary `S : CKNSourceSemantics`
would prove the target for every permitted interpretation. The tracked,
placeholder-free `ProofBlocker.lean` selects one permitted interpretation with
suitability true and the required measure-zero predicate false. Pinned Lean,
with `--trust=0 -t0`, checks:

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Both declarations report only `[propext, Classical.choice, Quot.sound]`. This
refutes the arbitrary-semantics universal closure, not the genuine mathematical
Caffarelli-Kohn-Nirenberg theorem. Choosing a favorable semantics, adding the
per-solution conclusion as a premise or structure field, using ambient
Euclidean Hausdorff measure, or proving a smooth/two-dimensional substitute
would change the theorem and was not done.

The proof dependency is also only provisional:
`S56-M-1228-OBLIGATION_TREE` is `[_]`, not master-accepted `[x]`.
`ObligationTree.root_compose` merely consumes the full per-solution analytic
conclusion as a premise, uses a repeated harness rather than a checked canonical
transport, and supplies no analytic body. The frozen root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

Pinned mathlib contains adjacent distribution, smoothness, Lp, Sobolev, and
ambient Hausdorff infrastructure but no suitable weak Navier-Stokes semantics,
parabolic Hausdorff construction, epsilon-regularity theorem, bad-cylinder
covering estimate, or terminal CKN body. The historical `S1_M_156` surface
stores central analytic conclusions as package fields, and the four immutable
external candidates recorded by `anchor-audit.json` provide no exact compatible
body to import. No `Proof.lean` or proof/validation/release receipt exists in
the target's history.

There are already 47 JSON and 47 Markdown proof-recheck packets, nine dated
blocker JSON packets, seven dated blocker Markdown packets, and three proof
attempt notes before this run, while the authoritative DAG still records zero
proof attempts and no child items. This exceeds the five-attempt split rule.
The integration lane must reconcile these repeated packets and split the repair
instead of scheduling the unchanged monolithic task again.

## Validation

All commands ran inside the worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, ref mutation, or network action was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546; stdout SHA-256 `dff0a4526c29c09a62f68b396820b5dc51671c30953bc5be847c0aaa70089abd`. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, `planned`, theorem incomplete; stdout SHA-256 `c997b7b9974a1e73519399026f2a9fa542681b712da1cd64d4b962cb234e7bf5`. |
| Target-scoped `validate_dependency_reuse_ledger` call | 0 | Schema, current base, exact graph/context digests, and all empty closure lists passed; stdout SHA-256 `3342b42c5cc4bf0926ea9fb5cad143d237e37f6fbeb53a4d2b437f5d147ec9f3`. |
| `timeout --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | M4 boundary, nine Lean probes, mathlib pin, and four immutable tree receipts passed; stdout SHA-256 `5cffeb1aefcadc4aa98df7d5ff6012c68b433277bd0db7d9b9a06bfcfac4a23c`. |
| `timeout --kill-after=5s 300s python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains M4. |
| Isolated pinned `lake env` trust-zero replay | 0 | `Statement.lean`, `ProofBlocker.lean`, and `ObligationTree.lean` elaborated from copies under `/tmp`; blocker stdout SHA-256 `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`; all stderr streams were empty; temporary outputs were removed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Global pre-existing authority blocker: checked-in theorem DAG differs from fresh deterministic generation; stderr SHA-256 `121c7ee0d7877e37eae12cb1569afcc0b528541d9cdf369ef451520adab94f86`. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Propagated the same v2-DAG drift; stderr SHA-256 `71e4d006ad4863c0976423b13fad5d9acd0999d34c650c8273b2bfc8e2aef176`. |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 1 | Propagated the same v2-DAG drift; stderr SHA-256 `8175ee64e7fb432cd8477485262da6da80bb3a7c6b7aebbe4d338fb7622cf6b1`. |

The current statement checker was deliberately not credited: concurrent Lean
load caused repeated long-running checks, and its known implementation already
reports `MutationChangedSpatialDimension` as killed without elaborating it.
Those checker processes and their target-local temporary files were terminated
and removed. The independent isolated replay above is the relevant kernel
evidence.

## Retry Condition

The master must first reconcile the repeated evidence and the global v2-DAG
drift. Then reopen and version the statement around fixed, source-faithful
definitions of suitable weak solutions, regular points, and one-dimensional
parabolic Hausdorff measure; freeze a corrected registry and node-specific
validation recipes; and split statement repair from the concrete-semantics,
epsilon-regularity, covering, and measure obligations. Each child then needs a
placeholder-free local body or immutable exact import, checked transports,
composition, trust, and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
