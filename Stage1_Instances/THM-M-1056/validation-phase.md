# THM-M-1056 validation-phase evidence

Item: `S56-M-1056-VALIDATION`. Base revision:
`4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3`; base tree:
`e38ee217e0bb768c5c915905d1d0b04fc89e25f2`.

## Validation scope

The executable recipe copies all 62 vendored Oseledets modules, the exact statement, nine local
proof/transport modules, and a proof-free validation probe into fresh temporary source and output
directories. Every Lean subprocess runs as `lake env lean --trust=0 -t0` inside a Bubblewrap
network namespace with a read-only host root, cleared fixed environment, one Lean thread, and only
the disposable replay directory writable. The automation-provided pinned `.lake` symlink is reused
read-only and remains a shared warm cache. No target-local `.olean` is read or created.

The replay reaches `ErgodicTheory.oseledets_splitting`, the coordinate and measurable projection
bridges, the concrete exact-root wrapper, and both public exact-root names. Lean's transitive sorry
collector finds all six audited declarations sorry-free. Each declaration reports exactly
`propext`, `Classical.choice`, and `Quot.sound`. A closure traversal covers 49,305 declarations from
1,700 modules and observes no additional bodyless nonaxiom or unsafe declaration. `Validation.lean`
adds no proof theorem.

`check_vendor.py` independently checks the complete source inventory, immutable upstream revision
and archive digest, Apache-2.0 license, per-file upstream/port hashes, frozen build order, prohibited
constructs, and reversal of the 26-file compatibility port. The current replay reproduces the
recorded terminal and proof `.olean` hashes. The historical `BlockSqueeze` intermediate `.olean`
mismatch remains non-normative provenance; its source hash and current deterministic build pass.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`,
dependency clone/fetch, checkout, `.lake` mutation, or network request was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1056
  exit 0: rank 248; planned L0/rework-required target; theorem_complete=false

python3 -I -B Stage1_Instances/THM-M-1056/check_statement.py
  exit 0: exact expression 8e1a96a...e65d403b; all four mutations killed

python3 -I -B Stage1_Instances/THM-M-1056/check_obligation_tree.py
  exit 0: 19 obligations and 49 typed edges passed; authoritative graph remains open M3

python3 -I -B Stage1_Instances/THM-M-1056/check_vendor.py
  exit 0: 62 modules, 1,504,769 bytes, reversible 26-file port

python3 -I -B Stage1_Instances/THM-M-1056/check_validation.py --probe
  exit 0: network-isolated trust-zero replay rebuilt 62 vendored and 11 target/probe modules;
  exact root, trust, hygiene, provenance, and closure observations passed

python3 -I -B Stage1_Instances/THM-M-1056/check_validation.py \
  --worker-packet .stage1-worker-selftest.json
  exit 0: the recorded recipe, receipt, blocker, worker packet, and fail-closed decisions passed

python3 -m json.tool on validation-spec.json, validation-receipt.json,
validation-blocker.json, and .stage1-worker-selftest.json
  exit 0 for each: valid JSON with duplicate keys rejected by the executable validator

PYTHONPYCACHEPREFIX=/tmp/stage1-m1056-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1056/check_validation.py
  exit 0: validator syntax checked without target-local bytecode

git diff --check -- Stage1_Instances/THM-M-1056 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The predecessor `check_proof.py` is deliberately not a current validation recipe. It is bound to
the proof worker's old base revision and old `[ ]` DAG view; on the integrated base, it fails its
snapshot guard before checking proof content. This validation hash-binds that checker and its
receipt but independently replays every proof source instead of weakening the old guard or claiming
it still passes. The older `validation-specs.json` is also obligation-tree evidence: its shell-string
recipes do not satisfy the rev-5.6 structured validation contract. The new `validation-spec.json`
is the validation-node recipe and records `argv` structurally.

## Fail-closed decisions

The first node gate is
`dependency.S56-M-1056-PROOF.master_acceptance_and_graph_reconciliation`. The predecessor is only
`[_]`. The frozen registry and typed graph still describe the pre-proof conditional route, keep the
root at `[H1, M3, R3]`, and name `M1056-T-CORE` as the authoritative graph cut. Only
`M1056-T-ASSEMBLE` has a terminal proof-body ID, while the newer external-wrapper route has not been
reconciled into append-only candidate, proof, composition, provenance, evidence, or trust edges.
The observed exact-root inhabitant therefore grants no accepted closed obligation or `M0-*` class.

The primary-source crosswalk remains `H1`, and required readable records remain `R3`. The observed
axioms have no accepted theorem-specific foundation profile. The 49,305-declaration observation is
not a serialized, independently reviewed transitive provenance graph, complete compiled-artifact
inventory, compiler/bootstrap/plugin/checker TCB, SBOM, or supply-chain closure.

Network isolation and fresh target `.olean` outputs strengthen the narrow replay but do not satisfy
the release hermetic gate. There is no separate clean checkout, empty-cache cold bootstrap,
content-addressed offline restoration, deterministic release bundle, distinct signed runner,
independently provisioned cache, second attestation, or independently implemented minimal verifier.
`AUDIT-Z`, `THEOREM-Z`, validation completion, release, theorem completion, and master acceptance
all remain false.

## Status boundary

This is self-tested validation-node evidence for a real network-isolated trust-zero warm kernel
replay, exact observed axioms, placeholder/unsafe closure, and selected pinned provenance. It
truthfully records failed dependency, authority, node-specific provenance, H0/R0, foundation/TCB,
cold-hermetic, and independent-verification gates. It is not accepted `M0`, `E0/E1`, audit
completion, validation completion, theorem completion, release, or master acceptance.
