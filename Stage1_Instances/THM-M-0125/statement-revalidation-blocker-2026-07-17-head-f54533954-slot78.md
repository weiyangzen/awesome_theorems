# THM-M-0125 Statement Revalidation: Blocked

Item `S56-M-0125-STATEMENT` was rechecked at base
`f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`) in claim order
`(v2 rank 278, phase layer 1, S56-M-0125-STATEMENT)`.

## Verdict

`blocked`. The only contract-declared, HEAD-tracked validator is
`Stage1_Instances/THM-M-0125/check_statement.py`. Its SHA-256 is
`ee7b12276f34af731b38b9155c0c119ad0accc0347527533a679ded16b7eef31`
and its HEAD Git blob is `ea899a7a5d8f22d9d40b5052d1bc181d5110232c`.
The validator is immutable to this worker and freezes base `1cc6aa61...`, tree
`dc3053b5...`, and theorem-DAG digest `e8472863...`; the current values are
`f5453395...`, `6dc92413...`, and `39dc7ce5...`.

Its exact scheduler-declared replay exits `1` and emits exactly one typed JSON
object reporting `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and first failure `S01-ARTIFACTS`. The message
is `negative statement packet validation failed: repository HEAD differs from
the claimed worker base`. Standard output is 486 bytes including its final LF,
with SHA-256 `d8a3deba...1bd1df`; standard error is empty.

Exactly one regular, non-symlink candidate exists, so selection is not
ambiguous. The failure is semantic freshness. The scheduler protects every
declared validator candidate, so this worker neither edited it nor created an
adapter. The sole `statement-receipt.json` and the schema-1.1 dependency ledger
are likewise bound to the historical base. Replacing either alone would break
the validator's content bindings and would not establish the positive phase
predicate. They remain untouched, and there is no current-base replacement
receipt or truthful self-test handoff.

## Dependency And Reuse Boundary

The supplied direct/transitive hard-parent inspection order is exactly empty.
That complete empty closure was traversed once, in order, before any possible
proof work. There are no hard edges, reuse hints, or shared groups. No proof
work was performed, and no declaration, receipt, checkbox, or acceptance credit
transfers.

The existing ledger correctly records schema 1.1, the stable dependency context
`068170c7...c5c`, empty inspections and decisions, and no compatibility
obligations. It nevertheless records graph `e8472863...` and revision
`1cc6aa61...`, rather than current graph `39dc7ce5...` and revision
`f5453395...`. Refreshing it in isolation would invalidate the historical
receipt binding and fail the unchanged validator's pinned hash. This blocker
therefore records the current empty-closure audit without manufacturing a
partial packet.

## Independent Statement Blocker

Even after scheduler freshness is repaired, the positive `S02-EXACT-TARGET`
predicate remains false. The repository gives only the gloss
"elliptic-curve derivative formula." Gross and Zagier's 1986 paper contains at
least three materially different candidates consistent with that gloss:

| Candidate | Source locator | Material boundary |
|---|---|---|
| General Rankin formula | I.(6.3), journal page 230 | A weight-two newform, class-group character, Rankin derivative, Heegner divisor, and explicit normalization factors |
| Elliptic application | I.(7.3), journal page 231 | `L'(E,1)` and the canonical height of a rational point, up to period and rational factors |
| Elliptic base-change identity | V.(2.1), journal page 311 | `L'(E/K,1)`, a modular parametrization, differential norm, traced Heegner point, height, unit index, and discriminant |

The scratch source scan is 4,395,679 bytes over 96 pages with SHA-256
`8afee839...d9521`; it is not a durable repository artifact. No authoritative
record or independent review selects one candidate, freezes its incorporated
definitions and normalizations, or supplies concrete Lean arithmetic objects.
Inferring an exact formula from OCR or the short catalog gloss would broaden,
narrow, or substitute the assigned theorem.

`Statement.lean` is explicitly a two-import boundary probe, not a canonical
Gross-Zagier declaration. With trust level zero it elaborates the generic
`WeierstrassCurve` and `HasDerivAt` interfaces. That proves only that the pinned
substrate is available; it supplies no exact expression, fingerprint,
transport, mutation result, statement acceptance, or proof credit.

## Narrow Validation

All dependency use was read-only. No network request, Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0125/check_statement.py` | 1 | exactly one typed JSON result; `repair_required`, first failure `S01-ARTIFACTS`, current HEAD differs from the claimed base |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0125/Statement.lean` | 0 | the two generic boundary interfaces elaborated; three sandbox stream-fd warnings were nonfatal |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 before edit; 1 after edit | pre-edit authority passed; post-edit expected integration boundary because the new target evidence changes the generated theorem-DAG inventory |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before edit; 1 after edit | same expected projection drift; master integration must regenerate and validate the worker-protected DAG |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44, planned, legacy artifacts unaccepted, theorem incomplete |

The post-edit DAG failures are not phase acceptance evidence. They are the
expected projection boundary after adding target-owned evidence: this worker is
forbidden to regenerate or edit `Docs/Stage1_Theorem_DAG_v2.json`.

## Retry Condition

The scheduler or authority-maintenance lane must publish one refreshed declared
validator together with a coherent current-base ledger and sole
`stage1-node-receipt/1.0` packet, then issue a fresh claim whose base already
contains that unchanged validator blob. Independently, after intake master
acceptance, an accountable source owner must select and review exactly one
primary-source theorem or corollary, freeze all definitions and conventions,
encode only that proposition with concrete pinned Lean objects, fingerprint it,
check any transports, and execute all four required mutation classes.

This is current-base target-scoped blocker evidence only. It does not satisfy
the statement phase, propose `[_]`, replace a selected phase artifact or
validator, claim audit/theorem completion, change task state, or claim master
acceptance. Because the phase is not genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
