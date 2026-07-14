# THM-M-1084 release reconciliation

Item: `S56-M-1084-RELEASE`. Base revision:
`111bbeb1a210ae4e8525a4342012921ab60e466f`; base tree:
`8f705aa79622bf1e9be0665ae1254313df21b4f6`.

## Exact verdict

The verdict is `blocked`. Lifecycle remains `planned`, the recorded root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt is accepted;
neither `AUDIT-Z` nor `THEOREM-Z` is claimed.

The first release-node failure is `dependency.S56-M-1084-VALIDATION.master_acceptance`, represented
by the normative `S56-10.2-DEPENDENCY-ACCEPTANCE` gate. Validation is only `[_]` worker evidence with
`accepted=false` and `release_grade=false`. Its nested first failure is proof master acceptance. The
first mathematical failure is `proof.root_kernel_closure`: neither `M1084-T-INTEGRABLE` nor
`M1084-T-ENTROPY` has a proof body. The first intrinsic release failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact constant-12, open-ball target has genuine but narrow provisional evidence. The release
checker re-elaborates `Statement.lean`, the conditional composition, the Gaussian-MGF package,
finite-cover existence/attainment/positivity, and two separately written partial reconstructions in
disposable output space under `--trust=0` and Bubblewrap network isolation. The audited declarations
are sorry-free and use only `propext`, `Classical.choice`, and `Quot.sound`.

That replay does not prove Dudley's bound. `root_of_integrability_and_entropy_packages` accepts the
two unproved packages as arguments. No body constructs the chaining parents, finite-maximum bound,
constant-12 dyadic sum-to-integral comparison, separability limit, supremum integrability package,
or exact entropy inequality package. The exact root therefore remains open at `M3`.

The structured inputs contain older projections that cannot promote state. The anchor audit calls
the non-exact, unintegrated external `SLT.dudley` near candidate `M1`; however it was not replayed
locally or independently, its type differs materially, and rev-5.6 requires at least `E2` for `M1`.
The later instance and validation receipt correctly retain the exact root at `M3`. The frozen graph
also uses older root `H2/R4` projections while the instance records `H1/R3`; none has accepted evidence
IDs, so the authoritative recorded vector is preserved rather than synthesized upward.

`AUDIT-Z` is unavailable: the exact primary-source theorem/page, assumptions, normalization, errata,
node crosswalk, and independent `H0` review remain open, as does an independently reviewed `R0`
reconstruction and full graph/evidence/public-state reconciliation. `THEOREM-Z` additionally lacks
an accepted foundation profile, complete transitive provenance/axiom/TCB closure, immutable clean
empty-cache cold and offline replay, SBOM/licenses and dependency archives, protected adversarial
CI, two independently provisioned signed runners, an independently implemented minimal verifier,
and a deterministic content-addressed release bundle.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The existing pinned `.lake`
symlink was reused without mutation. No `lake update`, `lake build`, dependency clone/fetch, checkout,
or network operation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | The 1546 unique targets in ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1084` | 0 | Rank 526 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py` | 0 | The 16-obligation, 36-edge graph passed while the exact root remained open at M3. |
| `python3 -I -B Stage1_Instances/THM-M-1084/check_release.py` | 0 | Hash-bound authority reconciliation and fresh network-isolated trust-zero replay agreed on the blocked unchanged verdict. |
| `python3 -m json.tool` on the three structured release artifacts and worker packet | 0 | Every JSON artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1084-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1084/check_release.py` | 0 | The checker compiled outside the repository. |
| comment-stripped prohibited-construct scan of all six owned Lean modules | 0 | No placeholder, bodyless, unsafe, external, implementation-escape, or native-oracle construct exists in Lean source. |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The historical `check_validation.py` is intentionally not invoked as the release recipe: it is
bound to the validation phase's older base revision and now-absent phase worker packet. The release
checker content-addresses its committed receipt and independently replays the actual Lean sources at
the current base. This handoff self-tests only the truthful negative release decision.

Retry requires exact terminal proofs and dependency-ordered master acceptance, then accepted
AUDIT-Z/H0/R0, complete trust and supply-chain evidence, cold offline reproduction, qualifying
independent verification, a deterministic bundle, and final master reconciliation.
