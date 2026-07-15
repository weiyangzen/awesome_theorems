# THM-M-0812 frozen obligation tree

This version-1 registry describes the finite bipartite matching-cover proof architecture. It is not a proof receipt. All proof children remain open, no provider result is reused, and the authoritative root remains `H1/M3/R2`.

The proof route fixes a maximum matching, follows alternating paths from unmatched left vertices, selects every unreached left vertex and every reached right vertex, proves this is a cover with exactly one selected endpoint per matching edge, and combines that construction with the injection from any matching into any cover.

## Frozen boundary

- Registry: `THM-M-0812-OBLIGATIONS-v1`
- Denominator: `d9131bd62ea1ff0e1a362804bff3be41eae48e3cccf1b6e85db2a7f43f0915b3`
- Obligations: `40`
- Accepted closed obligations: none
- Minimal open proof cut: matching attainment, cover from a maximum matching, and weak duality
- External candidates: ATLAS is placeholder-blocked; closed PR 33032 is unintegrated and incompatible with the pin

## Nodes

<a id="m0812-root"></a>
### M0812-ROOT

For every finite two-sorted bipartite incidence graph, one natural number is both its attained maximum matching size and attained minimum vertex-cover size.

Formal target: `Stage1Instances.THM_M_0812.KonigMatchingCoverTarget`

Output: The exact canonical proposition at universes uL, uR, and uE.

Budget: `8` substantive steps. Status: `H1/M3/R2`.

Method ledger: Compose finite matching attainment, the maximum-matching cover construction, and weak duality without changing the frozen binders or extrema.

Source anchor: `Statement.lean#KonigMatchingCoverTarget`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-target"></a>
### M0812-S-TARGET

Freeze the exact finite incidence target and its expression and bundle fingerprints.

Formal target: `Stage1Instances.THM_M_0812.KonigMatchingCoverTarget`

Output: The canonical target interface, counted once at the root.

Budget: `8` substantive steps. Status: `H2/M3/R2`.

Method ledger: Preserve the exact ordered types, instances, endpoint maps, existential k, and both extremal predicates.

Source anchor: `Statement.lean; statement.json canonical_formal_target`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-representation"></a>
### M0812-S-REPRESENTATION

Use typed sides L and R, an independent edge-identity type E, and endpoint maps so isolated vertices and parallel edges remain representable.

Formal target: `Stage1Instances.THM_M_0812.IsEdgeMatching; Stage1Instances.THM_M_0812.IsBipartiteVertexCover`

Output: A source-faithful finite bipartite incidence representation.

Budget: `14` substantive steps. Status: `H2/M3/R2`.

Method ledger: Propagate the typed-side incidence model to every construction and avoid silently switching to a one-sorted simple graph.

Source anchor: `Statement.lean:17-31`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-extrema"></a>
### M0812-S-EXTREMA

Maximum and minimum mean attained witnesses plus universal natural-cardinality bounds, not maximality or minimality by inclusion.

Formal target: `Stage1Instances.THM_M_0812.HasMatchingNumber; Stage1Instances.THM_M_0812.HasVertexCoverNumber`

Output: The exact matching-number and vertex-cover-number interfaces.

Budget: `14` substantive steps. Status: `H2/M3/R2`.

Method ledger: Retain both witness and universal-bound conjuncts and count matching edges versus tagged side vertices.

Source anchor: `Statement.lean:33-53`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-boundary"></a>
### M0812-S-BOUNDARY

Retain edgeless graphs, isolated vertices, empty sides when E is empty, singleton graphs, and parallel-edge identities.

Formal target: `Stage1Instances.THM_M_0812.edgelessBoundary; Stage1Instances.THM_M_0812.singleEdgeBoundary`

Output: No hidden nonempty or simplicity premise.

Budget: `16` substantive steps. Status: `H2/M3/R2`.

Method ledger: Carry every admitted degenerate case through the proof architecture; do not discharge it by strengthening the target.

Source anchor: `Statement.lean#edgelessBoundary; Statement.lean#singleEdgeBoundary`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-transport"></a>
### M0812-S-TRANSPORT

Bind the named target to its direct expansion and to simple-relation erasure in both checked directions.

Formal target: `Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_expanded; Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_simpleRelationKonigTarget`

Output: Checked representation relationships without duplicate root credit.

Budget: `16` substantive steps. Status: `H2/M3/R2`.

