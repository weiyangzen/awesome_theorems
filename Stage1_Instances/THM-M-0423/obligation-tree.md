# THM-M-0423 frozen obligation architecture

Item: `S56-M-0423-OBLIGATION_TREE`.

Registry version 2 freezes 105 canonical obligations at denominator
`32a5c78d7f9cf7b59541a9a35c52331cf5055159b93dbe758b3eb6134f7da866`. The bundle contains 570 typed edges and
177 substantive ledger steps. All accepted closure sets are empty.

This is a source-informed implementation architecture, not a completed historical proof
reconstruction. Hasse 1924 is still only an H1 anchor: pinpoint node/page mapping, errata
review, and independent source review remain open. Planned signatures below are canonical
targets for later implementation, not declarations asserted to exist.

## Proof route

```text
ROOT -> directional split
  global-to-local -> nonzero pure tensor + base-change evaluation
  local-to-global -> diagonal and place normalization
    local classification -> real/complex + nonarchimedean invariant packages
    local hyperbolic residuals -> compatible global residual realization
    comparison H + residual -> global Witt uniqueness/cancellation
    explicit hyperbolic witness -> isometry transport -> original form
```

The proof graph contains no checked composition certificate. Every reverse proof edge is
`logical_decomposition`; the Lean declarations in `ObligationTree.lean` are conditional
or candidate harnesses only. In particular, `direction_package` consumes the open hard
direction and is not an inhabitant of that package without a premise.

## Node ledger

### m0423-s-interface

Fix the arbitrary number field, finite-dimensional module, nondegenerate quadratic form, nonzero isotropy predicate, and the two concrete completion families.

Formal target: `Stage1.THM_M_0423.HasseMinkowskiStatement`.

Output: The exact ordered binders and conclusion interface serialized by statement.json.

Projected status: `[H1, M3, R3]`; candidate classification: `M3_exact_statement_interface`.

Source boundary: Statement.lean:20-63; statement.json.

Budget: 20 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-s-boundary

Keep the nonzero witness and nondegeneracy hypothesis, include finite and infinite completions, and exclude unrestricted Hasse principles and rational-only substitutes.

Formal target: `Stage1.THM_M_0423.IsIsotropic plus the four statement mutations`.

Output: The exact degenerate-case, domain, binder-scope, and place-family boundary.

Projected status: `[H1, M3, R3]`; candidate classification: `M3_checked_statement_boundary`.

Source boundary: Statement.lean:20-63; StatementMutations.lean.

Budget: 18 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-s-coordinates

Relate the coordinate-free form to diagonal and homogeneous-polynomial presentations in both directions, including scalar extension and nonzero-witness transport.

Formal target: `planned exact signature: coordinate, diagonal, and polynomial presentations are pairwise isometric and preserve global and completion-wise IsIsotropic`.

Output: A bidirectional presentation transport with no theorem strengthening.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: source_statement_crosswalk.md; no checked alternate encoding.

Budget: 42 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-s-foundation

Account for propext, Classical.choice, Quot.sound, the pinned Lean/mathlib artifacts, and the prohibition on placeholders, unsafe declarations, oracles, and unreviewed native computation.

Formal target: `planned accepted foundation and TCB inclusion predicate for every root-relevant declaration`.

Output: The release foundation, computation, and TCB boundary.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: ObligationTree.lean axiom probes; anchor-audit.json.

Budget: 36 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-mathlib

Bind every used tensor-product, quadratic-form, place/completion, real-classification, approximation, and algebraic declaration to the pinned mathlib body and dependency closure.

