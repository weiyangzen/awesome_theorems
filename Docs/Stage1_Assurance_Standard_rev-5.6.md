# Stage 1 Machine-Theorem Assurance Standard rev-5.6

> Document type: supporting theorem-generic assurance gate standard plus a retained historical instance
> Revision family: `5.6`; generalized assurance update: `2026-07-11`
> Supporting profile: `machine-theorem-assurance/1.0`; retained instance schema: `5.6`
> Original instance: `THM-M-0387` / Fermat's Last Theorem
> Primary profile: mathematical theorems in `Lean 4 + mathlib`
> Historical repository target scope: the `1546` IDs retained as membership input in
> `Docs/Stage1_Targets_rev-5.6.json`; current requirements and ordering come only from
> `Docs/Stage1_Blueprint_v2.md`
> Portability: the generic core is prover-neutral; prover-specific claims require a conforming adapter
> Status rule: changing this supporting standard creates no requirements or state. It does not
> validate a theorem, upgrade an old dossier, or promote any execution item.

## 0. Scope, Lifecycle, and Supporting Role

This document supplies assurance gate vocabulary for how a theorem project describes its target,
proof obligations, human-source status, kernel evidence, readable reconstruction, release evidence,
and long-term maintenance. It applies only when `Docs/Stage1_Blueprint_v2.md` incorporates a gate;
it is not a requirements, ordering, or task-state authority. The `THM-M-0387` section is retained as
a historical first instance and compatibility fixture; no FLT-specific literal is a generic rule.

The historical scope represented here was the `1546` metadata-screened Lean 4 theorem-proof
candidates now retained in `Docs/Stage1_Targets_rev-5.6.json` as membership input. The surrounding
Stage0 mathematics population had `1601` deduplicated records, with `55` outside that historical
scope. Current inclusion, exclusion, requirements, ordering, and structural validation rules are
defined only by `Docs/Stage1_Blueprint_v2.md`.

Membership in the `1546`-ID set is only metadata-level intake eligibility. It does not assert that
the source wording has been elaborated as an exact Lean proposition, that current mathlib contains
the required objects, that a `.lean` artifact exists, or that any proof obligation is closed. Those
stronger claims arise only from per-theorem instance evidence under this standard.

All `1546` targets begin at one uniform repository baseline: `L0 / rework_required`. The former
300-slot Stage1 output is retained only as legacy discovery and scheduling provenance. Its files,
wrappers, generated statements, build results, labels, and slot membership grant no elevated class,
accepted state, proof credit, or grandfathered gate. Each target, including `THM-M-0387`, must be
re-evaluated through its own rev-5.6 instance; valid old evidence may be re-admitted only after its
exact scope, inputs, provenance, trust closure, freshness, and receipts pass the current gates.

An implementation may claim conformance with a gate only when machine-readable artifacts and
validators enforce the corresponding `MUST`, `MUST NOT`, `SHALL`, and `SHALL NOT` language below
as incorporated by the current blueprint. Prose that describes a gate is not evidence that it passed.

Every standard artifact declares exactly one lifecycle mode:

| Mode | Meaning | Accepted execution state allowed |
|---|---|---|
| `template` | reusable requirements with no theorem state | no |
| `planned` | theorem scope and tasks frozen, execution not activated | no |
| `executing` | evidence may be proposed and reviewed | provisional only |
| `audited` | scope, graphs, evidence, and debts are completely classified | yes; proof may remain open |
| `theorem_complete` | exact root and release assurance gates are closed | yes |
| `revoked` | prior evidence is invalid, withdrawn, or superseded | historical only |

Lifecycle transitions are append-only, monotone except for explicit revocation, separately
attested, and bound to an immutable source snapshot. A `template` or `planned` artifact containing
accepted execution state is invalid. A copied template never imports another theorem's status.

All instance, graph, receipt, and attestation formats use published strict schemas with stable IDs,
canonical serialization, semantic versions, closed/explicit extension policies, compatibility
windows, and deterministic idempotent migrations. Breaking semantics increment the major version.
Migrations preserve prior evidence and status history, emit a semantic delta, and classify every
ambiguous legacy field as `needs_review`; they never infer or manufacture acceptance.

The supporting profile version is distinct from a theorem dossier's data-schema version. Existing
rev-5.6 instance data remains schema `5.6` and legacy evidence; conforming new artifacts adopt the
new schemas explicitly. This document does not relabel old schema-5.6 data as if a breaking migration
had already occurred.

Current authority is deliberately singular: `Docs/Stage1_Blueprint_v2.md` owns requirements,
ordering, and task state. `Docs/Stage1_Targets_rev-5.6.json` is a membership input; typed DAGs are
machine-readable projections; theorem instance artifacts and content-addressed receipts are scoped
evidence. This file only supplies supporting gate vocabulary and cannot override the blueprint,
set membership, change state, or manufacture acceptance.

The section 12 FLT records are superseded historical observations. They have no checkbox syntax and
no execution-cursor role. Current FLT state, like every other theorem's state, lives only in the v2
blueprint.

### 0.1 Executable-Skill Contract

The supporting gates are applied through the repository skill at
`skills/execute-stage1-rev56/SKILL.md`. The skill is an execution adapter, not an authority:
it MUST read the v2 blueprint, this standard, and the membership input, invoke the checked scripts, create or
update only one theorem dossier per invocation unless batch mode is explicitly requested, and stop
at the first failed hard gate. An agent's narration, checklist edit, or successful unrelated build
cannot change lifecycle, assurance, debt, audit, or theorem-completion state.

Every skill run has exactly one requested terminal intent:

| Intent | Permitted result |
|---|---|
| `intake` | validate target membership and create a `planned` instance with no accepted proof state |
| `audit` | classify statement, sources, candidates, obligations, provenance, and current debt; may reach `AUDIT-Z` |
| `prove` | implement specified open obligations after intake/audit prerequisites; never skip composition or trust gates |
| `validate` | recheck claimed evidence without adding mathematical proof content |
| `release` | decide `AUDIT-Z` and, independently, `THEOREM-Z` from immutable accepted evidence |

The run MUST emit a structured handoff containing target ID, immutable base/tree identity, intent,
changed paths, task and obligation IDs, commands and exit codes, receipt IDs, debt-vector deltas,
blocked gates, and an explicit verdict from this closed set:

```text
accepted | accepted_audit_only | no_state_change | blocked | rejected
```

`blocked` is a valid truthful result and MUST name the first failed gate plus retry condition.
`accepted_audit_only` MUST state `theorem_complete=false`. A run is invalid if it silently broadens
the source statement, substitutes a more convenient theorem, changes the 1546-target denominator,
or reports completion without a validator-derived terminal receipt.

The execution skill MUST NOT branch on any historical assurance distinction. It may use a legacy slot
only to locate candidate files. The first substantive action for every target is re-intake from the
same L0 baseline; no historical artifact may skip statement, obligation, provenance, trust,
composition, source, readability, reproducibility, or independent-verification gates.

## 1. Required Outcomes and Separate Terminal Decisions

Every theorem instance has these outcomes:

1. Freeze the exact mathematical claim and a kernel-elaborated canonical target.
2. Freeze the foundation, axiom, computation, and trusted-computing-base profiles.
3. Freeze an objective obligation registry before observing machine-closure status.
4. Build typed proof, refinement, provenance, evidence, documentation, and workflow graphs.
5. Discover, classify, integrate, or explicitly block known formal artifacts without confusing a
   statement, wrapper, alias, certificate, imported body, or local proof body.
6. Produce node-specific human-source crosswalks and readable proof reconstructions.
7. Execute structured validation specifications in an immutable, reproducible environment.
8. Emit content-addressed evidence, derive metrics and public surfaces, and preserve maintenance,
   expiry, revocation, and upgrade information.

There are two separate terminal decisions:

- **`AUDIT-Z` / audit completion:** the frozen inventory, typed graphs, source boundaries, discovery
  protocol, evidence states, and `H/M/R` debts are completely classified and reconciled. Open proof
  debt is permitted. `AUDIT-Z` MUST NOT depend on successful proof implementation or root closure.
- **`THEOREM-Z` / theorem completion:** `AUDIT-Z` is accepted; the exact canonical root is
  kernel-closed under its selected foundation profile; every root-critical dependency, provenance,
  reproducibility, readability, and release gate is accepted; no unresolved premise is hidden.

A validator MUST include an all-open or all-`M4` positive audit fixture whose result is
`audit_complete=true` and `theorem_complete=false`. A percentage, polished explanation, complete
inventory, or passing unrelated build is never a substitute for `THEOREM-Z`.

## 2. Non-Negotiable Invariants

1. Mathematical truth, human-source fidelity, kernel closure, and exposition are distinct claims.
2. Status is derived per canonical obligation; an editable theorem-level slogan is not authority.
3. Exact statement identity is established by elaborated expressions or checked transports, never
   by names, whitespace normalization, or author-supplied expected types alone.
4. A parent closes only through a checked semantic composition whose exact required children close.
5. Proof, refinement, provenance, evidence, documentation, trust, and workflow edges have different
   semantics and MUST NOT be collapsed into one untyped `child` relation.
6. A wrapper proves its conclusion when checked, but does not relocate, vendor, or duplicate credit
   for its terminal proof body.
7. Obligation eligibility and metric denominators are frozen before closure status is observed.
8. Aliases, wrappers, transports, summaries, and presentation-node splits cannot inflate semantic
   proof coverage.
