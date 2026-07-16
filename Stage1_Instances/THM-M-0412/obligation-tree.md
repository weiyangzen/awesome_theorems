# THM-M-0412 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 29 canonical obligations for
`S56-M-0412-OBLIGATION_TREE` before any proof-closure status is credited. The
source identity is unresolved: the repository supplies only the label "Pierce
conjecture", a Trygve Nagell attribution, the year 1948, and a topic gloss about
integer points on certain cubic curves. It supplies no proposition, curve
family, domains, binders, hypotheses, conclusion, or primary-source locator.

The denominator therefore starts with `M0412-ROOT-IDENTITY`, the obligation to
identify the exact theorem. The rest is an explicitly conditional, source-
identity-dependent arithmetic-geometry architecture. Every fingerprint is
marked `planned-identity-dependent`; none is an elaborated Lean statement.
Choosing Nagell-Lutz, another Nagell theorem, an arbitrary cubic, or the legacy
abstract predicate package would substitute the theorem and is forbidden.

All seven mandatory layers are present. Eligibility and risk were assigned
before the all-open `H5 / M4 / R4` status was recorded. A resolved claim or any
split, merge, exclusion, or eligibility change requires registry version 2 and
an append-only old/new ID delta; version 1 remains reportable.

## Typed route

```text
M0412-ROOT-IDENTITY  identify the exact source theorem [open M4]
|-- S  source, exact claim, domains, boundaries, transports, foundation
|-- N  curve/point normalization and transport back
|-- B  degenerate/generic branches and exhaustive recomposition
|-- C  curve/point constructions, well-definedness, invariants, compatibility
|-- L  arithmetic engine, geometric engine, exact classification
|-- X  imports, source, provenance, trust, readability, workflow
`-- T  generic conclusion, transport, and exact root assembly
```

The proof and refinement graphs carry reciprocal `proof_requires`/`composes`
or `logical_decomposition`/`composes` pairs. Provenance, evidence, trust,
documentation, and workflow relations are separate and have no proof credit.
Every graph indexes all 29 nodes; every mathematical proof-architecture node
is reachable from the root in the union of proof and refinement relations,
while the six `X` overlays are linked in their own typed graphs. No graph
contains an orphan or cycle under its declared direction.

## Composition boundary

`ObligationTree.lean` is intentionally declaration-free. No exact parent or
child Lean target exists, so a conditional composition harness would have to
invent a proposition or select a nearby theorem. That would be a substitution,
not a certificate. Accordingly the composition-certificate list is empty and
the graph records a checked `not_machine_eligible_no_exact_parent_or_child_targets`
classification. Once an exact source claim and child signatures exist, every
nonleaf must receive a Lean harness that consumes exactly its required children
and yields its exact parent.

## Node ledgers

Each entry follows the rev-5.6 readable order. These compact ledgers are
architecture records, not `R0` reconstructions or mathematical proof bodies.

### M0412-ROOT-IDENTITY

1. **Claim:** Identify one exact immutable source proposition for the catalog entry.
2. **Role:** It is the root and gates every downstream signature.
3. **Inputs:** Catalog metadata plus `M0412-S-SOURCE` and `M0412-S-CLAIM`.
4. **Proof route:** Reconcile title, attribution, year, publication, and exact proposition; reject nonidentical candidates.
5. **Branch logic:** The identity must be unique; conflicting Nagell results remain rejected branches.
6. **Formal map:** No declaration exists; planned fingerprint only.
7. **Trust boundary:** Source and independent-review evidence only; no kernel credit.
8. **Step ledger:** `STEP-01` bind immutable source bytes; `STEP-02` crosswalk metadata to one proposition; `STEP-03` approve uniqueness and emit the exact target input.
9. **Boundary:** Does not itself prove the eventual theorem.
10. **Status vector:** `[H5, M4, R4]`; no accepted evidence.

### M0412-S-SOURCE

1. **Claim:** Bind publication, locator, original title, author, date, corrections, and translation crosswalk.
2. **Role:** Supplies the authoritative human statement boundary.
3. **Inputs:** Primary-source bytes and catalog metadata.
4. **Proof route:** Archive and hash the source, locate the exact theorem, map every catalog field, and resolve conflicts.
5. **Branch logic:** Distinguish the 1935 Nagell-Lutz lead, 1948 Nagell lead, and any actual Pierce-named claim.
6. **Formal map:** `source-statement-crosswalk.md`; no Lean declaration.
7. **Trust boundary:** Independent source reviewer required.
8. **Step ledger:** `STEP-01` pin source; `STEP-02` locate claim; `STEP-03` review crosswalk.
9. **Boundary:** Bibliography alone cannot establish proof or formal identity.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-S-CLAIM

1. **Claim:** Transcribe the exact curve, variables, hypotheses, conclusion, and proof boundary.
2. **Role:** Supplies the canonical mathematical target.
3. **Inputs:** `M0412-S-SOURCE`, domain and boundary records.
4. **Proof route:** Expand every incorporated definition and preserve binder order and scope.
5. **Branch logic:** Record all variants and select only the source-authorized formulation.
6. **Formal map:** Future `Statement.lean` declaration; currently declaration-free.
7. **Trust boundary:** Source fidelity and Lean elaboration are separate gates.
8. **Step ledger:** `STEP-01` transcribe; `STEP-02` normalize notation; `STEP-03` compare source and Lean fingerprints.
9. **Boundary:** The current planned signature is not an exact claim.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-S-DOMAIN

1. **Claim:** Fix number systems, curve and point models, nonsingularity, coercions, and typeclasses.
2. **Role:** Prevents a domain or representation substitution.
3. **Inputs:** Exact source claim.
4. **Proof route:** Map each source object to a Lean type and prove coercion compatibility.
5. **Branch logic:** Separate integral, rational, affine, projective, singular, and nonsingular cases only as licensed by the source.
6. **Formal map:** Planned exact signature.
7. **Trust boundary:** Pinned mathlib object models remain support only.
8. **Step ledger:** `STEP-01` enumerate objects; `STEP-02` select types; `STEP-03` validate coercions.
9. **Boundary:** Weierstrass API availability does not choose the theorem.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-S-BOUNDARY

1. **Claim:** Classify every degenerate and exceptional case in the source statement.
2. **Role:** Makes the proof domain exhaustive.
3. **Inputs:** Exact claim, domains, and curve hypotheses.
4. **Proof route:** Enumerate zero discriminant, singular curves, exceptional parameters, and points at infinity where applicable.
5. **Branch logic:** Prove the list is exhaustive and that excluded cases are source-authorized exclusions.
6. **Formal map:** Planned case predicates.
7. **Trust boundary:** No case may be inferred from a nearby theorem.
8. **Step ledger:** `STEP-01` enumerate; `STEP-02` justify; `STEP-03` feed branch split.
9. **Boundary:** Current metadata reveals no actual boundary cases.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-S-TRANSPORT

1. **Claim:** Check both directions between source and canonical Lean encodings.
2. **Role:** Prevents a weakened or strengthened formal target.
3. **Inputs:** Exact source and Lean fingerprints.
4. **Proof route:** Construct forward and reverse maps and compare all binders and conclusions.
5. **Branch logic:** Every alternate encoding is accepted or rejected independently.
6. **Formal map:** Future consumer-owned transport declaration.
7. **Trust boundary:** Provider evidence never transfers consumer acceptance.
8. **Step ledger:** `STEP-01` bind fingerprints; `STEP-02` prove both directions; `STEP-03` validate consumer bytes.
9. **Boundary:** No fingerprints or wrapper currently exist.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-S-FOUNDATION

1. **Claim:** Freeze logic, choice, quotient, computation, kernel, and dependency policy.
2. **Role:** Defines the formal trust boundary.
3. **Inputs:** Exact target and intended proof techniques.
4. **Proof route:** Select profiles, inspect axioms, and bind toolchain and dependency closure.
5. **Branch logic:** Classify symbolic, reflected, certified, and external computation separately.
6. **Formal map:** Future axiom and environment reports.
7. **Trust boundary:** Lean 4.29.0 and pinned mathlib are observed, not release accepted.
8. **Step ledger:** `STEP-01` select profiles; `STEP-02` inspect dependencies; `STEP-03` issue trust record.
9. **Boundary:** A warm API probe supplies no root trust credit.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-N-CURVE

1. **Claim:** Normalize the resolved curve into a canonical integral or rational Weierstrass model.
2. **Role:** Provides a stable arithmetic representation.
3. **Inputs:** Exact curve family and domain conditions.
4. **Proof route:** Construct the change of variables and prove preservation of hypotheses and conclusion.
5. **Branch logic:** Treat characteristic, singularity, and denominator cases explicitly.
6. **Formal map:** Planned normalization declaration.
7. **Trust boundary:** Pinned Weierstrass structures are infrastructure, not this theorem.
8. **Step ledger:** `STEP-01` construct model; `STEP-02` prove equivalence; `STEP-03` export normalized data.
9. **Boundary:** The correct normalization cannot be chosen before identity resolution.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-N-POINT

1. **Claim:** Normalize point coordinates and arithmetic representatives.
2. **Role:** Exposes primitive, reduced, or integral data consumed by descent.
3. **Inputs:** Normalized curve and exact point domain.
4. **Proof route:** Clear denominators, control gcd and sign choices, and prove representation validity.
5. **Branch logic:** Split zero denominators and exceptional coordinates where required.
6. **Formal map:** Planned point-normalization signature.
7. **Trust boundary:** No coordinate convention is inferred from the gloss.
8. **Step ledger:** `STEP-01` choose representative; `STEP-02` prove invariants; `STEP-03` bind normalized point.
9. **Boundary:** Open until exact variables and conclusion are known.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-N-TRANSPORT

1. **Claim:** Transport normalized results back to the original curve and point.
2. **Role:** Closes representation changes.
3. **Inputs:** Curve and point normalizations.
4. **Proof route:** Compose inverse maps and prove independence of choices.
5. **Branch logic:** Cover every normalization branch.
6. **Formal map:** Planned checked transport.
7. **Trust boundary:** Exact source and consumer fingerprints required.
8. **Step ledger:** `STEP-01` bind maps; `STEP-02` prove invariance; `STEP-03` emit original-object conclusion.
9. **Boundary:** No transport is currently machine eligible.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-B-DEGENERATE

1. **Claim:** Discharge all exact exceptional cases.
2. **Role:** Supplies one side of exhaustive branch recomposition.
3. **Inputs:** `M0412-S-BOUNDARY`.
4. **Proof route:** Prove each source-authorized boundary case directly or reduce it to a named leaf.
5. **Branch logic:** Cases remain distinct until exact recomposition.
6. **Formal map:** Planned boundary theorem family.
7. **Trust boundary:** No case is silently discarded.
8. **Step ledger:** `STEP-01` select case; `STEP-02` derive exact result; `STEP-03` hand off branch conclusion.
9. **Boundary:** The branch list is not yet source-backed.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-B-GENERIC

1. **Claim:** Prove the exact conclusion in the complementary nonsingular generic case.
2. **Role:** Carries the central mathematical proof.
3. **Inputs:** Core classification lemma.
4. **Proof route:** Consume constructions and arithmetic/geometric engines without hidden packages.
5. **Branch logic:** Genericity is the proved complement of all exceptional cases.
6. **Formal map:** Planned generic-branch declaration.
7. **Trust boundary:** No adjacent Nagell theorem is imported as a substitute.
8. **Step ledger:** `STEP-01` enter generic context; `STEP-02` apply exact classification; `STEP-03` emit branch result.
9. **Boundary:** Central proof remains wholly open.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-B-RECOMPOSE

1. **Claim:** Prove exhaustiveness and exact recomposition of all branches.
2. **Role:** Prevents a selected branch from masquerading as the theorem.
3. **Inputs:** Degenerate and generic branch conclusions.
4. **Proof route:** Establish exhaustive disjunction and eliminate every case into the same exact conclusion.
5. **Branch logic:** All children are required.
6. **Formal map:** Future Lean composition certificate.
7. **Trust boundary:** Certificate must consume exact child fingerprints.
8. **Step ledger:** `STEP-01` prove split; `STEP-02` consume each branch; `STEP-03` merge exact output.
9. **Boundary:** No exact branch signatures exist today.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-C-MODEL

1. **Claim:** Construct the curve, point, torsion, divisor, or descent objects required by the source proof.
2. **Role:** Creates the mathematical objects consumed by the engines.
3. **Inputs:** Normalized source data.
4. **Proof route:** Define every object and expose every choice.
5. **Branch logic:** Construction variants are separate until compatibility is proved.
6. **Formal map:** Planned constructor signatures.
7. **Trust boundary:** The available Weierstrass API is support only.
8. **Step ledger:** `STEP-01` construct; `STEP-02` typecheck; `STEP-03` hand off object.
9. **Boundary:** Exact objects depend on source resolution.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-C-WELLDEFINED

1. **Claim:** Prove every constructed object is well-defined and satisfies all domain conditions.
2. **Role:** Guards construction soundness.
3. **Inputs:** `M0412-C-MODEL`.
4. **Proof route:** Check equations, fields, integrality, nonsingularity, and quotient representatives.
5. **Branch logic:** Failure conditions return to explicit boundary branches.
6. **Formal map:** Planned well-definedness lemmas.
7. **Trust boundary:** No unchecked computation or oracle is allowed.
8. **Step ledger:** `STEP-01` unfold; `STEP-02` prove conditions; `STEP-03` certify object.
9. **Boundary:** No object exists yet.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-C-INVARIANTS

1. **Claim:** Establish every arithmetic and geometric invariant used downstream.
2. **Role:** Connects constructions to core lemmas.
3. **Inputs:** Model and well-definedness certificates.
4. **Proof route:** Derive discriminant, coordinate, torsion, divisibility, height, or descent identities actually present in the resolved proof.
5. **Branch logic:** Each invariant owns its own split if source formalization exposes one.
6. **Formal map:** Planned invariant package.
7. **Trust boundary:** No vague "standard calculation" is admitted.
8. **Step ledger:** `STEP-01` name invariant; `STEP-02` prove exact equation; `STEP-03` bind use.
9. **Boundary:** Listed invariant families are conditional, not claims about the unknown theorem.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-C-COMPATIBILITY

1. **Claim:** Prove construction compatibility and independence of choices.
2. **Role:** Makes normalization and representation changes semantically harmless.
3. **Inputs:** Invariants and normalization transports.
4. **Proof route:** Compare alternate representatives and show downstream outputs agree.
5. **Branch logic:** Cover all choices introduced by construction.
6. **Formal map:** Planned compatibility lemmas.
7. **Trust boundary:** Equality or equivalence direction must be explicit.
8. **Step ledger:** `STEP-01` compare; `STEP-02` prove invariance; `STEP-03` export canonical data.
9. **Boundary:** No exact choices are currently defined.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-L-ARITHMETIC

1. **Claim:** Prove the central Diophantine arithmetic engine for the resolved cubic problem.
2. **Role:** Carries descent, divisibility, valuation, or coprimality work.
3. **Inputs:** Exact construction invariants.
4. **Proof route:** Expand every major theorem and split every descent or minimality argument into substantive leaves.
5. **Branch logic:** Prime, parity, valuation, and exceptional-factor cases must be exhaustive.
6. **Formal map:** Planned core-lemma declarations.
7. **Trust boundary:** A short imported call remains a bridge obligation.
8. **Step ledger:** `STEP-01` freeze arithmetic hypotheses; `STEP-02` execute exact engine; `STEP-03` export arithmetic conclusion.
9. **Boundary:** No particular arithmetic theorem is asserted before source identity is known.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-L-GEOMETRIC

1. **Claim:** Prove the central curve-theoretic engine required by the exact conclusion.
2. **Role:** Connects geometric structure to finiteness, integrality, torsion, or classification.
3. **Inputs:** Invariants and compatibility results.
4. **Proof route:** Expand group-law, descent, height, or algebraic-geometry interfaces actually selected by the source theorem.
5. **Branch logic:** Curve types and exceptional loci remain explicit.
6. **Formal map:** Planned exact geometric lemmas.
7. **Trust boundary:** Mathlib point-group declarations supply no terminal theorem credit.
8. **Step ledger:** `STEP-01` bind curve context; `STEP-02` prove exact geometric claim; `STEP-03` export classification input.
9. **Boundary:** Nagell-Lutz is not selected by attribution alone.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-L-CLASSIFY

1. **Claim:** Complete the source theorem's exact existence, finiteness, exclusion, or classification result.
2. **Role:** Joins arithmetic and geometric engines.
3. **Inputs:** `M0412-L-ARITHMETIC` and `M0412-L-GEOMETRIC`.
4. **Proof route:** Consume both engines and prove precisely the resolved conclusion.
5. **Branch logic:** Preserve all classification cases and prove their completeness.
6. **Formal map:** Planned terminal core lemma.
7. **Trust boundary:** All required children must be exact and checked.
8. **Step ledger:** `STEP-01` bind engines; `STEP-02` derive classification; `STEP-03` supply generic branch.
9. **Boundary:** Conclusion kind remains unknown.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-IMPORTED

1. **Claim:** Inventory all imported declarations and terminal bodies by exact bytes and fingerprints.
2. **Role:** Owns the formal import boundary.
3. **Inputs:** Pinned repo-local and mathlib sources plus any admitted external project.
4. **Proof route:** Compare exact statements, trace bodies, and bind consumer imports or transports.
5. **Branch logic:** Exact, checked transport, rejected, and support-only candidates remain distinct.
6. **Formal map:** Dependency ledger and future proof receipt.
7. **Trust boundary:** Provider checkbox state is observation only.
8. **Step ledger:** `STEP-01` bind provider bytes; `STEP-02` compare fingerprints; `STEP-03` validate consumer use.
9. **Boundary:** Current anchor audit found support only and no terminal root.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-SOURCE

1. **Claim:** Pinpoint every material proof transition in primary sources.
2. **Role:** Owns human-source coverage.
3. **Inputs:** Source identity and all proof nodes.
4. **Proof route:** Map premises, transitions, conclusions, dependencies, and errata to stable locators.
5. **Branch logic:** Source variants are reviewed independently.
6. **Formal map:** Source crosswalk records.
7. **Trust boundary:** Qualified independent source review required for H0.
8. **Step ledger:** `STEP-01` locate; `STEP-02` map; `STEP-03` review.
9. **Boundary:** Current H5 means the source identity itself is absent.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-PROVENANCE

1. **Claim:** Close wrapper, alias, body, dependency, license, and consumer provenance.
2. **Role:** Prevents wrapper names or copied rows from becoming proof credit.
3. **Inputs:** Imported-boundary inventory and exact proof sources.
4. **Proof route:** Trace each terminal body and bind every consumer-owned byte sequence.
5. **Branch logic:** Local, mathlib, and external providers have separate evidence paths.
6. **Formal map:** Future provenance ledger and validation receipts.
7. **Trust boundary:** Acceptance never transfers between theorem owners.
8. **Step ledger:** `STEP-01` trace body; `STEP-02` bind bytes; `STEP-03` validate consumer.
9. **Boundary:** No provider reuse occurs in the empty v2 context.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-TRUST

1. **Claim:** Close kernel, axiom, dependency, platform, computation, and reproducibility trust.
2. **Role:** Supplies the release trust gate.
3. **Inputs:** Exact proof and composition sources.
4. **Proof route:** Inspect axioms and constants, replay hermetically, and audit supply chain.
5. **Branch logic:** Kernel, classical, computation, dependency, and platform boundaries remain separate.
6. **Formal map:** Future trust and validation receipts.
7. **Trust boundary:** The canonical `.lake` is used read-only in this worker.
8. **Step ledger:** `STEP-01` inventory TCB; `STEP-02` replay; `STEP-03` independently verify.
9. **Boundary:** A warm narrow elaboration is not release evidence.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-READABLE

1. **Claim:** Produce independently reviewed readable coverage for every root-critical node.
2. **Role:** Owns R0 separately from machine closure.
3. **Inputs:** Exact statements, proof bodies, sources, and formal anchors.
4. **Proof route:** Provide short and long routes with substantive step ledgers and boundary sentences.
5. **Branch logic:** Every mathematical branch appears in both graph and prose.
6. **Formal map:** This file is an architecture seed only.
7. **Trust boundary:** Independent reader receipt required.
8. **Step ledger:** `STEP-01` reconstruct; `STEP-02` crosslink; `STEP-03` review.
9. **Boundary:** This worker-authored tree is not R0.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-X-WORKFLOW

1. **Claim:** Obtain dependency-ordered worker, validation, review, and master receipts.
2. **Role:** Orders acceptance without becoming a proof premise.
3. **Inputs:** Every phase artifact and exact authority snapshot.
4. **Proof route:** Replay validators, independent review, CAS, and atomic receipt publication.
5. **Branch logic:** Worker self-test and master acceptance remain distinct.
6. **Formal map:** Phase receipts and scheduler role maps.
7. **Trust boundary:** Checkbox state is never proof evidence.
8. **Step ledger:** `STEP-01` self-test; `STEP-02` independent replay; `STEP-03` master decision.
9. **Boundary:** This worker can propose only `[_]`.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-T-GENERIC

1. **Claim:** Derive the exact source conclusion for the generic branch.
2. **Role:** Converts core classification into a branch terminal.
3. **Inputs:** Generic branch and classification lemma.
4. **Proof route:** Instantiate every exact parameter and discharge every side condition.
5. **Branch logic:** Only the proved generic context is consumed.
6. **Formal map:** Planned terminal declaration.
7. **Trust boundary:** Exact child fingerprints required.
8. **Step ledger:** `STEP-01` bind context; `STEP-02` apply classification; `STEP-03` emit conclusion.
9. **Boundary:** No terminal signature exists.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-T-TRANSPORT

1. **Claim:** Transport all branch results back to the canonical source formulation.
2. **Role:** Reverses normalizations and alternate encodings.
3. **Inputs:** Generic conclusion and normalization transport.
4. **Proof route:** Compose exact equivalences and preserve every hypothesis and conclusion.
5. **Branch logic:** Each representation branch must return to one target.
6. **Formal map:** Planned checked transport.
7. **Trust boundary:** Both statement fingerprints and consumer bytes required.
8. **Step ledger:** `STEP-01` bind result; `STEP-02` transport; `STEP-03` compare target fingerprint.
9. **Boundary:** No exact target exists.
10. **Status vector:** `[H5, M4, R4]`; open.

### M0412-T-ASSEMBLE

1. **Claim:** Consume every exact branch result and yield the complete resolved root theorem.
2. **Role:** It is the final child-to-root composition interface.
3. **Inputs:** Branch recomposition and transported generic conclusion.
4. **Proof route:** Apply exhaustive split, consume every child, and return the exact root target.
5. **Branch logic:** No child may be unused or replaced by an undeclared premise.
6. **Formal map:** `ObligationTree.lean` is declaration-free until exact signatures exist.
7. **Trust boundary:** Future harness must pass axiom, constant, and fingerprint checks.
8. **Step ledger:** `STEP-01` bind children; `STEP-02` compose; `STEP-03` compare exact root.
9. **Boundary:** Composition is classified ineligible, not passed or failed.
10. **Status vector:** `[H5, M4, R4]`; open.

## Open boundary

The frozen root cut set is `M0412-ROOT-IDENTITY`. No canonical theorem, formal
target, proof body, imported terminal declaration, composition certificate,
H0/R0 result, accepted obligation, audit completion, theorem completion,
validation, release, or master acceptance is claimed. The obligation-tree phase
can truthfully freeze this complete conditional architecture while all of those
later gates remain open.
