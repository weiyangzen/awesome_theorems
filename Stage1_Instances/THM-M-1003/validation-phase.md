# THM-M-1003 validation-phase evidence

Item: `S56-M-1003-VALIDATION`. Base revision:
`d3d4bc991fae237427b8ac391bbe701dca8f2af2`; base tree:
`51d54892f625b3b42e3b0c2c6b3c8e173c4ad166`.

## Validation scope

The structured node recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` to fresh temporary output space and
elaborates them in dependency order with Lean `--trust=0`. Every Lean process
runs inside a Bubblewrap network namespace with the host root, toolchain, and
pinned dependency cache read-only. Only the temporary module directory is
writable; locale, timezone, thread count, and umask are fixed.

The exact frozen root, its conditional composition, and all thirteen local
proof declarations elaborate and are transitively sorry-free. Their
machine-derived axiom reports are exactly `propext`, `Classical.choice`, and
`Quot.sound`. `Validation.lean` imports the proof root and checks its exact
canonical type. It deliberately adds no mathematical proof route and shares
this worker, checkout, proof body, Lean executable, and dependency cache. It
is therefore a same-worker type/trust probe, not independent verification.

The validator also binds the frozen target and registry hashes, proof receipt,
clean mathlib revision/tree/remote, six selected source/blob/olean triples,
mathlib license, manifests, and Lean/Lake/Python/Git/Bash/Bubblewrap identities.
This is selected local provenance only, not a complete transitive declaration,
compiled-artifact, compiler/bootstrap/plugin, TCB, or SBOM inventory.

## Commands and results

Commands ran from the worker clone on 2026-07-14 (Asia/Shanghai). The
automation-provided pinned `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, dependency clone/fetch, checkout, or network
request ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets and ranks passed

python3 scripts/stage1_target.py show THM-M-1003
  exit 0: rank 283, planned L0/rework-required target;
  legacy artifacts unaccepted and theorem_complete=false

python3 Stage1_Instances/THM-M-1003/check_obligation_tree.py
  exit 0: 16 frozen obligations and 37 typed edges passed; the frozen
  pre-proof graph truthfully retains its root-open M4 observation

timeout 900s bash Stage1_Instances/THM-M-1003/check_validation.sh
  exit 0: network-isolated trust-zero replay passed; the exact composition,
  all thirteen proof declarations, root, and type probe report only the three
  recorded axioms and are transitively sorry-free

python3 -B Stage1_Instances/THM-M-1003/check_validation.py
  exit 0: target/registry/proof linkage, source and tool hashes, selected
  provenance, receipt, worker packet, and all fail-closed boundaries passed

python3 -m json.tool Stage1_Instances/THM-M-1003/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1003/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1003-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1003/check_validation.py
  exit 0: validator compiled outside the repository tree

git diff --check -- Stage1_Instances/THM-M-1003 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed explicit
  no-index whitespace checks
```

The proof-phase `check_proof.py` is intentionally not replayed as a validation
gate: it is bound to the proof worker's older base, DAG state, changed-path
set, and self-test packet. This validation phase hash-binds that proof receipt
and directly replays the exact Lean sources instead of weakening those
snapshot assertions or falsely claiming that they pass in a later workspace.

## Fail-closed gates

The exact mathematical root is locally kernel-closed, but the prerequisite
proof packet and every earlier node are only provisional `[_]`; none has
dependency-ordered master acceptance. The accepted vector therefore remains
`[H3, M4, R3]`, the frozen graph remains authoritative and open, and no
obligation or root closure is accepted.

The dossier has no accepted theorem-specific foundation policy to approve the
observed classical axiom set, no complete transitive declaration/import and
TCB/SBOM closure, no pinpoint independently reviewed `H0`, and no independently
reviewed `R0`. The warm shared dependency closure is not a clean-checkout,
empty-cache cold bootstrap, content-addressed offline restoration, deterministic
release bundle, or second-platform attestation. There is no second signed
identity, independently provisioned runner, or independently implemented
minimal release verifier. Those gates remain open rather than simulated.

## Status boundary

This is self-tested validation-node evidence proposing only `[_]` for master
inspection. It is not proof or master acceptance, accepted `M0-L`, a complete
foundation/TCB/provenance packet, `E0`, `E1`, independent validation, `H0`,
`R0`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem completion.
