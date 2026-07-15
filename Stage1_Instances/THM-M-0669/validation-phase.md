# THM-M-0669 validation-phase evidence

Item: `S56-M-0669-VALIDATION`. Base revision:
`443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`; base tree:
`c5771c47c12b80aba613e6d844570f83b39ded6d`.

## Validation scope

The structured recipe copies `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh disposable directory.
Every Lean process runs with `--trust=0 -t0` in a Bubblewrap network
namespace. The host root, installed toolchain, and canonical pinned dependency
cache are read-only; only the disposable directory is writable.

`Validation.lean` imports neither `Proof` nor `ObligationTree`. It
separately reimplements universal-polynomial semantics for pure-ring atoms,
Boolean `IsQF` closure, and formula recursion from an explicit one-variable
elimination premise. The final differential declaration consumes that premise
rather than hiding it. This is a same-worker differential check, not a distinct
runner or a second proof of the canonical root.

The validator binds the exact statement expression, frozen denominator, proof
receipt and blocker, local source hashes, exact mathlib revision/tree/remote,
four selected source and compiled-object boundaries, the mathlib license, and
executable identities. All twelve checked proof-bearing declarations are
placeholder-free and use only `propext`, `Classical.choice`, and
`Quot.sound`; two Boolean/syntax declarations use no axioms. A Lean
environment walk from the five differential declarations observes 9775
transitively used declarations in 385 modules, with no unexpected bodyless or
unsafe declaration. This is a trust observation, not an accepted foundation
policy or complete TCB/provenance inventory.

## Commands and results

All commands ran in the worker clone on 2026-07-15 (Asia/Shanghai). The
pre-existing canonical pinned `.lake` symlink was reused without update,
build, clone, fetch, or intentional mutation.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0669
  exit 0: rank 713, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-0669/check_anchor_audit.py
  exit 0: three frozen candidates classified; exact candidate absent; M3 retained

python3 Stage1_Instances/THM-M-0669/check_obligation_tree.py
  exit 0: 14 obligations and 49 typed edges passed; frozen root remains open M3

python3 -I -B Stage1_Instances/THM-M-0669/check_validation.py
  --worker-packet .stage1-worker-selftest.json
  exit 0: network-isolated trust-zero narrow replay, selected provenance
  checks, and all fail-closed receipt assertions passed

python3 -m json.tool Stage1_Instances/THM-M-0669/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0669/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-0669 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed explicit
  hygiene checks
```

The requested root-level `lake env lean` recipe is not usable on this
snapshot: the automation-provided canonical `flt-regular` package directory
has no checked-out `HEAD`, so Lake attempts dependency resolution and fails.
The worker did not fetch or repair that moving/missing artifact. The recorded
replay instead invokes the digest-checked installed Lean binary directly and
constructs `LEAN_PATH` only from the existing pinned compiled package
directories, matching the successful proof-phase kernel path without a Lake
operation.

The legacy `check_proof.sh` also is not recorded as a passing validation
command. Its Lean subprocesses elaborate successfully, but its proof-phase
Python checker is intentionally bound to the old proof base and the old
proof-phase worker packet, so it exits nonzero in this validation workspace.
The new checker replays and verifies the same seven declarations independently.

## Fail-closed gates

The proof prerequisite has scheduler-provisional state `[_]`, but its receipt
is unaccepted and records no accepted closed obligations. Narrow validation
replays the provisional Boolean body, atomic progress, and conditional formula
composition. The frozen graph remains authoritative at `[H1, M3, R3]`.

The first mathematical gap is `M0669-E-ONE-VAR`: no local or pinned
placeholder-free body constructs the one-variable real-closed-field
elimination package. Its sign, roots, projection, and semantics dependencies
remain open, so the canonical root is not kernel-closed.

The observed axioms and selected source/object boundaries do not establish an
accepted foundation policy, serialized complete transitive provenance graph,
or full TCB/SBOM. The shared cache is warm, the checkout is a dirty worker
snapshot, and the incomplete pinned package blocks ordinary Lake replay. This
is not a fresh clean checkout, empty-cache cold build, offline archive
restoration, or release-grade hermetic receipt.

The separately elaborated no-import implementation uses this worker identity,
checkout, Lean binary, and dependency cache. No distinct signed independently
provisioned runner or independently implemented minimal release verifier
exists. Primary-source H0,
independently reviewed R0, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, accepted state, and master acceptance all remain open.

## Status boundary

This is a self-tested validation-node handoff for integration-lane inspection.
It records narrow gates that passed and assurance/release gates that failed. It
does not claim accepted obligation closure, `M0`, `E0`/`E1`, accepted
foundation/TCB closure, theorem completion, release, or master acceptance.
