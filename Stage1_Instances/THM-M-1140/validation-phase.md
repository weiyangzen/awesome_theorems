# THM-M-1140 validation phase

Item: `S56-M-1140-VALIDATION`. Validation base:
`557b928b377b386864527c9fb4831d45857837aa` (tree
`e677879a6eb4cb9d6795ba1bd78726af06ab9465`).

## Verdict

The validation implementation is self-tested, but the assurance result is
`blocked`. No accepted state, `E0`, `M0-L`, audit completion, theorem
completion, or release is claimed.

The exact frozen statement, conditional package composition, repo-local proof
root, and two separately written import-dependent probes elaborate with Lean
`--trust=0`. The root, both substantive packages, and both probes are
sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`.
The probe's machine-derived transitive declaration closure reports no bodyless
nonaxioms or unsafe declarations.

Every Lean invocation uses a fresh temporary output directory, fixed
locale/timezone/thread settings, a read-only host view, and a Bubblewrap network
namespace with outbound network unavailable. The run also binds the local
sources, toolchain and manifest, clean mathlib revision/tree/origin/license,
and the source/blob/olean hashes of all eight mathlib modules directly imported
by the theorem/proof modules. The validation-only assertion utilities are
kernel-replayed but are not included in this selected source triple inventory.
This is selected provenance, not the complete transitive release closure.

## Fail-closed gates

The first dependency gate is open: `S56-M-1140-PROOF` has provisional worker
evidence but no master acceptance. The frozen registry names an
`M1140-L-MEAN-VALUE` analytic bridge, while the proof implements the same local
rigidity output by a Gaussian-barrier argument. The proof receipt leaves that
mapping for master review or an append-only registry-v2 method supersession.
The authoritative typed graph therefore remains `H2/M3/R3`, `root_closed=false`,
with both package nodes in its recorded cut set.

The accepted theorem-specific foundation profile, complete transitive
declaration/body/import/compiled-object and executable TCB closure, SBOM and
licenses, and restorable offline archive are absent. Reusing the automation
clone's canonical pinned warm `.lake` artifacts is not the new-checkout,
empty-cache cold build required by section 10.6. The validation probes import
`Proof.lean` and run under the same worker identity, checkout, kernel, and
cache; they are not a distinct signed runner or an independently implemented
minimal verifier under section 10.7. Human-source `H0`, independently reviewed
`R0`, deterministic release bundle, `AUDIT-Z`, and `THEOREM-Z` also remain open.

## Commands and results

All commands were run from the repository root on 2026-07-15.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | rank 345, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | 16 obligations, 36 typed edges, denominator `355cbcf3...0bee`; frozen root remains open M3 |
| `python3 -B Stage1_Instances/THM-M-1140/check_proof.py` | 0 | preflight proof receipt/source checker passed before the validation self-test replaced the root worker packet |
| recorded Bubblewrap `argv` in `validation-spec.json` | 0 | canonical network-denied structured recipe reproduced the same pass/fail-closed observations |
| `python3 -m json.tool Stage1_Instances/THM-M-1140/validation-spec.json` | 0 | recipe JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1140/validation-receipt.json` | 0 | receipt JSON parsed |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | worker packet JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

`check_proof.py` is intentionally snapshot-bound to the earlier proof worker
packet, so it is not rerun after the validation self-test manifest is written.
The kernel replay is performed directly by `check_validation.py` instead.

## Retry condition

The integration lane must first accept the proof prerequisite and reconcile the
Gaussian-barrier method with the frozen architecture. Complete foundation,
provenance, TCB, cold offline, and distinct-runner evidence must then be
produced against one immutable clean snapshot before this node can pass its
master gate.