9. A URL, theorem name, paper citation, generated declaration, parser success, solver exit code, or
   author-written status is not machine completion evidence.
10. `sorry`, `admit`, `sorryAx`, bodyless declarations, unreviewed axioms, unsafe injection paths,
    unverifiable oracles, fake certificates, and backend equivalents never count as proof bodies.
11. Unknown statement, provenance, dependency, TCB, source-boundary, or trust state fails closed.
12. Every material imported theorem, case split, induction/descent, local/global transition,
    construction invariant, computation, or oracle boundary is represented explicitly.
13. `<=100` is a leaf split threshold, not a readability score. A short call to a major theorem is
    an unresolved bridge until separately modeled.
14. Machine evidence cannot clear human-source or readability debt; human prose cannot clear
    machine debt; citations cannot clear any kernel obligation.
15. A completion receipt binds the exact source, specification, toolchain, dependencies, commands,
    outputs, trust closure, and validator version that produced it.
16. A dirty or untracked working tree is not release evidence unless fully content-addressed and
    explicitly classified as nonrelease evidence.
17. Repetition in one mutable workspace is not independent verification.
18. Every accepted state must be dependency-legal in the typed workflow DAG.
19. Any changed input automatically invalidates its receipt and all dependent derived states.
20. If evidence conflicts or cannot be independently resolved, the weaker status wins.

## 3. Three-Axis Debt Model

Every theorem, branch, package, and leaf receives a status vector:

```text
<node-id> = [H?, M?, R?]
```

The three axes are orthogonal. No combined label such as `done`, `verified`, or `complete` may
replace the vector.

### 3.1 Human Mathematical-Proof Debt (`H`)

This axis records the state of the human mathematical proof and its source fidelity. It does not
measure prose quality; prose quality belongs to `R`.

| Level | Meaning | Debt state | Minimum evidence |
|---|---|---|---|
| `H0` | Exact statement has a complete, accepted human mathematical proof and its assumptions are mapped | no human-proof debt | primary proof source plus statement/assumption crosswalk |
| `H1` | A complete proof is believed/published, but exact statement, assumptions, errata, or source-to-node mapping is not yet fully audited | source-reconstruction debt | named source and explicit unresolved mapping list |
| `H2` | Proof is conditional, contested, contains a known gap, or depends on an unclosed mathematical premise | conditional/gap debt | primary source and exact condition/gap |
| `H3` | Only special cases or partial human results are known | partial human-proof debt | branch-level source ledger |
| `H4` | The exact proposition is open | full human-proof debt | current primary-source status audit |
| `H5` | Target is refuted, independent under the chosen foundations, ill-posed, or not a stable proposition | terminal classification, not a completion lane | counterexample/independence/source evidence and target decision |

Rules:

- A historically proved theorem such as FLT can be `H0` while remaining `M2` or `M4`.
- An exact machine proof does not authorize inventing a human-source genealogy. Record the machine
  result on `M`; audit human literature independently on `H`.
- `H5` blocks ordinary theorem-proof execution. The instance must be redirected to a corrected
  statement, barrier theorem, independence theorem, or counterexample target.

### 3.2 Machine-Proof Debt (`M`)

This axis records kernel-checked closure of the exact node under the accepted axiom policy.

| Level | Meaning | Debt state | Counts as machine-completed |
|---|---|---|---|
| `M0-L` | Proof body is repo-local, kernel-checked, and placeholder-free | no machine-proof debt; local body | yes |
| `M0-W` | Exact theorem is supplied by pinned mathlib and checked through a repo-local wrapper/derived wrapper | no machine-proof debt; pinned library wrapper | yes |
| `M0-P` | Exact theorem is supplied by an immutable external project in the local dependency closure and checked through a local wrapper | no machine-proof debt; pinned external closure | yes |
| `M1` | A credible external kernel-checked proof exists, but it is not in the repo-local validation closure | repo-local integration debt | no |
| `M2` | Some children/branches are machine-closed, but the exact node is not | partial formalization debt | no |
| `M3` | Only definitions, statement shape, reductions, interfaces, or unproved theorem declarations exist | statement/interface debt | no |
| `M4` | No usable formal artifact has been located | full formalization debt | no |
| `M5` | Candidate is blocked or invalid because of placeholders, disallowed axioms, incompatible foundations/toolchain, failed build, or statement mismatch | explicit machine blocker | no |

An `M0-*` label is legal only when machine proof is the evidence. The evidence record must contain:

```text
formal system + toolchain version
immutable dependency revisions
exact module/file and declaration
normalized statement match
kernel/build/check command and dated result
axiom/dependency report
placeholder scan result
proof-body location: local / mathlib / pinned external
repo-local wrapper or direct import path
```

An `M0-W` or `M0-P` node has no machine-proof debt for its exact conclusion, but the record must
still state that the proof body is not repo-local. "No machine debt" never means "vendored locally."

### 3.3 Human-Readability Debt (`R`)

This axis measures whether a mathematically trained reader can follow the proof architecture and
verify its relationship to formal evidence. It is separate from whether the theorem has a human
proof (`H`) and whether it is machine-checked (`M`).

| Level | Meaning | Debt state | Minimum public surface |
|---|---|---|---|
| `R0` | Complete readable route with node-by-node formal anchors, assumptions, branch logic, boundaries, and `<=100` leaf ledgers | no readability debt | reviewed proof outline/process surface |
| `R1` | Route is readable, but one or more formal mappings, assumptions, or local transitions are incomplete | minor mapping debt | explicit missing-map ledger |
| `R2` | Summary exists, but important proof branches or high-risk nodes are not explained | structural readability debt | missing-node list |
| `R3` | Only status tables, theorem names, raw code, or execution logs exist | reconstruction debt | planned public merge target |
| `R4` | No usable explanation exists, or existing prose materially overclaims/misstates the proof | full/corrective readability debt | correction blocker and owner |

Readability closure rules:

- Every `M0-*` node must ultimately reach `R0`; the machine proof is the primary factual evidence
  used to reconstruct the readable version.
- The readable version must say what the node proves, how it connects to its parent and children,
  where its proof body lives, which assumptions/axioms it uses, and what it does not prove.
- For `M1`-`M5`, readable material is a labeled proof plan, boundary explanation, or blocker report,
  not prose written in the grammatical form of a completed proof.
- Closing `R` is allowed to be documentation-only, but that closure cannot advance `M`, close the
  root theorem, or satisfy a machine implementation gate.

### 3.4 Examples of Legal Mixed States

| Vector | Correct interpretation |
|---|---|
| `[H0, M4, R0]` | Human proof is known and well explained; no machine formalization exists |
| `[H0, M0-W, R2]` | Pinned mathlib closes the exact node; readable reconstruction is incomplete |
| `[H0, M0-P, R0]` | Pinned external proof is checked locally and fully reconstructed for readers |
| `[H0, M2, R1]` | Human proof is complete; machine coverage is partial; exposition has mapping gaps |
| `[H4, M4, R0]` | Open problem is accurately explained; neither human nor machine proof exists |
| `[H1, M5, R3]` | Human source mapping is incomplete and the formal candidate is blocked |

## 4. Evidence Hierarchy and Claim Rules

Evidence tiers are not debt levels and are never manually promoted. They describe the strongest
accepted evidence packet for one canonical obligation:

| Tier | Evidence |
|---|---|
| `E0` | Release-grade kernel check of a repo-local proof body, bound to source, trust closure, and receipt |
| `E1` | Release-grade local kernel check through a pinned library/external body and exact wrapper |
| `E2` | Independently reproducible upstream kernel check at an immutable revision, not integrated locally |
| `E3` | Exact formal source anchor located, but checkability/closure not established |
| `E4` | Primary human proof source |
| `E5` | Secondary source, prose claim, issue, README, search result, or URL only |

Claim constraints:

- `M0-L` requires `E0`; `M0-W` and `M0-P` require `E1`.
- `M1` requires at least `E2`; an `E3` anchor is `M3` or `M4`, not `M1`.
- `H0` requires `E4` with a versioned, pinpoint statement/premise/assumption/errata crosswalk and
  an identified reviewer.
- `E5` can start an audit task but cannot close a proof status.
- A passing build proves only the declarations actually covered by that build/check command.
- A theorem name or normalized text is never accepted as statement identity. The elaborated target
  and checked equality, `Iff`, or required implications must cover coercions, binders, domains,
  universes, typeclass assumptions, side conditions, and degenerate cases.
- An `E0` or `E1` packet is valid only while all content-addressed inputs remain unchanged and its
  selected freshness policy remains current.
- A signature identifies an attestor; it does not make false mathematical or machine evidence true.

## 5. Theorem Intake Contract

Before tree construction, every theorem instance must freeze the following record:

