# THM-M-1522 validation-phase evidence

Item: `S56-M-1522-VALIDATION`. Base revision:
`0afbf514f9bd5f339943542106f6b811869fe572`; base tree:
`adbd9c80e360931a3e7c51cae73dda809b5bed65`.

## Validation scope

The node recipe re-elaborates the exact statement, complete vendored maximal and
pointwise Birkhoff modules, frozen conditional composition, both proof roots,
and a new exact-root adapter in fresh temporary output space. Every Lean
subprocess runs at trust level zero in a Bubblewrap network namespace with a
read-only host root. `Validation.lean` imports neither `Proof` nor
`ObligationTree`; it reconstructs the target directly from the vendored
`ErgodicTheory.tendsto_birkhoffAverage_ae_integral` terminal. This is a
same-worker differential check, not a distinct-runner attestation.

The checked proof and differential declarations are sorry-free and report
exactly `propext`, `Classical.choice`, and `Quot.sound`. The validator also
binds the canonical expression, obligation denominator, source and proof
receipt hashes, reconstructed upstream source identities, target and mathlib
licenses, selected pinned mathlib source blobs, clean dependency revision/tree,
and executable identities. No prohibited placeholder, bodyless declaration,
unsafe/native/oracle, or external implementation construct was found in the
six target Lean sources after comment removal.

## Commands and results

Commands ran from this worker clone on 2026-07-14 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, clone, fetch, checkout, dependency mutation, or
network request ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1522
  exit 0: rank 190, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-1522/check_validation.sh
  exit 0: network-isolated trust-level-zero replay elaborated Statement,
  MaximalErgodic, Birkhoff, ObligationTree, Proof, and the Proof-free
  differential Validation module; all requested sorry and axiom reports passed

python3 -B Stage1_Instances/THM-M-1522/check_validation.py
  exit 0: target/composition replay, hygiene, selected trust/provenance, frozen
  hashes, pin, receipt, recipe, and worker packet passed; authority and release
  gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-1522/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1522/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1522-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1522/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-1522 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; an explicit trailing-whitespace scan of
  the seven untracked owned artifacts also found no matches
```

Snapshot-bound predecessor Python checkers are intentionally not reused as
current validation recipes: `check_proof.py` expects its proof-worker base and
self-test packet. This phase binds its immutable proof artifacts by hash,
reconstructs the vendored upstream byte identities, and replays the Lean proof
directly instead of misreporting snapshot drift as a proof failure.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | Exact statement, vendored terminals, frozen composition, package proofs, both root adapters, and differential exact root elaborate under trust level zero and network isolation. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no placeholder, bodyless, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations report exactly the observed `propext`, `Classical.choice`, and `Quot.sound` set; no accepted theorem-specific foundation profile or complete transitive TCB closure exists. |
| Selected provenance | provisional pass | Local hashes, reversible two-edit upstream reconstruction, pinned source blobs, clean mathlib revision/tree, remotes, licenses, manifest, and tool hashes agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-1522-PROOF` is only `[_]`; the authoritative graph remains `M3` with pre-proof cut set `M1522-L-POINTWISE`, `M1522-T-IDENTIFY`. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The separate adapter shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, second attestation, or independent minimal release verifier exists. |

The first failed node gate is
`dependency.S56-M-1522-PROOF.master_acceptance`; the first failed release gate
is `S56-10.6-HERMETIC-COLD-BUILD`. Accepted debt remains `[H1, M3, R3]`.
Primary-source H0, independently reviewed R0, full trust/provenance,
`AUDIT-Z`, `THEOREM-Z`, release, and theorem completion remain false. This
self-tested worker evidence claims no `E0/E1`, accepted `M0-P`, independent
validation, release, or master acceptance.
