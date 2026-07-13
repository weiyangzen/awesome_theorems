# THM-M-0276 validation-phase evidence

Item: `S56-M-0276-VALIDATION`. Base revision:
`dc600635160cace0916df5234bf8808c39dc656d`; base tree:
`8ee34b31ec38be1ef067aaab38c9a4cb4935b75a`.

## Validation scope

The structured node recipe copies and re-elaborates `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, and the new `Validation.lean` with `--trust=0` in a fresh
temporary module directory. Every Lean subprocess runs with the host filesystem read-only except
for that temporary directory and inside a Bubblewrap network namespace with outbound networking
unavailable. `Validation.lean` imports neither `Proof` nor `ObligationTree`; it separately
specializes the pinned Banach theorem to both exact scalar branches. This is same-worker
differential corroboration, not a distinct proof body or independent-runner attestation.

The validator binds the canonical expression and frozen denominator, proof receipt, exact mathlib
revision/tree/remote, clean dependency source, three terminal file/blob/body hashes, compiled
object, license, executable identities, and local prohibited-construct boundary. The replayed
selected declaration closure contains 17,187 declarations from 654 modules and reports exactly
`propext`, `Classical.choice`, and `Quot.sound`, with no bodyless nonaxiom or unsafe declaration.
The 12 proof declarations and four validation declarations are sorry-free and have exactly that
same axiom set.

## Commands and results

All commands ran from the isolated worker clone on 2026-07-13 (Asia/Shanghai). The pre-existing
canonical pinned `.lake` symlink was reused without mutation. No `lake update`, `lake build`, clone,
fetch, dependency mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0276
  exit 0: rank 1282, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0276/check_proof.sh
  exit 0: exact direct, frozen-composition, and expanded roots; 12 declarations sorry-free;
  every axiom report was exactly [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0276/check_validation.py
  exit 0: exact target, selected closure, frozen composition, proof roots, and differential root
  elaborated with trust=0 under network isolation; local trust/provenance/pin/hygiene checks passed;
  full release gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-0276/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0276/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0276-validation-pycache python3 -m py_compile \
  Stage1_Instances/THM-M-0276/check_validation.py
  exit 0: validator syntax compiled outside the repository tree

scoped prohibited Lean construct scan over Statement.lean, AnchorAudit.lean,
  ObligationTree.lean, Proof.lean, and Validation.lean
  exit 1 as expected: no prohibited construct matched comment-stripped source

git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json plus
  no-index checks for every new file
  exit 0/no diagnostics: tracked and untracked whitespace checks passed
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow exact-root kernel replay | pass | Copied statement, obligation, proof, and differential sources elaborate with `--trust=0`; direct, frozen-composition, expanded, and separately written roots agree. |
| Placeholder/unsafe/bodyless observation | pass for selected closure | Lean sorry checks pass, local scans are clean, and the replayed 17,187-declaration closure reports no bodyless nonaxiom or unsafe declaration. This is not a full executable TCB inventory. |
| Foundation observation | pass for selected declarations | Every checked proof and validation declaration reports exactly the selected classical trio. Full foundation/TCB acceptance remains downstream. |
| Selected provenance and pin checks | pass | Statement/registry/receipt hashes, clean mathlib revision/tree/remote, terminal source/blob/body/olean, license, and toolchain pins agree. Complete serialized transitive origin/import closure remains open. |
| Dependency legality | fail closed | `S56-M-0276-PROOF` is only provisional `[_]`; only the integration lane may accept it. The local task DAG also predates integrated proof evidence. |
| Internal composition credit | fail closed | The exact root checks, but 14 frozen source-body decomposition plans still lack abstract-child certificates and receive no individual obligation credit. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no independent clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, full TCB/SBOM archive, or second platform attestation. |
| Independent verification | fail closed | The differential wrapper ran in this worker clone and shared cache; there is no distinct verifier identity, independently provisioned runner, second signature, or independent release verifier. |

The authoritative accepted state remains `[H2, M3, R4]`, `root_closed=false`, with zero accepted
obligations. The local kernel replay supports only an unaccepted `M0-W` root candidate. The H2
source gap, H0/R0, accepted provenance/trust, cold hermetic reproduction, distinct-runner
verification, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance remain
open.

Snapshot-bound predecessor `check_proof.py` is not a current validation gate: it requires the
proof-phase base revision, pre-integration proof DAG state, and proof self-test packet. This phase
hash-binds its receipt and immutable inputs and directly replays all claimed Lean declarations
instead of weakening or rewriting that historical checker.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It truthfully records passed
narrow gates and failed release gates. It does not claim E0/E1, accepted M0, independent evidence,
theorem completion, release, or master acceptance.