```yaml
schema_version: <major.minor>
lifecycle_mode: planned
theorem_id: <stable repository UID>
canonical_name: <name>
canonical_statement: <human mathematical statement>
canonical_formal_target:
  backend: lean4
  module: <minimal import module>
  declaration_or_expression: <exact Prop/type>
  elaborated_expression_hash: <hash of normalized kernel expression>
  environment_fingerprint: <toolchain + imports + options + foundation profile>
domain_and_universes: <types, universes, structures>
quantifiers: <ordered quantifier list>
hypotheses: <all explicit assumptions>
conclusion: <exact result>
alternate_encodings:
  - target: <expression>
    relationship: equal | iff | implies | implied_by
    checked_witness: <kernel-checked declaration or explicitly non-machine bridge>
excluded_degenerate_cases: <boundary conditions>
foundation_profile: <versioned accepted/disallowed logical principles>
tcb_profile: <versioned trusted-computing-base policy>
computation_profile: <certificate/oracle/experiment policy>
formal_system: <backend and adapter version; Lean 4 + mathlib is primary>
source_revisions: <toolchain, libraries, and complete dependency lock>
obligation_registry_hash: <frozen before status discovery>
discovery_protocol_hash: <precommitted search inventory and cutoff>
assurance_standard: Docs/Stage1_Assurance_Standard_rev-5.6.md
public_merge_targets: <stable repo-relative paths>
owners_and_reviewers: <accountable identities or roles>
freshness_and_revocation_policy: <review due, invalidation inputs, incident path>
```

Statement ambiguity, unresolved metavariables, and a missing expression fingerprint are hard
tree-construction blockers. Every backend encoding must map to the canonical mathematical claim;
closing one backend-specific encoding does not automatically close an unmapped canonical claim.

### 5.1 Lean 4 Statement Gate

For Lean 4, the statement gate MUST:

1. use the pinned Lean executable and minimal declared imports;
2. elaborate the target with fixed options, namespaces, universes, and typeclass context;
3. preserve or canonically serialize the resulting expression and environment fingerprint;
4. compile checked equivalence/implication wrappers for each credited alternate form;
5. mutation-test at least a removed hypothesis, changed domain, changed binder scope, and boundary
   case; every non-equivalent mutation must fail before proof evidence is inspected.

## 6. Proof-Tree Standard

### 6.1 Canonical Obligation Registry

Before machine status is discovered, the instance freezes a registry of canonical semantic
obligations. An obligation ID represents a mathematical/formal claim in a fixed context, not a
Markdown row. Each record contains:

```yaml
obligation_id: <stable semantic id>
statement_fingerprint: <elaborated target + context hash, or planned canonical hash>
kind: <root/definition/reduction/branch/construction/lemma/computation/transport/terminal>
root_relevant: true | false
machine_eligibility: required | not_applicable | informational
human_source_eligibility: required | not_applicable
readable_eligibility: required | not_applicable
risk_class: critical | high | normal | low
exclusion_reason: <closed reason code, justification, independent approval if not required>
terminal_proof_body_id: <when known; never inferred from a wrapper name>
```

Eligibility is derived from the frozen theorem architecture and typed edge roles, never from whether
proof evidence is easy or already available. A target-to-nontarget change, split, merge, exclusion,
or weight change creates a new registry version with an append-only delta. Old denominators remain
reportable. Aliases, wrappers, transports, and presentation nodes share canonical obligation or
proof-body identities where appropriate and cannot create duplicate semantic credit.

### 6.2 Required Node Schema

Every node must have all fields below. A missing field keeps the node open.

```yaml
node_id: <THEOREM-ID>-<stable hierarchical id>
obligation_id: <canonical semantic obligation id>
kind: root | definition | normalization | reduction | branch | construction |
      bridge | core_lemma | computation | certificate | transport | terminal
human_statement: <precise statement>
formal_target: <exact declaration type or planned signature>
output: <conclusion delivered to parent>
human_debt: H0..H5
machine_debt: M0-L..M5
readability_debt: R0..R4
evidence_ids: [<content-addressed packets>]
source_crosswalk_id: <pinpoint human-source record or not-applicable>
provenance_id: <wrapper/body/conclusion provenance record or none>
foundation_profile: <version>
tcb_profile: <version>
computation_record: <certificate/oracle record or none>
step_budget: <integer <=100 for a leaf; split-required otherwise>
semantic_step_ledger: <premises/inference/output/source anchors; no filler>
public_readable_target: <stable repo-relative path#unique-node-anchor>
validation_spec_id: <structured executable recipe>
status_boundary: <what this node does not prove>
task_ids: [<creating/validating workflow tasks>]
owned_sources: [<actual declarations/files/evidence/readable targets>]
owner: <accountable role>
reviewer: <independent role when required>
validity: <validated_at/review_due/invalidation inputs/revocation state>
```

### 6.3 Typed Graph Contract

Instances MUST NOT infer semantics from undifferentiated `parent_ids`/`child_ids`. They store typed,
reciprocal edges in separate graphs or one typed edge relation:

| Edge type | Meaning | Affects machine closure |
|---|---|---|
| `proof_requires` | child conclusion is a required premise | yes |
| `composes` | checked term maps exact children to exact parent | yes |
| `logical_decomposition` | children jointly refine the same proof obligation | yes |
| `source_map` | explanatory mapping into a source or upstream body | no |
| `expository_decomposition` | reader-facing decomposition only | no |
| `equivalent_to` / `transports` | checked statement relationship | only in declared direction |
| `evidence_for` / `provenance_of` | evidence or body-origin link | no |
| `documents` | readable-surface link | no |
| `trusts` | TCB/foundation/computation dependency | release gate only |
| `workflow_depends_on` | execution ordering | task acceptance only |

The validator checks legal endpoint kinds, reciprocity, reachability, cycles per graph, and closure
semantics. Governance or documentation nodes cannot become proof premises. A closed parent with
open `logical_decomposition` children is invalid; a source/expository child must not be presented
or counted as an independent proof obligation and must have a checked or reviewed mapping.

### 6.4 Mandatory Mathematical Layers

The following tree is a schema, not permission to skip inapplicable analysis. Mark a layer
`not_applicable` only with a written reason and reviewer acceptance.

```text
ROOT Exact theorem
|
+-- S Statement and foundation layer
|   +-- S1 definitions and notation
|   +-- S2 domains, universes, coercions, and typeclass assumptions
|   +-- S3 degenerate/boundary cases
|   +-- S4 equivalent formulations and transport directions
|   `-- S5 logic, classical choice, quotient, extensionality, and axiom policy
|
+-- N Normalization layer
|   +-- N1 canonical representatives / primitive form
|   +-- N2 symmetry and sign/order normalization
|   +-- N3 finite/infinite or local/global normalization
|   `-- N4 reduction of general input to normalized input
|
+-- B Branch layer
|   +-- every case split
|   +-- every parity/prime/boundary split
|   +-- every local/global or primitive/non-primitive split
|   `-- exhaustiveness and branch recomposition theorem
|
+-- C Construction layer
|   +-- constructed objects
|   +-- well-definedness
|   +-- invariants
|   `-- functoriality/compatibility/independence of choices
|
+-- L Core lemma layer
|   +-- algebraic/analytic/combinatorial/geometric engines
|   +-- induction/descent/minimality steps
|   +-- existence/uniqueness/classification steps
|   `-- contradiction or terminal estimate steps
|
+-- X External and computational boundary
|   +-- imported theorem boundaries
|   +-- decision procedures and automation
|   +-- finite computation and certificates
|   `-- trusted kernel/checker and reproducibility boundary
|
`-- T Terminal layer
    +-- each branch terminal
    +-- transport back to canonical statement
    +-- branch merge / composition theorem
    `-- exact root theorem and axiom report
```

### 6.5 Recursive Expansion Triggers

A node must be expanded rather than treated as a leaf when any condition holds:

- its readable ledger would exceed `100` logical steps;
- it invokes a theorem carrying a central part of the result;
- it hides a case split, induction, descent, minimal counterexample, compactness argument, or
  local-to-global transition;
- it constructs an object whose well-definedness or invariants are nontrivial;
- it crosses types, foundations, universes, representations, or equivalent formulations;
- it relies on external code, an external formal project, automation, reflection, a solver,
  numerical computation, or a certificate;
- it uses an opaque declaration or custom axiom whose role has not been audited;
- machine evidence and human proof architecture do not align one-to-one;
- a child is described with vague words such as "standard," "routine," "similarly," "by library,"
  or "by computation" while carrying material proof work;
- the node is high-risk according to domain experts, source structure, code size, dependency fan-in,
  axiom use, or prior validation failures.

### 6.6 Leaf Stop Rule

A project-level node may stop as a leaf only when all are true:

1. Its statement is exact and independently checkable.
2. It contains no hidden unresolved branch or high-risk theorem package.
3. Its structured proof ledger contains at most `100` substantive logical steps. Every step names
   stable premise IDs, an inference/theorem/source, an exact output claim, and its outgoing use.
4. Every cited foundation primitive is named and already audited; a major imported theorem becomes
   a bridge node rather than a primitive citation.
5. Its machine status and evidence are explicit.
6. Its parent composition edge is explicit.
7. Its public readable target and boundary sentence are specified.

Line count, tactic count, generated phrases, repeated “verify intermediate condition,” or a short
proof term do not establish the step budget. One call to a large theorem counts as an unresolved
bridge until that theorem has its own obligation and evidence. The `100` threshold only forces
decomposition; it does not establish semantic adequacy or `R0`.

### 6.7 Parent Closure and Composition Certificate

For every parent `P` with required proof children `C1..Cn`, a checked composition certificate MUST:

1. bind the exact statement fingerprints of `P` and every required `Ci`;
2. explicitly consume, or kernel-derive from, every required child conclusion;
3. yield the complete parent target, not a weaker summary or one selected branch;
4. introduce no undeclared premise, axiom, oracle, or child;
5. identify unused children as a modeling error rather than silently accepting them.

