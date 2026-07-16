# THM-M-0390 anchor-audit revalidation blocker

Item: `S56-M-0390-ANCHOR_AUDIT`  
Theorem: `THM-M-0390`  
Claim order: `(v2_execution_rank=4, phase_layer=2,
phase_item_id=S56-M-0390-ANCHOR_AUDIT)`  
Worker base revision: `d41a1ade92426e33aade0ff4e796cd5b4da27a44`  
Worker base tree: `c592c028b1d440807661d791cf10af9f4dd08331`  
Worker verdict: `blocked`  
Authoritative state: `[_]` (unchanged)  
Phase accepted: `false`  
Lifecycle: `planned -> planned`  
Accepted root vector: `[H2, M4, R4] -> [H2, M4, R4]`  
Best provisional root evidence: `[H2, M3, R4]` (unchanged)  
Accepted receipt IDs: none

## First failed gate

`G05-AUTHORITY-REPLAY.validator_is_scheduler_owned_but_stale_for_current_base`

The HEAD phase contract declares two candidate paths for `anchor_audit`. Exactly one exists:
`Stage1_Instances/THM-M-0390/check_anchor_audit.py`, with SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08` and Git blob
`50c2541e90f0f01795bb51b18b25a13bf9660137`. The absent alias is
`Stage1_Instances/THM-M-0390/check_anchor.py`, so candidate selection is unambiguous. The selected
validator exists at this worker base with that same blob, and this worker did not change it.

The validator is nevertheless internally pinned to the obsolete pre-integration revision
`c5037228977a81948bbd6119e1728b4b65b9924e`, tree
`78b2627e717156dffe240bea12d14205af667d2a`, and theorem-DAG SHA-256
`fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`. Current HEAD is the base
above and the mandatory DAG digest is
`7c81855adb1d19b7be5dd3dfbbb41dd441b3dc17021d08471909b28018881962`. Running the exact declared
argv therefore exits 1 and emits exactly one schema-valid negative semantic object whose message is
`repository revision drift`, with `phase_accepted=false`, `phase_predicate_proven=false`,
`audit_complete=false`, and `theorem_complete=false`.

Exact argv:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

Exact stdout (463 bytes; SHA-256
`e737f1c1abc68113dc377db8293ce83a978ff3bca827fa90e80206a7cb518abe`):

```json
{"audit_complete": false, "blocked": false, "first_failed_gate": "ANCHOR-AUDIT-SEMANTIC-CHECK", "item_id": "S56-M-0390-ANCHOR_AUDIT", "message": "repository revision drift", "open_obligations": 1, "phase": "anchor_audit", "phase_accepted": false, "phase_predicate_proven": false, "schema_version": "stage1-validator-semantic-result/1.0", "stale_inputs": [], "status": "failed", "theorem_complete": false, "theorem_id": "THM-M-0390", "verdict": "repair_required"}
```

Exit code is 1 and stderr is empty. The stdout is accepted unchanged by
`scripts.stage1_acceptance_evidence._parse_validator_semantic_stdout`.

The contract and execution skill make every declared candidate scheduler-owned and immutable in a
worker handoff. The worker may not refresh, rename, replace, delete, or wrap this validator, and an
undeclared adapter or exit code alone cannot support acceptance. The prior integrated phase receipt
is also stale: it names the obsolete base and tree, and each
`/inputs/discovery_evidence` binding contains fields outside the contract role mapper's closed
binding schema. It therefore cannot be resolved by the mandatory HEAD role mapper for the current
worker base. Those defects require a later base-bound worker receipt, but that receipt cannot
truthfully claim a passed self-test until the scheduler first publishes a refreshed validator.

The prior receipt, validation note, anchor inventory, discovery evidence, and dependency ledger are
retained byte-for-byte as integrated historical observations. They are not refreshed or presented
as current-base evidence: doing so would create dangling bindings while the immutable validator
cannot validate current-base bytes. This blocked attempt adds only this report and creates no
replacement receipt. The unchanged exact declared argv reads the historical receipt, then emits the
schema-valid negative revision-drift result described above. No historical artifact grants
acceptance or a state change at the current base.

`G02-TOPOLOGY` independently remains pending: `S56-M-0390-STATEMENT` is authoritative `[_]`, not
master-accepted `[x]`. Anchor observations may be audited provisionally, but this phase cannot be
master accepted before its predecessor. The first failed gate in the exact validator execution is
`ANCHOR-AUDIT-SEMANTIC-CHECK` with message `repository revision drift`; the scheduler-ownership
staleness label above is this handoff's diagnosis of that result, not a replacement validator field.

## Dependency and reuse audit

The complete hard-parent/transitive-ancestor closure and `parent_inspection_order` are empty. The
empty order was traversed exactly once. There are no hard edges or reuse hints. The sole weak,
nonblocking group is `SHARED-MODULE-32f9c9eb1b52d871`, canonical identity
`Mathlib.NumberTheory.FLT.Polynomial`, with members `THM-M-0133` and `THM-M-0390`.

The integrated `dependency-reuse-ledger.json` remains a historical
`stage1-dependency-reuse-ledger/1.1` observation at its recorded repository revision and DAG
digest; this blocked attempt does not refresh it. Its context digest remains
`a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598`, matching the current
dependency context. The topology itself is unchanged, and the current DAG independently confirms
the same empty parent order and sole weak group. The recorded group decision remains
`not_applicable`: the provider target is Fermat's Last Theorem, while
`Polynomial.flt_catalan` is over `k[X]` and concludes three constant degrees. No exact body,
checked transport, receipt identity, checkbox state, or acceptance credit is consumed or
inherited. A current-revision ledger and its mandatory receipt binding must be produced only after
the scheduler refreshes the validator.

Inspected parent IDs: none. Reused declaration IDs: none. The remaining root cut set is the
scheduler-owned validator refresh and predecessor acceptance for this phase, followed downstream by
the open exact Catalan proof branches, source/readability review, trust/provenance closure, hermetic
replay, and independent verification. This audit blocker does not attempt those later-phase gates.

## Bounded anchor evidence

The frozen inventory remains a truthful six-candidate classification over all seven required lanes:
repo-local, pinned mathlib, official primary project, other immutable public projects,
statement-only collections, historical/other provers, and primary human sources.

- Repo-local and same-claim files provide exact statement shapes, finite checks, and open proof
  architecture only (`M3`); no terminal `CatalanStatement` proof body exists.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, has documentation row `Q174955` without `decl` or
  `decls`. `Polynomial.flt_catalan` is materially incompatible. Support APIs are nonterminal only.
- Formal Conjectures revision `7871d8fc7a8164a1ac16c3765b40c25ce015b681` has the near statement
  `Catalan.catalans_conjecture`, but its body is `by sorry`, its Nat-subtraction surface differs, and
  it is outside the pinned Lean 4.29 closure (`M5`, no proof credit).
- Prior anonymous public discovery was access-limited. Global absence and saturation are not
  claimed. The primary human publication is identified, but exact page/theorem, assumptions,
  errata, and independent H0 review remain open.

The strongest root boundary is unchanged: `M3/E4` formalization debt, no exact terminal candidate,
no H0/R0, no `AUDIT-Z`, and no theorem completion.

## Validation performed

No `lake update`, `lake build`, clone, fetch, or dependency mutation was run. The automation-provided
`.lake` symlink was used read-only.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed negative JSON object, `repository revision drift`, with `phase_accepted=false` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 authorities, v2 DAG, contract, and execution skill pass |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, two hard edges, five hints, and 311 groups pass |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and twenty-three source references pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned, rework required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only statement and four mutation surfaces re-elaborate; stderr also reports three sandbox stream-fd warnings |
| JSON parsing and target-owned binding audit | 0 | integrated historical artifacts remain parseable; exact role-map resolution rejects the historical receipt because its base revision differs from this worker base |
| `git diff --check -- Stage1_Instances/THM-M-0390` | 0 | no whitespace errors |

The declared-validator stdout parses under the scheduler's exact semantic-result parser. Its
negative semantics are authoritative for this attempt; no alternate validator output was used.

## Retry condition

The scheduler must publish a refreshed `check_anchor_audit.py` at a new authoritative commit without
worker participation. A fresh worker base must contain the identical selected validator blob. That
worker can then refresh exactly one phase receipt and its role bindings, run the declared validator,
and emit `.stage1-worker-selftest.json` only if the semantic result is positive. Independent review,
read-only authority replay, and SSOT CAS remain scheduler-owned, and master acceptance still waits
for `S56-M-0390-STATEMENT` to reach `[x]`.

No `.stage1-worker-selftest.json` is produced in this blocked handoff. This report grants no state
transition, no proof credit, and no acceptance.
