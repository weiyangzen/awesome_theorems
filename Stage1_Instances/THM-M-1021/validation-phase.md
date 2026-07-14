# THM-M-1021 validation-phase evidence

Item: `S56-M-1021-VALIDATION`. Base revision:
`6cf20c1ab97fcd6970455baa23022062ebc14fe1`; base tree:
`5fa65edc9a9b91b49f7f925ad524ec374328e14c`.

## Validation scope

The executable recipe copies the three vendored Bochner modules, the exact
`BochnerStatement.lean`, `Proof.lean`, and a proof-only `Validation.lean`
trust probe into fresh temporary output space. Every Lean process runs with
`--trust=0` in a Bubblewrap network namespace with a read-only host root,
fixed locale and timezone, and one Lean thread. Only the disposable module
directory is writable. The automation-provided pinned `.lake` symlink is
reused read-only and remains a shared warm cache.

The replay reaches the unchanged
`AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget` through
`bochner_exact`. Lean's transitive sorry collector finds no sorry in the
vendored `bochner_theorem` or the local forward, reverse, and exact-root
declarations. All four report exactly `propext`, `Classical.choice`, and
`Quot.sound`. `Validation.lean` adds no theorem or proof body; it is a trust
probe over the existing proof, not an implementation-diverse validation.

Selected provenance checks reconstruct all three upstream files from the
documented target-local import and comment changes and require the immutable
upstream SHA-256 values. They also bind the Apache-2.0 license, statement,
frozen registry and graph, proof receipt, clean pinned mathlib revision/tree/
remote/license, selected direct mathlib source blobs, and the Lean, Lake,
Python, Git, Bash, Bubblewrap, and Elan executable identities. This is not a
complete transitive declaration/source graph, compiled-artifact inventory,
TCB closure, SBOM, or offline source archive.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). No
`lake update`, `lake build`, dependency clone/fetch, checkout, `.lake`
mutation, or network request was performed by the validation recipe.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1021
  exit 0: rank 497, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1021/check_obligation_tree.py
  exit 0: frozen 50-obligation registry and 65 typed edges passed; root remains M3

bash Stage1_Instances/THM-M-1021/check_validation.sh
  exit 0: all three vendored modules, the exact statement, proof, and trust
  probe elaborated from fresh source in network-isolated trust-zero processes;
  four requested sorry and axiom checks passed

python3 -I -B Stage1_Instances/THM-M-1021/check_validation.py
  exit 0: exact target, kernel replay, selected trust/provenance, frozen
  authority boundaries, receipt, recipe, ownership, and fail-closed decisions passed

python3 -m json.tool Stage1_Instances/THM-M-1021/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1021/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1021-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1021/check_validation.py
  exit 0: validator syntax checked without writing bytecode into the target

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' \
  Stage1_Instances/THM-M-1021/{BochnerStatement,Proof,Validation}.lean \
  Stage1_Instances/THM-M-1021/External/Bochner/*.lean
  exit 1 (expected no match): no prohibited executable construct was found
  after the validator's nested-comment-aware scan

git diff --check -- Stage1_Instances/THM-M-1021 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is intentionally not a current validation
recipe: it is bound to the proof worker's older base revision, execution state,
and root self-test packet. This phase hash-binds the proof receipt and directly
replays every Lean input instead of weakening that checker or falsely claiming
its stale workspace assertions pass.

## Fail-closed decisions

The first node gate is
`dependency.S56-M-1021-PROOF.master_acceptance`. The proof predecessor is
only `[_]`, so accepted state remains `[H1, M3, R3]` with no accepted closed
obligation. The checked reverse body uses Gaussian regularization, tightness,
and Prokhorov compactness, while the frozen `M1021-C1` through `M1021-C5`
architecture specifies a Riesz-Markov construction. `M1021-T2` also lacks the
required child-to-parent certificate, and the earlier anchor audit records a
negative external-candidate result. A master-owned append-only discovery and
registry/graph reconciliation is required before validation can ratify graph
closure or accepted `M0-P`.

The primary-source crosswalk is only `H1`, no required readable obligation has
an independently accepted `R0` record, and the observed axioms have no accepted
theorem-specific foundation profile. Complete declaration, source-origin,
compiled-object, compiler/bootstrap, plugin, checker, TCB, and SBOM closure is
absent.

Network isolation and fresh local `.olean` outputs strengthen this narrow
replay but do not satisfy the release hermetic gate. There is no separate
immutable clean checkout, empty-cache cold bootstrap, content-addressed offline
restoration, deterministic release bundle, distinct signed runner,
independently provisioned cache, second attestation, or independently
implemented minimal verifier. `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, and master acceptance remain false.

## Status boundary

This is self-tested validation-node evidence for a network-isolated narrow
kernel replay, exact observed axioms, placeholder closure, and selected local
and vendored provenance. It truthfully records failed authority, route and
composition, source/readability, foundation/TCB, cold-hermetic, and independent
verification gates. It is not accepted `M0-P`, `E0/E1`, audit completion,
theorem completion, release, or master acceptance.
