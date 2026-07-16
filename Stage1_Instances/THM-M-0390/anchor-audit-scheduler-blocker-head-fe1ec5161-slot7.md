# THM-M-0390 anchor-audit scheduler blocker

Item: `S56-M-0390-ANCHOR_AUDIT`

Worker base: `fe1ec5161fd86894fef54d2a1860437053d9e8d7` (tree
`3777ff4ba4b38bc02217f033c19d32763d75d039`)

Claim order: `(v2 rank 4, phase layer 2, S56-M-0390-ANCHOR_AUDIT)`

Verdict: `blocked`; authoritative state remains `[_]`;
`phase_accepted=false`

## First failed gate

`G05-AUTHORITY-REPLAY.immutable_HEAD_validator_is_stale_for_worker_base`

The HEAD anchor-audit contract declares two scheduler-owned candidates. Exactly
one exists: `Stage1_Instances/THM-M-0390/check_anchor_audit.py`, SHA-256
`36b8d075f9a09ecd598ad0a69696265644dee6b984c83b87a0c89537126bad08`,
Git blob `50c2541e90f0f01795bb51b18b25a13bf9660137`. The worker did not
change it or add the alternate candidate.

Its exact authority-selected replay is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0390/check_anchor_audit.py
```

It exits `1` and emits one `stage1-validator-semantic-result/1.0` JSON object
with `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `message="repository revision drift"`.
The validator pins base `c5037228...`, tree `78b2627e...`, theorem-DAG
`fb17743f...`, and old target artifact hashes. The assigned base is
`fe1ec516...`, tree `3777ff4b...`, with theorem-DAG SHA-256 `6d0668e7...`.
Scheduler policy forbids this worker from refreshing either declared candidate.

The tracked `anchor-audit-receipt.json` is not current evidence. It is also
bound to `c5037228...` and includes incomplete or closed-schema-invalid role
bindings. Rewriting it without a passing unchanged validator would manufacture
a second false claim rather than satisfy the exactly-one-receipt contract.

## Dependency and reuse audit

The supplied direct/transitive `parent_inspection_order` is exactly empty. That
complete empty closure was traversed once, in order, before any possible proof
work. No proof work was performed; there are no hard edges or reuse hints.

The one weak group, `SHARED-MODULE-32f9c9eb1b52d871`, was re-inspected through
`THM-M-0133`, including its current seven `[_]` phase states, anchor audit,
statement, proof body, and validation receipt. Its target is Fermat's Last
Theorem and its root remains open. `Polynomial.flt_catalan` is a theorem over
field polynomials concluding constant degrees, not a proof or checked transport
for the natural-number `CatalanStatement`. The decision remains
`not_applicable`; no declaration, receipt, checkbox, acceptance, or proof credit
transfers.

The tracked schema-1.1 `dependency-reuse-ledger.json` records the right stable
context, empty hard-parent inspection, weak-group decision, and no unresolved
compatibility obligation. It is nevertheless stale on graph digest and
repository revision. Refreshing only that file would immediately violate the
unchanged validator's pinned ledger hash and cannot create a lawful phase
packet, so this blocked run records the discrepancy rather than manufacturing a
partial self-test.

## Stale evidence

The canonical read-only pinned cache contains
`Mathlib/NumberTheory/FLT/Polynomial.olean` (SHA-256
`7a4c5f1b...11337e`, 48088 bytes). A trust-zero scratch probe imports the module
and elaborates `Polynomial.flt_catalan` without a Lake build, update, clone, or
fetch. Existing audit files incorrectly say that olean is unavailable. This
changes dependency-feasibility evidence only: the theorem's material statement
mismatch still gives no Catalan root credit.

`discovery-evidence.json` also pairs the current SHA-256
`00144249...9fd1` of `anchor-audit-validation.md` with its predecessor Git blob
`7ed460eb...`; the actual HEAD blob is `f992749b...`. That is not a valid
content/blob binding.

## Validation

At the untouched base, the standard, v2 DAG, phase-contract, target-manifest,
and target-show checks all exit `0`. Trust-zero `lake env lean` elaboration of
the exact `Statement.lean` and the pinned polynomial import probe also exits
`0`. The scheduler-owned semantic validator exits `1` with the typed negative
result above. No dependency source or build artifact was changed.

The structured JSON blocker records the exact argv, exit codes, semantic
result, source/artifact hashes, current dependency pins, and command summaries.
Adding these target-owned blocker files will make the generated theorem-DAG
evidence inventory differ from the checked-in projection. This worker does not
edit that forbidden authority; scheduler integration must regenerate it before
aggregate post-edit validation.

## Retry condition

The scheduler or authority-maintenance lane must land one coherent packet with
a corrected declared validator plus a refreshed ledger, inventory, discovery
evidence, validation record, and sole phase receipt bound to one graph/base. It
must fix the olean and Git-blob findings and use complete
path/SHA-256/Git-blob role bindings. A fresh claim must start from a base that
already contains the unchanged corrected validator, then replay it successfully
and emit the required worker self-test. Master acceptance remains ordered after
the statement predecessor becomes `[x]`.

This is current-base, target-scoped blocker evidence only. It does not satisfy
the phase, refresh the receipt or ledger, transfer acceptance, claim proof
credit, `AUDIT-Z`, `THEOREM-Z`, theorem completion, task-state change, or master
acceptance. Because the phase is not genuinely self-tested,
`.stage1-worker-selftest.json` is deliberately absent.
