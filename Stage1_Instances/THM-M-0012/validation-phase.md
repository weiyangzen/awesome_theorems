# THM-M-0012 validation-phase result

Item `S56-M-0012-VALIDATION` was run against the provisional proof-phase snapshot at base
`b09b188fbf6e0e288ddccb92314ef863d473ebad` (tree
`d64707bb77427b4e8569657bcd92a2c7f5713dc9`). Validation added no mathematical proof content.
It re-elaborated the existing exact proof and frozen analytic composition from copied sources in a
fresh temporary module directory, using only the existing pinned Lean artifacts.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborate; the direct, expanded, and pinned compositions close the exact frozen target. |
| Placeholder/unsafe/oracle hygiene | pass in inspected local and terminal source | No prohibited proof construct occurs in the three local modules or the pinned `Complex.exists_root` source body. This source scan is additional defense, not a complete transitive parser/elaborator audit. |
| Axiom observation | provisional pass | Every checked proof declaration reports exactly `propext`, `Classical.choice`, and `Quot.sound`; final foundation-profile approval remains open. |
| Local provenance | pass | Proof receipt hashes, terminal body identity, mathlib revision/tree/source hash, compiled artifact hash, remote, license, and clean dependency worktree agree. |
| Dependency legality and structured freshness | fail closed | The proof prerequisite is only `[_]`, not master accepted; the frozen typed graph still reports `root_closed=false`, `M3`, and no accepted obligations. |
| Complete transitive provenance and TCB | fail closed | No complete declaration/import closure hash, compiled-import inventory, compiler/bootstrap inventory, plugin/evaluator inventory, or complete trust-closure hash exists. |
| Hermetic release replay | fail closed | The worker reused the shared warm `.lake` symlink. It did not create a new checkout or empty cache, cold-build, restore offline, or produce an SBOM/archive/signed attestation. |
| Independent verification | fail closed | This is one worker and one shared cache. There is no distinct runner, verifier identity, signature, second attestation, or independently implemented release verifier. |

## Commands and results

All commands ran on 2026-07-13 (`Asia/Shanghai`). No `lake update`, `lake build`, dependency clone,
dependency fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups; 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0012
  exit 0: rank 1062, planned, theorem_complete false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0012/check_proof.sh
  exit 0: exact root, analytic engines, and composition declarations elaborated;
  all printed axiom sets were [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0012/check_proof.py
  exit 0: existing proof source, receipt, pin, source hash, and composition checks passed

python3 -B Stage1_Instances/THM-M-0012/check_obligation_tree.py
  exit 0: 20 obligations and 41 typed edges passed; authoritative root stayed open H1/M3/R4

python3 -B Stage1_Instances/THM-M-0012/check_validation.py
  exit 0: narrow kernel, trust observation, source/proof hash, pin, and fail-closed state gates passed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
  exit 0: revision 8a178386...ea95, tree bdc39a31...c2b

git -C Formalizations/Lean/.lake/packages/mathlib status --short
  exit 0: empty output; pinned dependency worktree clean
```

The first validation gate failure is `S56-M-0012-VALIDATION-PREREQUISITE-NOT-ACCEPTED`; the first
release gate failure is `S56-10.6-HERMETIC-COLD-BUILD`. The accepted debt vector remains
`H1/M3/R4`. This packet claims no `E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, theorem
completion, release, or master acceptance.
