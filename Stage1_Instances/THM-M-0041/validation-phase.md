# THM-M-0041 validation-phase result

Item: `S56-M-0041-VALIDATION`. Base revision:
`ebd5f75831296a8a35e7b33013b964f2baf31bb9`; base tree:
`d1e4bc83c803eefcd9898aac57352265a29f0658`.

## Validation scope

The phase recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the new
`Validation.lean` in a fresh temporary module directory. `Validation.lean` imports neither `Proof`
nor `ObligationTree`; it separately writes the exact-type wrapper from the frozen Cayley-Hamilton
target to pinned `Matrix.aeval_self_charpoly`. This is differential same-worker corroboration, not
an independent proof body or independent-runner attestation.

The validator binds the canonical expression and registry denominator, proof receipt, exact mathlib
revision/tree/remote, clean dependency source, terminal file/blob/body/compiled-object hashes,
license, executable identities, reported axioms, and local prohibited-construct boundary. The
terminal, local expanded and pinned proof routes, frozen composition, and differential wrapper
report exactly `propext`, `Classical.choice`, and `Quot.sound`; the differential declarations are
also checked with Lean's `assert_no_sorry`.

## Commands and results

All commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). The pre-existing canonical
pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, dependency
mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0041
  exit 0: rank 1081, planned L0/rework-required target; theorem_complete=false

(cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0041/check_proof.sh)
  exit 0: all eight local proof declarations and the terminal body elaborated and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 -B Stage1_Instances/THM-M-0041/check_validation.py
  exit 0: exact target, frozen composition, expanded and pinned proof roots, and differential root
  elaborated; local trust/provenance/pin/hygiene checks passed; release gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-0041/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0041/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0041/check_validation.py
  exit 0: validator syntax checked without writing into the owned path

rg -n -i --glob '*.lean' '<prohibited proof and oracle markers>' \
  Stage1_Instances/THM-M-0041/{Statement,AnchorAudit,ObligationTree,Proof,Validation}.lean
  exit 1 with empty output: expected no-match result

git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json
  exit 0: no tracked whitespace diagnostics; the validator also checked newline, CR/NUL, and
  trailing-whitespace invariants on every untracked handoff artifact
```

## Fail-closed gates

This run is warm, dirty, same-worker evidence. It did not create a new clean checkout, empty caches,
a kernel-enforced network-isolated cold build, an offline restoration archive, a complete
transitive declaration and TCB closure, a complete SBOM, or a second-platform attestation. The
separate differential wrapper used the same clone and dependency cache; there is no distinct
verifier identity, independently provisioned runner, second signature, or independently implemented
release verifier.

The proof prerequisite remains provisional `[_]`. The authoritative structured state therefore
remains `[H1, M3, R3]`, `root_closed=false`, with no accepted proof obligation, even though the
local kernel replay supports an `M0-W` proposal. H0, R0, full provenance/trust, hermetic release,
independent verification, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance
remain open.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It truthfully records passed
narrow gates and failed release gates. It does not claim E0/E1, accepted M0, independent evidence,
theorem completion, release, or master acceptance.