The Lean 4 adapter SHOULD generate a harness in which child theorems are abstract named hypotheses,
elaborate the composition term, compare the conclusion fingerprint, and inspect constant/axiom
dependencies. Workflow acceptance then follows:

```text
P may become [_] only after all required Ci are at least [_] and a provisional composition check passes.
P may become [x] only after all required Ci are [x], the composition declaration is checked in the
integration checkout, debt/status surfaces are reconciled, and the master records validation evidence.
```

If any child is `[ ]`, the parent is `[ ]`. If no child is `[ ]` but one is `[_]`, the parent may be
`[_]` but never `[x]`.

## 7. Maximum Machine-Coverage Protocol

"Maximum coverage" means a replayable discovery effort plus the largest truthful kernel-checked
closure over a pre-status frozen obligation universe. It never means maximizing green rows by
weakening targets, hiding obligations, cloning aliases, or changing the denominator.

### 7.1 Discovery Protocol

Discovery assurance is independent from inventory classification. Before searching, an instance
records repositories/registries, immutable refs or selection rules, theorem aliases and translated
names, namespace/declaration query families, API/command forms, cutoff time, access credentials
policy, and expected negative-result evidence. Each prescribed query produces a timestamped result,
archive/response hash, or explicit access failure. New discoveries are append-only and create a new
inventory version; they never disappear merely to preserve a percentage.

Classification coverage of `100%` means only that every member of one frozen inventory version is
classified. A claim of exhaustive discovery additionally requires reviewed saturation evidence.

### 7.2 Search Order

For every node, search and record results in this order:

1. Existing repo-local proof bodies and wrappers.
2. Pinned mathlib declarations and their transitive module/source boundaries.
3. Official or primary formalization projects for the theorem.
4. Other public formal repositories at immutable revisions.
5. Formal-conjecture/statement collections, clearly classified as statement-only.
6. Historical versions or other proof assistants as research evidence. They do not count as Lean 4
   completion unless a canonical claim mapping and the requested backend completion both close.
7. Human primary sources needed to formalize remaining nodes.

Searches must include aliases, equivalent statements, namespaces, translated names, and terminal
declarations. Negative search results require query list, repositories/registries searched, date,
and access limitations; "not found" without a search ledger is not evidence.

### 7.3 Formal Candidate and Provenance Audit

For each candidate:

1. Normalize and compare the candidate statement to the target.
2. Resolve the checked wrapper/conclusion separately from the terminal declaration and proof body.
3. Extract the direct and transitive declaration/import dependency closure.
4. Inspect machine-produced axioms and the selected foundation profile.
5. Apply parser/elaborator-aware placeholder, bodyless, unsafe, oracle, external-code, generated-
   artifact, and unknown-trust classification to the actual dependency closure. Regex is additional
   defense only.
6. Identify project, canonical remote, complete dependency graph, immutable revisions, clean tree
   digests, source archives, licenses, toolchain, and adapter.
7. Execute the smallest structured direct check and bind it to a receipt.
8. Decide `M0-L`, `M0-W`, `M0-P`, `M1`, `M2`, `M3`, `M4`, or `M5`.
9. For `M1`, create a concrete pin/import/wrapper/compatibility task.
10. For `M5`, record the exact blocker and the event that reopens integration.
11. Never upgrade a parent, source-map child, or duplicate alias beyond the exact scope proved.

Every machine-closed provenance packet records at least:

```yaml
conclusion_id: <canonical obligation>
local_declaration: <checked declaration>
local_role: body | wrapper | composition | alias
terminal_declaration: <actual terminal theorem>
terminal_proof_body_id: <content-addressed body identity>
origins: [{project, remote, revision, tree_hash, file, declaration, source_hash}]
direct_dependencies: [<declarations>]
transitive_trust_closure_hash: <declarations + TCB + axioms + computation>
```

### 7.4 Lean 4 Trust and Foundation Profile

Each Lean 4 instance selects versioned foundation and TCB profiles. The foundation profile lists
fully qualified allowed/disallowed principles and why they are compatible with the intended claim;
it is not a repository-global FLT allowlist. The Lean adapter MUST compare the exact machine-derived
axiom set of terminal declarations with this profile.

The TCB profile inventories and hashes the Lean kernel executable, compiler/bootstrap provenance,
Lake/Elan or equivalent package tooling, imported compiled artifacts, trusted plugins, native or
external evaluators, certificate checkers, and every executable used by a release recipe. An
undeclared or unknown trusted element prevents release-grade `E0/E1`.

For automation and computation, the record distinguishes:

- `proof_producing` or `certificate_replayed_by_kernel`: may close only when the exact output is
  replayed under the accepted TCB;
- `trusted_oracle`: closes only if explicitly allowed by the foundation/TCB profile and disclosed;
- `experiment_only`: never closes a theorem obligation.

It stores complete input/domain digests, producer/version, seed/environment, output digest,
certificate format, checker identity and theorem, determinism, resource bounds, and replay spec.
Certificate tampering and incomplete-domain fixtures MUST fail.

### 7.5 Coverage and Anti-Goodhart Metrics

Report numerator and denominator ID sets, not percentages alone. Required metrics are:

```text
Inventory classification = classified canonical obligations / frozen inventory obligations
Unique logical-leaf closure = closed required leaf obligations / frozen required leaf obligations
Distinct proof-body closure = accepted terminal proof-body IDs / required terminal body IDs
Interface/transport closure = closed wrapper/transport obligations / required interface obligations
Readable closure = independently accepted R0 obligations / required readable obligations
Human-source closure = accepted H0 obligations / required human-source obligations
Source-boundary coverage = classified provenance boundaries / required formal/computation obligations
Root closure = exact canonical root accepted, true or false
```

Also publish minimal open root cut sets, critical-path closure, frozen pre-status risk-bucket
coverage, and optimistic/pessimistic bounds for disputed eligibility. Risk-weighted values supplement
raw unique counts and root closure; they never replace them.

Metamorphic gates MUST demonstrate that adding aliases/wrappers, cloning evidence rows, or splitting
and merging presentation nodes leaves root, unique-leaf, distinct-body, and critical-path metrics
unchanged. A scope/denominator change always publishes old and new ID sets plus rationale.

Audit completion requires inventory classification and source-boundary coverage of `100%` for its
frozen version. Theorem completion requires the root itself and all root-critical release gates;
there is no percentage substitute.

## 8. Human-Readable Reconstruction Standard

`R0` is an independently accepted reconstruction result, not an author-set Boolean or the existence
of a Markdown file. Every required readable obligation has a unique stable `path#node-anchor` and a
structured entry with this fixed order:

1. **Claim:** exact mathematical statement in domain language.
2. **Role:** why the node exists and what parent edge it supplies.
3. **Inputs:** hypotheses, earlier nodes, and imported structures.
4. **Proof route:** numbered mathematical transitions, not tactic narration.
5. **Branch logic:** cases and proof of exhaustiveness.
6. **Formal map:** exact module, theorem, important child declarations, and revision.
7. **Trust boundary:** proof-body location, axioms/classical principles, automation/computation.
8. **Step ledger:** stable step IDs, exact premise IDs, inference/theorem/source, exact output, and
   outgoing use; total `<=100` substantive steps for a leaf.
9. **Boundary:** what the node does not prove and which debts remain.
10. **Status vector:** `[H?, M?, R?]` with evidence references.

The entry binds bidirectionally to the obligation statement fingerprint, formal declaration,
provenance packet, and evidence receipts. `R0` additionally requires an identified independent
reader or domain-review receipt. Machine validation proves fields and links exist; it does not prove
that prose is mathematically adequate. Missing fields, filler/template steps, duplicate normalized
steps, broken claim flow, a bare file target, or a stale fingerprint downgrades the node below `R0`.

The reader surface must support two routes:

- a short `proof_outline` route that exposes the whole tree and machine boundary without drowning
  the reader in implementation detail;
- a long `proof_process`/appendix route that expands high-risk packages and leaf ledgers.

Raw worker logs, private ledgers, absolute clone paths, chat summaries, and temporary result files
are not public readable proof surfaces. They may supply provisional evidence only until merged into
a stable repository-relative target.

### 8.1 Human-Source `H0` Contract

Every `H0` obligation maps each material premise, transition, and conclusion to a primary source
record containing edition/version, stable identifier, theorem/section/page or archival locator,
assumption mapping, dependent source IDs, correction/errata status, and reviewer. A broad citation
to a famous paper, a secondary exposition, or a resolved URL is not `H0`. Machine gates validate
completeness, locators, hashes, and consistency; a qualified source reviewer validates mathematical
fidelity. Source/version drift invalidates the affected `H0` packet.

## 9. Artifact and Evidence Contract

An instantiated theorem should converge on these roles. Existing repository names may be reused;
do not create parallel files when a stable surface already owns the role.

| Role | Required content |
|---|---|
| theorem README | entry, navigation, exact overall boundary |
| theorem intake | canonical claim, expression fingerprint, profiles, owners, lifecycle |
| obligation registry | canonical obligation IDs, eligibility, risk, frozen denominator hash |
| typed graph bundle | proof, refinement, provenance, trust, documentation, and workflow edges |
| machine-readable metadata | derived root/branch vectors and release reference |
| short proof outline | reader-first complete tree route and formal anchors |
| proof-unit manifest | nodes, canonical IDs, debt vectors, typed artifact references |
| validation specifications | structured executable recipes and coverage claims |
| evidence/receipt bundle | content-addressed raw results, provenance, TCB, SBOM, signatures |
| machine audit | exact declaration/source/axiom/placeholder/build evidence |
| process/tree audit | node decomposition, branch logic, leaf budgets, parent composition |
| long readable proof surface | detailed reconstruction for high-risk packages |
| build validation | dated commands, environment, results, failures, scope boundary |
| formal source tree | proof bodies, wrappers, integrations, and checked composition declarations |

