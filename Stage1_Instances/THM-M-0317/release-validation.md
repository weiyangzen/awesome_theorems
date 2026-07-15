# THM-M-0317 release-phase reconciliation

Item: `S56-M-0317-RELEASE`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M4, R4]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release,
or theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0317-VALIDATION` is only a provisional `[_]` worker projection. Its
receipt has `accepted=false` and `release_grade=false`, so the release node's
dependency is not master accepted.

The next theorem gate fails independently: `proof.root_kernel_closure`.
`M0317-T-APPROX` has no placeholder-free inhabitant of the frozen
`ApproximationPackage`. The exact Tychonoff root therefore remains open.

## Evidence reconciliation

The existing narrow validation supplies useful nonrelease evidence. It
elaborates the hash-bound exact statement and four mutations, the conditional
root composer, the compactness-limit proof branch, and a separately written
same-worker reconstruction with trust zero. The local hygiene checks find no
prohibited proof device, and the checked declarations report only `propext`,
`Classical.choice`, and `Quot.sound`. None of this proves the missing
finite-dimensional approximation branch or accepts the exact root.

Structured authority remains `planned` at `[H1, M4, R4]`. The frozen graph is
a pre-proof snapshot whose authoritative root cut is `M0317-T-APPROX` plus
`M0317-T-LIMIT`. The latter has provisionally replayed proof evidence, leaving
`M0317-T-APPROX` as the post-provisional mathematical cut, but no receipt is
accepted and the partial proof and validation packets remain provisional.
`AUDIT-Z` is also independently blocked:
the exact primary-source text, assumptions, errata, node crosswalk, duplicate
resolution, independent H0 review, and independent R0 reconstruction remain
open.

The first release-specific failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`; the current worker has an untracked shared
`.lake` link and the validation receipt explicitly classifies its checkout as
dirty nonrelease evidence. The next release gate is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. There is no clean empty-cache cold build,
offline archive restoration, complete TCB/SBOM/license closure, two distinct
signed runners, independent minimal verifier, protected CI fixture evidence,
or deterministic content-addressed release bundle.

A current prescribed `lake env lean` replay is additionally blocked. The shared
canonical `.lake` does not contain a valid checkout of the lakefile-pinned
`flt-regular` dependency. During independent audit, invoking an existing proof
script indirectly triggered Lake materialization and left that shared package
with an invalid `HEAD`; the attempt failed and is not evidence. No repair,
fetch, update, build, or further dependency mutation was performed. The
release decision therefore binds and reconciles the earlier integrated
validation receipt rather than claiming a fresh pinned-lane Lean result.

## Commands and results

Commands ran from the worker root on 2026-07-15 in the Asia/Shanghai timezone.
The release checker itself was local and network-free. During independent
audit, however, `bash Stage1_Instances/THM-M-0317/check_proof.sh` indirectly
caused Lake to attempt materialization/fetch in the shared `.lake` target and
then failed. That forbidden cache mutation supplies no evidence. It was not
repaired, and no further fetch, update, build, or dependency mutation was
attempted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0317` | 0 | Rank 683 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0317/check_obligation_tree.py` | 0 | 17 obligations and 33 typed edges passed; the authoritative frozen root remained open. |
| `bash Stage1_Instances/THM-M-0317/check_proof.sh` | 1 | `lake env which lean` indirectly attempted shared-cache materialization/fetch and then failed with Git exit 128; the attempt is forbidden non-evidence. |
| `STAGE1_SKIP_RECEIPT_CHECK=1 python3 -B Stage1_Instances/THM-M-0317/check_validation.py` | 1 | Historical validator is revision-bound to its original `e46e0735` turn and correctly rejects this integrated base. |
| `lake env lean` narrow replay preflight | blocked, no valid evidence | Shared artifacts report `.lake/packages/flt-regular: could not resolve 'HEAD' to a commit`; no repair or further fetch was performed. |
| `python3 -B Stage1_Instances/THM-M-0317/check_release.py` | 0 | Reconciled the bound structured authority and derived the exact blocked verdict. |
| `python3 -m json.tool` on the release spec, decision, receipt, and worker packet | 0 | All structured release artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0317-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0317/check_release.py` | 0 | The checker compiled without creating a generated owned file. |
| `git diff --check -- Stage1_Instances/THM-M-0317 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Retry requires an exact placeholder-free `ApproximationPackage`, append-only
graph reconciliation, and dependency-legal master acceptance. The release
lane must then close H0/R0, foundation/provenance/trust/TCB/SBOM evidence,
clean cold offline replay, distinct signed attestations, the independent
minimal verifier, protected CI fixtures, and the deterministic release bundle.

Status boundary: this artifact self-tests only the truthful negative release
decision. It grants no accepted `M0`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`,
release, theorem-completion, or master-acceptance credit.