Method ledger: Use the local Iffs only in their declared directions and deduplicate them from semantic proof coverage.

Source anchor: `Statement.lean#konigMatchingCoverTarget_iff_expanded; Statement.lean#konigMatchingCoverTarget_iff_simpleRelationKonigTarget`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-s-foundation"></a>
### M0812-S-FOUNDATION

Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, and a no-oracle computation policy.

Formal target: `stage1-foundation-profile/1.0`

Output: A reviewed foundation decision, not a theorem premise.

Budget: `40` substantive steps. Status: `H2/M3/R2`.

Method ledger: Compare machine-derived terminal dependencies with the accepted profile and reject unknown or placeholder trust paths.

Source anchor: `anchor-audit.json immutable_environment`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-n-finite-sets"></a>
### M0812-N-FINITE-SETS

Expose finite matching candidates and finite cardinalities without adding decidability or nonemptiness assumptions.

Formal target: `planned finite Set E and Set.ncard interfaces`

Output: A finite search space on which maximum cardinality is attained.

Budget: `24` substantive steps. Status: `H1/M3/R2`.

Method ledger: Obtain local finite interfaces from [Finite E] and keep the empty matching as the nonempty candidate witness.

Source anchor: `Statement.lean finite binders; Mathlib.Data.Finite.Card`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-n-simple-relation"></a>
### M0812-N-SIMPLE-RELATION

Erase parallel edge identities only after the checked statement transport proves that both extrema are preserved.

Formal target: `Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_simpleRelationKonigTarget`

Output: A simple endpoint-pair relation route equivalent to the canonical target.

Budget: `20` substantive steps. Status: `H2/M3/R2`.

Method ledger: Use endpoint representatives and cardinality-preserving image lemmas; retain the canonical incidence target as the root.

Source anchor: `Statement.lean:367-406`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-n-alternating-reach"></a>
### M0812-N-ALTERNATING-REACH

Normalize the translated path process to alternating reachability from unmatched left vertices relative to a chosen maximum matching.

Formal target: `planned alternating reachability predicate`

Output: Stable reachable-left and reachable-right vertex sets.

Budget: `34` substantive steps. Status: `H1/M3/R2`.

Method ledger: Define reachability with explicit parity and matching/nonmatching edge roles before selecting the cover.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-t-matching-attain"></a>
### M0812-T-MATCHING-ATTAIN

Every finite incidence graph has an attained maximum matching cardinality.

Formal target: `Stage1Instances.THM_M_0812_Obligations.MatchingAttainmentTarget`

Output: Exists k, HasMatchingNumber left right k for every finite E.

Budget: `24` substantive steps. Status: `H1/M3/R2`.

Method ledger: Select a matching of greatest ncard from the finite candidate set and prove the universal bound.

Source anchor: `ObligationTree.lean#MatchingAttainmentTarget`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-max-matching"></a>
### M0812-C-MAX-MATCHING

Choose a maximum matching witness M and retain both injectivity conditions and M.ncard = k.

Formal target: `planned extraction from HasMatchingNumber`

Output: A fixed matching driving the alternating construction.

Budget: `10` substantive steps. Status: `H1/M3/R2`.

Method ledger: Eliminate only the attained-witness conjunct and keep the universal bound available for the no-augmentation contradiction.

Source anchor: `Statement.lean#HasMatchingNumber`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-t-cover-from-max"></a>
### M0812-T-COVER-FROM-MAX

Every attained maximum matching of size k yields a vertex cover of cardinality k.

Formal target: `Stage1Instances.THM_M_0812_Obligations.MaximumMatchingCoverTarget`

Output: Exists CLeft CRight, cover and CLeft.ncard + CRight.ncard = k.

Budget: `18` substantive steps. Status: `H1/M3/R2`.

Method ledger: Build alternating reachability, select the unreached left and reached right endpoints, prove coverage, and count exactly one selected endpoint per matching edge.

