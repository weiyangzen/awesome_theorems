# THM-M-0861 release reconciliation

Item `S56-M-0861-RELEASE` has the exact verdict `blocked`. The lifecycle remains
`planned`, the authoritative root vector remains `[H1, M4, R4]`, and both
`audit_complete` and `theorem_complete` are false. This worker accepts no
receipt or obligation and proposes only `[_]` for integration review of the
negative release decision.

## First failed gates

`S56-10.2-DEPENDENCY-ACCEPTANCE` fails first. `S56-M-0861-VALIDATION` is a
provisional `[_]` worker projection whose receipt says `accepted=false` and
`release_grade=false`. Release is therefore not dependency-legal for master
acceptance. That receipt in turn records
`dependency.S56-M-0861-PROOF.master_acceptance` as its first failure.

The first mathematical failure is `M0861-T-SATZ-C`. The bounded anchor audit
and target packet identify no placeholder-free inhabitant of
`BoundedSatzCTarget`; this is bounded absence evidence, not an exhaustive claim
about all Lean projects. Both target-local exact-root declarations take that
package as an explicit premise, so neither is an unconditional proof. The
remaining mathematical root cut is `M0861-T-UPPER`.

The first release-specific failure is immutable clean input. The next is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`: the available network-isolated
replay uses the automation-provided shared warm pinned `.lake` closure. It is
not an empty-cache cold build or a content-addressed offline restoration.

## Evidence reconciled

The positive machine evidence is real but partial and provisional. A fresh
Bubblewrap replay with network denied elaborates the exact statement, audited
anchor probes, conditional obligation composition, all nine partial proof
declarations, and the separate conditional root composition at Lean trust
level zero. The ten checked roots are sorry-free and expose only `propext`,
`Classical.choice`, and `Quot.sound`. This does not close Satz C or the theorem.

The structured authority stays weaker. The instance and typed graph retain an
empty accepted receipt and obligation set, `root_closed=false`, and H1/M4/R4.
The local task DAG is entirely open and the instance projection still reflects
intake-era formal-target fields. Release records those discrepancies rather
than rewriting predecessor-owned authority.

`AUDIT-Z` remains blocked by unreconciled evidence links, absent accepted H0
primary-source review, and absent independently reviewed R0 reconstruction.
`THEOREM-Z` additionally lacks exact upper/root closure, accepted composition
and foundation state, complete transitive provenance/trust/TCB, an SBOM and
license archive, immutable clean cold/offline reproduction, a deterministic
bundle, two distinct signed runner attestations, an independently implemented
minimal verifier, protected release CI, and master acceptance.

## Commands and results

Commands ran from the worker clone on 2026-07-15 (Asia/Shanghai). The pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, dependency mutation, or network request ran.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | Rank 1415; planned; L0/rework-required; theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0861/check_release.py` | 0 | Target, DAG, hashes, fresh network-isolated trust-zero replay, and blocked `AUDIT-Z`/`THEOREM-Z` decisions passed. |
| `/usr/bin/python3 -O -I -B Stage1_Instances/THM-M-0861/check_release.py` | 1 | Expected: the checker refuses optimized Python with assertions disabled. |
| `python3 -m json.tool` on the three release JSON artifacts and worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0861-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0861/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0861 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The release checker is the terminal node-specific recipe and performs the
fresh Lean replay itself. It does not accept the historical validation receipt
as current solely because that receipt's prose says the old run passed.

Status boundary: this is only a self-tested negative release decision. It
grants no accepted `H0`, `M0`, `E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, independent verification, or master acceptance.