Role boundaries:

- The v2 blueprint is the sole requirements, ordering, and task-state authority; this standard only
  supplies supporting assurance gates and stores no theorem's live status.
- Instance manifests and registries are scoped evidence; typed state DAGs are derived projections.
- Signed, content-addressed receipts are validation evidence. `H/M/R`, metrics, and terminal
  decisions are computed projections, not editable truth.
- The human-source ledger and signed reviews supply `H` evidence; structured readable entries and
  signed reviews supply `R` evidence. Neither overrides kernel evidence.
- Public summaries MUST be generated from the accepted deterministic evidence bundle or checked by
  a clean-diff reconciliation gate. Consistent repetition of a manually wrong value is not evidence.
- Historical artifacts and prior schema versions remain immutable and clearly labeled; migrations
  produce new artifacts and semantic delta reports rather than rewriting history.

### 9.1 Evidence Receipt and Bundle Contract

Each validation action emits canonical machine-readable data containing specification/registry
hashes, repository commit/tree/dirty state, patch and untracked input hashes when nonrelease, exact
tool/TCB and dependency digests, platform/environment, structured recipe, input/output/log hashes,
start/end/exit, covered obligation/declaration IDs, expression fingerprints, axiom/trust closure,
attestor, freshness, and invalidation inputs.

Release assembles receipts, exact-type probes, axiom output, declaration/provenance graphs, hygiene
reports, SBOM/licenses, computation certificates, readable records, source crosswalks, and root
decision into a deterministic content-addressed bundle. Building twice with fixed canonicalization
MUST produce the same semantic digest. A signature proves attestation identity and integrity only.

Every packet declares owner, `validated_at`, `review_due` or a no-expiry rationale, invalidation
inputs, support state, supersession/revocation state, and incident path. Changed source, statement,
profile, adapter, validator, dependency, public reconstruction, upstream erratum/release, or expired
policy invalidates the packet and its dependent states automatically.

## 10. Execution, Reproducibility, and Release Protocol

### 10.1 Dual-Cursor State

The v2 blueprint defines the state machine. Markdown may render these compatibility symbols:

- `[ ]`: unclaimed, unimplemented, failed, or otherwise not done.
- `[_]`: worker implementation and self-test exist, but master integration/validation is pending.
- `[x]`: master accepted in the integration checkout after dependency, validation, evidence, and
  reconciliation gates passed.

Workers may write only `[_]`. Only the master/integration lane may write `[x]`. Both `[ ]` and `[_]`
are unfinished. A worker's prose assertion of success is not a state transition. An accepted item
with an unfinished transitive prerequisite is invalid unless its typed task kind is
`report_open_state` and its completion semantics explicitly permit open proof debt.

### 10.2 DAG and Layer Order

- Every blueprint task item has a unique id, dependency ids, owned path scopes, deliverables, evidence,
  and a completion gate.
- Duplicate ids or cycles are hard failures.
- Work proceeds from statement/source audit to tree, leaf machine work, readable reconstruction,
  composition, validation, and reconciliation.
- Workers may prepare provisional later nodes in stable topological order when concurrency is
  explicitly enabled, but master closure remains dependency ordered.
- The validator topologically recomputes state and rejects duplicate/missing IDs, cycles, orphan
  obligations, empty accepted deliverables, and illegal accepted ancestors. Markdown is generated
  from the accepted DAG, not parsed as the primary database.
- If an upper-layer item is `[x]` while a required lower task is unfinished, downgrade the invalid
  status, revoke dependent receipts where required, and record a stable rejection code.
- After five unresolved execution ticks, split the item into smaller child nodes; do not repeatedly
  ask a worker to solve the same oversized task.

### 10.3 Worker Evidence Packet

Every `[_]` handoff must identify structured records for:

```text
item id and node ids
base revision and worker branch/worktree reference
changed paths and diff summary
exact statements added/changed
source revisions and proof-body locations
commands run and output summary
axiom and placeholder results
debt-vector changes proposed, with evidence
known failures, boundaries, and follow-up nodes
canonical obligation ids and statement fingerprints
typed graph changes and composition certificates
content-addressed recipe/receipt ids
actual source/declaration/readable ownership and change-impact set
```

### 10.4 Master Acceptance

The master must independently:

1. Verify lifecycle mode, dependencies, reciprocal task-obligation links, ownership, and conflicts.
2. Re-elaborate the canonical target and inspect proof/composition/provenance, not only test output.
3. Re-run structured node checks and the applicable aggregate build against the attested snapshot.
4. Recompute axiom, declaration dependency, TCB, placeholder/unsafe/oracle, supply-chain, and source-
   boundary gates from actual terminal objects.
5. Check semantic ledgers and independent `H0/R0` reviews; `<=100` alone never accepts prose.
6. Recompute unique metrics, root cut sets, invalidations, and both terminal decisions.
7. Regenerate public surfaces from the evidence bundle and require a clean diff.
8. Advance only the dependency-legal state whose receipts pass; no longest-prefix heuristic may
   override typed dependency semantics.

### 10.5 Structured Validation Specification

Release-supporting validation commands are never shell strings. Each recipe is:

```yaml
recipe_id: <stable id>
cwd: <repository-relative directory>
argv: [<executable>, <argument>, ...]
env_allowlist: {<name>: <fixed or explicitly variable value>}
timeout_seconds: <bound>
network_policy: fetch_only | denied | explicitly_required
expected_exit: 0
expected_outputs: [{path_or_stream, semantic_hash_policy}]
covered_obligation_ids: [<ids>]
covered_declarations: [<fully qualified names>]
```

Every distinct recipe supporting `M0-*`, `R0`, `H0`, a metric, or a terminal decision executes
exactly as recorded. The runner invokes `argv` without shell interpolation, captures outputs, proves
the claimed declarations were checked, and binds results to receipts. A passing aggregate build
cannot excuse a broken or falsely scoped per-node recipe.

### 10.6 Hermetic Lean 4 Reproduction

Release-grade Lean 4 validation separates two phases:

1. **Fetch/bootstrap:** from declared content-addressed inputs, create the pinned toolchain,
   dependency source closure, archives, and licenses/SBOM.
2. **Verify:** in a new checkout with empty user/package/build caches, fixed locale/timezone/umask,
   and outbound network denied, perform a cold build and every structured recipe.

Tool discovery uses one explicit relocatable mechanism (`elan run/which`, declared tool root,
container/Nix/Guix derivation, or adapter equivalent); no component independently guesses
`$HOME/.elan`. Every invoked runtime has a verified identity/digest. Warm builds are performance
evidence only, and their semantic output must agree with the cold run. Supported OS/architecture,
filesystem, Lean/Lake/Elan, Python/Git/shell helpers, time, memory, disk, and concurrency bounds are
declared. A portable-release claim requires CI on each claimed platform and at least two materially
independent platform configurations.

The release archive must support network-disconnected restoration of the source/dependency closure
and reproduction of the semantic evidence digest, subject to recorded license constraints.

### 10.7 Independent Verification and CI

High-assurance theorem release requires:

- two signed attestations over identical immutable specification/source/dependency digests;
- distinct verifier identities, clean checkouts, independently provisioned runners, and no shared
  writable dependency or build cache;
- a minimal independently implemented verifier that recomputes canonical target identity, typed
  graph invariants, root state, axiom/profile inclusion, hashes/signatures, unique metrics, and
  attestation agreement without importing the primary validator;
- mandatory protected CI for all relevant source, specification, dependency, adapter, validator,
  evidence, and public-status changes, plus scheduled clean rebuilds.

Disagreement blocks release. Re-running the same validator in the same workspace is not independent.

The repository maintains positive and negative dossiers, mutation tests, differential fuzzing, and
metamorphic tests for every blueprint-incorporated P0 gate. At minimum it tests statement weakening, illegal task
state, denominator removal, alias multiplication, invalid composition, wrapper/body lies, hidden
axioms/placeholders/unsafe code, dirty and transitive dependencies, malformed recipes, stale or
tampered receipts, cache poisoning, missing readable/source records, and false public summaries.
Each failure has a stable rule ID; all published critical mutations must be killed.

### 10.8 Prohibited Completion Shortcuts

Never mark a machine item or root complete for:

- docs-only changes, test-only changes, or a generated statement;
- a wrapper around an axiom, `sorry`, or unproved declaration;
- an external URL or unpinned repository;
- compilation that does not reach the claimed theorem;
- proof of a weaker, finite, specialized, conditional, or differently typed statement;
- a numerical experiment without a verified certificate covering the theorem;
- a readable proof that has not been formalized;
- a machine proof whose statement, composition, provenance, source snapshot, dependency, TCB,
  accepted-axiom, reproducibility, or invalidation audits are missing;
- duplicate aliases or presentation nodes used to inflate coverage;
- a signature, second run, cache hit, or multi-platform result presented as additional mathematics.

### 10.9 Maintenance, Revocation, and Upgrade Rehearsal

Every maintained dossier, profile, dependency, discovery ledger, and evidence packet has an owner,
reviewer policy, support window, review due date, revocation/incident procedure, and at least two
independent durable archive locations or a documented lawful recovery mechanism. Expired,
unsupported, advisory-affected, or revoked critical evidence cannot satisfy a current release.

