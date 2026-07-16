# THM-M-0126 anchor-audit scheduler blocker

Item: `S56-M-0126-ANCHOR_AUDIT`

Theorem: `THM-M-0126`

Worker base revision: `00583717e4a5f73f89f5ffee33343caf65cc9721`

Worker base tree: `9f2ff1432d1b90ade32db3437fd531e38b49dcf3`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory phase contract at HEAD has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4` and Git blob
`84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `anchor_audit` it declares exactly these
scheduler-owned candidates:

- `Stage1_Instances/THM-M-0126/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0126/check_anchor.py`

Neither path exists in this worktree or in the worker-base commit. The contract requires exactly
one candidate, requires it to exist at the worker base, and requires its HEAD blob to equal its
worker-base blob. This worker is expressly forbidden to create, refresh, rename, replace, or delete
either candidate. Therefore no lawful validator argv can emit the required single
`stage1-validator-semantic-result/1.0` JSON object. An undeclared adapter, a different phase's
validator, prose, or exit code zero cannot replace scheduler-owned semantic replay.

The independent topology gate `G02-TOPOLOGY` is also closed for master acceptance. The sole
intra-theorem predecessor, `S56-M-0126-STATEMENT`, is authoritatively worker-self-tested `[_]`, not
master-accepted `[x]`. Its receipt is a truthful blocked receipt with `accepted=false`, and the
canonical statement remains null. This does not prevent scoped discovery observations, but it does
prevent this phase from receiving master acceptance now.

## Claim order and dependency context

The exact claim tuple is `(v2_execution_rank=279, phase_layer=2,
phase_item_id=S56-M-0126-ANCHOR_AUDIT)`. The theorem-DAG SHA-256 is
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`; the target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order` is the empty sequence. Direct hard parents, transitive hard
ancestors, incoming hard edges, reuse hints, and shared groups are all empty. That exact empty
closure was inspected once against the current theorem node. No provider phase state, receipt,
declaration body, reusable artifact, proof body, copy, transport, checkbox state, or acceptance was
consumed or transferred. The empty closure is not a mathematical-independence claim.

The existing target-owned `dependency-reuse-ledger.json` is schema
`stage1-dependency-reuse-ledger/1.1` and already has empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it binds graph
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`, repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, and the prior statement phase. It is also an exact
input of the current statement receipt. This blocked claim does not rewrite it: doing so would
invalidate prior content binding while neither repairing the absent scheduler-owned validator nor
enabling a lawful anchor self-test. A fresh eligible anchor claim must refresh it before proof work
or a self-test handoff.

## Bounded anchor observations

These observations are discovery guidance only. They do not constitute a precommitted seven-lane
receipt, global search saturation, exact statement normalization, or phase acceptance.

- The source identity remains unresolved. The repository provides only the label "Shimura curve
  theorem", Goro Shimura/1967 metadata, and the gloss "modular curve over a quaternion algebra".
  It does not select among moduli representability, algebraicity or a canonical model of an
  arithmetic quotient, smoothness/properness, complex uniformization, or p-adic uniformization.
  There is consequently no canonical expression or statement fingerprint against which a formal
  candidate can be classified as an exact root.
- The repo-local legacy module
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_045.lean` is Git blob
  `65c55c0d2fc914880209131464e92e920b298a4c` and SHA-256
  `70646e0d9bc0f9df5fc17ca4dd3e22db05386df5e7e129b7e80f9781fa7a09f9`. It elaborates under
  trust level zero, but its order, level, functor, and representability interfaces are explicitly
  lightweight local inventions. Its existential `QuaternionicModuliStatementShape` is an `M5`
  mismatched/circular interface for the unresolved root, not a source-faithful terminal theorem or
  reusable proof body.
