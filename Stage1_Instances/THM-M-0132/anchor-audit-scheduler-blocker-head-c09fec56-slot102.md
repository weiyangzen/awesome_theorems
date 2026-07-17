# THM-M-0132 anchor-audit scheduler blocker

Item: `S56-M-0132-ANCHOR_AUDIT`

Base: `c09fec56b723330b06490622768353922c42475f` (tree
`0d742d5018bc3b55b0352c28cca02f5d961018fb`)

Verdict: `blocked`; state remains `[ ]`; `phase_accepted=false`, `audit_complete=false`, and
`theorem_complete=false`.

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The immutable HEAD phase contract declares two scheduler-owned candidate paths for this phase:

- `Stage1_Instances/THM-M-0132/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0132/check_anchor.py`

Neither exists in the worktree or worker-base commit. The contract requires exactly one candidate,
requires it at the worker base, and forbids this worker from creating, refreshing, renaming,
replacing, or deleting either path. There is therefore no authority-derived validator argv and no
exact `stage1-validator-semantic-result/1.0` JSON stdout to bind. Another command's zero exit code,
prose, an undeclared adapter, or a worker-authored validator cannot support a phase receipt or
master acceptance.

The independent topology gate is also closed. `S56-M-0132-STATEMENT` is `[_]`, not `[x]`; its
receipt has `verdict=blocked`, `accepted=false`, and `phase_accepted=false`, with no canonical
source-faithful Lean proposition or statement fingerprint. It is discovery guidance only, not an
accepted normalization boundary.

## Claim and parent audit

The exact claim key is `(v2_execution_rank=283, phase_layer=2,
phase_item_id=S56-M-0132-ANCHOR_AUDIT)`. The current theorem-DAG SHA-256 is
`c5d478054cf32914251001d24d128b3b21ba29414965d64947d78768329660bd`; the target context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The supplied complete parent inspection order is empty. Direct hard parents, transitive hard
ancestors, hard edges, reuse hints, and shared groups are all empty. That empty sequence was
traversed exactly once before any possible proof work. No proof work occurred, and no provider
state, receipt, declaration, proof body, artifact, import, copy, transport, acceptance, or proof
credit was consumed or transferred. An empty admitted graph context does not claim mathematical
independence.

The tracked schema-1.1 dependency ledger truthfully records the same empty lists, but binds an older
graph and base. It is not rewritten in this validator-ineligible run: changing only that byte-bound
input cannot supply the missing scheduler replay or lawful handoff, and the existing statement
receipt binds its current bytes. A fresh eligible claim must refresh it before proposing phase
evidence.

## Bounded observations

- Trust-zero elaboration of `Statement.lean` checks rational Weierstrass curves, `Gamma0`, `Gamma1`,
  and weight-two cusp forms. It declares no canonical modularity proposition, transport, or body.
- The legacy `S1_M_049.lean` module elaborates but is `M5` for the root: arbitrary level, subgroup,
  form, and freely supplied compatibility propositions make its witness circular or materially
  mismatched. Its own text denies theorem completion.
- Pinned mathlib is revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; pinned `flt-regular` is
  revision `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Both worktrees are clean. The only pinned-library
  topic hit is an expository Wiles citation in `Mathlib/NumberTheory/FLT/Basic.lean`; no terminal
  modularity declaration was located.
- The source crosswalk identifies BCDT Theorem A, but exact admitted bytes, complete convention and
  errata treatment, and independent review are not accepted here, so the source remains `H1`.
- Network access is denied. Official projects beyond the materialized closure, other public
  projects, statement-only collections, historical/other-prover projects, and a complete primary
  source packet were not executed as a precommitted seven-lane protocol. No saturation or global
  absence is claimed.

These observations preserve `H1 / M3 / R3` and grant no root proof credit.

## Validation boundary

Before this file pair was added, the Stage1 standard, theorem DAG, phase contracts, target manifest,
and target lookup checks passed. The two narrow Lean commands passed using the existing pinned
environment; no update, build, clone, fetch, or dependency mutation occurred. Candidate probes
confirmed zero eligible validators at both HEAD and the worktree.

The companion JSON is the structured record of exact commands, hashes, blobs, classifications,
failures, and retry conditions. After adding this pair, deterministic theorem-DAG validation is
expected to report evidence-inventory drift because workers may not regenerate the checked-in DAG
projection. Scheduler integration owns that regeneration.

## Retry and status boundary

The scheduler must commit exactly one declared validator and issue a fresh claim containing that
unchanged blob. The statement predecessor must separately become master-accepted with a
source-faithful canonical proposition. A fresh eligible worker can then refresh the empty ledger,
precommit and run all seven lanes, bind every result or access failure, classify the inventory,
produce exactly one phase receipt, and replay the unchanged validator.

Per the explicit zero-candidate rule, this run emits no `anchor-audit.json`, discovery packet,
`AnchorAudit.lean`, phase receipt, or `.stage1-worker-selftest.json`. It changes no task state and
claims no phase acceptance, proof credit, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master
acceptance.
