# THM-M-0451 validation-phase result

Item: `S56-M-0451-VALIDATION`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`. The successful scoped replay
ran from `2026-07-15T05:49:34+08:00` to `2026-07-15T06:02:29+08:00`.

## Validated scope

The node-scoped runner copied `Statement.lean`, `AnchorAudit.lean`,
`ObligationTree.lean`, `Proof.lean`, `ProofAudit.lean`, and `Validation.lean`
to a disposable directory. Every Lean process used the pinned executable at
trust level zero inside Bubblewrap with outbound network unshared, the host
root read-only, and only the disposable module directory writable.

The frozen conditional composition, eleven proof-phase declarations, and the
separately implemented split-field target adapter are recursively sorry-free.
All thirteen complete `#print axioms` reports are exactly `propext`,
`Classical.choice`, and `Quot.sound`. The validator parses each full report;
an unknown additional axiom cannot be hidden by searching only for allowed
names.

This is narrow partial validation, not theorem completion. `Proof.lean` still
requires the elliptic height estimates and supplies no zero-height-to-torsion
body. The adapter likewise consumes an uninhabited engine. No frozen
obligation receives accepted closure.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Trust-zero kernel replay | pass | The statement carrier, conditional composition, eleven partial proof declarations, selected recursive sorry closures, and split-field adapter elaborate from copied sources. |
| Local trust hygiene | pass | The full observed axiom sets are exact, and the comment-aware source scan finds no `sorry`, `admit`, axiom/constant/opaque/unsafe/external implementation, or native oracle. |
| Selected provenance | partial pass | Target hashes and selected clean pinned mathlib source/blob/olean/remote/license identities agree; complete transitive proof-body/TCB/SBOM closure is absent. |
| Exact root | fail closed | Uniform elliptic height estimates and zero-height-to-torsion are unproved; the engine is uninhabited. |
| Source fidelity | fail closed | The target calls unscaled `Height.logHeight` absolute, while the pinned number-field formula has total place weight `[K:Q]`; the Silverman normalization and possible degree factor need resolution. |
| Structured authority | fail closed | The proof receipt is provisional, and the accepted typed graph/local task DAG remain pre-proof. Only master integration may reconcile the proposed progress. |
| Hermetic release | fail closed | Network was denied, but the canonical dependency cache is shared and warm rather than a clean empty-cache cold build restored from an offline archive. |
| Independent verification | fail closed | The adapter uses the same worker, checkout, kernel, and cache; no second signed attestation or distinct independently provisioned verifier exists. |

## Commands and results

All commands ran from the worker clone. No `lake update`, `lake build`, clone,
fetch, network request, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | rank 93 remains planned, rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0451/check_anchor_audit.py` | 0 | 4/4 candidates, statement and pinned source hashes, and anchor probes agreed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0451/check_obligation_tree.py` | 0 | 17 obligations and 44 typed edges passed with the exact root open. |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -I -B Stage1_Instances/THM-M-0451/check_validation.py` | 0 | network-denied trust-zero replay, exact axiom parsing, source hygiene, hash/pin/provenance binding, and all fail-closed decisions passed; stdout SHA-256 `c3f63daa...79e91`, 847 bytes. |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0451 .stage1-worker-selftest.json` | 0 | no whitespace errors. |

The recorded proof checker remains snapshot-bound to
`c45f3c7090cb4adf616d45e5414985f956e807b2` and rejects current HEAD before
replay. This validation refreshes kernel observation at the current base; it
does not supersede proof acceptance.

The accepted root vector remains `[H1, M3, R3]`, `audit_complete=false`, and
`theorem_complete=false`. The first dependency gate is proof master
acceptance; the first theorem gate is `M0451-APPROX`; the first release gate is
the section 10.6 cold hermetic build. This packet proposes only worker `[_]`
evidence for the validation node itself.
