# THM-M-1278 release-phase reconciliation

Item: `S56-M-1278-RELEASE`

Base revision: `fcfd52dc69db3bf455310be55903278133a15a10`

## Exact Verdict

`blocked`. The lifecycle remains `planned`; the accepted intake vector remains
`[H2, M4, R4]`; and both `audit_complete` and `theorem_complete` are false.
The best provisional evidence is `[H2, M3, R4]`, but the weaker accepted
structured state wins. This worker accepts no receipt and makes no `AUDIT-Z`,
`THEOREM-Z`, release, or theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-1278-VALIDATION` is only a provisional `[_]` worker projection; its
receipt has `accepted=false` and `release_grade=false`, and it has not been
master accepted. The first release-input failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`. The next release gate is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence Reconciliation

The exact canonical statement elaborates, and the network-denied validation
recipe replays two local mean-shift obligations plus separately written
same-worker probes. The four credited declarations report exactly `propext`,
`Classical.choice`, and `Quot.sound`. This evidence closes neither the sharp
Onofri estimate nor the canonical root. The remaining mathematical root cut is
`M1278-L-SHARP-ONOFRI`, `M1278-S-AREA`, and `M1278-S-FINITE`.

The obligation harness also redeclares the statement structures in a nominally
distinct namespace. No checked transport connects its `Root` to canonical
`Stage1Instances.THM_M_1278.OnofriInequality`. The zero-mean proof,
exponential/logarithmic transport, full mean-shift interface, source route, and
root composition remain open. The frozen graph records no accepted closed
obligation.

The older statement checker also cannot currently replay its recorded command:
`python3 Stage1_Instances/THM-M-1278/check_statement.py` exits before invoking
Lean because it tries to express the target file relative to
`Formalizations/Lean` even though the file is outside that directory. Direct
pinned Lean elaboration succeeds, but the broken historical recipe is another
reproducibility failure and is not concealed by the newer narrow validation.

`AUDIT-Z` is independently blocked by missing pinpoint H0 source review and
independently reviewed R0 reconstruction. Release additionally lacks an
accepted foundation policy and complete transitive provenance/TCB closure,
immutable clean input, an empty-cache cold build, disconnected offline
restoration, full SBOM/licenses, two independently provisioned signed runners,
an independently implemented minimal verifier, protected mutation/metamorphic
CI, and a deterministic content-addressed bundle.

## Commands And Results

Commands ran from the worker root on 2026-07-14. The automation-provided pinned
`.lake` link was reused without mutation. No `lake update`, `lake build`, clone,
fetch, checkout, dependency mutation, or network request ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1278` | 0 | Rank 449 remains planned, L0/rework-required, and theorem-incomplete. |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1278/check_validation.py` | 0 | Four modules replayed at trust zero with network denied; the two partial bodies and two separate probes reported exactly the recorded axiom set; root and release gates failed closed. |
| `python3 Stage1_Instances/THM-M-1278/check_statement.py` | 1 | Historical statement checker failed before Lean with `ValueError` from an invalid `Path.relative_to`; its recorded replay is not reproducible as written. |
| `python3 -B Stage1_Instances/THM-M-1278/check_release.py` | 0 | Reconciled manifest/DAG state, hashes, receipts, graph, current narrow Lean evidence, and every negative release gate; derived the exact blocked verdict. |
| `PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-1278/check_release.py` | 1 (expected) | The fail-closed guard rejected execution with Python assertions disabled. |
| `python3 -m json.tool` on the three release JSON files and `.stage1-worker-selftest.json` | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1278 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink points at a
shared canonical pinned cache. It makes this a nonrelease worker checkout even
though the Lean subprocesses use a read-only filesystem and denied network.

Retry requires dependency-legal master acceptance after closing the sharp
estimate, sphere normalization and side conditions, transports, canonical
bridge, and root composition. A separate release lane must then close H0/R0 and
`AUDIT-Z`, full trust and supply-chain evidence, cold/offline reproduction,
independent attestations and verifier, mutation gates, deterministic bundling,
`THEOREM-Z`, and final master acceptance.

Status boundary: this artifact self-tests only the negative release decision.
It supplies no accepted `M0`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, independent verification, or master acceptance.
