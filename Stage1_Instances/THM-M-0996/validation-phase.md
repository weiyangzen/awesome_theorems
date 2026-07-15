# THM-M-0996 validation-phase record

Item: `S56-M-0996-VALIDATION`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Validation timestamp: `2026-07-15T13:40:09+08:00`

## Scope and verdict

The structured recipe performs a fresh, network-isolated, trust-zero replay of
the exact statement module, the frozen conditional composition, all 34 partial
proof declarations, the anchor probe, and two separately written validation
probes. `Validation.lean` does not import `Proof`. It independently reconstructs
half-space measurability and the exact conditional composer, while preserving
`GeneralSetEnlargementBound` as the explicit open premise.

The replay observes exactly `propext`, `Classical.choice`, and `Quot.sound` for
the 37 declarations that print axiom reports. Both validation probes are
machine-reported sorry-free. The source scan rejects executable placeholders,
bodyless or unsafe declarations, native or implementation escapes, and external
code. It also binds the current target sources, frozen denominator, graph cut,
proof receipt and blocker, pinned mathlib revision/tree/license, and selected
Gaussian, CDF, and thickening source/blob/olean identities.

This validates partial bodies, not a theorem root. No premise-free declaration
proves `GaussianIsoperimetricTarget`; the arbitrary-measurable-set bound remains
open. The six supported nodes retain `planned:v1` fingerprints and receive no
whole-obligation credit. The authoritative graph cut remains
`M0996-L-HALFSPACE` and `M0996-L-GENERAL`, the root remains M3, and both
`audit_complete` and `theorem_complete` remain false. The validation verdict is
therefore `blocked`, while the truthful self-tested worker handoff proposes
only `[_]` for integration review.

## Gate results

| Gate | Result |
|---|---|
| Exact kernel replay | Pass for the statement surface, conditional composition, 34 partial proof declarations, and two differential probes under `--trust=0`; no root closure follows. |
| Trust observation | Pass for the direct axiom reports and owned-source hygiene; fail closed for an accepted foundation profile and complete transitive declaration, import, executable, bootstrap, plugin, oracle, and TCB closure. |
| Direct provenance | Pass for current local hashes, clean pinned mathlib revision/tree/remote/license, and three selected source/blob/olean identities; fail closed for a complete restorable dependency/SBOM archive. |
| Recorded predecessor replay | Fail closed: `lake env` attempted shared dependency resolution and could not resolve the existing pinned `flt-regular` checkout because it had no resolvable `HEAD`. That failed attempt receives no validation credit; the successful validator avoids Lake and dependency-network commands. |
| Hermetic release | Fail closed: the successful absolute-Lean replay reuses the shared warm canonical dependency artifacts and is not a new immutable checkout, empty-cache dependency build, or offline restoration. |
| Independent verification | Fail closed: the separately implemented Lean probes run in this worker checkout and cache, not on a second signed independently provisioned runner with an independent minimal release verifier. |
| Proof dependency | Fail closed: `S56-M-0996-PROOF` is only provisional `[_]` evidence and has not received master acceptance. |

The intake `instance.json` remains authoritative at H2/M4/R4, whereas the exact
statement and later provisional proof evidence support a nonaccepted M3
observation. Validation records this stale projection mismatch without editing
or silently reconciling structured state. The authoritative vector stays
H2/M4/R4; only the integration lane may accept dependencies or promote it.

## Commands and exact results

Commands ran from the worker clone on 2026-07-15 (Asia/Shanghai). The canonical
`.lake` symlink is shared and mutable. The failed predecessor command attempted
Lake resolution; the successful validator uses its mathlib artifacts read-only,
invokes no Lake or dependency-network command, and writes only under `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all remain L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0996` | 0 | Rank 276; planned lifecycle; L0/rework_required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0996/check_obligation_tree.py` | 0 | The frozen 19-obligation, seven-graph architecture passed with reciprocal acyclic proof edges and an open root. |
| `nice -n 19 bash Stage1_Instances/THM-M-0996/check_proof.sh` | 1 | The recorded predecessor recipe stopped before Lean because Lake could not resolve the existing `flt-regular` checkout `HEAD`; this result receives no proof credit. |
| `python3 -I -B Stage1_Instances/THM-M-0996/check_validation.py` | 0 | Network-isolated trust-zero fresh target replay, exact axiom reports, source hygiene, current open graph, selected pinned provenance, receipt boundary, and every fail-closed release decision passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/validation-spec.json` | 0 | Structured validation recipe is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/validation-receipt.json` | 0 | Node receipt is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0996 .stage1-worker-selftest.json` | 0 | No tracked diff diagnostics; the validator separately byte-checks all untracked artifacts. |

## Remaining boundary

The first dependency gate is proof master acceptance; the first mathematical
theorem gate is `M0996-L-GENERAL.kernel_closure`; and the first release gate is
complete transitive provenance/trust closure. Restoring the pinned Lake artifact
without moving revisions is additionally required to replay the predecessor's
recorded recipe. Source H0, independently reviewed R0, cold offline replay,
distinct signed verification, deterministic release evidence, `AUDIT-Z`,
`THEOREM-Z`, release, and master acceptance all remain open.