Source anchor: `ObligationTree.lean#MaximumMatchingCoverTarget; translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-alt-path"></a>
### M0812-C-ALT-PATH

Construct alternating paths whose first edge is outside M and whose edge membership alternates thereafter.

Formal target: `planned finite path object with parity invariant`

Output: A path/reachability witness with explicit endpoints and alternation.

Budget: `42` substantive steps. Status: `H1/M3/R2`.

Method ledger: Define the finite path object, endpoint side, simplicity, and parity-indexed membership in M.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-alt-path-normalize"></a>
### M0812-L-ALT-PATH-NORMALIZE

Any alternating walk witness can be shortened to a simple alternating path without changing endpoints.

Formal target: `planned walk-to-path normalization`

Output: A simple path suitable for augmentation and counting.

Budget: `35` substantive steps. Status: `H1/M3/R2`.

Method ledger: Erase loops while proving the alternating invariant survives every splice.

Source anchor: `translated proof route; formal normalization obligation`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-reachable-sides"></a>
### M0812-C-REACHABLE-SIDES

Define ZLeft and ZRight as vertices reached from unmatched left vertices by alternating paths of the appropriate parity.

Formal target: `planned Set L and Set R definitions`

Output: The two reachability sets used by the cover formula.

Budget: `28` substantive steps. Status: `H1/M3/R2`.

Method ledger: Project normalized path endpoints to typed sides and retain an origin unmatched-left witness.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-augment"></a>
### M0812-C-AUGMENT

Toggle matching membership along an alternating path from an unmatched left vertex to an unmatched right vertex.

Formal target: `planned Set E symmetric-difference construction`

Output: A new matching with one additional edge.

Budget: `38` substantive steps. Status: `H1/M3/R2`.

Method ledger: Define the toggled edge set and separate endpoint, internal-vertex, and off-path injectivity cases.

Source anchor: `translated Konig 1931 no-augmenting-path argument`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-augment-matching"></a>
### M0812-L-AUGMENT-MATCHING

The toggled edge set is still injective under both endpoint maps.

Formal target: `planned IsEdgeMatching proof for augmentation`

Output: IsEdgeMatching left right augmentedM.

Budget: `48` substantive steps. Status: `H1/M3/R2`.

Method ledger: Use path simplicity and alternation to show each internal vertex loses and gains exactly one incident chosen edge.

Source anchor: `translated proof route; formal invariant obligation`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-augment-card"></a>
### M0812-L-AUGMENT-CARD

An odd alternating augmenting path adds exactly one chosen edge.

Formal target: `planned ncard augmentedM = M.ncard + 1`

Output: Strictly larger matching cardinality.

Budget: `36` substantive steps. Status: `H1/M3/R2`.

Method ledger: Pair removed path edges with all but one added path edge and preserve off-path membership.

Source anchor: `translated proof route; finite cardinality obligation`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-no-augmenting"></a>
### M0812-L-NO-AUGMENTING

A maximum matching admits no alternating path from an unmatched left vertex to an unmatched right vertex.

Formal target: `planned contradiction from HasMatchingNumber universal bound`

Output: Every reached right vertex is matched by M.

Budget: `22` substantive steps. Status: `H1/M3/R2`.

Method ledger: Assume such a path, invoke the matching and cardinality augmentation lemmas, and contradict maximal cardinality.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-reached-r-matched"></a>
### M0812-L-REACHED-R-MATCHED

Each reached right vertex is incident to a unique matching edge.

Formal target: `planned endpoint existence and uniqueness`

Output: A matching-edge predecessor for every member of ZRight.

Budget: `24` substantive steps. Status: `H1/M3/R2`.

Method ledger: Use no-augmentation for existence and right-endpoint injectivity for uniqueness.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-matched-reach-iff"></a>
### M0812-L-MATCHED-REACH-IFF

For each matching edge, its left endpoint is reached exactly when its right endpoint is reached.

Formal target: `planned iff on endpoints of e in M`

Output: Matched edges pair ZLeft and ZRight membership.

Budget: `28` substantive steps. Status: `H1/M3/R2`.

Method ledger: Extend or truncate an alternating path by the matching edge in the two directions.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-selected-cover"></a>
### M0812-C-SELECTED-COVER

Select CLeft = left endpoints not in ZLeft and CRight = ZRight.

Formal target: `planned Set L and Set R cover`

Output: The canonical cover extracted from the maximum matching.

Budget: `12` substantive steps. Status: `H1/M3/R2`.

Method ledger: Define the two sets extensionally and retain their disjoint typed-side cardinalities.

Source anchor: `translated Konig 1931 endpoint selection`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-b-edge-member-split"></a>
### M0812-B-EDGE-MEMBER-SPLIT

Split every graph edge according to membership in the fixed maximum matching.

Formal target: `planned by_cases e in M`

Output: Exhaustive matching-edge versus nonmatching-edge cases.

Budget: `8` substantive steps. Status: `H1/M3/R2`.

Method ledger: Run classical excluded middle on e membership and preserve the exact endpoint goal in both branches.

Source anchor: `translated Konig 1931 four-case coverage proof`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-b-four-endpoint-cases"></a>
### M0812-B-FOUR-ENDPOINT-CASES

For a nonmatching edge, split reachability of its left and right endpoints and rule out the uncovered configuration by extending an alternating path.

Formal target: `planned four endpoint-membership cases`

Output: Every nonmatching edge meets CLeft or CRight.

Budget: `26` substantive steps. Status: `H1/M3/R2`.

Method ledger: Enumerate the four membership pairs; the only potentially uncovered pair would make the right endpoint reachable.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-cover-every-edge"></a>
### M0812-L-COVER-EVERY-EDGE

The selected left and right sets cover every edge.

Formal target: `Stage1Instances.THM_M_0812.IsBipartiteVertexCover left right CLeft CRight`

Output: The cover predicate for the constructed sets.

Budget: `24` substantive steps. Status: `H1/M3/R2`.

Method ledger: Combine the matching-edge reachability iff with the exhaustive nonmatching endpoint cases.

Source anchor: `translated Konig 1931 four cases`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-cover-bijection"></a>
### M0812-C-COVER-BIJECTION

Associate each matched edge with exactly one selected endpoint: right when reached, left otherwise.

Formal target: `planned equivalence between M and Sum CLeft CRight`

Output: A cardinality-preserving selection map.

Budget: `38` substantive steps. Status: `H1/M3/R2`.

Method ledger: Use left/right endpoint injectivity for injectivity and reached-right matching plus matched reachability iff for surjectivity.

Source anchor: `translated Konig 1931 endpoint selection`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-cover-card"></a>
### M0812-L-COVER-CARD

The constructed cover has CLeft.ncard + CRight.ncard = M.ncard = k.

Formal target: `planned Set.ncard equality`

Output: Exact cover cardinality k.

Budget: `26` substantive steps. Status: `H1/M3/R2`.

Method ledger: Convert the cover bijection to cardinal equality and rewrite by the maximum-matching witness equation.

Source anchor: `translated Konig 1931 pp.1-2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-b-cover-merge"></a>
### M0812-B-COVER-MERGE

