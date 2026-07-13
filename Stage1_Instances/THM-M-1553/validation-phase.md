# THM-M-1553 validation-phase result

Item: `S56-M-1553-VALIDATION`
Base revision: `f78ecdb166de720e4af8d8859826b4a22a4c1733`

The proof-phase root and a separately written exact-root reconstruction both
elaborate. `Validation.lean` imports `ProofLemmas`, but imports neither `Proof`
nor `ObligationTree` and does not invoke any proof-phase declaration. This is
useful same-worker differential evidence, not rev-5.6 independent verification:
the reconstruction shares the decisive lower-level lemmas, worker identity,
checkout, kernel, and dependency cache.

## Exact validation

Run from the repository root on 2026-07-14 (Asia/Shanghai). The structured
validator invokes narrow `lake env lean` checks through the pinned executable,
writes all target-local compiled outputs to a fresh temporary directory, and
removes it. Every Lean process runs under Bubblewrap with the root mounted
read-only, network unshared, `--trust=0`, fixed locale/timezone, and one Lean
thread. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was run.

```text
python3 -B Stage1_Instances/THM-M-1553/check_validation.py
  exit 0
  PASS THM-M-1553 narrow validation
  PASS network-isolated kernel replay: exact statement, frozen composition,
    proof root, and differential root elaborated
  PASS trust observation: proof and validation declarations are sorry-free and
    report exactly propext, Classical.choice, and Quot.sound
  PASS selected provenance: frozen input hashes, local proof-body location,
    clean mathlib pin, and tool identities agree
  FAIL CLOSED authority: proof is worker-self-tested but not master-accepted;
    authoritative graph remains pre-proof M3
  FAIL CLOSED foundation/trust: accepted axiom policy and complete transitive
    declaration, compiled-artifact, and TCB closure remain open
  FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout
    empty-cache cold bootstrap, offline restoration, or a deterministic
    TCB/SBOM bundle
  FAIL CLOSED independent release: differential proof used this worker, shared
    lemmas, checkout, kernel, and cache, not a distinct signed verifier
  audit_complete=false; theorem_complete=false

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1553
  exit 0: rank 212, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1553/check_obligation_tree.py
  exit 0: 14 obligations and 33 typed edges passed; frozen root remains open M3
python3 Stage1_Instances/THM-M-1553/check_anchor_audit.py
  exit 0: structured candidate inventory and Lean probes passed
python3 -m json.tool Stage1_Instances/THM-M-1553/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1553/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all JSON documents parsed
PYTHONPYCACHEPREFIX=/tmp/stage1-m1553-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1553/check_validation.py
  exit 0: checker syntax compiled outside the repository
git diff --check -- Stage1_Instances/THM-M-1553 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact expression digest, three structural mutations, frozen composition, proof root, and differential root were checked with Lean 4.29.0. |
| Placeholder/unsafe scan | pass | Five Lean modules contain no proof placeholder, local axiom, unsafe declaration, native oracle, or external injection token; elaborator checks report five declarations sorry-free. |
| Trust observation | provisional pass | Six declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`; no accepted theorem-specific axiom/TCB profile or complete closure exists. |
| Selected local provenance | pass | Bound local source hashes, local root body, proof receipt, toolchain/manifest, clean pinned mathlib revision/tree/remote, and executable hashes agree. Complete transitive provenance remains open. |
| Proof dependency | fail closed | `S56-M-1553-PROOF` is `[_]`, not master-accepted `[x]`; validation can only be proposed `[_]`. |
| Structured root state | fail closed / stale | The frozen pre-proof graph remains `root_closed=false`, `M3`, with cut set `M1553-B-POLYNOMIAL`, `M1553-T-ZERO`; only the master may reconcile it. |
| Hermetic release replay | fail closed | Shared warm canonical `.lake`; no new clean checkout, empty-cache cold bootstrap, content-addressed offline restoration, complete TCB/SBOM/license archive, or deterministic release bundle. |
| Independent verification | fail closed | Separate exact-root source, but same identity, shared decisive lemmas, clone, kernel, and cache; no distinct signed independently provisioned runner or independent minimal release verifier. |

Primary-source `H0`, independently reviewed `R0`, `AUDIT-Z`, `THEOREM-Z`,
release, and theorem completion remain false. The first node gate is
`dependency.S56-M-1553-PROOF.master_acceptance`; the first release gate is
`S56-10.6-HERMETIC-COLD-BUILD`.
