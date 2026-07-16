# THM-M-0422 anchor-audit scheduler blocker

Item: `S56-M-0422-ANCHOR_AUDIT`  
Theorem: `THM-M-0422`  
Claim order: `(v2_execution_rank=303, phase_layer=2,
phase_item_id=S56-M-0422-ANCHOR_AUDIT)`  
Worker base revision: `3045b020487392327c4752460c5b048f1cca5331`  
Worker base tree: `a3abeb4373c7513d12024c11ee1a363181f923f9`  
Worker verdict: `blocked`  
Proposed state: `[ ]` (unchanged)  
Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`. For
`anchor_audit` it declares these scheduler-owned candidate paths after theorem-ID substitution:

- `Stage1_Instances/THM-M-0422/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0422/check_anchor.py`

Neither candidate exists in the worktree or in the worker-base commit. The contract requires
exactly one candidate, requires it to exist at the worker base, and requires its authoritative HEAD
blob to equal its worker-base blob. The worker contract separately forbids creating, refreshing,
renaming, replacing, or deleting a validator candidate. Therefore this worker cannot lawfully run
the required semantic replay, produce a self-tested phase receipt, or emit
`.stage1-worker-selftest.json`. An undeclared adapter, a different exit-zero command, or prose cannot
replace the scheduler-owned validator.

The independent topology gate is also not ready for master closure. The sole intra-theorem
predecessor, `S56-M-0422-STATEMENT`, is authoritatively `[_]`, not master-accepted `[x]`. Its receipt
truthfully reports a blocked exact-statement gate and no canonical source-faithful Lean expression.

## Dependency and reuse inspection

The authoritative theorem DAG has SHA-256
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`; the target dependency
context has SHA-256 `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The exact direct-parent, transitive-ancestor, hard-edge, reuse-hint, shared-group, and
`parent_inspection_order` lists are all `[]`. The mandated order was traversed exactly once as the
empty complete closure. No provider phase state, receipt, declaration body, reusable artifact,
copy, transport, proof credit, or acceptance was consumed or inherited. The empty closure does not
assert mathematical independence.

The tracked `dependency-reuse-ledger.json` is schema
`stage1-dependency-reuse-ledger/1.1` and has empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it binds the earlier graph
`9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b`, statement item, and base
`778c2db4855d48868391ea236f702e592067e798`. It is also content-bound by the existing statement
receipt. This blocked run does not rewrite it: doing so cannot repair scheduler authority and would
invalidate the pending statement evidence. A fresh eligible anchor-audit worker must refresh the
ledger to its then-current graph, base, claim key, and empty closure before handoff.

## Bounded anchor observations

These observations preserve useful target-scoped discovery evidence only. They are not the
contract-required precommitted seven-lane inventory or a phase receipt, do not claim saturation, and
grant no proof credit.

- The repository-local legacy discovery module
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_077.lean` has SHA-256
  `9854d3f2d827c935f2df569fc67fd639f6213404c7555b9711c33d99bcd6da6b` and Git blob
  `ec8f276bb7892d095fe8e556ce9603b5f8688122`. It re-elaborates at trust zero, but
  `ClassFieldReciprocityData` accepts an arbitrary `Extension` and arbitrary `reciprocityKernel`,
  and `StatementShape` merely asks that this caller-supplied map be bijective. This materially
  mismatches the compound source claim and is `M5` discovery/interface evidence, not an exact root
  or reusable proof body.
- The same legacy module constructs `MultiplicativeIdeles K` as units of the adele ring and a
  quotient called `IdeleClassGroup K`. Pinned mathlib's
  `Mathlib/Topology/Algebra/IsOpenUnits.lean` (SHA-256
  `c6699fcb90e5cb3f5ac7244a39b3c23e1ce6eb24bd9ad17afdcd1e37e82188dd`) explicitly says the idele
  topology is not the induced topology from adeles. These declarations are useful algebraic
  boundary checks but cannot be transported to the required topological idele class group without
  new checked work.
