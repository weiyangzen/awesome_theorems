# THM-M-1291 validation-phase evidence

Item: `S56-M-1291-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`; base tree:
`d881fd9641fa3e5f3ebe5082b35672981e90adcf`.

## Validation scope

The executable recipe copies the exact `Statement.lean`, `Proof.lean`, and a proof-only
`Validation.lean` trust probe into fresh temporary output space. Every Lean process runs with
`--trust=0` in a Bubblewrap network namespace with a read-only host root, fixed locale and timezone,
and one Lean thread. Only the disposable module directory is writable. The automation-provided
pinned `.lake` symlink is reused read-only and remains a shared warm cache.

The replay reaches the exact unchanged `BrezisLiebTarget` and
`brezisLiebTarget_proof : BrezisLiebTarget`. Lean's transitive sorry collector finds no sorry in
the root or nine named support theorems. Every checked declaration uses only `propext`,
`Classical.choice`, and `Quot.sound`, and the root uses exactly that set. `Validation.lean` adds no
proof declaration; it imports the existing proof and runs trust commands. A proof-independent exact
root would require reimplementing the substantial subunit/superunit analytic argument, which the
validation phase may not add merely to make earlier proof status agree.

Selected provenance checks bind the repo-local proof body, statement, frozen registry and graph,
proof receipt, clean pinned mathlib revision/tree/remote/license, four directly imported mathlib
source blobs, and the Lean/Lake/Python/Git/Bash/Bubblewrap/Elan executable identities. This is not a
complete transitive declaration/source graph, compiled-artifact inventory, TCB closure, or SBOM.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). No `lake update`, `lake build`,
dependency clone/fetch, checkout, `.lake` mutation, or network request was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1291
  exit 0: rank 462, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1291/check_obligation_tree.py
  exit 0: frozen 17-obligation registry and 38 typed edges passed; pre-proof root remains M3

bash Stage1_Instances/THM-M-1291/check_validation.sh
  exit 0: network-isolated trust-zero replay elaborated the exact statement, complete local proof,
  and trust probe; ten requested sorry and axiom checks passed; captured stdout was 4627 bytes with
  SHA-256 68c25af3d13d3a465c3f7ad9a612b79a316e248f9edcfeb350461742fb80c33d

python3 -I -B Stage1_Instances/THM-M-1291/check_validation.py
  exit 0: exact target, kernel replay, selected trust/provenance, frozen authority boundaries,
  receipt, recipe, ownership, and fail-closed decisions passed

python3 -m json.tool Stage1_Instances/THM-M-1291/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1291/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1291-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1291/check_validation.py
  exit 0: validator syntax checked without writing bytecode into the target

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|native_decide|extern[[:space:]]' \
  Stage1_Instances/THM-M-1291/{Statement,Proof,Validation}.lean
  exit 1 (expected no match): no prohibited construct was found after the validator's
  nested-comment-aware scan

git diff --check -- Stage1_Instances/THM-M-1291 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is intentionally not a current validation recipe: it conditionally
requires the proof worker's root self-test packet. Its receipt and sources are hash-bound here, and
the proof is freshly replayed rather than weakening that checker. `check_obligation_tree.py` remains
current for the intentionally frozen pre-proof architecture and passes separately.

## Fail-closed decisions

The first node gate is `dependency.S56-M-1291-PROOF.master_acceptance`. The proof predecessor is
only `[_]`, so accepted state remains `[H2, M3, R4]` with no accepted closed obligation. The proof
receipt proposes all 14 required-machine IDs using only three exact declarations; the frozen
registry still has planned fingerprints and no terminal proof-body IDs, while typed-graph nodes
have no evidence and only pending provenance. Master reconciliation of exact node bodies and
composition evidence is therefore required before validation can ratify `M0-L`.

The primary-source crosswalk is not `H0`, no required readable obligation has an independently
accepted `R0` record, and the observed axioms have no accepted theorem-specific foundation profile.
Complete declaration, source-origin, compiled-object, bootstrap, plugin, checker, TCB, and SBOM
closure is absent.

Network isolation and fresh local `.olean` outputs strengthen the narrow replay but do not satisfy
the release hermetic gate. There is no separate immutable clean checkout, empty-cache cold
bootstrap, content-addressed offline restoration, deterministic release bundle, distinct signed
runner, independently provisioned cache, second attestation, or independently implemented minimal
verifier. `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, and master acceptance remain false.

## Status boundary

This is self-tested validation-node evidence for a network-isolated narrow kernel replay, exact
observed axioms, placeholder closure, and selected local provenance. It truthfully records failed
authority, node-specific provenance/composition, source/readability, foundation/TCB,
cold-hermetic, and independent-verification gates. It is not accepted `M0-L`, `E0/E1`, audit
completion, theorem completion, release, or master acceptance.
