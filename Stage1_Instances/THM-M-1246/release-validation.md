# THM-M-1246 release decision

Item `S56-M-1246-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
authoritative root vector remains `H2/M3/R4`, and both `AUDIT-Z` and `THEOREM-Z` are false.
`theorem_complete` remains false, and this worker accepts no receipt or obligation closure. This is
a self-tested negative release reconciliation, not theorem completion or master acceptance.

## Evidence reconciliation

The exact frozen Hardy root has strong provisional evidence. A fresh network-isolated Lean replay
at trust level zero elaborated the statement, conditional composition, local proof terminal/root,
and the reconstruction that does not import the `Proof` module. All six audited declarations are
sorry-free and report exactly `propext`, `Classical.choice`, and `Quot.sound`. The output is 30,446
bytes with SHA-256 `cd4a55ba...27d4d3`. This is evidence for a repo-local proof body, so its correct
possible class after acceptance is `M0-L`, not the predecessor receipt's `M0-W` proposal.

The weaker authoritative state still wins. The direct prerequisite `S56-M-1246-VALIDATION` is only
`[_]`, and its receipt has `accepted=false`, `release_grade=false`, and `content_addressed=false`.
The first failed node gate is therefore
`dependency.S56-M-1246-VALIDATION.master_acceptance`. The typed graph also still records
`root_closed=false`, machine debt `M3`, and root cut `M1246-T-ANALYTIC`; its literal punctured-domain
cutoff leaves have not been reconciled with the positive-denominator regularization implementation.

`AUDIT-Z` fails because the inventory and public projections are not fully reconciled, the source
record has no accepted pinpoint primary-source and independent `H0` review, and no independently
reviewed `R0` reconstruction exists. `THEOREM-Z` additionally lacks accepted foundation and full
transitive provenance/TCB closure, immutable clean release input, empty-cache offline cold replay,
complete SBOM/license archives, distinct signed runners, an independently implemented minimal
verifier, protected adversarial CI, and a deterministic content-addressed bundle. The first
release-specific failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Validation

Commands were run from the repository root on `2026-07-15`.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1246` | 0 | Rank 426, planned, theorem incomplete. |
| `bash Stage1_Instances/THM-M-1246/check_validation.sh` | 0 | Network-isolated trust-zero replay passed; six sorry-free reports and the expected three-axiom closure. |
| `python3 -B Stage1_Instances/THM-M-1246/check_release.py` | 0 | Current hashes, authority, dependency, graph, trust, and every fail-closed release decision agreed. |
| `python3 -m json.tool` on the four structured handoff files | 0 | Every JSON artifact parsed. |
| `python3 -m py_compile Stage1_Instances/THM-M-1246/check_release.py` | 0 | Checker compiled with bytecode directed outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-1246 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The replay uses the pinned shared warm dependency cache read-only and creates only temporary module
outputs. It runs no update, build, clone, fetch, or dependency mutation. Retry requires
dependency-legal master acceptance and architecture reconciliation, followed by all source,
readability, trust, supply-chain, hermetic, independent-verification, deterministic-bundle, and
master release gates named in `release-decision.json`.
