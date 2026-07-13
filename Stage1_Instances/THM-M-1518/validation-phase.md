# THM-M-1518 validation-phase evidence

Item: `S56-M-1518-VALIDATION`. Base revision:
`35d23d0193cd7c8fccb1d09f22534c6eba066b02`; base tree:
`4325d20b5ec8db888f28fcedc79cc1b7745c0c68`.

## Validation scope

The node recipe re-elaborates the exact statement, frozen composition, both
analytic proof packages, exact proof root, and a separately written exact-root
composition in fresh temporary output space. Every Lean subprocess runs at
trust level zero in a Bubblewrap network namespace with a read-only host root.
`Validation.lean` imports the two analytic packages but not `ExactProof`; it
recomposes them directly at the unchanged canonical target. This is a
same-worker differential composition, not an independent analytic proof or a
distinct-runner attestation.

The checked declarations are transitively sorry-free and report exactly
`propext`, `Classical.choice`, and `Quot.sound`. The validator also binds the
canonical expression and denominator, source and proof-receipt hashes, four
selected pinned mathlib source blobs and oleans, the clean dependency
revision/tree and license, and executable identities. This selected provenance
does not claim a complete transitive declaration, compiled-artifact, TCB, or
SBOM closure.

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

python3 scripts/stage1_target.py show THM-M-1518
  exit 0: rank 187, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-1518/check_validation.sh
  exit 0: network-isolated trust-level-zero replay elaborated Statement,
  ObligationTree, Proof, WeakToPointwise, ExactProof, and the separately
  composed Validation module; all requested sorry and axiom reports passed

python3 -B Stage1_Instances/THM-M-1518/check_validation.py
  exit 0: target/composition replay, hygiene, selected trust/provenance, frozen
  hashes, pin, receipt, recipe, and worker packet passed; authority and release
  gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-1518/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1518/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1518-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1518/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-1518 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; an explicit trailing-whitespace scan of
  the seven untracked validation artifacts also found no matches
```

One preliminary proof-validator invocation during inspection transiently
failed at Lean step 1 because its external `git` command exited 255; a complete
retry exited 0 and reported the same three allowed axioms. The validation
recipe above does not hide this attempt and validates the proof independently
of that snapshot-bound proof checker. During final verification, a concurrent
automation fetch also temporarily left the shared `flt-regular` checkout with
an invalid HEAD, causing one `lake env which lean` call to exit 1. Once the
canonical pinned artifact was restored, subsequent complete `lake env lean`
recipes exited 0. This shared-cache race is further evidence that the run is
not the cold isolated release replay required by section 10.6.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel and composition replay | provisional pass | Exact statement, frozen composition, analytic packages, exact root, and differential exact-root composition elaborate under trust level zero and network isolation. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no placeholder, bodyless declaration, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted theorem-specific foundation profile or complete transitive TCB closure exists. |
| Selected provenance | provisional pass | Local hashes, selected pinned mathlib source blobs/oleans, clean revision/tree, remote, license, manifest, and tool hashes agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-1518-PROOF` is only `[_]`; the authoritative graph remains `M4` with its pre-proof analytic cut set. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The separate composition shares this worker, checkout, kernel, and cache; no distinct identity, runner, signature, second attestation, independent analytic implementation, or independent minimal release verifier exists. |

The first failed node gate is
`dependency.S56-M-1518-PROOF.master_acceptance`; the first failed release gate
is `S56-10.6-HERMETIC-COLD-BUILD`. Accepted debt remains `[H2, M4, R3]`.
Primary-source H0, independently reviewed R0, full trust/provenance,
`AUDIT-Z`, `THEOREM-Z`, release, and theorem completion remain false. This
self-tested worker evidence claims no `E0/E1`, accepted `M0-L`, independent
validation, release, or master acceptance.