- The duplicate-topic legacy module
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_084.lean` is Git blob
  `5fbd2476579a6c69a60f67dcaed926b005c5e09b` and SHA-256
  `1c3ce78fe131b2bc5657075e59c22eead0f62972f279426aea4f8ec41f92f37f`. It also elaborates at
  trust level zero and exposes richer arithmetic and scheme substrate, but its decisive moduli
  predicate remains a parameter. It is an `M5` non-authoritative duplicate statement family and
  transfers neither proof nor acceptance credit to this target.
- The pinned environment is Lean `4.29.0` at commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. A bounded source scan found generic
  `QuaternionAlgebra`, scheme, smooth/proper, descent, number-field, ideal, class-group, and local-
  field infrastructure but no `ShimuraCurve`, `ModularCurve`, quaternionic-moduli, or terminal
  representability declaration. This pinned support is `M3` substrate only.
- Every other materialized Lake package was searched for `ShimuraCurve`, `Shimura curve`,
  `quaternionic moduli`, `false elliptic`, and related quaternionic-moduli spellings. No terminal
  declaration was located. The manifest-pinned `flt-regular` source at revision
  `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
  `32c9eace926573a9981787ae97643e520353c893`, contains no topic hit. These are bounded local
  negatives, not a claim about all public Lean projects.
- The tracked legacy audit records `ImperialCollegeLondon/FLT` at immutable commit
  `2f4325e3b3e647225890f143d4f2dbf1315d4ebd` as an adjacent Lean 4 project with quaternion-
  algebra automorphic-form code, no terminal Shimura-curve theorem, inspected proof gaps, and a
  different Lean/mathlib pin. Those external bytes are not present in this dependency closure, so
  the row remains an unverified `M5` historical research lead and supplies no root or integration
  credit.
- The same-topic source crosswalk for `THM-M-0435` identifies Goro Shimura, "Construction of class
  fields and zeta functions of algebraic curves", *Annals of Mathematics* 85 (1967), 58-159, DOI
  `10.2307/1970526`, as a plausible primary-source lead. It explicitly lacks an inspected stable
  copy, theorem/page locator, definitions, assumptions, errata disposition, and independent review.
  It is bibliographic guidance only, not source authority or `H0` evidence for this target.
- Fresh official-project, other-public-project, statement-only collection, other-prover, and
  primary-page response packets could not be produced with network access denied. Those lanes are
  open access boundaries, not zero-result searches. A raw aborted protocol cannot be promoted to a
  completed negative inventory.

The truthful provisional root state remains `M4`: no usable artifact can be matched to an exact
target because the target itself is not selected. Individual local and pinned surfaces are `M3` or
`M5` as described above. No candidate receives `M0-L`, `M0-W`, `M0-P`, `M1`, `H0`, root-proof,
`AUDIT-Z`, or `THEOREM-Z` credit.

## Commands and exact results

All checks used the existing canonical `.lake` symlink read-only. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or package mutation was run.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, seven-phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 states, two hard edges, five reuse hints, 311 shared groups, acyclic |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0126` | 0 | rank 45, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and twenty-three source references passed |
| worktree and `git cat-file -e HEAD:<candidate>` checks for both declared validator paths | missing; Git exits 128 | zero scheduler-owned anchor-audit validator candidates exist at the worker base |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC /home/sansha-2/.elan/bin/lake env lean --trust=0 ../../Stage1_Instances/THM-M-0126/StatementInfrastructure.lean` | 0 | generic quaternion-algebra and scheme types elaborated; no root declaration or proof body |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC /home/sansha-2/.elan/bin/lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_045.lean` | 0 | legacy target interface and audit metadata elaborated; no exact-root credit |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC /home/sansha-2/.elan/bin/lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_084.lean` | 0 | duplicate-topic arithmetic and scheme substrate elaborated; no exact-root credit |
| pinned mathlib and `flt-regular` revision/tree/status checks | 0 | revisions and trees matched the manifest and both dependency worktrees were clean |

The initial non-login invocation could not resolve `lake` from `PATH` and exited 127; the exact
toolchain binary `/home/sansha-2/.elan/bin/lake` then ran all three narrow elaborations successfully.
Neither that recovery nor any Lean exit zero is a semantic anchor-audit validator result.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor-audit validator at one of the two contract
paths and issue a fresh claim whose worker base contains that identical blob. The statement
predecessor must separately become master-accepted `[x]`. A fresh worker must then precommit and
execute all seven ordered discovery lanes, content-bind every immutable candidate, response,
negative result, and access failure, normalize candidates against a source-selected statement,
refresh the exact empty schema-1.1 dependency ledger, produce exactly one
`stage1-node-receipt/1.0`, and replay the unchanged validator.

No `anchor-audit.json`, discovery-evidence artifact, phase receipt, or
`.stage1-worker-selftest.json` is produced by this blocked claim. This blocker changes no task
state and grants no phase acceptance, proof credit, provider acceptance transfer, audit completion,
theorem completion, or master acceptance.