Recompose coverage and cardinality into the exact cover-from-maximum existential.

Formal target: `planned conjunction/existential assembly`

Output: Exists CLeft CRight, cover and exact cardinality.

Budget: `10` substantive steps. Status: `H1/M3/R2`.

Method ledger: Package the selected sets, coverage lemma, and cardinality lemma without introducing a minimum-cover premise.

Source anchor: `ObligationTree.lean#MaximumMatchingCoverTarget`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-t-weak-duality"></a>
### M0812-T-WEAK-DUALITY

Every vertex cover has size at least every matching.

Formal target: `Stage1Instances.THM_M_0812_Obligations.WeakDualityTarget`

Output: M.ncard <= CLeft.ncard + CRight.ncard.

Budget: `18` substantive steps. Status: `H1/M3/R2`.

Method ledger: Map each matching edge to a covering endpoint and prove injectivity using matching endpoint injectivity and tagged sides.

Source anchor: `ObligationTree.lean#WeakDualityTarget; translated Konig 1931 reverse inequality`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-c-duality-injection"></a>
### M0812-C-DUALITY-INJECTION

Choose for each matching edge a tagged covering endpoint in CLeft or CRight.

Formal target: `planned injection M -> Sum CLeft CRight`

Output: A finite injection from matching edges to cover vertices.

Budget: `34` substantive steps. Status: `H1/M3/R2`.

Method ledger: Use the cover disjunction to choose a tagged endpoint and prove equal images force equal edges on the corresponding side.

Source anchor: `translated Konig 1931 p.2 reverse bound`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-l-weak-duality-injection"></a>
### M0812-L-WEAK-DUALITY-INJECTION

The tagged endpoint choice is injective and yields the natural-cardinality inequality.

Formal target: `planned Fintype.card_le_of_injective / Set.ncard bound`

Output: The exact weak-duality inequality.

Budget: `22` substantive steps. Status: `H1/M3/R2`.

Method ledger: Apply finite cardinal monotonicity and normalize the cardinal of a disjoint sum to the sum of set ncard values.

