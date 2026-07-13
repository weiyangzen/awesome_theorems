# THM-M-0079 proof-phase validation

Item: `S56-M-0079-PROOF`. Base revision
`2b649e7f3c2c6e3617cfb58c680e29f34d2ca5d7`, tree
`c9dfabc312a58c05c89917f6d7298a8e140356fc`.

## Implemented proof route

`Proof.lean` installs the pinned mathlib Nielsen-Schreier route at every explicit interface needed
by the frozen local composition harness. It supplies quotient pretransitivity and nonemptiness,
free-action-groupoid and connected-free-end packages, the stabilizer/end equivalence, the exact
quotient stabilizer identity, and freeness transport along a multiplicative equivalence. It then
uses all five checked composers in `ObligationTree.lean` to obtain quotient connectedness, the
end/subgroup equivalence, vertex-end freeness, exact assembly, and the unchanged canonical
`NielsenSchreierTarget`. A direct exact-root wrapper provides a second type check against
`subgroupIsFreeOfIsFree`; both roots are deduplicated to the same upstream body.

The terminal declaration is in
`Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean` lines 313-316 at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, source blob
`08cc647c220b852784860c281f06a6ede45bb06f`, file SHA-256
`e777c40c3902fd54747eac57d2952b985aff464e5d6bf803c5c78037e4c0c847`, and source-region
SHA-256 `1ab685e13340e3ee539c977dcd78b5f83b2cf8614feb23e5efef6b918cf6557d`.
Its body is `IsFreeGroup.ofMulEquiv (endMulEquivSubgroup H)`. The substantive route remains
upstream in pinned mathlib, so this phase proposes `M0-W`, not a repo-local `M0-L` reconstruction.

The receipt maps the pinned body to all 27 proof-reachable frozen IDs but deliberately awards no
individual obligation closure. Five abstract-child composition interfaces are checked locally;
nine deeper source-body decomposition certificates in `typed-graphs.json` remain
`planned_source_composition_pending_exact_child_harness`. Exact-root kernel closure and per-node
composition credit are therefore reported separately rather than conflated.

## Commands and results

Validation ran in the isolated worker clone on 2026-07-13 (`Asia/Shanghai`). The existing
automation-provided canonical `.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, network operation, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0079
  exit 0: rank 1105, planned, L0/rework_required, theorem_complete=false

bash Stage1_Instances/THM-M-0079/check_proof.sh
  exit 0: isolated temporary Statement.olean and ObligationTree.olean elaborated; the pinned
  terminal and all 13 local leaf, interface, composition, and root declarations were sorry-free;
  all 14 axiom reports were exactly [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0079/check_proof.py
  exit 0: exact source, frozen target/denominator and 30 proof edges, pin, terminal source body,
  composition, receipt, worker packet, and no-completion boundary passed

python3 -B Stage1_Instances/THM-M-0079/build_obligation_artifacts.py --check
  exit 1: the predecessor generator remains bound to the obligation-tree phase's authoritative
  execution-DAG hash, while integration has advanced that authority; no predecessor artifact was
  edited by this worker, and the proof checker binds their current hashes directly

python3 -B Stage1_Instances/THM-M-0079/check_obligation_tree.py
  exit 1: the predecessor checker requires its obligation-tree worker self-test changed-path list;
  this proof packet correctly replaces the root self-test, while the predecessor receipt remains
  immutable and truthfully retains its pre-proof M3 boundary

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-0079/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

python3 -m json.tool Stage1_Instances/THM-M-0079/proof-receipt.json /dev/null
  exit 0: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0079-proof-pycache python3 -m py_compile \
  Stage1_Instances/THM-M-0079/check_proof.py
  exit 0: checker compiled outside the repository

git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is narrow proof-phase evidence only and does not claim theorem completion. The accepted state
remains `[H1, M3, R4]` with empty accepted proof state until the integration lane acts.
`M0079-S-FOUNDATION`, primary-source `H0`, readable `R0`, complete transitive provenance and trust,
validation, hermetic replay, independent verification, release, `AUDIT-Z`, and `THEOREM-Z` remain
downstream. The node-specific provisional receipt is `proof-receipt.json`.