Prover and dependency upgrades are rehearsed one material change at a time. Old and proposed clean
environments compare normalized target expressions, axiom/TCB closure, provenance/body identities,
source paths, root result, unique metrics, readable/source hashes, performance, and artifact
availability. Unexplained semantic or trust drift fails the upgrade; accepted changes publish a
migration decision and rollback artifact.

## 11. Generic Instantiation Gate Template

When the v2 blueprint incorporates these gates, its structured tasks may use the template below for
unique IDs, typed dependencies, deliverables, covered obligation IDs, owned sources, validation
specs, and stable gate IDs. The table is descriptive vocabulary, not a checklist or source of
requirements/state. Every new theorem starts in `planned` mode with no accepted inherited evidence.

| Template id | Required action | Depends on | Required acceptance evidence |
|---|---|---|---|
| `<UID>-G01` | Freeze canonical claim and Lean expression fingerprint | none | intake plus mutation-tested statement certificate |
| `<UID>-G02` | Select foundation, TCB, computation, platform, and freshness profiles | G01 | versioned approved profiles |
| `<UID>-G03` | Freeze schema, artifact authority, owners, and lifecycle activation | G01, G02 | valid instance manifest and activation receipt |
| `<UID>-D01` | Precommit discovery protocol and freeze inventory version | G01 | query protocol hash and inventory hash |
| `<UID>-H01` | Audit pinpoint primary human sources and errata | G01, D01 | reviewed source crosswalks and H states |
| `<UID>-M01` | Audit repo-local, mathlib, and external formal candidates | G01, D01 | candidate/provenance ledger with exact targets |
| `<UID>-T01` | Freeze canonical obligation registry and eligibility | H01, M01 | immutable registry hash and reviewed exclusions |
| `<UID>-T02` | Build typed proof/refinement/evidence/trust/workflow graphs | T01 | schema-valid typed graphs and root reachability |
| `<UID>-T03` | Expand high-risk/import/computation work into semantic leaves | T02 | no hidden work; substantive ledgers and bridge nodes |
| `<UID>-M02` | Resolve wrappers, terminal bodies, dependencies, axioms, and TCB | T03 | transitive provenance/trust closure per candidate |
| `<UID>-M03` | Classify every obligation and source boundary | M02 | 100% inventory and boundary classification |
| `<UID>-M04` | Integrate eligible external completion candidates | M03 | pin/import/check receipt or explicit blocker |
| `<UID>-M05` | Implement prioritized open machine obligations | M03, M04 | exact kernel evidence per closed obligation |
| `<UID>-C01` | Check every nonleaf composition certificate | M05 | child-fingerprint harness and dependency report |
| `<UID>-R01` | Produce and independently review node-specific readable entries | T03, M03 | anchored structured R records, no filler |
| `<UID>-V01` | Execute all structured node and aggregate recipes | C01, R01 | content-addressed receipts on immutable snapshot |
| `<UID>-V02` | Perform cold clean, offline, supply-chain, and platform validation | V01 | hermetic signed attestation and archive replay |
| `<UID>-V03` | Perform independent verification with second verifier | V02 | distinct signed attestation and agreement report |
| `<UID>-V04` | Build deterministic evidence bundle and generated public views | V03 | repeatable digest and clean generated diff |
| `<UID>-A-Z` | Decide audit completion | H01, M03, R01, V04 | full frozen-inventory classification; proof may remain open |
| `<UID>-T-Z` | Decide theorem completion | A-Z, C01, V04 | exact root plus all root-critical release gates |

`<UID>-A-Z` MUST remain independent of `<UID>-M04`, `<UID>-M05`, and `<UID>-C01` success except
where those tasks create records needed to classify their current open state. `<UID>-T-Z` is
forbidden unless the exact root is `M0-*`, all required root-critical public nodes are independently
accepted `R0`, human status is separately recorded, no unresolved theorem-completion task remains,
and all statement, composition, provenance, trust, source, reproducibility, freshness, and
independent-verification gates pass.

### 11.1 Required Generic Conformance Fixtures

A framework implementation is not reusable merely because one flagship dossier passes. Before
claiming generic conformance it MUST validate, with the same unmodified core:

1. a small repo-local Lean 4 theorem with no external proof body;
2. a theorem closed through a pinned mathlib body and a local wrapper;
3. a theorem with an honestly open root but complete audit;
4. a computation/certificate theorem exercising the computation profile;
5. a second nonisomorphic mathematical domain;
6. a second materially different prover adapter before claiming prover-neutral conformance.

The conformance suite also includes all adversarial and metamorphic fixtures in section 10.7.

## 12. First Instance: `THM-M-0387` rev-5.6

### 12.1 Starting Hypotheses to Re-Audit

These are discovery inputs from the pre-rev-5.6 repository, not accepted rev-5.6 completion marks:

- The repository reports mathlib-backed wrappers for `n = 3` and `n = 4`.
- It reports derived wrappers for integer `n = 4` and `n = 8` via exponent divisibility.
- It reports a pinned `leanprover-community/flt-regular` wrapper for regular primes.
- It reports that complete `FermatLastTheorem` is not repo-local closed.
- Existing human-readable material reports detailed `n = 4` and regular-prime package expansion.
- A Stage1 candidate file reports an external full-FLT project whose terminal axiom report contains
  `sorryAx`; this must remain a blocker unless a fresh audit proves otherwise.

No item below may be checked merely because one of these sentences appears in an existing file.

### 12.2 Required FLT Proof Tree

The executor must instantiate the node schema and recursively expand this tree. Nodes labeled
`expand` are packages, never final leaves.

```text
M0387-ROOT  FermatLastTheorem
|
+-- M0387-S  Statement/foundation layer
|   +-- S01 FermatLastTheoremWith over the selected domains
|   +-- S02 FermatLastTheoremFor n
|   +-- S03 full FermatLastTheorem quantifier structure
|   +-- S04 natural/integer/rational transports
|   +-- S05 primitive/coprime solution formulation
|   `-- S06 accepted classical/choice/quotient/axiom boundary
|
+-- M0387-R  Exponent reduction and recomposition
|   +-- R01 exclude n <= 2 from target
|   +-- R02 exponent-divisibility monotonicity
|   +-- R03 reduce composite exponents to prime exponent or n = 4
|   +-- R04 all odd-prime exponents family
|   `-- R05 FermatLastTheorem.of_odd_primes root assembly
|
+-- M0387-B3  Exponent 3 coverage branch
|   +-- B3.1 mod-9 / Case-I boundary (expand)
|   +-- B3.2 generalized cubic equation (expand)
|   +-- B3.3 solution-object normalization (expand)
|   +-- B3.4 multiplicity descent (expand)
|   `-- B3.5 terminal theorem and local wrapper
|
+-- M0387-B4  Exponent 4 branch
|   +-- B4.1 bridge packaging
|   +-- B4.2 minimal normalization
|   +-- B4.3 first primitive Pythagorean-triple classification
|   +-- B4.4 second triple classification
|   +-- B4.5 coprimality bridge
|   +-- B4.6 square extraction and sign cleanup
|   +-- B4.7 smaller-solution construction and strict size comparison
|   +-- B4.8 contradiction/terminal theorem
|   `-- B4.9 integer transport and divisible-exponent derivatives
|
+-- M0387-RP  Regular odd-prime branch
|   +-- RP.1 regularity/class-group setup
|   +-- RP.2 primitive MayAssume reduction
|   +-- RP.3 Case I outer statement
|   |   +-- ideal extraction (expand)
|   |   +-- principalization (expand)
|   |   `-- element recovery and Case I close (expand)
|   +-- RP.4 Case II pi-language reduction
|   |   +-- ideal-factor layer (expand)
|   |   +-- distinguished-root layer (expand)
|   |   +-- raw descent core (expand)
|   |   `-- no-solution close (expand)
|   `-- RP.5 Case I/II merge and flt_regular wrapper
|
`-- M0387-WTW  General odd-prime / Wiles-Taylor-Wiles branch
    +-- W01 primitive odd-prime counterexample normalization (expand)
    +-- W02 Frey curve construction
    |   +-- curve definition and nonsingularity
    |   +-- discriminant and minimal model
    |   +-- semistability
    |   `-- conductor/local reduction data
    +-- W03 mod-p Galois representation
    |   +-- construction
    |   +-- irreducibility hypotheses/exceptional cases
    |   +-- ramification and determinant
    |   `-- compatibility with Frey invariants
    +-- W04 modularity of semistable elliptic curves over Q
    |   +-- modular forms and Hecke algebra foundations (expand)
    |   +-- residual modularity/base cases (expand)
    |   +-- deformation problems and universal rings (expand)
    |   +-- local deformation conditions (expand)
    |   +-- Taylor-Wiles auxiliary primes (expand)
    |   +-- patching and numerical criterion (expand)
    |   +-- minimal R=T theorem (expand)
    |   +-- non-minimal lifting (expand)
    |   `-- semistable modularity terminal (expand)
    +-- W05 Ribet/level-lowering bridge
    |   +-- representation hypotheses
    |   +-- conductor lowering
    |   +-- modular level transition
    |   `-- lowered representation terminal
    +-- W06 terminal low-level modular-form impossibility (expand)
    +-- W07 Frey modularity versus level-lowering contradiction
    +-- W08 all odd-prime exponent closure
    `-- W09 recomposition with n = 4 into exact root
