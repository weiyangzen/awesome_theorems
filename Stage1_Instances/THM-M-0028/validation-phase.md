# THM-M-0028 validation-phase evidence

Item: `S56-M-0028-VALIDATION`. Base revision:
`a16267e7165144d202080fb647261658fa75ceb2`; base tree:
`6edd90c440309a0c5ba277ef62d1733b4b9c05b1`.

## Validation scope

The phase recipe re-elaborates `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and the new
`Validation.lean` in a fresh temporary module directory. `Validation.lean` imports neither `Proof`
nor `ObligationTree`; it separately writes the exact wrapper from the frozen ascending-chain target
through `isNoetherianRing_iff_ideal_fg` and `monotone_stabilizes_iff_noetherian`. This provides
differential same-worker corroboration, not an independent proof body or independent-runner
attestation.

The validator binds the canonical expression and registry denominator, proof receipt, exact
mathlib revision/tree/remote, clean dependency source, terminal file/blob/body/compiled-object
hashes, license, executable identities, reported axioms, and local prohibited-construct boundary.
The two terminals, local proof wrappers, frozen composition, and differential wrapper are
sorry-free. The finite-generation terminal and bridge report `propext` and `Quot.sound`; the chain
terminal and exact root declarations additionally report `Classical.choice`.

## Commands and results

All commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). The pre-existing canonical
pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`, clone, fetch, dependency
mutation, or network operation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0028
  exit 0: rank 1073, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-0028/check_proof.sh
  exit 0: both terminals and four exact proof declarations are sorry-free; exact reported axiom
  sets matched the finite-generation and chain/root profiles

python3 -B Stage1_Instances/THM-M-0028/check_validation.py
  exit 0: exact target, frozen composition, proof roots, and differential root elaborate; local
  trust/provenance/pin/hygiene checks pass; release gates fail closed as recorded

python3 -m json.tool Stage1_Instances/THM-M-0028/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0028/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics

for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0028/Validation.lean \
  Stage1_Instances/THM-M-0028/check_validation.py \
  Stage1_Instances/THM-M-0028/validation-phase.md \
  Stage1_Instances/THM-M-0028/validation-receipt.json \
  Stage1_Instances/THM-M-0028/validation-spec.json; do
  git diff --no-index --check /dev/null "$f" >/tmp/m0028-diffcheck 2>&1
  rc=$?
  if test $rc -ne 1 || test -s /tmp/m0028-diffcheck; then
    cat /tmp/m0028-diffcheck
    exit 1
  fi
done
  exit 1 for each because each file is untracked, with no whitespace diagnostics; the expected
  no-index diff status was checked explicitly
```

## Fail-closed gates

This run is warm, dirty, same-worker evidence. It did not create a new clean checkout, empty caches,
a network-isolated cold build, an offline restoration archive, a full transitive declaration and
TCB closure, a complete SBOM, or a second-platform attestation. The separate differential wrapper
used the same clone and dependency cache; there is no distinct verifier identity, independently
provisioned runner, second signature, or independently implemented release verifier.

The proof prerequisite is still only provisional `[_]`. Consequently the authoritative structured
state remains `[H1, M3, R3]`, `root_closed=false`, with no accepted proof obligation, even though the
local kernel replay supports an `M0-W` candidate. H0, R0, full provenance/trust, hermetic release,
independent verification, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance
remain open.

## Status boundary

This is a self-tested validation-node handoff for master inspection. It truthfully records passed
narrow gates and failed release gates. It does not claim E0/E1, accepted M0, independent evidence,
theorem completion, release, or master acceptance.
