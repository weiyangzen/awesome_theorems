# THM-M-0414 release reconciliation

Item: `S56-M-0414-RELEASE`

Base revision: `0afbf514f9bd5f339943542106f6b811869fe572`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R3]`, and both `audit_complete` and `theorem_complete` remain false. This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion claim.

The structured worker recipe is `release-spec.json`; its provisional node receipt is
`release-receipt.json`. The receipt is explicitly `release_grade=false`, records a dirty warm-cache
worker run, and remains subject to integration-lane acceptance.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-0414-VALIDATION` is only a provisional worker projection (`[_]`) with no master acceptance.
The first failed release-assurance gate is
`S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE`, and the first reproduction failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The current narrow replay checks the exact target, its two frozen components, their conditional
composition, the proof-phase exact root, and a separately written validation-only exact root.
Both proof routes use the pinned mathlib declarations `Ideal.uniqueFactorizationMonoid` and
`Ideal.finprod_heightOneSpectrum_factorization`. All checked declarations report only `propext`,
`Classical.choice`, and `Quot.sound`, and the inspected local Lean sources contain no placeholder,
bodyless axiom, unsafe declaration, native shortcut, or external oracle. This supports a
provisional `M0-W` candidate, not accepted `M0-W` or release-grade `E1`.

Structured authority remains fail-closed. The instance and local task DAG remain `planned` with
zero accepted states. The registry and graph predate proof acceptance, their evidence graph does not
contain the proof or validation receipts, and the root-to-`THM-M-0414-TRUST` edge remains an
`open_release_gate`. Existing files also disagree on unaccepted H/R proposals: the instance retains
`H2/R3`, while the anchor audit proposes `H1/R4`. Release preserves the weaker accepted authority.

`AUDIT-Z` is false because there is no accepted complete inventory/source-boundary reconciliation,
pinpoint H0 source mapping with independent review, or independently reviewed R0 reconstruction.
`THEOREM-Z` additionally lacks complete transitive provenance and TCB closure, immutable clean
input, empty-cache network-denied cold build, offline restoration, complete SBOM/licenses, two
signed independent-runner attestations, an independently implemented minimal verifier, protected
release CI, and a deterministic content-addressed evidence bundle.

## Commands and results

Commands ran from the isolated worker clone on 2026-07-14 (`Asia/Shanghai`). The pre-existing
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, or network operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0414` | 0 | Rank 69 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 -B Stage1_Instances/THM-M-0414/check_release.py` | 0 | Content-bound authority and predecessor evidence agreed; the narrow Lean replay passed and the exact blocked terminal decisions held. |
| `python3 -m json.tool` on the three release JSON artifacts and `.stage1-worker-selftest.json` | 0 | Every structured release artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0414-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0414/check_release.py` | 0 | The checker compiled without writing generated files into the owned path. |
| `git diff --check -- Stage1_Instances/THM-M-0414 .stage1-worker-selftest.json` | 0 | No whitespace errors; the checker also inspected every handoff file. |

Retry requires dependency-legal master acceptance, reconciliation of the proof and validation
proposals into current authority, independently reviewed H0/R0 evidence, closure of
`THM-M-0414-TRUST`, and a separately provisioned hermetic and independent release run that produces
the complete deterministic evidence bundle.

Status boundary: this packet self-tests only the truthful negative release decision. It supplies
no accepted receipt, `E1`, accepted `M0-W`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or
master acceptance.
