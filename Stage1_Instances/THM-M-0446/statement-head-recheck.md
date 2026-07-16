# THM-M-0446 statement HEAD recheck: blocked

Item: `S56-M-0446-STATEMENT`

Base revision: `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`

Verdict: `blocked`; the positive statement phase is not self-tested or accepted.

## Exact-target boundary

The intake selects the precise human root from Wiles (1995), Theorem 0.4: every semistable elliptic
curve over `Q` is modular. The current pinned Lean surface still cannot encode that claim without
substitution. `Mathlib.AlgebraicGeometry.EllipticCurve.Reduction` provides an elliptic
Weierstrass-curve domain and local good, multiplicative, and additive reduction predicates for a
chosen discrete valuation ring. It does not provide the required global predicate over every
finite prime with the local-model transports. The pinned modular-form surface does not provide the
curve-to-normalized-weight-two-Hecke-eigenform compatibility relation required by modularity.

Replacing those missing notions with unconstrained `Prop` fields would make the target true only
relative to caller-supplied assertions. Replacing modularity by `Nonempty (ModularForm Gamma 2)` or
`Nonempty (CuspForm Gamma 2)` would be weaker because zero inhabits those spaces and carries no
eigenform or elliptic-curve compatibility. The legacy `S1_M_064.StatementShape` also adds a
residual-representation premise absent from the selected root. These are useful boundary probes,
not exact statements.

The one-import `StatementProbe.lean` and the legacy discovery module both elaborate under Lean
4.29.0 and pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The probe prints
the local reduction API and an honest rational elliptic-curve subtype; it makes no theorem claim.
A bounded search of pinned mathlib Lean sources found only the Wiles bibliography line, not a
semistability, newform/eigenform, or elliptic modularity declaration. This is a bounded local
observation, not a completed anchor audit or universal absence claim.

Therefore there is no truthful `Statement.lean`, `statement.json`, elaborated-expression hash,
minimal-import claim for a canonical target, checked alternate transport, or removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutation suite. The root remains `M4`.

## Dependency and reuse audit

The authoritative theorem DAG has SHA-256
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`; this target's stable
dependency context is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The supplied `parent_inspection_order` is the complete empty list: there is no direct hard parent,
transitive hard ancestor, incoming hard edge, reuse hint, or shared group. That empty order was
traversed exactly once as the empty closure and is recorded in
`dependency-reuse-ledger.json`. No provider declaration, proof body, receipt, checkbox state, or
acceptance was imported, copied, or transferred. Empty context is not a proof-independence claim.

## HEAD contract boundary

The HEAD statement contract is a positive gate. It requires the exact statement record and Lean
source, an expression/environment fingerprint, checked transports, all four mutation classes, one
`stage1-node-receipt/1.0`, and exactly one contract-declared semantic validator. It explicitly says
that a missing expression fingerprint or surviving/unavailable mutation cannot close this phase,
and that classified negative findings do not satisfy the deliverable.

Neither `Stage1_Instances/THM-M-0446/check_statement.py` nor
`Stage1_Instances/THM-M-0446/check_statement_artifacts.py` existed at this worker base. The same
contract requires the selected candidate to have existed at the worker base with identical Git
bytes. Creating one now would therefore be ineligible for same-base master replay. No validator,
phase receipt, or `.stage1-worker-selftest.json` is emitted. Doing so would falsely imply that the
positive statement predicate had been self-tested.

## Validation boundary

Pre-edit rev-5.6 standard, v2 theorem-DAG, target-manifest, target-lookup, and phase-contract checks
passed. The target-owned dependency ledger passed the scheduler's exact schema/context validator.
The Lean probe and legacy module elaborated narrowly with the existing canonical `.lake` symlink;
no update, build, clone, fetch, or dependency mutation ran. The complete structured command records,
hashes, pins, exclusions, known failures, and invalidation inputs are in
`statement-head-blocker.json`.

Adding the mandatory ledger and blocker JSON changes the v2 generator's evidence inventory. This
worker may not edit or regenerate the authoritative theorem DAG; the integration lane performs that
reconciliation after merging target-owned blocker evidence. Such projection drift cannot be used
as positive statement evidence.

## Retry condition

First resolve the provisional intake predecessor. Then provide pinned Lean definitions for global
semistability and elliptic-curve modularity, including local-model transport, normalized weight two,
the exact level, eigenform status, and a concrete compatibility relation, or pin an exact audited
upstream declaration. The scheduler must publish a selected validator before the fresh worker base.
Only then can a statement worker elaborate the exact target, minimize imports, bind expression and
environment fingerprints, check transports, and kill all four required mutations.

Until those conditions hold, `S56-M-0446-STATEMENT` remains `[ ]`. This handoff is a target-scoped
blocker, not a receipt, `[_]` proposal, statement acceptance, proof, audit completion, theorem
completion, release, or master acceptance.
