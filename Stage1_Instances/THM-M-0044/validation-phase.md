# THM-M-0044 validation-phase result

Item: `S56-M-0044-VALIDATION`
Base revision: `9a1ce196889e32911beeeffa685084b48a969866`

The exact Real-and-Complex rectangular SVD proof, the frozen conjunction composition, and a
separately written exact-root reconstruction all elaborate against the pinned environment. The
differential module imports neither `Proof` nor `ObligationTree` and reconstructs the Gram spectral,
basis-extension, unitary-factor, and conjugate-transpose argument directly. This is useful local
corroboration, but it is not rev-5.6 independent verification because both proofs ran in this worker
against the same warm dependency cache.

## Exact validation

The validator invokes the pinned Lean executable obtained with `lake env`, creates only temporary
statement and obligation `.olean` files under `/tmp`, uses a minimal fixed environment, and removes
the temporary directory. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation
is performed.

```text
python3 -B Stage1_Instances/THM-M-0044/check_validation.py
  exit 0
  PASS THM-M-0044 narrow validation
  PASS kernel replay: exact proof, frozen composition, and differential exact root elaborated
  PASS trust observation: checked declarations report only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen hashes, direct source/olean boundary, clean mathlib pin, remote, and license agree
  PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed
  FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R3
  FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive
  FAIL CLOSED independent release: differential proof used this worker/shared cache, not a distinct signed runner
  audit_complete=false; theorem_complete=false

python3 Docs/tools/check_stage1_standard.py
  exit 0: all 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets in ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0044
  exit 0: rank 1084, planned, theorem_complete false
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The exact proof, frozen composition, and separate exact-root proof elaborate with pinned Lean 4.29.0 and mathlib `8a178386`. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry` checks the differential root transitively; supplemental comment-stripped scans find no placeholder, local axiom/bodyless declaration, unsafe/native/oracle, or external implementation construct in the five checked modules. |
| Trust observation | provisional pass | The root, four proof construction declarations, frozen composition, and differential root report exactly `propext`, `Classical.choice`, and `Quot.sound`. A theorem-specific accepted foundation/TCB policy and full transitive closure are absent. |
| Direct provenance | provisional pass | Frozen hashes, the local terminal proof, nine direct mathlib source/olean pairs, clean immutable mathlib revision/tree, canonical remote, tool hashes, manifest, and license agree. This is not a complete transitive TCB/SBOM inventory. |
| Structured authority | fail closed | The proof prerequisite is only `[_]`; the authoritative instance and graph remain H1/M3/R3, `root_closed=false`, with no accepted receipt or obligation closure. The proof receipt maps 30 obligations and omits three planned machine obligations from its closed/open partition, so only the master may reconcile per-node credit. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, cold empty-cache offline restoration, enforced network namespace, complete executable/bootstrap inventory, or deterministic SBOM archive. |
| Independent verification | fail closed | Separate proof implementation, but no distinct identity, independently provisioned runner/cache, second signed attestation, or independently implemented minimal receipt/graph verifier. |

This is genuinely self-tested validation-node evidence and records every available gate outcome. It
grants no release-grade `E0/E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion
credit. `audit_complete=false` and `theorem_complete=false` remain explicit.
