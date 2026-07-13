# THM-M-0995 release-phase reconciliation

Item: `S56-M-0995-RELEASE`

Base revision: `4d2c77230343716176b4192dc38e26f4c20c7547`

## Exact verdict

`blocked`. Lifecycle remains `planned`; the accepted root vector remains
`[H2, M3, R3]`; `audit_complete=false` and `theorem_complete=false`. This
worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, or master-acceptance claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0995-VALIDATION` is only a provisional `[_]` projection. Its receipt has
`accepted=false` and `release_grade=false`, and neither it nor its transitive
prerequisites has been master accepted. The first release-input failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`; the next release-protocol failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact frozen Bernstein target has substantive provisional machine evidence.
The current network-isolated `--trust=0` replay elaborates the exact statement,
the corrected registry-v2 child-to-parent composition, two exact local root
proofs, the registry-v1 optimizer refutation, and three validation adapters from
temporary oleans. It emits 31 axiom reports; the exact roots and composition
certificates use exactly `propext`, `Classical.choice`, and `Quot.sound`. The
target Lean sources pass the placeholder, custom-axiom, unsafe, trust-extension,
and generated-artifact scan. This supports a candidate `M0-L` root for later
master reconciliation, not accepted `M0-L`, `E0`, `E1`, or release evidence.

The weaker accepted authority wins. The intake remains `planned` at
`[H2, M3, R3]`, while the later graph's `[H2, M0-L, R4]` root and closed machine
cut are provisional. No accepted receipt or obligation permits this worker to
promote the root.

`AUDIT-Z` is also blocked. The primary-source boundary lacks an independently
accepted edition, exact theorem or passage, premise and constant mapping,
correction and errata review, and H0 crosswalk. Required readable nodes remain
R3/R4 without independently accepted R0 reconstructions. Complete transitive
provenance, foundation, axiom, computation, executable, compiler, plugin, and
TCB closure is absent. The instance and public projections are not fully
reconciled.

Release additionally lacks immutable clean input, an empty-cache cold build,
network-disconnected offline restoration, complete SBOM/licenses and archives,
two signed attestations from separately provisioned runners, an independently
implemented minimal verifier, protected CI and adversarial fixtures, and a
deterministic content-addressed evidence bundle.

## Commands and results

Commands ran from this worker clone on 2026-07-14 (Asia/Shanghai). The pinned
`.lake` link and artifacts were reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, `.lake` mutation, or network request ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0995` | 0 | Rank 275 remains planned, L0/rework-required, and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-0995/check_validation.sh` | 0 | Exact statement, corrected composition, proof roots, and adapters elaborated at trust zero with network denied; 31 axiom reports and three sorry-free adapters passed; output was 10,899 bytes with SHA-256 `c9dd937b380fd9701391a2616452af6278026a9bf7a4a8d1c23ddcdb4a695454`. |
| `python3 -B Stage1_Instances/THM-M-0995/check_validation.py` | 1 (expected stale evidence) | The historical validation recipe failed its base-revision assertion because it is bound to `92246ea92c0c44282c05728798bc7c7e4a5a1464`, not current HEAD; it was not rewritten or credited as a current structured replay. |
| `python3 -B Stage1_Instances/THM-M-0995/check_release.py` | 0 | Reconciled authority, receipts, hashes, provisional Lean evidence, accepted state, and every negative release gate; derived the exact blocked verdict. |
| `PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0995/check_release.py` | 1 (expected) | The fail-closed guard rejected execution with Python assertions disabled. |
| `python3 -m json.tool` on `release-spec.json`, `release-decision.json`, `release-receipt.json`, and `.stage1-worker-selftest.json` | 0 | The three release JSON artifacts and the root packet parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0995-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0995/check_release.py` | 0 | The checker compiled without generating an owned cache file. |
| Parser-aware prohibited-token scan inside `check_release.py` | 0 | No placeholder, custom axiom, bodyless or unsafe declaration, native/oracle, or external implementation escape matched after comments were excluded. |
| `git diff --check -- Stage1_Instances/THM-M-0995 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | No whitespace, CR, NUL, or terminal-newline failure. |

The historical structured validation command
`python3 -B Stage1_Instances/THM-M-0995/check_validation.py` is intentionally not
used as a current release recipe. It is bound to validation base
`92246ea92c0c44282c05728798bc7c7e4a5a1464`, that phase's root worker packet,
and its dirty-path inventory; after integration it fails before replay. This
release checker binds the historical checker and receipt by hash and reruns the
narrow Lean script directly rather than manufacturing the old state.

Retry requires dependency-legal master acceptance and authoritative state
reconciliation, independently reviewed H0/R0 evidence and `AUDIT-Z`, accepted
foundation/provenance/trust closure, and a separately provisioned hermetic and
independent release run closing every remaining gate.

Status boundary: this artifact self-tests only the negative release decision.
It supplies no accepted `M0-L`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