Formal target: `pinned mathlib support boundary at 8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Output: Immutable support-declaration provenance without proof credit.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: anchor-audit.json mathlib_candidates; future proof receipts.

Budget: 45 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-external

Preserve the two immutable rational-only, placeholder-contaminated external candidates as rejected audit evidence and never use them as proof premises.

Formal target: `anchor-audit candidates S56-M-0423-E01 and S56-M-0423-E02`.

Output: The exact scope, placeholder, toolchain, and license blockers for both external candidates.

Projected status: `[H2, M5, R3]`; candidate classification: `M5_rejected_external_candidates`.

Source boundary: anchor-audit.json external_candidates.

Budget: 24 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-source

Map every mathematical proof node to a pinpoint primary source, its assumptions, dependencies, correction status, and an independent reviewer.

Formal target: `planned section-8.1 source-coverage predicate over required_human_source`.

Output: Node-level primary-source coverage without machine-proof credit.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: source_statement_crosswalk.md; Hasse 1924 pp. 113-130.

Budget: 60 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-provenance

Resolve local wrappers, terminal bodies, immutable revisions, licenses, direct dependencies, and transitive declaration provenance without duplicate credit.

Formal target: `planned content-addressed provenance-closure predicate`.

Output: Formal-body provenance without mathematical proof credit.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: anchor-audit.json; future proof receipts.

Budget: 54 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-trust

Audit the transitive Lean TCB, compiled artifacts, executables, axioms, unsafe/oracle boundaries, and replay environment for all credited bodies.

Formal target: `planned accepted trust-closure predicate`.

Output: Release-grade trust inventory without proof credit.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: ObligationTree.lean probes; future validation and release receipts.

Budget: 54 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-readable

Produce an independently reviewed readable reconstruction with assumptions, branch logic, boundaries, and formal/source anchors for every readable-required node.

Formal target: `planned section-8 readable-coverage predicate`.

Output: Reader-facing proof reconstruction without machine-proof credit.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: obligation-tree.md is architecture only.

Budget: 70 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-workflow

Require dependency-legal proof, validation, release, freshness, revocation, and independent-verification receipts before any promotion.

Formal target: `planned task and receipt acceptance predicate`.

Output: Workflow acceptance without mathematical proof credit.

Projected status: `[H2, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Docs/Stage1_Execution_DAG_rev-5.6.json.

Budget: 24 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-root

Every nondegenerate finite-dimensional quadratic form over an arbitrary number field is isotropic exactly when it is isotropic at every finite and infinite completion.

Formal target: `Stage1.THM_M_0423.HasseMinkowskiStatement`.

Output: Stage1.THM_M_0423.HasseMinkowskiStatement.

Projected status: `[H1, M3, R3]`; candidate classification: `M3_conditional_composition_harness_only`.

Source boundary: Statement.lean:57-63; statement.json expression hash.

Budget: 12 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-b-directions

Split the exact equivalence into global-to-local and local-to-global implications and require both conclusions under the same frozen binders.

Formal target: `planned exact package: GlobalToLocalObligation and LocalToGlobalObligation, jointly yielding HasseMinkowskiStatement`.

Output: Both exact directional implications with an exhaustive recomposition map.

Projected status: `[H1, M3, R3]`; candidate classification: `M3_conditional_composition_harness_only`.

Source boundary: ObligationTree.lean:23-95; conditional harness only.

Budget: 14 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-global-local

Carry a nonzero global isotropic witness to every finite and infinite completion by scalar extension.

Formal target: `Stage1.THM_M_0423.ObligationTree.GlobalToLocalObligation`.

Output: Global isotropy implies both exact completion-wise isotropy predicates.

Projected status: `[H1, M3, R3]`; candidate classification: `M0-L_requires_E0`.

Source boundary: ObligationTree.lean:23-29,60-71.

Budget: 18 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-pure-tensor

For every field extension, construct 1 tensor x from a nonzero isotropic x and prove both its nonzeroness and its zero quadratic value.

Formal target: `Stage1.THM_M_0423.ObligationTree.isotropic_after_baseChange`.

Output: A nonzero isotropic witness for the base-changed form.

Projected status: `[H1, M3, R3]`; candidate classification: `M0-L_requires_E0`.

Source boundary: ObligationTree.lean:45-58.

Budget: 20 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-x-flat-injection

The map x to 1 tensor x is injective for a field extension, so a nonzero global vector remains nonzero after scalar extension.

Formal target: `Module.FaithfullyFlat.tensorProduct_mk_injective`.

Output: Injectivity of the pure-tensor unit map used by the witness construction.

Projected status: `[H1, M3, R3]`; candidate classification: `M0-W_requires_E1`.

Source boundary: Mathlib/RingTheory/Flat/FaithfullyFlat/Algebra.lean.

Budget: 18 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-basechange-eval

Evaluate the base-changed quadratic form at 1 tensor x as the algebra-map image of Q(x).

Formal target: `QuadraticForm.baseChange_tmul`.

Output: The base-changed quadratic value of the pure tensor is zero whenever Q(x)=0.

Projected status: `[H1, M3, R3]`; candidate classification: `M0-W_requires_E1`.

Source boundary: Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean.

Budget: 12 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-local-global

From isotropy at every finite and infinite completion, derive a nonzero global isotropic vector for the original nondegenerate form.

Formal target: `Stage1.THM_M_0423.ObligationTree.LocalToGlobalObligation`.

Output: Stage1.THM_M_0423.IsIsotropic Q.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: ObligationTree.lean:30-39; selected classification-and-comparison route.

Budget: 24 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-n-diagonalize

Choose a finite basis, diagonalize the nondegenerate form with nonzero coefficients, and preserve global and completion-wise isotropy in both directions.

Formal target: `planned exact package: a diagonal weighted-squares form, an isometry Q ~= diag(a), all a_i != 0, and global/local isotropy iff transports`.

Output: A diagonal nondegenerate representative with checked global and local transports.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: QuadraticForm diagonalization candidates; exact wrapper not implemented.

Budget: 72 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-diagonal-merge

Recombine the diagonal representative, coefficient invariant, and both transport directions into one normalization package.

Formal target: `planned exact diagonal-normalization recomposition`.

Output: The complete diagonalization package consumed by the hard direction.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 24 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-basis-diagonal

Construct a basis in which Q is a weighted sum of squares and record the explicit isometry equivalence.

Formal target: `planned exact wrapper around QuadraticForm.equivalent_weightedSumSquares_units_of_nondegenerate'`.

Output: A finite coefficient family and isometry Q ~= weightedSumSquares(a).

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: pinned quadratic-form diagonalization declarations; wrapper audit open.

Budget: 48 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-nondegenerate-coefficients

For a diagonal representative of a nondegenerate form, every diagonal coefficient is nonzero.

Formal target: `planned exact signature: Nondegenerate(diag a) -> forall i, a i != 0`.

Output: A unit/nonzero coefficient family suitable for discriminants and Hilbert symbols.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: quadratic radical of a diagonal form; exact lemma audit open.

Budget: 30 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-global-isotropy-transport

A quadratic-form isometry transports nonzero isotropic witnesses globally in both directions.

Formal target: `planned exact signature: Q.IsometryEquiv Q' -> (IsIsotropic Q <-> IsIsotropic Q')`.

Output: Bidirectional global isotropy transport along the diagonalizing isometry.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: QuadraticForm.IsometryEquiv map and inverse.

Budget: 24 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-local-basechange-transport

Base changing a quadratic-form isometry to every completion preserves completion-wise nonzero isotropy in both directions.

Formal target: `planned exact signature: baseChange of an isometry equivalence induces IsIsotropicAfterBaseChange iff at each finite/infinite completion`.

Output: Bidirectional completion-wise isotropy transport for the diagonalizing isometry.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: QuadraticForm baseChange functoriality; exact isometry wrapper missing.

Budget: 44 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-n-place-family

Normalize the disjoint finite and infinite completion predicates to the complete place family used by the invariant route.

Formal target: `planned exact package equating the frozen conjunction with universal local data over finite plus infinite places`.

Output: One exhaustive local-data family with no omitted archimedean or nonarchimedean place.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Statement.lean:29-49; number-field place APIs.

Budget: 36 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-place-merge

Recompose finite-place coverage, infinite-place coverage, and their disjoint exhaustiveness into the exact local family.

Formal target: `planned exact finite/infinite place recomposition`.

Output: The normalized all-place package consumed by reciprocity and realization.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 22 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-finite-place-coverage

Index every nonarchimedean completion used in the proof by the exact NumberField.FinitePlace binder in the statement.

Formal target: `planned exact identity/transport for NumberField.FinitePlace completion fields`.

Output: Complete finite-place coverage with the statement's completion types.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Statement.lean:29-38.

Budget: 18 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-infinite-place-coverage

Index every archimedean completion used in the proof by the exact NumberField.InfinitePlace binder in the statement.

Formal target: `planned exact identity/transport for NumberField.InfinitePlace.Completion`.

Output: Complete infinite-place coverage with the statement's completion types.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Statement.lean:40-49.

Budget: 18 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-place-exhaustiveness

Every place used by the selected global invariant theorem belongs to exactly the finite or infinite branch represented in the frozen statement.

Formal target: `planned exact place-partition theorem and completion identification`.

Output: A disjoint exhaustive finite/infinite place partition.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: number-field place/completion API; selected source route audit open.

Budget: 32 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-b-local-places

Split local classification into the archimedean and nonarchimedean branches and recompose their exact outputs for the normalized all-place family.

Formal target: `planned exact local-classification branch package`.

Output: Classification and isotropy data at every frozen completion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: selected invariant route; primary-source node map open.

Budget: 26 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-local-places-merge

Use the exhaustive place partition to merge the finite and infinite local classification packages.

Formal target: `planned exact local-place recomposition`.

Output: A uniform local classification and isotropy interface over all places.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 24 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-infinite

Classify nondegenerate forms at every infinite completion and give the exact local isotropy and hyperbolic-splitting interface.

Formal target: `planned exact archimedean local-classification package`.

Output: The complete infinite-place classification branch.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: real/complex completion APIs and quadratic classification.

Budget: 52 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-infinite-merge

Split each infinite place into real or complex, consume both branch packages, and recompose the result for its actual completion.

Formal target: `planned exact real/complex completion recomposition`.

Output: Classification and isotropy data for every infinite completion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 24 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-infinite-dichotomy

For every infinite place, produce the exclusive real/complex case and the corresponding completion equivalence.

Formal target: `planned exact wrapper around InfinitePlace isReal/isComplex dichotomy and completion equivalences`.

Output: An exhaustive tagged real-or-complex completion equivalence.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Mathlib NumberField Completion InfinitePlace.

Budget: 28 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-b-infinite-real

At a real infinite place, transport to R, classify by signature, and derive the exact nonzero-isotropy criterion.

Formal target: `planned exact real-place classification package`.

Output: The real-completion classification and isotropy conclusion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: InfinitePlace real equivalence; QuadraticForm.Real.

Budget: 44 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-n-real-completion-transport

Transport a form, nondegeneracy, and nonzero isotropy between a real completion and R along the pinned field equivalence.

Formal target: `planned exact wrapper around InfinitePlace.ringEquivRealOfIsReal and quadratic-form scalar transport`.

Output: Bidirectional real-completion transport for classification and witnesses.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Mathlib NumberField Completion InfinitePlace.

Budget: 32 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-real-classification

Every finite-dimensional real quadratic form is isometric to a diagonal form with entries 1, 0, and -1, with nondegeneracy excluding the zero block.

Formal target: `planned exact wrapper around QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared`.

Output: A nondegenerate real signature normal form.

Projected status: `[H1, M3, R3]`; candidate classification: `M3_exact_mathlib_child_requires_wrapper_and_E1`.

Source boundary: anchor-audit candidate S56-M-0423-C03.

Budget: 46 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-real-isotropy

A nondegenerate real form is isotropic exactly when its signature has both a positive and a negative direction, subject to the low-dimensional boundary.

Formal target: `planned exact signature criterion for the real normal form`.

Output: The exact real nonzero-isotropy criterion and witness.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: real signature algebra; primary-source mapping open.

Budget: 36 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-b-infinite-complex

At a complex infinite place, transport to C, classify the nondegenerate form, and derive its exact nonzero-isotropy boundary.

Formal target: `planned exact complex-place classification package`.

Output: The complex-completion classification and isotropy conclusion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: InfinitePlace complex equivalence; algebraically closed quadratic forms.

Budget: 44 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-n-complex-completion-transport

Transport a form, nondegeneracy, and nonzero isotropy between a complex completion and C along the pinned field equivalence.

Formal target: `planned exact wrapper around InfinitePlace.ringEquivComplexOfIsComplex and quadratic-form scalar transport`.

Output: Bidirectional complex-completion transport for classification and witnesses.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Mathlib NumberField Completion InfinitePlace.

Budget: 32 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-complex-classification

A nondegenerate finite-dimensional quadratic form over C is isometric to a sum of nonzero squares.

Formal target: `planned exact algebraically-closed-field diagonal classification specialized to C`.

Output: A complex diagonal normal form with every coefficient scaled to one.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: algebraically closed square roots plus diagonalization; exact Lean anchor missing.

Budget: 44 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-complex-isotropy

A nondegenerate complex quadratic form has a nonzero isotropic vector exactly in dimension at least two.

Formal target: `planned exact dimension criterion for nondegenerate complex forms`.

Output: The exact complex nonzero-isotropy criterion and explicit witness.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: complex square root of -1 and one-dimensional boundary.

Budget: 28 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite

Classify nondegenerate quadratic forms over every finite completion by dimension, determinant square class, and Hasse invariant, including Witt decomposition and isotropy.

Formal target: `planned exact nonarchimedean local-classification package for the statement's adic completion fields`.

Output: The complete finite-place classification branch.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: missing from pinned mathlib; primary-source node map open.

Budget: 64 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-finite-merge

Consume the invariant definitions and every existence, uniqueness, Witt, and isotropy result needed for nonarchimedean classification.

Formal target: `planned exact finite-place classification recomposition`.

Output: A uniform invariant classification and isotropy interface at every finite place.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 28 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-hilbert-symbol

Define the local Hilbert symbol on nonzero square classes at every completion and establish its algebraic and completion-compatibility laws.

Formal target: `planned exact HilbertSymbol package over the normalized place family`.

Output: A coherent, well-defined local binary symbol family.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hilbert-symbol API absent from pinned mathlib.

Budget: 62 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-symbol-merge

Recombine the Hilbert-symbol definition with all laws used by local invariants and global reciprocity.

Formal target: `planned exact Hilbert-symbol law-package recomposition`.

Output: The full local Hilbert-symbol interface with no hidden law premise.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 24 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-symbol-definition

For nonzero a and b over a local field, define (a,b) through solvability of the norm/conic equation and return a two-element sign.

Formal target: `planned exact local Hilbert-symbol definition with nonzero-domain proof`.

Output: A raw local symbol together with its norm/conic criterion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: classical local-field definition; source pinpoint open.

Budget: 50 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-symbol-welldefined

The raw Hilbert symbol is unchanged when either argument is multiplied by a nonzero square, so it descends to square classes.

Formal target: `planned exact square-class well-definedness theorem`.

Output: A well-defined binary function on local square classes.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local norm invariance; source pinpoint open.

Budget: 46 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-symbol-bilinear

The Hilbert symbol is multiplicative in each square-class argument.

Formal target: `planned exact bilinearity theorem for the local Hilbert symbol`.

Output: Bilinearity on the two local square-class groups.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local norm-residue algebra; source pinpoint open.

Budget: 58 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-norm-residue-bilinearity

The quadratic norm-residue character over a local field is additive in each Kummer class, and its sign realization is the Hilbert symbol.

Formal target: `planned exact degree-two local norm-residue pairing bilinearity theorem`.

Output: Bilinearity of the local Kummer/norm-residue pairing before translation to Hilbert signs.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local Kummer theory and cup-product bilinearity; source and Lean implementation open.

Budget: 96 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-symbol-symmetry-normalization

The Hilbert symbol is symmetric and satisfies the unit, square, and (a,-a) normalization identities used in diagonal transformations.

Formal target: `planned exact symmetry and normalization law bundle`.

Output: Symmetry and every named normalization identity used downstream.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local Hilbert-symbol identities; source pinpoint open.

Budget: 42 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-symbol-completion-compatibility

The symbol transported along each completion equivalence agrees with the normalized finite or infinite place symbol.

Formal target: `planned exact compatibility under finite/infinite completion field equivalences`.

Output: One coherent symbol value independent of the chosen completion presentation.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: completion transport and norm compatibility; wrapper missing.

Budget: 38 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-hasse-invariant

Define the Hasse invariant from pairwise Hilbert symbols of diagonal coefficients and prove independence of the diagonal presentation without invoking local classification.

Formal target: `planned exact localHasseInvariant package`.

Output: A presentation-independent local invariant of a nondegenerate quadratic form.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hasse-invariant API absent from pinned mathlib.

Budget: 68 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-hasse-merge

Consume the diagonal definition, presentation-move invariance, and presentation connectivity to obtain a form-level invariant.

Formal target: `planned exact Hasse-invariant well-definedness recomposition`.

Output: The Hasse invariant of the form, independent of all basis and diagonalization choices.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 26 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-hasse-diagonal

For a diagonal form with nonzero coefficients a_i, form the product of (a_i,a_j) over all i<j.

Formal target: `planned exact finite pair-product definition on diagonal coefficient square classes`.

Output: A local Hasse value for one chosen diagonal presentation.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: finite pair product over the Hilbert-symbol package.

Budget: 30 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-hasse-presentation-moves

The diagonal Hasse value, together with dimension and determinant, transforms correctly under permutation, square rescaling, and elementary binary diagonal changes.

Formal target: `planned exact invariance bundle for generators of diagonal-form isometry`.

Output: Hasse-value invariance under every generating presentation move.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hilbert-symbol identities and elementary 2x2 isometries.

Budget: 72 substantive steps maximum; ledger: 3 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-diagonal-presentation-connectivity

Any two diagonal presentations of isometric nondegenerate forms are connected by a finite sequence of the audited generating moves.

Formal target: `planned exact diagonal-presentation connectivity theorem`.

Output: A finite move chain between any two diagonalizations of the same form.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: quadratic-form congruence generators; source pinpoint open.

Budget: 74 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-congruence-generators

Every congruence between nondegenerate diagonal quadratic matrices over a field of characteristic not two is generated, through nondegenerate checkpoints, by permutations, nonzero square rescalings, and elementary binary diagonal replacements.

Formal target: `planned exact generator theorem for diagonal quadratic-form presentations`.

Output: A finite audited generating-move factorization for any diagonal congruence.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: quadratic congruence generator theorem; primary source and Lean implementation open.

Budget: 100 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite-classification-existence

Every admissible dimension, determinant square class, and Hasse value over a finite completion is realized by a nondegenerate quadratic form.

Formal target: `planned exact nonarchimedean local invariant-existence theorem`.

Output: A local form realizing each admissible invariant tuple.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local quadratic-form classification; source pinpoint open.

Budget: 78 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite-classification-uniqueness

Two nondegenerate forms over a finite completion with equal dimension, determinant square class, and Hasse invariant are isometric.

Formal target: `planned exact nonarchimedean local invariant-uniqueness theorem`.

Output: Completeness of the local invariant tuple for isometry.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local quadratic-form classification; source pinpoint open.

Budget: 88 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite-representation

Over a nonarchimedean local field of odd or dyadic residue characteristic, characterize the nonzero values represented by each nondegenerate diagonal form in terms of its dimension, determinant, and Hilbert-symbol data.

Formal target: `planned exact local value-representation theorem for the finite completion fields`.

Output: The representation criterion used to align and cancel diagonal coefficients in local uniqueness.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local norm groups and binary/ternary representation theory; source pinpoint open.

Budget: 94 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite-witt-decomposition

Every isotropic nondegenerate local form splits an explicit hyperbolic plane and a nondegenerate orthogonal residual form.

Formal target: `planned exact local Witt-splitting theorem`.

Output: A hyperbolic plane plus nondegenerate residual decomposition preserving invariants.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Witt decomposition over fields of characteristic not two.

Budget: 58 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-finite-isotropy-criterion

Give the exact dimension-sensitive criterion for a finite-completion invariant tuple to contain a hyperbolic plane.

Formal target: `planned exact nonarchimedean local isotropy criterion`.

Output: An iff between local IsIsotropic and the classified invariant condition.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local classification corollary; source pinpoint open.

Budget: 82 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-global-classification

From the normalized local isotropy data, construct a global hyperbolic comparison form and identify it with the diagonal input using explicit global invariant existence and uniqueness engines.

Formal target: `planned exact global classification-and-comparison package yielding an isometry diag(Q) ~= H orthogonalSum R`.

Output: A global isometry from an explicitly isotropic comparison form to the diagonalized input.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: selected invariant route; node/page source audit open.

Budget: 76 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-global-classification-merge

Recompose local hyperbolic residuals, compatible global invariants, their realization, the isotropic comparison form, and global uniqueness.

Formal target: `planned exact global-classification recomposition`.

Output: The complete algebraic local-to-global comparison package.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 32 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-local-residuals

At every completion, split the locally isotropic form as a hyperbolic plane plus a nondegenerate residual form and record its coherent invariants.

Formal target: `planned exact all-place residual-family package`.

Output: A completion-indexed family of dimension n-2 residual forms and invariant data.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Witt splitting plus normalized place family.

Budget: 64 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-residual-merge

Consume the dimension lower bound, local hyperbolic split, and residual invariant computation at every place.

Formal target: `planned exact local-residual recomposition`.

Output: A coherent nondegenerate residual family suitable for global realization.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 26 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-dimension-at-least-two

A nondegenerate form with a nonzero isotropic vector has dimension at least two.

Formal target: `planned exact signature: Nondegenerate Q -> IsIsotropic Q -> 2 <= finrank K V`.

Output: The legal n-2 dimension boundary for every local residual.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: elementary polar-form argument.

Budget: 24 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-hyperbolic-split

A nonzero isotropic vector in a nondegenerate form over characteristic not two generates, with a suitable partner, an isometric hyperbolic plane summand.

Formal target: `planned exact field-generic hyperbolic-splitting theorem`.

Output: An isometry Q ~= H orthogonalSum Qres with Qres nondegenerate.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Witt splitting; exact Lean wrapper missing.

Budget: 58 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-residual-invariants

Compute dimension, determinant, and Hasse invariant of the residual after removing a hyperbolic plane, consistently at every completion.

Formal target: `planned exact hyperbolic-residual invariant formulas`.

Output: Coherent invariant data for every local residual form.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: orthogonal-sum determinant and Hasse formulas.

Budget: 54 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-global-invariants

Extract the global dimension and determinant together with the finite-support family of local Hasse data for the diagonalized form and its residual target.

Formal target: `planned exact global invariant-data record`.

Output: A normalized global/local invariant tuple with explicit finite support.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: diagonal coefficients, local Hasse invariant, all-place normalization.

Budget: 60 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-hilbert-reciprocity

For global nonzero a and b, all but finitely many local Hilbert symbols are one and the product over every finite and infinite place is one.

Formal target: `planned exact arbitrary-number-field Hilbert reciprocity package`.

Output: The finite-support global product constraint for local symbols.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: ordinary absolute-value product formula is insufficient; theorem missing.

Budget: 84 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-reciprocity-merge

Consume finite support, the local/global norm-residue bridge, and the reciprocity law to derive the Hilbert-symbol product formula.

Formal target: `planned exact Hilbert-reciprocity recomposition`.

Output: A well-defined finite product of local factors equal to one.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 28 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-reciprocity-finite-support

For fixed global nonzero a and b, prove that the local Hilbert symbol is trivial outside an explicit finite set containing dyadic, ramified, and coefficient-supported places.

Formal target: `planned exact finite-support certificate for v |-> (a,b)_v`.

Output: A finite set containing every nontrivial local factor.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: integrality/unramified local norm criterion; source pinpoint open.

Budget: 66 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-reciprocity-local-bridge

Identify each completion Hilbert symbol with the local norm-residue invariant occurring in global reciprocity.

Formal target: `planned exact compatibility theorem between HilbertSymbol and the global reciprocity map`.

Output: Equality of the local quadratic norm-residue factors.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: class-field/norm-residue bridge; no Lean anchor.

Budget: 82 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-reciprocity-product

The product of all quadratic local norm-residue factors of two global elements is one.

Formal target: `planned exact quadratic global reciprocity/product theorem`.

Output: The global identity for the finite product of local norm-residue signs.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: global reciprocity theorem; primary source and Lean implementation open.

Budget: 90 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-principal-idele-reciprocity

The global Artin reciprocity map is trivial on principal ideles, and its quadratic character decomposes as the product of the local norm-residue characters.

Formal target: `planned exact principal-idele global reciprocity theorem with local factorization`.

Output: Triviality and local-product factorization of the quadratic global reciprocity character.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: global class field theory reciprocity; primary source and Lean implementation open.

Budget: 100 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-invariant-compatibility

The residual local invariant family extracted from the input satisfies every determinant, signature, finite-support, and product constraint required for global realization.

Formal target: `planned exact admissibility theorem for the residual invariant family`.

Output: An admissible global-realization input family.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: global invariant formulas plus Hilbert reciprocity.

Budget: 58 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-global-realization

Construct a global nondegenerate residual form realizing the compatible dimension, determinant, signatures, and local Hasse data.

Formal target: `planned exact arbitrary-number-field global invariant-realization theorem`.

Output: A global residual form matching the prescribed local residual at every place.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hasse existence/classification route; source mapping open.

Budget: 94 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-realization-merge

Consume every construction and verification needed to realize the compatible local residual invariants globally.

Formal target: `planned exact global-realization recomposition`.

Output: A nondegenerate global residual and certified local isometries at all places.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 30 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-finite-support-reduction

Reduce the infinite local realization request to a finite set of nontrivial square-class, sign, determinant, and Hasse constraints.

Formal target: `planned exact finite realization-support set and outside-triviality certificate`.

Output: A finite family of local neighborhoods whose satisfaction forces all required local invariants.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: finite support from residual data and reciprocity.

Budget: 64 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-weak-approximation

For finitely many finite and infinite places, choose one global element in prescribed open neighborhoods simultaneously.

Formal target: `planned exact number-field weak-approximation theorem for the statement's completion family`.

Output: A global coefficient meeting every selected local neighborhood.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: number-field weak approximation; exact pinned anchor absent.

Budget: 78 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-approximate-coefficients

Choose all but the final diagonal coefficient so their local square classes and real signs meet the finite realization constraints.

Formal target: `planned exact iterative coefficient-approximation construction`.

Output: A partial global diagonal form satisfying every prescribed constraint except the final Hasse correction.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: finite-support reduction plus weak approximation.

Budget: 76 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-final-invariant-correction

Choose the final coefficient so the determinant is exact and every local Hasse value agrees, using the single reciprocity compatibility relation.

Formal target: `planned exact last-coefficient correction theorem`.

Output: A complete global diagonal form with the prescribed invariant family.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hilbert reciprocity and admissibility equation.

Budget: 82 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-local-match-verification

At every finite and infinite completion, the realized global residual has the same complete local invariants as the prescribed residual and hence is locally isometric to it.

Formal target: `planned exact all-place local-match theorem`.

Output: A completion-wise isometry between realized and prescribed residual forms.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: finite and infinite local classification packages.

Budget: 68 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-isotropic-comparison

Adjoin a fixed global hyperbolic plane to the realized residual and certify that the resulting global form is explicitly isotropic and locally isometric to the input.

Formal target: `planned exact comparison-form package H orthogonalSum R`.

Output: A globally isotropic comparison form locally isometric to the diagonalized input everywhere.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: realization plus hyperbolic-sum invariant formulas.

Budget: 70 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-comparison-merge

Consume the one realized residual, hyperbolic plane, explicit witness, and local matching result to build the comparison form.

Formal target: `planned exact isotropic-comparison recomposition`.

Output: A single comparison object with global witness and all local isometries.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 28 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-hyperbolic-plane

Define one fixed nondegenerate two-dimensional hyperbolic plane over K with an explicit basis and quadratic convention.

Formal target: `planned exact HyperbolicPlane K package compatible with the residual invariant formulas`.

Output: A nondegenerate global hyperbolic-plane quadratic form.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: standard hyperbolic plane; convention must be fixed.

Budget: 26 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-explicit-hyperbolic-witness

Exhibit a named nonzero vector in the fixed hyperbolic plane whose quadratic value is zero, and preserve it in an orthogonal sum.

Formal target: `planned exact witness theorem for HyperbolicPlane K and H orthogonalSum R`.

Output: A nonzero global isotropic witness for the comparison form.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: hyperbolic basis vector calculation.

Budget: 16 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-comparison-invariant-match

At every completion, H plus the realized residual has exactly the input form's dimension, determinant, Hasse invariant, and archimedean signature.

Formal target: `planned exact comparison invariant-match theorem`.

Output: Complete local invariant equality between comparison and input forms.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: hyperbolic-removal formulas and realized residual local matches.

Budget: 64 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-global-uniqueness

Two nondegenerate global forms that are isometric at every finite and infinite completion are globally isometric, proved through an explicit Witt-group injectivity and cancellation engine.

Formal target: `planned exact arbitrary-number-field global uniqueness theorem`.

Output: A global isometry from completion-wise isometries of equal-dimensional forms.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Hasse global classification/uniqueness; source pinpoint open.

Budget: 92 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-global-uniqueness-merge

Consume local Witt-class equality, injectivity of localization, and cancellation to obtain a global isometry.

Formal target: `planned exact global-uniqueness recomposition`.

Output: Global isometry of the two original nondegenerate forms.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 28 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-local-data-equality

A completion-wise isometry gives equality of localized Witt classes, dimension, determinant, Hasse data, and real signatures.

Formal target: `planned exact invariant preservation theorem for every local isometry`.

Output: Equality of the complete localized data used by global uniqueness.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: local isometry invariance and all-place normalization.

Budget: 38 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-witt-injectivity

The diagonal localization map from the Witt group of K to the product of the Witt groups of all finite and infinite completions is injective.

Formal target: `planned exact signature: Function.Injective (WittGroup.localizeAll K)`.

Output: Equality of global Witt classes from equality at every completion.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: global Witt exact sequence; no Lean implementation.

Budget: 96 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-witt-injectivity-merge

Consume the Witt generators and every arithmetic relation needed to prove that the localization kernel is zero.

Formal target: `planned exact Witt-localization injectivity recomposition`.

Output: The zero-kernel theorem for the all-place Witt localization map.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: future abstract-child composition harness.

Budget: 30 substantive steps maximum; ledger: 1 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-c-witt-generators

Every Witt class of a nondegenerate form over K is represented by a finite orthogonal sum of one-dimensional nonzero forms, modulo hyperbolic relations.

Formal target: `planned exact diagonal generator presentation of WittGroup K`.

Output: A finite generator-and-relation representation for every global Witt class.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: diagonalization and Witt quotient algebra.

Budget: 62 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-squareclass-local-global

A nonzero global element that is a square in every finite and infinite completion is already a square in K.

Formal target: `planned exact injectivity theorem K*/K*^2 -> product_v Kv*/Kv*^2`.

Output: Global equality of square classes from all local equalities.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: quadratic extension detected by a nontrivial place; source pinpoint open.

Budget: 76 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-quadratic-nonsplit-place

Every nontrivial quadratic extension of a number field has a finite or infinite place at which the completed extension is nontrivial.

Formal target: `planned exact nonsplit-place existence theorem for nontrivial quadratic extensions`.

Output: A completion detecting every nontrivial global quadratic extension.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Chebotarev/Frobenius or norm argument; primary source and Lean implementation open.

Budget: 100 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-reciprocity-kernel-exactness

The only finite-support local Hilbert-symbol relations invisible at every global square class are those generated by global square classes subject to the single reciprocity product relation.

Formal target: `planned exact quadratic norm-residue localization-sequence exactness theorem`.

Output: Exactness at the local symbol-family term used by Witt localization.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: quadratic reciprocity exact sequence; source and Lean implementation open.

Budget: 98 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-quadratic-duality-exactness

The global-to-local quadratic norm-residue sequence is exact: finite-support local square-class characters satisfying the reciprocity product constraint arise from global data.

Formal target: `planned exact quadratic Albert-Brauer-Hasse-Noether/Poitou-Tate degree-two exactness theorem`.

Output: The arithmetic duality engine identifying the kernel and cokernel in the quadratic localization sequence.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: global quadratic reciprocity duality; primary source and Lean implementation open.

Budget: 100 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-witt-reduction

If a diagonal Witt class localizes to zero everywhere, the generator presentation and reciprocity exactness reduce it by global hyperbolic relations to zero.

Formal target: `planned exact zero-kernel reduction for diagonal Witt classes`.

Output: Global triviality of every locally trivial Witt class.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Witt relations plus quadratic reciprocity exactness.

Budget: 94 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-l-witt-cancellation

Equal-dimensional nondegenerate forms with equal Witt classes are isometric.

Formal target: `planned exact Witt cancellation theorem over fields of characteristic not two`.

Output: An isometry after cancelling equal hyperbolic summands.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: Witt cancellation; exact pinned Lean anchor not audited.

Budget: 68 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-isotropic-extraction

Transport the explicit hyperbolic witness through the global comparison isometry and then through the inverse diagonalizing isometry to the original form.

Formal target: `planned exact witness extraction yielding Stage1.THM_M_0423.IsIsotropic Q`.

Output: Stage1.THM_M_0423.IsIsotropic Q.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: comparison package and diagonal transport.

Budget: 40 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-witness-isometry-transport

An isometry from an explicitly isotropic comparison form to the diagonal input transports the named witness without collapsing it to zero.

Formal target: `planned exact nonzero-isotropic witness transport along QuadraticForm.IsometryEquiv`.

Output: A nonzero isotropic vector for the diagonalized input.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: linear-equivalence injectivity and isometry law.

Budget: 24 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

### m0423-t-diagonal-transport-back

Transport a nonzero isotropic vector from the diagonal representative back to Q through the inverse basis isometry.

Formal target: `planned exact inverse of the global isotropy transport in M0423-N-DIAGONALIZE`.

Output: A nonzero isotropic vector for Q.

Projected status: `[H1, M4, R3]`; candidate classification: `M4_no_implemented_exact_body`.

Source boundary: diagonalization isometry inverse.

Budget: 22 substantive steps maximum; ledger: 2 step(s).

Boundary: Architecture, exact statement interface, or unaccepted candidate body only; no accepted E0/E1, M0, H0, R0, composition, audit completion, theorem completion, or master acceptance.

## Cut reporting

The singleton `M0423-T-LOCAL-GLOBAL` is only the immediate mathematical cut if the
top conditional harnesses and every planned internal composition are assumed valid. It is
not the unqualified executable or release cut.

The executable open-leaf cut contains 32 leaves, all listed in
`typed-graphs.json`. Every proof parent also lacks a machine-derived composition
certificate. Foundation, source, provenance, trust, readability, workflow, downstream
proof/validation/release receipts, and master acceptance are separate release cuts.

## Freeze boundary

Registry v2 supersedes the unaccepted v1 draft and preserves its denominator in the
append-only delta. V2 removes the speculative low/high-dimension shortcut, makes every
finite/infinite merge consume its branches, proves Hasse-invariant independence through
presentation moves rather than local classification, exposes reciprocity inputs, and
separates global realization, comparison, Witt injectivity, cancellation, uniqueness, and
witness extraction.

The root remains `[H1, M3, R3]`. There is no E0/E1 evidence, accepted M0 node, checked
composition certificate, H0/R0 review, audit completion, theorem completion, release
receipt, or master acceptance.
