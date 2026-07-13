# THM-M-0045 validation-phase result

Item: `S56-M-0045-VALIDATION`

Base revision: `eb9c2192f79a480deff66d2c0f8e31032bcc2d9f`

The exact Schur proof, frozen equation-package composition, and a separately written exact-root
adapter elaborate against pinned Lean 4.29.0 and mathlib `8a178386`. The adapter imports neither
`Proof` nor `ObligationTree`, but it reuses the same `SchurPort` terminal body. It is useful local
corroboration, not an independent proof implementation or distinct-runner verification.

## Exact validation

The validator obtains the pinned executable through `lake env`, copies five owned Lean modules into
a temporary directory, writes only temporary `.olean` files there, uses a minimal fixed environment,
and removes the directory. The automation-provided `.lake` symlink is reused read-only. No Lake
update/build, dependency clone/fetch, checkout, or `.lake` mutation is performed.

```text
python3 -B Stage1_Instances/THM-M-0045/check_validation.py
  exit 0
  PASS THM-M-0045 narrow validation
  PASS kernel replay: exact proof, frozen composition, and alternate exact-root adapter elaborated
  PASS trust observation: checked declarations report only propext, Classical.choice, and Quot.sound
  PASS local provenance: frozen hashes, direct source/olean boundary, historical lineage, clean pin, remote, and license agree
  PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed
  FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R4
  FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive
  FAIL CLOSED independent release: alternate adapter shares the proof body, worker, and cache; no distinct signed runner
  audit_complete=false; theorem_complete=false

bash Stage1_Instances/THM-M-0045/check_proof.sh
  exit 0: both exact proof declarations were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets in ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0045
  exit 0: rank 1085, planned, L0/rework_required, theorem_complete false
```

The frozen `validation-specs.json` recipe is not reported as a current pass. It was frozen during
the obligation-tree phase, invokes `check_obligation_tree.py`, pins an earlier base revision, and
expects the deliberately root-open pre-proof graph. It is stale for proof validation. The new
node-specific `validation-spec.json` makes this boundary explicit rather than changing the frozen
architecture or pretending that an obsolete recipe passed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, frozen composition, port, proof wrappers, and alternate exact-root adapter elaborate in a fresh temporary module directory. |
| Placeholder and unsafe boundary | pass | `assert_no_sorry` checks the terminal and alternate root transitively; supplemental comment-stripped scans find no placeholder, bodyless axiom/constant, unsafe/native/oracle, or external implementation construct in the five modules. |
| Trust observation | provisional pass | The composition declarations, two proof declarations, terminal theorem, and alternate adapter report exactly `propext`, `Classical.choice`, and `Quot.sound`; accepted theorem-specific foundation policy and full transitive closure remain absent. |
| Direct provenance | provisional pass | Frozen owned hashes, local port and proof, historical source lineage, six direct source/olean pairs, immutable clean mathlib revision/tree, canonical remote, tool hashes, manifest, and license agree. This is not complete transitive declaration/TCB/SBOM provenance or a full semantic port-delta proof. |
| Structured authority | fail closed | The proof prerequisite is only `[_]`; the authoritative instance and graph remain H1/M3/R4 with `root_closed=false`, no accepted receipt, and no accepted closed obligation. |
| Frozen recipe freshness | fail closed | `validation-specs.json` describes the earlier root-open obligation-tree snapshot and pins its historical base; only the new validation-node recipe applies to this snapshot. |
| Hermetic release replay | fail closed | Shared warm `.lake`; no clean checkout, cold empty-cache offline restoration, enforced network namespace, complete bootstrap/TCB inventory, or deterministic restorable SBOM archive. |
| Independent verification | fail closed | The alternate adapter is separately written but shares the terminal proof body, worker identity, checkout, and cache; no distinct signed verifier or independently implemented minimal checker exists. |

This is genuinely self-tested validation-node evidence and records every available gate outcome. It
grants no accepted `M0-L`, release-grade `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-
completion credit. `audit_complete=false` and `theorem_complete=false` remain explicit.