```

The tree is a mandatory minimum architecture. Source/code audit may add nodes. It may not collapse
`W02`-`W06` into prose phrases or one-step leaves. Each `expand` package must be recursively split
until the rev-5.6 leaf stop rule is met.

### 12.3 Historical `THM-M-0387` Execution Record

Compatibility note: this record began as the first rev-5.6 execution instance. Its former checkbox
states are retained below only as the words `historically checked` and `historically open`; they are
not a live checklist, writable cursor, or reusable template, and they do not prove conformance with
the generalized gates added in sections 0-11. `Docs/Stage1_Blueprint_v2.md` is the sole requirements,
ordering, and task-state authority. `Depends`, deliverables, and evidence remain part of each legacy record. A future schema
migration MUST preserve these historical observations, recompute dependency legality, and use
`needs_review` rather than inventing new acceptance.

#### A. Governance and Statement Freeze

- Historically checked: `S56-M0387-A01` Freeze the exact natural-number root statement and its quantifiers.
  Depends: none. Deliverable: legacy intake record. Evidence: comparison with the selected Lean
  declaration under the original rev-5.6 gate. Generalized gate still requires an elaborated
  expression/environment fingerprint and statement mutation fixtures.
- Historically checked: `S56-M0387-A02` Freeze the natural/integer/rational, primitive, and exponent-specific
  equivalence directions.
  Depends: `S56-M0387-A01`. Deliverable: equivalence map. Evidence: primary source or checked declarations in
  both required directions. Gate: no prose-only equivalence.
- Historically checked: `S56-M0387-A03` Freeze the accepted axiom/foundation policy and disallowed placeholder policy.
  Depends: `S56-M0387-A01`. Deliverable: axiom policy. Evidence: explicit accepted baseline and commands for
  reporting deviations. Gate: `sorryAx` and unreviewed custom axioms are disallowed.
- Historically checked: `S56-M0387-A04` Freeze stable public roles and the proof-unit node schema without creating a
  second progress authority.
  Depends: `S56-M0387-A01`. Deliverable: artifact map. Evidence: path/role table. Gate: runtime paths excluded.

#### B. Independent Human-Proof Debt Audit

- Historically checked: `S56-M0387-H01` Audit the exact human proof status of the root FLT statement, including accepted
  Wiles/Taylor-Wiles sources, corrections, and assumption match.
  Depends: `S56-M0387-A01`, `S56-M0387-A03`. Deliverable: root `H` classification. Evidence: primary sources and crosswalk.
- Historically open: `S56-M0387-H02` Audit human sources for exponent reduction, `n = 3`, and `n = 4`.
  Depends: `S56-M0387-A02`. Deliverable: branch-level `H` records. Evidence: exact sources and statement match.
- Historically open: `S56-M0387-H03` Audit the Kummer regular-prime human proof and match Case I/II terminology to
  the formal source tree.
  Depends: `S56-M0387-A02`. Deliverable: regular-prime `H` record. Evidence: primary proof/source crosswalk.
- Historically open: `S56-M0387-H04` Assign `H0`-`H5` independently to every final proof-tree node.
  Depends: `S56-M0387-H01`, `S56-M0387-H02`, `S56-M0387-H03`, `S56-M0387-T03`. Deliverable: complete human-debt ledger. Gate: `100%` of
  required nodes classified; no machine status used as a substitute for human-source evidence.

#### C. Machine Artifact Discovery and Re-Audit

- Historically checked: `S56-M0387-M01` Re-audit repo-local FLT modules, wrappers, samples, manifests, and validation
  entrypoints from source rather than metadata claims.
  Depends: `S56-M0387-A01`, `S56-M0387-A03`. Deliverable: local candidate ledger. Evidence: exact files/declarations.
- Historically checked: `S56-M0387-M02` Re-audit pinned mathlib statement/reduction, `n = 3`, `n = 4`, transport, and
  monotonicity declarations at the actual manifest revision.
  Depends: `S56-M0387-M01`. Deliverable: mathlib candidate ledger. Evidence: module, declaration, revision,
  normalized type, proof-body boundary, and axiom report.
- Historically checked: `S56-M0387-M03` Re-audit `flt-regular` pin, transitive modules, terminal theorem, proof-body
  location, placeholder state, compatibility, and repo-local wrapper.
  Depends: `S56-M0387-M01`. Deliverable: external-pinned ledger. Evidence: immutable revision and local closure.
- Historically checked: `S56-M0387-M04` Re-audit every known full-FLT Lean 4 project, including the previously reported
  `ImperialCollegeLondon/FLT` candidate, at fresh immutable revisions.
  Depends: `S56-M0387-A01`, `S56-M0387-A03`. Deliverable: external full-FLT ledger. Evidence: exact terminal type,
  `#print axioms`, placeholder scan, toolchain pin, and reproducibility result.
- Historically checked: `S56-M0387-M05` Search for additional Lean 4 FLT formalizations, aliases, forks, extracted
  proof bodies, and compatible modularity/level-lowering components.
  Depends: `S56-M0387-A01`. Deliverable: dated search ledger, including negative queries/access limits.
- Historically checked: `S56-M0387-M06` Classify all discovered candidates as `M0-L/W/P`, `M1`, `M2`, `M3`, `M4`, or
  `M5`; generate an integration task for each `M1` and reopening condition for each `M5`.
  Depends: `S56-M0387-M01`, `S56-M0387-M02`, `S56-M0387-M03`, `S56-M0387-M04`,
  `S56-M0387-M05`, `S56-M0387-T03`. Deliverable: complete machine-debt ledger. Gate: no anchor-only
  candidate counted as completed.

#### D. Full Tree Expansion

- Historically checked: `S56-M0387-T01` Materialize `M0387-S` and `M0387-R` with exact formal targets, edges, and
  boundary cases.
  Depends: `S56-M0387-A01`, `S56-M0387-A02`, `S56-M0387-A03`, `S56-M0387-M02`.
  Deliverable: statement/reduction subtree. Gate: exact root assembly edge.
- Historically checked: `S56-M0387-T02` Materialize the `B3`, `B4`, and `RP` trees from actual formal source structure,
  preserving every high-risk imported theorem as a bridge node.
  Depends: `S56-M0387-M02`, `S56-M0387-M03`. Deliverable: special-branch subtrees. Gate: no package exceeds leaf rules.
- Historically checked: `S56-M0387-T03` Materialize and recursively expand `M0387-WTW` from primary human proof
  architecture and all located formal components.
  Depends: `S56-M0387-H01`, `S56-M0387-M04`, `S56-M0387-M05`. Deliverable: full modern-proof subtree. Gate: W02-W06 and all
  source-identified high-risk packages expanded; no "standard" black boxes.
- Historically checked: `S56-M0387-T04` Add explicit external/automation/computation/axiom boundary nodes across the
  complete tree.
  Depends: `S56-M0387-T01`, `S56-M0387-T02`, `S56-M0387-T03`. Deliverable:
  trust-boundary overlay. Gate: every nonlocal or automated edge named.
- Historically checked: `S56-M0387-T05` Produce independent `<=100` logical-step ledgers for all final leaves and split
  every oversized node.
  Depends: `S56-M0387-T04`. Deliverable: leaf ledgers. Gate: no hidden major theorem counted as one step.
- Historically checked: `S56-M0387-T06` Validate tree identity, edge completeness, exhaustiveness, parent composition,
  unique ids, and DAG acyclicity.
  Depends: `S56-M0387-T05`. Deliverable: tree audit. Gate: classification denominator frozen at `100%` discovered nodes.

#### E. Machine-Coverage Maximization Work Queue

- Historically checked: `S56-M0387-C01` Re-establish exact repo-local checked closure for statement/reduction APIs,
  without claiming root closure.
  Depends: `S56-M0387-M02`, `S56-M0387-T01`, `S56-M0387-T06`. Evidence: node-scoped kernel checks and axiom reports.
- Historically checked: `S56-M0387-C02` Re-establish `n = 3` exact branch closure and classify proof-body boundary.
  Depends: `S56-M0387-M02`, `S56-M0387-T02`, `S56-M0387-T06`. Evidence: terminal type, wrapper check, axiom report.
- Historically checked: `S56-M0387-C03` Re-establish `n = 4`, integer transport, and divisible-exponent derivative
  closure; separately classify every node.
  Depends: `S56-M0387-M02`, `S56-M0387-T02`, `S56-M0387-T06`. Evidence: node-scoped checks; no wrapper/body conflation.
- Historically checked: `S56-M0387-C04` Re-establish regular-prime closure through the pinned dependency and local
  wrapper, preserving `upstream proof body / repo-local checked dependency / not vendored`.
  Depends: `S56-M0387-M03`, `S56-M0387-T02`, `S56-M0387-T06`. Evidence: dependency pin, terminal theorem, wrapper and axiom checks.
- Historically checked: `S56-M0387-C05` Integrate every eligible placeholder-free `M1` component found for the general
  odd-prime branch; record concrete blockers for incompatible candidates.
  Depends: `S56-M0387-M04`, `S56-M0387-M05`, `S56-M0387-M06`, `S56-M0387-T03`,
  `S56-M0387-T06`. Evidence: pin/import/check or explicit blocker.