Source anchor: `translated Konig 1931 p.2`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-t-assemble"></a>
### M0812-T-ASSEMBLE

Bundle attainment, equal-size cover construction, and weak duality into the exact extremal predicates.

Formal target: `Stage1Instances.THM_M_0812_Obligations.AssemblyTarget`

Output: All three child packages required by the exact root.

Budget: `12` substantive steps. Status: `H1/M3/R2`.

Method ledger: Use the attained matching witness, construct an equal-size cover, and derive its universal minimum bound from weak duality.

Source anchor: `ObligationTree.lean#AssemblyTarget`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-imports"></a>
### M0812-X-IMPORTS

Audit direct and transitive Lean imports, declaration bodies, licenses, and exact compatibility before any external theorem is credited.

Formal target: `stage1-import-boundary-record/1.0`

Output: A content-bound import decision with no hidden proof premise.

Budget: `55` substantive steps. Status: `H2/M3/R2`.

Method ledger: Reject ATLAS sorryAx and the unintegrated PR; retain mathlib APIs only as substrate until exact use is implemented.

Source anchor: `anchor-audit.json; dependency-reuse-ledger.json`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-computation"></a>
### M0812-X-COMPUTATION

Record that this symbolic architecture uses no solver, oracle, experiment, native decision, or unchecked certificate.

Formal target: `stage1-computation-record/1.0`

Output: An explicit no-computation boundary pending independent approval.

Budget: `12` substantive steps. Status: `H2/M3/R2`.

Method ledger: Reopen this obligation if future finite search or reflected computation becomes proof-relevant.

Source anchor: `instance.json computation_profile`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-source"></a>
### M0812-X-SOURCE

Map every material mathematical obligation to an admitted primary edition, exact locator, assumptions, translations, corrections, and independent review.

Formal target: `stage1-source-crosswalk-record/1.0`

Output: An independently reviewed H0 source crosswalk.

Budget: `90` substantive steps. Status: `H1/M3/R2`.

Method ledger: Inspect the Hungarian original, translation fidelity, and errata, then approve the node-specific mapping; the current translation remains H1 evidence only.

Source anchor: `source-statement-crosswalk.md; translated Konig 1931 pp.1-3`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-provenance"></a>
### M0812-X-PROVENANCE

Bind wrapper, conclusion, future terminal bodies, origins, hashes, licenses, aliases, and revocations without duplicate credit.

Formal target: `stage1-provenance-closure-record/1.0`

Output: Release-grade proof-body provenance.

Budget: `70` substantive steps. Status: `H2/M3/R2`.

Method ledger: Traverse actual terminal declarations and keep statement transports and conditional composition separate from proof bodies.

Source anchor: `anchor-audit.json; dependency-reuse-ledger.json`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-trust"></a>
### M0812-X-TRUST

Close transitive declarations, axioms, compiled artifacts, unsafe/oracle boundaries, TCB, and independent replay.

Formal target: `stage1-trust-closure-record/1.0`

Output: Accepted trust closure under the selected foundation policy.

Budget: `70` substantive steps. Status: `H2/M3/R2`.

Method ledger: Derive trust from terminal objects, not names; reject placeholders, unknown bodies, and moving dependencies.

Source anchor: `anchor-audit.json immutable_environment`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-readable"></a>
### M0812-X-READABLE

Produce and independently review a complete node-specific proof reconstruction linked to exact fingerprints.

Formal target: `stage1-readable-crosswalk-record/1.0`

Output: Readable R0 coverage without machine proof credit.

Budget: `90` substantive steps. Status: `H2/M3/R2`.

Method ledger: Expand the accepted alternating-path proof route while distinguishing architecture plans from checked proof bodies.

Source anchor: `obligation-tree.md`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.

<a id="m0812-x-workflow"></a>
### M0812-X-WORKFLOW

Bind dependency inspection, proof, composition, validation, source, readability, freshness, revocation, independent verification, and release tasks.

Formal target: `stage1-workflow-state-record/1.0`

Output: Only dependency-legal provisional or accepted execution states.

Budget: `30` substantive steps. Status: `H2/M3/R2`.

Method ledger: Reject acceptance before predecessor and node-specific receipt gates pass, and refresh the dependency context on invalidation.

Source anchor: `Docs/Stage1_Execution_DAG_rev-5.6.json; dependency-reuse-ledger.json`

Boundary: Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.
