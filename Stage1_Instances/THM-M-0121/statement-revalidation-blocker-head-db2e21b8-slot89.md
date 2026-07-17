# THM-M-0121 Statement Revalidation: Blocked

Item `S56-M-0121-STATEMENT` was rechecked at base
`db2e21b8fec263c5b65014acb1ee2039566e35a3` (tree
`815414c57391f2c12871c05a6e3d2944b0f2fef2`) in exact claim order
`(274, 1, S56-M-0121-STATEMENT)`.

## Verdict

`blocked`. The mandatory scheduler-owned validator is present and uniquely selected, but it is
not semantically fresh for this worker base. The HEAD contract selects
`Stage1_Instances/THM-M-0121/check_statement.py`, SHA-256
`c841ab68d902a14de2ba961c98e8ad0a17c9cdbd3e19442587b2dce9d9496e0c`, Git blob
`7ef798a50f2c5b0dbddb63f50a29841ff2baa5e9`. The same blob exists at the worker base. This worker
did not edit it or create the alternate candidate.

Running the exact authority-derived argv

`/usr/bin/python3 -I -B Stage1_Instances/THM-M-0121/check_statement.py`

exited `1`. Stdout was exactly one `stage1-validator-semantic-result/1.0` JSON object, 453 bytes
including its final newline at SHA-256
`b80b5abb48a5e720a15a55d6d5b003bc9f72aab281e0f49e77a4f2eb666ce4dd`. Its semantic result is
`status=failed`, `verdict=repair_required`, `phase_accepted=false`, and
`phase_predicate_proven=false`. The validator fails first because it hard-binds repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, while this claim starts from
`db2e21b8fec263c5b65014acb1ee2039566e35a3`. Every declared validator candidate is
scheduler-owned and immutable, so a worker refresh or replacement is forbidden.

The canonical statement packet is historical negative evidence bound to that earlier base. Its sole
`statement-receipt.json` is `accepted=false`, `verdict=blocked`, and
`phase_predicate_proven=false`. The schema-1.1 dependency ledger binds the earlier graph digest and
repository revision. Replacing only the receipt or ledger cannot make the protected validator pass
and would discard their truthful provenance, so both are preserved.

## Dependency And Reuse Audit

The authoritative theorem DAG has SHA-256
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`; the target's stable
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete direct-parent, transitive-ancestor, hard-edge, reuse-hint, shared-group, and supplied
`parent_inspection_order` lists are all empty. That complete sequence was traversed exactly once
before any possible proof work. No proof work was performed; no parent declaration, terminal body,
receipt, import, copy, or transport was available to inspect or consume. No checkbox state,
acceptance, or proof credit transfers. The empty declared graph context is not a mathematical
independence claim.

The task-state authority records both the intake predecessor and this statement item as `[_]` with
one attempt. Those are unfinished provisional observations, not master acceptance. This recheck
does not propose another state transition or inherit the predecessor's evidence.

## Exact Statement Blocker

The positive statement gate remains independently false. Repository sources still supply only the
label "Mori rationality theorem", Mori attribution, a year, and the gloss "rationality of Fano
varieties". They do not select one immutable proposition. At least these materially different
readings remain unresolved:

- the rationality theorem for a nef threshold in the minimal model program;
- existence of rational curves or uniruledness for Fano varieties;
- rational connectedness of smooth projective Fano varieties.

The unqualified assertion that every Fano variety is birationally rational is false in standard
meanings and is not adopted. Selecting one candidate from the label alone, or treating the legacy
arbitrary-predicate statement shape as exact identity, would invent, broaden, narrow, or substitute
the assigned mathematics. No canonical proposition, ordered binders, hypotheses, conclusion,
boundary cases, expression fingerprint, environment fingerprint, checked transport, or executable
mutation suite therefore exists.

## Narrow Validation

Before adding this blocker, the Stage1 standard, theorem-DAG, phase-contract, and target-manifest
checks all exited `0`. The target has v2 rank 274 and the required empty dependency context.

The narrow Lean replay

`cd Formalizations/Lean && env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0121/Statement.lean`

exited `0`. Stdout was 524 bytes at SHA-256
`f04467486d9f147a5c10c752c6894fa5179a23fbd60f6ae90e38f0c157aa1362`, with empty stderr. It
checked `Scheme.RationalMap`, `Scheme.RationalMap.domain`, and
`Scheme.RationalMap.equivFunctionField`. This is adjacent vocabulary only: the file declares no
canonical target or proof body, so the replay supplies no exact-statement, minimal-import,
transport, mutation, or proof credit. A scoped scan found no prohibited proof escape in
`Statement.lean` or `StatementProbe.lean`.

The pinned environment is Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, with a clean mathlib worktree. The
automation-provided canonical `.lake` symlink was reused read-only. No `lake update`, `lake build`,
clone, fetch, network access, or dependency mutation was performed.

Adding these two target-owned blocker files makes the generated theorem-DAG evidence inventory
differ from the checked-in projection. The worker does not edit that protected projection; the
integration lane must regenerate and validate it while preserving this evidence.

## Required Repair

The scheduler or authority-maintenance lane must publish a refreshed declared validator together
with a coherent current-graph schema-1.1 ledger and sole current-base
`stage1-node-receipt/1.0`, then issue a fresh claim whose base already contains the unchanged
validator blob. Separately, after intake master acceptance, an accountable source owner must admit
and independently approve one immutable theorem passage and freeze every definition, domain,
binder, hypothesis, conclusion, correction, erratum, translation, and boundary case. Only then can
a later worker encode that exact claim, minimize imports, fingerprint the expression and
environment, check transports, and execute all four mutation classes.

This is target-scoped blocker evidence only. It does not satisfy or re-propose the statement phase,
alter its authoritative `[_]` state, replace its receipt or ledger, transfer acceptance, claim an
exact statement or proof, or claim `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master acceptance.
Because the mandatory validator returned a negative result and the positive predicate is false,
`.stage1-worker-selftest.json` is deliberately absent.