- Historically open: `S56-M0387-C06` Implement or import the remaining W01-W06 leaves in dependency order, splitting
  any item that cannot converge within its budget.
  Depends: `S56-M0387-C05`, `S56-M0387-T05`. Evidence: `M0-*` packet per leaf. Gate: no proof placeholder.
- Historically open: `S56-M0387-C07` Check W07-W09 composition: contradiction, all odd-prime closure, and root
  recomposition.
  Depends: `S56-M0387-C03`, `S56-M0387-C06`. Evidence: exact checked composition declarations and root axiom report.
- Historically checked: `S56-M0387-C08` Compute truthful machine coverage metrics and root status.
  Depends: `S56-M0387-C01`, `S56-M0387-C02`, `S56-M0387-C03`, `S56-M0387-C04`,
  `S56-M0387-C05`, `S56-M0387-C06`, `S56-M0387-C07`. Deliverable: numerator/denominator
  ledger. Gate: root reported independently.

`C01`-`C08` are superseded compatibility records. Their `Historically checked` labels report only
the former rev-5.6 cursor; they do not satisfy immutable-snapshot, typed-graph, semantic-ledger,
hermetic-release, or independent-verifier gates unless corresponding new receipts are produced.

#### F. Readability-Debt Clearance

- Historically checked: `S56-M0387-R01` Produce the short whole-tree proof outline with exact machine boundaries.
  Depends: `S56-M0387-T06`, `S56-M0387-M06`. Gate: reader can see root, branches, debts, and formal anchors in one route.
- Historically checked: `S56-M0387-R02` Reconstruct every `M0-*` statement/reduction, `n = 3`, and `n = 4` node from
  machine evidence using the ten-part readable entry standard.
  Depends: `S56-M0387-C01`, `S56-M0387-C02`, `S56-M0387-C03`, `S56-M0387-T05`.
  Gate: all such nodes reach `R0` or retain explicit lower status.
- Historically checked: `S56-M0387-R03` Reconstruct every `M0-*` regular-prime node from pinned machine evidence,
  including Case I/II branch logic and upstream/local boundary.
  Depends: `S56-M0387-C04`, `S56-M0387-T05`. Gate: no upstream proof described as a repo-local body.
- Historically checked: `S56-M0387-R04` Reconstruct every machine-closed Wiles/Taylor-Wiles node and describe every
  machine-open node only as a proof plan or blocker.
  Depends: `S56-M0387-C05`, `S56-M0387-C06`, `S56-M0387-C07`, `S56-M0387-C08`,
  `S56-M0387-T05`. Gate: grammatical and status boundary prevents completion overclaim.
- Historically checked: `S56-M0387-R05` Assign `R0`-`R4` independently to every required public node and clear all
  readability debt required for release.
  Depends: `S56-M0387-R01`, `S56-M0387-R02`, `S56-M0387-R03`, `S56-M0387-R04`.
  Gate: `100%` readable classification; every `M0-*` release node is `R0`.
- Historically checked: `S56-M0387-R06` Verify canonical names, links, dates, equations, hypotheses, and status vectors
  across short and long reader routes.
  Depends: `S56-M0387-R05`. Gate: no competing node vocabulary or stale runtime reference.

#### G. Validation, Reconciliation, and Final Decision

- Historically checked: `S56-M0387-V01` Run node-scoped checks for every proposed `M0-*` classification.
  Depends: `S56-M0387-C08`. Evidence: dated command/result per node or coherent covered batch.
- Historically checked: `S56-M0387-V02` Run full local aggregate validation in the pinned environment.
  Depends: `S56-M0387-V01`. Evidence: toolchain/library/external revisions, command, exit result, covered modules.
- Historically checked: `S56-M0387-V03` Run placeholder, axiom, declaration-type, dependency-pin, and proof-body-location
  audits after the aggregate build.
  Depends: `S56-M0387-V02`. Gate: no disallowed placeholder/axiom and no statement mismatch.
- Historically checked: `S56-M0387-V04` Reconcile blueprint, proof-unit manifest, metadata, README, machine audit,
  process audit, readable surfaces, and validation record in one master-owned integration step.
  Depends: `S56-M0387-H04`, `S56-M0387-M06`, `S56-M0387-R06`, `S56-M0387-V03`. Gate: all summaries derive from accepted evidence.
- Historically checked: `S56-M0387-V05` Report all four legacy node-row coverage metrics, every remaining `H/M/R` debt, and exact root
  vector with absolute date.
  Depends: `S56-M0387-V04`. Gate: no combined percentage or vague global "verified" label. These
  legacy metrics do not replace the generalized unique-obligation, distinct-body, source-boundary,
  critical-path, and cut-set metrics.
- Historically checked: `S56-M0387-V06` Decide audit completion.
  Depends: `S56-M0387-V05`. Gate: tree/source/debt classification coverage is `100%`; blockers may remain but
  must be concrete. This does not imply theorem completion.
- Historically open: `S56-M0387-V07` Decide theorem completion.
  Depends: `S56-M0387-V06`. Gate: exact root is `M0-*`, required readable nodes are `R0`, human status is
  independently recorded, all root dependencies are master-accepted, and no disallowed axiom,
  placeholder, open integration debt, `[ ]`, or `[_]` remains in the root completion DAG.

## 13. Final Master Audit

Before any rev-5.6 theorem instance can close, the master must answer all questions with evidence:

1. Is lifecycle state legal, append-only, and bound to one immutable instance snapshot?
2. Is the proved elaborated expression exactly the frozen canonical target, or connected by a
   checked transport that preserves every binder, assumption, domain, universe, and boundary case?
3. Was the canonical obligation universe frozen before status discovery, with reviewed exclusions?
4. Are all proof/refinement/provenance/evidence/trust/workflow edges typed and semantically valid?
5. Is every genuine proof branch represented and exhaustive, with all high-risk/import/computation
   work expanded into substantive semantic leaves?
6. Does every closed parent have a checked composition certificate consuming its exact children?
7. Are aliases/wrappers/transports deduplicated from terminal proof-body credit, and do refactoring
   metamorphic tests preserve the metrics?
8. Are wrapper, conclusion, terminal declaration, proof body, project, revision, and source digest
   separately resolved rather than self-reported?
9. Are axiom, declaration dependency, placeholder, unsafe, oracle, external code, and TCB results
   machine-derived from actual terminal objects and accepted by versioned profiles?
10. Are all direct/transitive dependencies clean, origin-verified, content-addressed, licensed, and
    restorable from the recorded closure?
11. Is every `M0-*` label supported by a content-addressed `E0/E1` receipt on the exact source tree?
12. Are computation certificates replayable, exact in scope, and rejected when tampered?
13. Is every `H0` supported by pinpoint primary-source/assumption/errata mapping and independent
    review, rather than a broad citation?
14. Is every `R0` anchored, structurally complete, fingerprint-linked, substantive, and independently
    reviewed; are machine-open nodes explicitly plans/blockers?
15. Did every structured validation spec run exactly as recorded, with claimed declarations covered?
16. Did a fresh empty-cache cold build and network-denied offline replay reproduce the result on the
    declared platform profile without hard-coded user paths?
17. Do two independently provisioned verifiers and an independently implemented minimal checker
    agree on immutable inputs, normalized results, graph state, root, and metrics?
18. Do mutation/adversarial tests kill the false statement, graph, trust, denominator, cache,
    command, stale-evidence, readability, and public-summary cases they claim to cover?
19. Is the evidence bundle deterministic, signed, current, unrevoked, archived, and the sole source
    of generated public metrics/status?
20. Are audit completion and theorem completion computed separately, with the exact root boolean,
    open cut sets, unique coverage, source-boundary coverage, and all debts visible?

Any "no," missing evidence, indirect evidence, or uncertainty keeps the affected item unfinished.

## 14. Definition of rev-5.6 Success

Rev-5.6 succeeds as an **audit** only when the frozen inventory is fully classified, source-boundary
coverage is complete, typed graphs and execution state are valid, evidence and public projections
are reconciled, and every remaining blocker is concrete. This may coexist with any honest open
machine status.

The root theorem is **theorem-complete** only at `M0-L`, `M0-W`, or `M0-P` with exact canonical
statement identity, checked child composition, accepted provenance/axiom/TCB closure, immutable
source and dependency receipts, independently accepted `R0` where required, hermetic reproduction,
independent verification, and a current deterministic release bundle. A theorem may finish the
audit while retaining `M1`-`M5`; then the audit is complete, the theorem is not, and every blocker
stays visible.

The framework itself may be called **theorem-generic** only after the same unmodified generic core
passes the conformance fixtures in section 11.1. It may be called **prover-neutral** only after a
second materially different prover adapter passes the adapter contract and canonical-claim mapping.
Lean 4 remains the primary mathematical profile, not an excuse to hard-code one theorem, one package
layout, one axiom set, one home directory, or one expected metric into generic acceptance logic.

For the retained `THM-M-0387` compatibility instance, its legacy local Lean check remains evidence
for the exact declarations it covered, not proof that the generalized assurance gates retroactively
passed. Complete FLT may be marked theorem-complete only when its exact root and every current gate
above close. No partial coverage, duplicate wrappers, polished prose, historical mathematical
certainty, or successful framework lint substitutes for that checked and attested root.

## 15. Stage1 v2 Execution-State Pointer

The former generated phase checklist was migrated without state loss to
`Docs/Stage1_Blueprint_v2.md`. That file is the sole requirements, ordering, and task-state
authority; the execution DAG and daily todo are derived projections. This section is only a pointer.
