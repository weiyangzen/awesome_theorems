# THM-M-0043 validation-phase evidence

Item: `S56-M-0043-VALIDATION`. Base revision:
`9a1ce196889e32911beeeffa685084b48a969866`; base tree:
`00d5c1749015f44fb0c5694181253c3a08db5d47`.

## Validation scope

The phase recipe copies `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the new
`Validation.lean` into a fresh system temporary directory. It invokes the pinned Lean executable
directly with trust level zero, fixed locale and timezone, and temporary local `.olean` outputs.
The exact proof, frozen composition, and duplicate-route exact target all elaborate. Five proof and
differential declarations are sorry-free. Those five plus the composition certificate report
exactly `propext`, `Classical.choice`, and `Quot.sound`.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. Its commuting-Hermitian core
deliberately duplicates the local proof route, while the exact root composition is independently
inlined rather than consumed from `ObligationTree`. This is a same-worker differential composer
check, not implementation-diverse or rev-5.6 independent verification: it ran in the same clone
against the same shared dependency cache.

The validator binds the exact expression and frozen denominator, all local proof inputs, the proof
receipt, selected principal mathlib source/blob/compiled-object hashes, dependency revision/tree/
remote/cleanliness, license, toolchain and executable identities, and the local prohibited-source
boundary. It deliberately does not claim complete transitive provenance or TCB closure.

The proof receipt lists 23 closed proof-route IDs, but its three structured composition
certificates map only 22. `M0043-T-OPERATOR-DECOMP` is absent from every certificate, so this
validation explicitly excludes it from the locally validated set and records the missing mapping
as a fail-closed proof-evidence gap.

## Commands and results

Commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided canonical
pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, dependency
mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0043
  exit 0: rank 1083, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0043/check_proof.sh
  exit 0: exact proof route elaborated in an isolated temporary module directory; all three proof
  declarations were sorry-free and reported exactly propext, Classical.choice, and Quot.sound

python3 -B Stage1_Instances/THM-M-0043/check_validation.py
  exit 0: exact proof, composition, and differential root replayed at Lean trust level zero; local
  trust, selected provenance, pin, receipt, graph-boundary, hygiene, and worker-packet checks passed;
  the unmapped M0043-T-OPERATOR-DECOMP receipt claim was excluded fail-closed

python3 -m json.tool Stage1_Instances/THM-M-0043/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0043/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0043-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0043/check_validation.py
  exit 0: validator compiled outside the repository tree

rg -n -i --glob '*.lean' \
  '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' \
  Stage1_Instances/THM-M-0043/{Statement,AnchorAudit,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass with one evidence gap | Exact proof, frozen composition, and duplicate exact target elaborate at Lean trust level zero; 22 mapped proof IDs validate, while `M0043-T-OPERATOR-DECOMP` lacks a receipt certificate. |
| Placeholder/unsafe/oracle scan | pass | Five owned Lean modules contain none of the prohibited declarations or proof escapes. |
| Trust observation | provisional pass | Six declarations report exactly the three recorded Lean/mathlib axioms; complete release TCB closure is absent. |
| Local and selected dependency provenance | pass | Frozen hashes, proof receipt, clean dependency pin, four principal source/object pairs, license, toolchain, and executables agree. |
| Structured root state | fail closed / stale | The graph remains `M3`, `root_closed=false`, with no accepted proof state; only the master may reconcile it. |
| Proof prerequisite | fail closed / provisional | `S56-M-0043-PROOF` is only `[_]`, not master-accepted. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean empty-cache network-isolated cold build, offline restoration, full TCB, or SBOM/license archive. |
| Independent verification | fail closed | The duplicate route only varies the final composer and ran without a distinct identity, independently provisioned runner, second signature, or independent receipt/graph verifier. |

## Status boundary

This is genuinely self-tested validation-node evidence for integration-lane inspection. It grants
no `E0/E1`, accepted `M0-L`, `AUDIT-Z`, `THEOREM-Z`, release, theorem-completion, or master-acceptance
credit. `audit_complete=false` and `theorem_complete=false`.
