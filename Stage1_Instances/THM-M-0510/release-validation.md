# THM-M-0510 release reconciliation

Item: `S56-M-0510-RELEASE`

Base revision: `19eddccb8988b4da9e007b60f4a25b6806877160`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the authoritative root vector remains
`[H2, M3, R4]`, and both `audit_complete` and `theorem_complete` are false. `AUDIT-Z` and
`THEOREM-Z` are blocked. This worker accepts no receipt and makes no release or theorem-completion
claim.

The first failed workflow gate is `dependency.S56-M-0510-VALIDATION.master_acceptance`.
`S56-M-0510-VALIDATION` is only provisional `[_]` evidence with `accepted=false`,
`release_grade=false`, and no master acceptance. Its integrated checker is historical at this base:
it hard-binds revision `472dc79eb4d406a6707691193fbe3ab58d0f0cc4` and the absent validation-turn
worker packet. The first remaining mathematical gate after the provisional Euler-product result is
`M0510-N-COEFFICIENT.kernel_closure`. The first release-input failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`, followed by `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

There is real but narrow positive evidence. The exact statement and its four mutations check. A
fresh trust-zero replay checks all five local Euler-product declarations and reports exactly
`propext`, `Classical.choice`, and `Quot.sound`. The structural checker validates 17 obligations,
59 typed edges, and denominator
`59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd`.

That evidence closes no accepted obligation. The authoritative graph remains pre-proof: it records
the Euler node as `M4`, has no evidence IDs there, and reports an open `M3` root. More importantly,
no checked term constructs the Hardy-Ramanujan root. The coefficient-contour bridge, modular
transformation, major/minor-arc analysis, recomposition, source, and foundation gates remain open.
The declaration `root_of_finalAsymptotic` cannot repair this: it assumes a proposition definitionally
equal to the root and returns that premise, although the graph labels it `M0-L` for a claimed
relative-error transport.

`AUDIT-Z` fails independently. Pinpoint primary-source assumptions and errata, independent `H0`
review, substantive node-specific readable reconstruction, independent `R0` review, complete
inventory reconciliation, and accepted provenance/foundation/trust records are absent. The anchor
inventory also predates the direct `Partition.Glaisher` dependency used by `Proof.lean`.

`THEOREM-Z` additionally lacks an immutable clean snapshot, empty-cache cold build, offline archive
restoration, complete TCB/SBOM/license closure, two independent signed clean-runner attestations, an
independently implemented minimal verifier, protected adversarial CI, a deterministic
content-addressed release bundle, and master acceptance. The automation-provided `.lake` symlink is
shared warm-cache state, so all live evidence here is explicitly nonrelease.

## Validation

Commands ran from this worker clone on 2026-07-15 in the Asia/Shanghai timezone. Existing pinned
Lake artifacts were reused without mutation. No `lake update`, `lake build`, dependency clone,
fetch, checkout, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | Rank 884 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0510/check_statement.py` | 0 | The exact expression, four killed mutations, pinned toolchain, and mathlib revision agreed. |
| `python3 Stage1_Instances/THM-M-0510/check_anchor_audit.py` | 0 | The bounded nine-probe anchor audit and negative status boundary passed. |
| `python3 Stage1_Instances/THM-M-0510/check_obligation_tree.py` | 0 | Seventeen obligations and 59 typed edges passed; the authoritative root remains open `M3`. |
| `python3 -I -B Stage1_Instances/THM-M-0510/check_validation.py --probe` | 1 (expected) | The historical recipe rejected current HEAD at its hard-bound base-revision assertion; it was not misreported as current release evidence. |
| `bash Stage1_Instances/THM-M-0510/check_proof.sh` | 0 | A fresh trust-zero replay checked five Euler-product declarations, observed only the three permitted axioms, and reported the root open `M3`. |
| `python3 -I -B Stage1_Instances/THM-M-0510/check_release.py` | 0 | Reconciled current authority and evidence hashes, reran the live narrow proof check, and derived the exact blocked verdict. |
| `python3 -m json.tool` on the release spec, decision, receipt, and worker packet | 0 | All structured release artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0510-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0510/check_release.py` | 0 | The checker compiled without adding generated files under the owned path. |
| `git diff --check -- Stage1_Instances/THM-M-0510 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Retry requires dependency-legal master acceptance and a current validation replay, truthful graph
reconciliation, real checked bodies for the complete circle-method path and premise-free root,
independently reviewed `H0`/`R0` and `AUDIT-Z`, full provenance and trust closure, and a separately
provisioned hermetic and independent release protocol closing every remaining gate.

Status boundary: this artifact self-tests only the negative release decision. It supplies no
accepted root proof, `M0`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master
acceptance.
