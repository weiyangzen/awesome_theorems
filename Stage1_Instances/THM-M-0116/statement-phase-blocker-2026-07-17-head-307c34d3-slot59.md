# Statement phase handoff: exact target blocked

Item: `S56-M-0116-STATEMENT`

Theorem: `THM-M-0116`

Base: `307c34d30fc3763c82a944a142ae922b48ff18aa`

The HEAD statement contract was applied without weakening the received claim. The required
statement roles now have one target-owned candidate each, and `check_statement.py` emits the
required typed semantic result. That result is intentionally negative: `phase_accepted=false`.

The human claim is finite generation of the concrete Neron-Severi group of a smooth projective
algebraic surface over an algebraically closed field, with the group understood as divisors modulo
algebraic equivalence. Pinned mathlib supplies schemes, algebraically closed fields, proper and
smooth relative-dimension predicates, projective spectra, additive quotients, group finite
generation, and a ring-level Picard group. It does not supply all root-critical interfaces needed
to state the received claim: general scheme projectivity, a concrete scheme divisor or Picard
group, algebraic equivalence on that group, and the resulting Neron-Severi quotient.

`Statement.lean` therefore checks only that pinned boundary. It deliberately contains no canonical
target, transport, mutation fixture, proof body, `sorry`, axiom, opaque proxy, or abstract object
storing the desired result. The legacy `S1_M_036.StatementShape` remains ineligible because it
quantifies over an arbitrary additive-group family, omits algebraic closedness and projectivity,
and does not construct divisors modulo algebraic equivalence.

The exact DAG claim order is `(271, 1, S56-M-0116-STATEMENT)`. The supplied
`parent_inspection_order` is empty, matching the complete direct and transitive hard-parent
closure. The refreshed schema-1.1 ledger binds graph digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`, context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, and the worker base.
No provider artifact, receipt, checkbox, acceptance, or proof credit is reused or transferred.

The worker self-test proves only the truthfulness and consistency of this target-scoped blocker.
It does not satisfy the positive statement predicate: there is no expression fingerprint, no
credited transport, and none of the four required semantic mutations can be run meaningfully.
The intake predecessor also remains provisional `[_]`, not master accepted `[x]`.

Validation used the pinned Lean 4.29.0 toolchain and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `lake env lean --trust=0` elaborated the boundary
module and produced output SHA-256
`154c9dfa96f406e5bb1901160e65419d13748136c85099274d96d53be9fa173c`. The structured
validator exited zero with exactly one semantic JSON object reporting `status=blocked`,
`phase_accepted=false`, and the first failed `S02-EXACT-TARGET` gate. The phase-contract and target
manifest validators passed. After the new target-owned evidence was present, the aggregate
standard and theorem-DAG checks failed only their deterministic evidence-inventory comparison;
workers are forbidden to regenerate those authoritative projections, so that is an explicit
integration-lane handoff rather than a hidden success claim.

Retry after intake acceptance and source-definition review by pinning or implementing
conclusion-free concrete interfaces for projectivity over the base, the chosen scheme divisor or
Picard object, algebraic equivalence, and the Neron-Severi quotient. Then elaborate only the frozen
claim, prove import minimality, serialize the exact expression and environment, compile any
credited transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.
