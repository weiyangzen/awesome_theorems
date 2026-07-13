# THM-M-1138 proof-phase validation

Item: `S56-M-1138-PROOF`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`.

## Implemented proof

`Proof.lean` proves the exact terminal `BoundaryMaximumPackage` and the exact public
`HarmonicWeakMaximumPrinciple`. For a positive `epsilon`, it perturbs the harmonic function by
`epsilon * ||x||^2`. The proof derives that every twice differentiable real function has
nonpositive Laplacian at a local maximum, computes
`Laplacian (fun x => ||x||^2) = 2 * finrank`, and therefore excludes an interior maximum of the
perturbation. Compactness places a perturbed maximizer on the frontier. A frontier maximizer of
the unperturbed function and an `epsilon -> 0` estimate then give the required inequality on the
whole closure.

The connectedness hypothesis is consumed at the exact package boundary but is mathematically
unneeded by this stronger perturbation argument. The implementation changes neither the target nor
its hypotheses.

The two exact terminal declarations are sorry-free. Lean reports their axiom closures as exactly
`propext`, `Classical.choice`, and `Quot.sound`.

## Frozen-route boundary

Registry version 1 described a strong-maximum/local-constancy route. This proof instead establishes
the same frozen terminal package through a strict-subharmonic perturbation. It does not pretend to
separately implement `M1138-L-INTERIOR-LOCAL`, `M1138-L-CONNECTED-PROPAGATION`, or
`M1138-L-CONTINUITY-EXTENSION`, and it does not give those nodes individual closure credit.
Likewise, its compact maximizer is for the perturbed function rather than the exact intermediate
described by `M1138-C-CLOSURE-MAXIMIZER`.

The receipt therefore claims exact kernel closure only for the root, the implemented terminal
package, the already checked terminal-to-root transport, and route-independent supporting facts.
The integration lane must reconcile the alternate proof route with a versioned append-only
architecture delta before granting complete per-node frozen-denominator closure. The registry,
typed graphs, generated checklist, and item state are unchanged by this proof worker.

## Commands and results

Validation ran on 2026-07-14 (`Asia/Shanghai`) in the worker clone. The existing canonical pinned
`.lake` artifacts were reused without mutation. No Lake update/build, clone, fetch, dependency
installation, or network access was performed.

```text
bash Stage1_Instances/THM-M-1138/check_proof.sh
  exit 0: disposable Statement.olean and ObligationTree.olean were built outside the repository;
  Proof.lean elaborated; both exact terminal declarations were sorry-free and reported exactly
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1..1546 passed

python3 scripts/stage1_target.py show THM-M-1138
  exit 0: rank 343, planned, L0/rework_required, theorem_complete=false

python3 Stage1_Instances/THM-M-1138/check_obligation_tree.py
  exit 0: frozen version-1 registry still has 15 obligations and 36 typed edges

python3 -B Stage1_Instances/THM-M-1138/check_proof.py
  exit 0: exact source, target, hashes, route boundary, receipt, and worker packet passed

rg -n -i --glob '*.lean' '<prohibited proof-token expression>' \
  Stage1_Instances/THM-M-1138/Proof.lean
  exit 1 with empty output: expected pass; no placeholder, custom axiom, unsafe/opaque body,
  implementation escape, external declaration, or native oracle was found

python3 -m json.tool Stage1_Instances/THM-M-1138/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: both structured artifacts parsed

git diff --check -- Stage1_Instances/THM-M-1138 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is provisional proof-phase evidence, not theorem completion. Master acceptance, the
architecture reconciliation, downstream validation and release, accepted source/readability/trust
closure, hermetic replay, independent verification, `AUDIT-Z`, and `THEOREM-Z` remain open.
