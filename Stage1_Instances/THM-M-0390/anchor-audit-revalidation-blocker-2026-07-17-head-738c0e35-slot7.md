# THM-M-0390 Anchor-Audit Revalidation: Blocked

Item `S56-M-0390-ANCHOR_AUDIT` was rechecked at base
`738c0e35f61cf22c1ab5e31a5cd0ad6432f12f01` (tree
`90fca08279c74cf64ace6ae4fa9fbe4fa31896dc`) in claim order
`(v2 rank 4, phase layer 2, S56-M-0390-ANCHOR_AUDIT)`.

## Verdict

`blocked`. The bounded six-candidate classification is still useful, and no
new exact terminal Catalan/Mihailescu proof appeared. However, the only
contract-declared, HEAD-tracked validator cannot prove the phase predicate on
this claim base. Its exact replay exits `1` with one schema-valid semantic JSON
object reporting `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `message="repository revision drift"`.

The validator SHA-256 is
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`
and its HEAD Git blob is `50c2541e90f0f01795bb51b18b25a13bf9660137`.
It freezes base `c5037228...`, tree `78b2627e...`, and theorem-DAG digest
`fb17743f...`; the current values are `738c0e35...`, `90fca082...`, and
`6ce46e0d...`. The HEAD scheduler policy protects every declared validator
candidate from worker edits, so this worker neither changed that file nor
introduced an alternate candidate.

The existing `anchor-audit-receipt.json` is not a current replacement. It is
also bound to base `c5037228...`. Current-base role resolution fails with
`phase receipt base_revision disagrees with worker base`. Historical-base role
resolution independently rejects `inputs.discovery_evidence[0]` because its
`binding_boundary` field is outside the contract's closed binding schema.
Consequently there is no truthful current-base receipt and immutable-validator
pair that can support a self-test handoff.

## Dependency And Reuse Boundary

The supplied direct/transitive hard-parent inspection order is exactly empty;
that complete empty closure was traversed once, in order, before any possible
proof work. No proof work was performed. There are no hard edges or reuse
hints.

The sole weak group `SHARED-MODULE-32f9c9eb1b52d871` was checked through
`THM-M-0133`. It is only a nonblocking co-mention of
`Mathlib.NumberTheory.FLT.Polynomial`: the provider root is open and none of
its declarations proves `CatalanStatement`. The correct decision remains
`not_applicable`; no declaration, receipt, checkbox, or proof credit transfers.

The tracked schema-1.1 ledger has the correct stable dependency context
`a615cea5...c1598`, empty inspection arrays, the weak-group decision, and no
unresolved compatibility obligation. But it records the earlier graph digest
`fb17743f...` and revision `c5037228...`, not the required current graph
`6ce46e0d...` and base `738c0e35...`. Refreshing only that ledger would fail
the unchanged validator's pinned ledger hash and cannot establish the phase
predicate, so this blocker records the discrepancy without manufacturing a
partial packet.

## Stale Evidence Found

The canonical pinned cache now contains
`Mathlib/NumberTheory/FLT/Polynomial.olean` (SHA-256
`7a4c5f1b...11337e`, 48088 bytes). A scratch, read-only `lake env lean` probe
successfully imported the module and printed `Polynomial.flt_catalan` at its
field-polynomial type. Existing audit files instead say this olean is absent.
That changes dependency-feasibility evidence, but not candidate credit:
`Polynomial.flt_catalan` still has a materially different carrier, equation,
hypotheses, and constant-degree conclusion, so it remains `M5` for the root.

There is also an internal content binding error. `discovery-evidence.json`
records the current SHA-256 `00144249...9fd1` for
`anchor-audit-validation.md` but the predecessor Git blob `7ed460eb...`; the
actual HEAD blob is `f992749b...`. The protected validator would reject this
after its revision check is repaired.

## Narrow Validation

All dependency use was read-only. No network request, Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py` | 1 | exactly one typed JSON result; `repair_required`, first failure `ANCHOR-AUDIT-SEMANTIC-CHECK`, message `repository revision drift` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Statement.lean` | 0 | exact Init-only target and boundary fixtures elaborated; three sandbox stream-fd warnings were nonfatal |
| `cd Formalizations/Lean && lake env lean /tmp/thm_m_0390_polynomial_import_probe.lean` | 0 | imported the pinned polynomial module and printed `Polynomial.flt_catalan`; no build was run |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranked L0/rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0390` | 0 | rank 4, planned, theorem incomplete |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | expected post-edit integration boundary: fresh deterministic generation includes the two new target blocker files, while this worker cannot rewrite the checked-in theorem-DAG projection |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | same target-scoped evidence-inventory projection drift; master integration must regenerate and validate the read-only DAG |

## Retry Condition

An authority-maintenance/master action outside this worker handoff must first
land one corrected declared validator together with a refreshed target ledger,
inventory, discovery evidence, validation record, and sole phase receipt
against one current graph/base. It must fix the closed role bindings and both
stale evidence findings while preserving the honest negative classifications
and zero root proof credit. A fresh claim must then start from a base that
already contains that unchanged validator blob; only then can
scheduler-selected replay, complete HEAD SHA-256/Git-blob role resolution,
independent review, and the dependency-ordered master CAS proceed after the
statement predecessor is accepted `[x]`.

This is current-base target-scoped blocker evidence only. It does not satisfy
the anchor-audit phase, propose `[_]`, replace the phase receipt or validator,
claim audit/theorem completion, change task state, or claim master acceptance.
Because the assigned phase is not genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
