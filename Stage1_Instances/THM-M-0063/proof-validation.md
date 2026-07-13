# THM-M-0063 proof-phase validation

Item: `S56-M-0063-PROOF`. Base revision:
`ee8c1843ef3ce74178a990f4e64554c1558c51fa`.

## Implemented proof route

`Proof.lean` realizes every mathematical node in the frozen Cayley proof graph. It constructs the
permutation homomorphism, derives injectivity from pointwise faithfulness, chooses a left inverse,
builds the equivalence to `MonoidHom.mrange`, uses the checked definitional transport to subgroup
range, specializes the generalized faithful-action package to the regular action, and composes the
result through `ObligationTree.root_of_exactAssembly` to the unchanged
`CayleyTheoremTarget`. It also installs a direct exact wrapper over the audited pinned declaration
`Equiv.Perm.subgroupOfMulAction`.

The direct and expanded routes deduplicate to the same pinned regular-action injectivity argument.
The terminal body remains in mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` and is not
vendored, so the direct route is a provisional `M0-W` candidate. `M0063-S-FOUNDATION` is a separate
required assurance certificate outside the mathematical proof graph and remains open for downstream
validation. The accepted vector therefore remains `[H1, M3, R4]`. This worker evidence does not claim theorem completion.

## Commands and exact results

Validation ran on 2026-07-13 (`Asia/Shanghai`). The automation-provided pinned `.lake` symlink was
reused read-only. No Lake update/build, dependency clone/fetch, checkout, or `.lake` mutation ran.

```text
bash Stage1_Instances/THM-M-0063/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof elaboration passed; all twelve material
  proof declarations were sorry-free and used only propext, Classical.choice, and Quot.sound

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0063
  exit 0: rank 1094, planned, L0/rework_required, theorem_complete=false

python3 -B Stage1_Instances/THM-M-0063/check_proof.py
  exit 0: exact source, target, graph, denominator, pin, receipt, worker packet, and status passed

python3 -B Stage1_Instances/THM-M-0063/check_obligation_tree.py
  exit 1: the predecessor receipt still binds the pre-integration authoritative DAG and blueprint
  hashes; the integration lane changed those master-owned files after the obligation-tree worker ran

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0063/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0063/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both files are valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0063-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0063/check_proof.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The proof node remains provisional until prerequisite and node-specific master acceptance.
Validation, trust/provenance closure, hermetic replay, independent verification, release,
`AUDIT-Z`, and `THEOREM-Z` remain downstream.
