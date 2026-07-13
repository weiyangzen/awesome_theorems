# THM-M-0276 release-phase reconciliation

Item: `S56-M-0276-RELEASE`

Base revision: `9f2a15ae074a155a719c4b743df26f1e993312da`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H2, M3, R4]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or
theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0276-VALIDATION` is only a provisional `[_]` worker projection. Its
receipt has `accepted=false`, `release_grade=false`, and
`content_addressed=false`, and it has not been master accepted. The first
release-input failure is `S56-RELEASE-IMMUTABLE-CLEAN-INPUT`; the next release
gate is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact frozen Real-and-Complex Banach open-mapping target has substantive
provisional machine evidence. `Proof.lean` specializes the pinned transparent
`ContinuousLinearMap.isOpenMap` body to both scalar branches, checks direct and
frozen-composition roots, and transports the result to the expanded open-image
statement. A fresh isolated trust-zero replay reports all three upstream and
nine local declarations sorry-free, with every axiom report exactly `propext`,
`Classical.choice`, and `Quot.sound`. The integrated validation packet also
records a separately written same-worker root. This supports only a candidate
`M0-W` route for master review, not accepted `M0-W`, `E0`, or `E1` evidence.

Structured authority remains weaker and therefore wins. `instance.json` and
the frozen graph stay `planned` at `[H2, M3, R4]`, with `root_closed=false`, no
accepted obligation, and no accepted receipt. The local task DAG predates the
integrated proof and validation packets. Fourteen internal source-body
decompositions lack exact abstract-child composition certificates and receive
no individual closure credit. Only the integration lane may reconcile those
surfaces.

`AUDIT-Z` is blocked independently of the root wrapper. The admitted lecture
notes print a unit-ball Baire cover where the later proof requires radius-`n`
balls, and there is no accepted correction, primary-source mapping, or
independent H0 review. There is also no independently reviewed R0 structured
reconstruction. Release further lacks accepted full transitive provenance and
TCB closure, immutable clean input, empty-cache cold build, offline restoration,
complete SBOM and licenses, two independent signed runner attestations, an
independently implemented minimal verifier, protected CI and mutation evidence,
and a deterministic content-addressed bundle.

## Commands and results

Commands ran from the worker root across 2026-07-13 and 2026-07-14 in the
Asia/Shanghai timezone. The automation-provided pinned `.lake` link was reused
without mutation. No `lake update`, `lake build`, clone, fetch, checkout,
dependency mutation, or network request ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0276` | 0 | Rank 1282 remains planned, L0/rework-required, and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-0276/check_proof.sh` | 0 | Exact direct, frozen-composition, and expanded roots elaborated; 12 declarations were sorry-free and all reported exactly the selected classical axiom trio. |
| `python3 -B Stage1_Instances/THM-M-0276/check_release.py` | 0 | Reconciled immutable packet hashes, authority, structured state, fresh narrow Lean evidence, and every negative release gate; derived the exact blocked verdict. |
| `python3 -m json.tool` on the release spec, decision, receipt, and root self-test packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0276-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0276/check_release.py` | 0 | The checker compiled without creating a generated owned file. |
| Scoped prohibited-token scan over the target Lean modules | 1 (expected) | No `sorry`, `admit`, `sorryAx`, custom axiom, bodyless declaration, unsafe/opaque/native/oracle, or external implementation escape matched after comments were excluded. |
| `git diff --check -- Stage1_Instances/THM-M-0276 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | No whitespace, CR, NUL, or terminal-newline failure. |

The historical command
`python3 -B Stage1_Instances/THM-M-0276/check_validation.py` is not a current
release recipe. It is intentionally bound to the validation turn's base
revision, worker packet, and exact dirty-path inventory. This release checker
binds that validator and its receipt by hash and replays the narrow proof
directly instead of manufacturing historical state.

Retry requires dependency-legal master acceptance and truthful graph and task
reconciliation, checked internal composition, independently reviewed H0/R0 and
`AUDIT-Z` evidence, accepted foundation/provenance/trust closure, and a
separately provisioned hermetic and independent release run closing every
remaining gate.

Status boundary: this artifact self-tests only the negative release decision.
It supplies no accepted `M0-W`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