- The pinned environment is Lean `4.29.0` at commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its worktree is clean. The relevant checked sources
  provide finite abelian Galois extensions, the adele ring, class groups, and open-units topology,
  but bounded source search found no correctly topologized idele-class API, idele norm, global
  Artin map, global reciprocity quotient theorem, or existence correspondence. This is `M3`
  substrate only; the root remains `M4` because no exact canonical expression exists.
- The immutable external lead already recorded in the legacy module is
  `kbuzzard/ClassFieldTheory@11f0a7f3874b6891e8e8290d1e645d61ed06e1aa`. The recorded nonterminal
  declarations include `localInv`, `localInvIso`, `Rep.split.FiniteClassFormation`,
  `Rep.split.tateCohomologyIso`, and `Rep.split.reciprocityIso`; the recorded global material is
  blueprint labels rather than terminal Lean declarations. The module records no terminal global
  Artin-reciprocity theorem, an external mathlib pin
  `3bd2603b817feffa4cc0ce9f5d6bad4094ca746e` that differs from this repository's pin, and no
  repo-local import. Because the external source bytes are not in the current closure, this remains
  an immutable but unverified `M5` integration lead, not accepted reuse.
- No second terminal global-class-field-theory candidate was found in the eleven locally
  materialized manifest packages, repository history, or locally present mathlib history. Network
  access is denied and the GitHub CLI is unauthenticated, so fresh official/public project search
  was not possible. This is an access boundary, never evidence of global absence.
- The tracked source crosswalk identifies Neukirch (1999), Chapter VI; Cassels-Froehlich (1967),
  class-field-theory chapters; and Milne, *Class Field Theory* v4.03 (2020) as human-source leads.
  Exact edition/page/theorem passages, incorporated definitions and assumptions, errata, and
  independent review remain absent. The human status remains `H3`, not `H0`.

## Commands and exact results

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, 1546-target scope, v2 DAG, and contract checks passed at the untouched base |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, 2 hard edges, 5 hints, 311 shared groups, acyclic |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts and twelve common gates passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0422` | 0 | rank 77, planned, legacy artifacts unaccepted, theorem incomplete |
| candidate existence and `git cat-file -e HEAD:<candidate>` checks | worktree count 0; Git exits 128 for both | zero declared anchor validators exist at the immutable worker base |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_077.lean` | 0 | legacy algebraic anchors and explicit open gates elaborated; no exact root credit |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0422/Statement.lean` | 0 | target-owned boundary interfaces elaborated; no canonical target or proof body |
| bounded `rg` searches over repo-local and all materialized package Lean sources | 0/1 according to matches | legacy/adjacent references only; no locally pinned terminal global CFT candidate |
| mathlib revision/tree/status and source hash checks | 0 | pinned immutable mathlib identity agreed and its worktree was clean |

No `lake update`, `lake build`, dependency clone/fetch, checkout, proof work, or `.lake` mutation was
performed. The untracked `.lake` link was already present before this run and was used read-only.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor-audit validator and issue a fresh claim whose
base contains that identical blob. The statement predecessor must separately become
master-accepted `[x]`. A fresh worker can then precommit and execute all seven ordered discovery
lanes, content-bind every immutable result and access failure, refresh the exact empty schema-1.1
dependency ledger, classify the frozen inventory, produce exactly one
`stage1-node-receipt/1.0`, replay the unchanged validator at the contract argv, and emit the worker
self-test packet only if that semantic replay succeeds. Any external candidate additionally needs
source bytes, exact type/body/trust inspection, dependency feasibility, and statement comparison.

No anchor-audit phase receipt and no `.stage1-worker-selftest.json` are produced. This blocker
changes no task state and grants no phase acceptance, H0, M0, R0, provider acceptance, proof credit,
audit completion, theorem completion, or master acceptance.
