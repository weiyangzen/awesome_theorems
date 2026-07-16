# THM-M-0115 Obligation Tree

This is the frozen architecture for `S56-M-0115-OBLIGATION_TREE`. It does not
prove Grothendieck-Riemann-Roch. The root remains `H4 / M3 / R4`, all canonical
obligations remain open, and every checked Lean theorem below is conditional on
explicit uninhabited mathematical packages.

## Frozen Denominator

Registry `THM-M-0115-OBLIGATIONS-v1` contains 32 canonical obligations. Its
ten-field status-independent projection has SHA-256
`f1455869731874b94cb533d3a6ee70bb15d428438472ffc205b63888eae68527`.
The projection fixes all machine, human-source, readable, risk, and exclusion
axes before the existing M3 statement and negative anchor status are attached.

The v2 theorem DAG declares an empty direct/transitive parent closure, no hard
edges, no reuse hints, and no shared groups. The target-owned dependency ledger
records that exact empty audit. No provider proof body or acceptance state is
used.

## Architecture

```text
M0115-ROOT exact frozen GRR target
`-- M0115-T-ASSEMBLE checked exact-root assembly
    `-- M0115-T-FORMULA formula for every D, hypothesis package, and alpha
        |-- M0115-T-RELATIVE relative Chern/pushforward comparison
        |   |-- M0115-B-FACTOR exhaustive source-proof factorization
        |   |   |-- M0115-N-PERFECT K_0 representative normalization
        |   |   |-- M0115-N-FACTORIZATION morphism normalization
        |   |   |-- M0115-L-IMMERSION closed-immersion GRR
        |   |   `-- M0115-L-PROJECTION_CASE projection GRR
        |   |-- M0115-L-CHERN Chern-character engine
        |   |-- M0115-L-PROJECTION Chow projection formula
        |   `-- M0115-L-COMPOSE composition stability
        `-- M0115-T-TODD_ACTION target Todd-factor transport
            |-- M0115-L-TODD tangent/Todd engine
            `-- M0115-L-PROJECTION Chow projection formula
```

The statement/foundation obligations `M0115-S-*` own the exact target, domain,
K-theory, Chow, operations, boundaries, transports, and trust policy. The
construction obligations `M0115-C-*` own deformation/factorization objects and
their invariants. The external and release overlays `M0115-X-*` separately own
formal imports, future external candidates, human sources, body provenance,
evidence, trust, readable reconstruction, and workflow state. Overlay edges
never become machine proof premises.

## Checked Composition

`ObligationTree.lean` elaborates three conditional certificates under
`--trust=0`:

1. `root_of_assembled_root_package` consumes the exact assembled-root package
   through an identity wrapper and yields `GrothendieckRiemannRochTarget`.
2. `assembled_root_package_of_formula_package` consumes the terminal formula
   package and yields the exact assembled-root package.
3. `formula_package_of_relative_and_todd` consumes both the relative comparison
   and target Todd-action packages and yields the terminal formula package.

Each declaration reports only `propext`, `Classical.choice`, and `Quot.sound`,
matching the statement substrate. None constructs either mathematical premise.
Every deeper source-proof decomposition is explicitly marked unverified until a
later proof phase supplies an exact child-to-parent Lean certificate.

## Mandatory Layers

### M0115-ROOT

**Claim:** The exact universally quantified GRR proposition frozen in
`Statement.lean`.

**Role:** Canonical root and sole machine-theorem completion target.

**Inputs:** `M0115-T-ASSEMBLE` plus the separate source, provenance, evidence,
trust, readability, and workflow release overlays.

**Proof route:** 1. Obtain the exact terminal formula package. 2. apply the
checked root composer. 3. validate statement identity and axiom closure. 4.
close every independent release gate.

**Branch logic:** No special case or overlay substitutes for the universal
root.

**Formal map:** `GrothendieckRiemannRochTarget`.

**Trust boundary:** The root is a proposition with no proof body.

**Step ledger:** `M0115-ROOT-STEP-01..03` in `typed-graphs.json`.

**Boundary:** Architecture and a conditional composer do not establish root
closure.

**Status vector:** `[H4, M3, R4]`.

### M0115-S-TARGET

**Claim:** Preserve the exact elaborated public and expanded targets.

**Role:** Fix the proposition that every later package must yield.

**Inputs:** `Statement.lean`, expression fingerprint, statement record.

**Proof route:** 1. Read the expanded binders. 2. Preserve the checked public
alias. 3. Reject any narrower specialization or semantic stand-in.

**Branch logic:** No mathematical branch occurs at statement identity.

**Formal map:** `GrothendieckRiemannRochExpandedTarget` and
`grothendieckRiemannRochTarget_iff_expanded`.

**Trust boundary:** Statement elaboration only; no root body.

**Step ledger:** `M0115-S-TARGET-STEP-01..03` in `typed-graphs.json`.

**Boundary:** Exact statement identity supplies no GRR proof.

**Status vector:** `[H4, M3, R4]`.

### M0115-S-DOMAIN

**Claim:** X and Y are smooth quasi-projective varieties over one field and f
is a proper morphism over that base.

**Role:** Supplies every geometric binder and admissibility premise.

**Inputs:** Base compatibility, variety predicates, smoothness,
quasi-projectivity, properness.

**Proof route:** 1. Bind both structure maps. 2. prove their smoothness and
quasi-projectivity interpretation. 3. prove `sourceStructureMap = map >>
targetStructureMap`. 4. prove `IsProper map`.

**Branch logic:** Empty objects stay in scope; singular and nonproper inputs are
excluded by explicit hypotheses, not by a hidden theorem change.

**Formal map:** `GrothendieckRiemannRochData.Hypotheses`.

**Trust boundary:** Current conclusion-free predicates require future native or
reviewed semantic integrations.

**Step ledger:** `M0115-S-DOMAIN-STEP-01..03`.

**Boundary:** Domain fidelity does not construct K_0, Chow, or the equality.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-KZERO

**Claim:** The selected family and proper pushforward are genuine scheme K_0
data with the exact relations needed by GRR.

**Role:** Supplies the source class alpha and its K-theory pushforward.

**Inputs:** Perfect complexes or vector bundles, exact-sequence relations,
proper pushforward construction.

**Proof route:** 1. Select the source-faithful model. 2. construct K_0. 3. show
representative independence. 4. construct proper pushforward. 5. prove its
functorial and additive laws.

**Branch logic:** Model choices must be connected by checked transports.

**Formal map:** `D.KZero`, `D.kTheoryPushforward`, and their compatibility
hypotheses.

**Trust boundary:** Pinned mathlib currently provides only generic adjacent
substrate, not this package.

**Step ledger:** `M0115-S-KZERO-STEP-01..03`.

**Boundary:** An arbitrary additive group cannot be credited as scheme K_0.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-CHOW

**Claim:** The selected rational Chow homology, cap action, and proper
pushforward have the exact grading and coefficient conventions of the source.

**Role:** Provides the equality codomain and its operations.

**Inputs:** Cycles, rational equivalence, rational coefficients, cap product,
proper pushforward.

**Proof route:** 1. Construct graded Chow homology. 2. quotient by rational
equivalence. 3. extend scalars to Q. 4. define cap action. 5. define and verify
proper pushforward.

**Branch logic:** Ring multiplication and homological cap notation require an
explicit checked relation; they are not silently identified.

**Formal map:** `D.ChowHomologyQ`, `D.capX`, `D.capY`, and
`D.chowPushforward`.

**Trust boundary:** No pinned terminal Chow package was found.

**Step ledger:** `M0115-S-CHOW-STEP-01..03`.

**Boundary:** A generic additive group does not discharge this obligation.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-OPERATIONS

**Claim:** Chern character, tangent bundle, Todd class, both pushforwards, and
cap actions implement their standard meanings and compatibility laws.

**Role:** Connects K-theory inputs to the Chow-valued formula.

**Inputs:** The K_0 and Chow models plus characteristic-class constructions.

**Proof route:** 1. Define Chern characters. 2. construct tangent classes. 3.
define Todd classes. 4. prove naturality/additivity. 5. prove compatibility with
pushforward and cap action used by the terminal comparison.

**Branch logic:** Source and target operations are typed separately.

**Formal map:** Fields and eight compatibility predicates in
`GrothendieckRiemannRochData`.

**Trust boundary:** Compatibility propositions are open premises, never stored
GRR equalities.

**Step ledger:** `M0115-S-OPERATIONS-STEP-01..03`.

**Boundary:** Merely naming operations supplies no semantic or proof credit.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-BOUNDARY

**Claim:** Empty varieties and alpha = 0 remain covered, and every exclusion is
already visible in the frozen hypotheses.

**Role:** Prevents a special-case proof from masquerading as the universal root.

**Inputs:** Exact ordered binders and mutation results.

**Proof route:** 1. Keep alpha universally quantified. 2. retain empty objects.
3. reject zero-only, projective-only, immersion-only, or singular/generalized
substitutes.

**Branch logic:** The later proof must handle all admissible values uniformly.

**Formal map:** `MutationOnlyZeroClass` and the other statement mutations.

**Trust boundary:** Mutation rejection checks identity, not truth.

**Step ledger:** `M0115-S-BOUNDARY-STEP-01..03`.

**Boundary:** No degenerate case closes a general branch.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-TRANSPORT

**Claim:** Every public alias or source-shaped reformulation transports in the
explicit direction required by the root.

**Role:** Prevents relative, cap, multiplication, or alternate-model formulas
from being counted as exact without a witness.

**Inputs:** Both statement fingerprints and a checked wrapper.

**Proof route:** 1. Compare normalized binders. 2. bind both fingerprints. 3.
elaborate the wrapper. 4. axiom-audit it. 5. validate it in this consumer.

**Branch logic:** `equal`, `iff`, and one-way implication are never conflated.

**Formal map:** Public alias transport is checked; future source transports are
open.

**Trust boundary:** Transport is consumer-owned proof work.

**Step ledger:** `M0115-S-TRANSPORT-STEP-01..03`.

**Boundary:** A similar formula or theorem name transfers no acceptance.

**Status vector:** `[H4, M4, R4]`.

### M0115-S-FOUNDATION

**Claim:** Every axiom, quotient, extensionality, computation, import, and TCB
element is allowed and content-bound.

**Role:** Supplies the foundation and release trust gate.

**Inputs:** Machine-derived axiom sets and the transitive import/tool closure.

**Proof route:** 1. Extract dependencies. 2. classify axioms and unsafe/oracle
boundaries. 3. compare the profile. 4. bind executables and compiled artifacts.

**Branch logic:** Proof-producing automation and trusted oracles are distinct.

**Formal map:** Current conditional composers report only the standard three
axioms; full closure remains open.

**Trust boundary:** This is a release gate, not a root premise.

**Step ledger:** `M0115-S-FOUNDATION-STEP-01..03`.

**Boundary:** A clean local source scan is not complete TCB closure.

**Status vector:** `[H4, M4, R4]`.

### M0115-N-PERFECT

**Claim:** Every alpha is represented in the exact perfect-complex or
vector-bundle model used by the selected proof, independently of choices.

**Role:** Normalizes general K_0 input before the geometric argument.

**Inputs:** `M0115-S-KZERO`, `M0115-S-OPERATIONS`.

**Proof route:** 1. Choose a representative. 2. respect exact relations. 3.
prove independence. 4. show Chern character and pushforward descend.

**Branch logic:** Alternate K_0 models require checked equivalence.

**Formal map:** Planned exact signature.

**Trust boundary:** No terminal normalization body exists.

**Step ledger:** `M0115-N-PERFECT-STEP-01..03`.

**Boundary:** Selecting one representative cannot change the quantified class.

**Status vector:** `[H4, M4, R4]`.

### M0115-N-FACTORIZATION

**Claim:** Every proper map in scope reduces to the morphism cases used by the
source proof.

**Role:** Connects the general input to closed-immersion and projection engines.

**Inputs:** Domain fidelity plus deformation/factorization constructions.

**Proof route:** 1. Embed or graph-factor the map. 2. construct the projection.
3. preserve properness and smooth/quasi-projective conditions. 4. prove the
composite is the original map.

**Branch logic:** Factorization cases must be exhaustive and recomposable.

**Formal map:** Planned exact signature.

**Trust boundary:** Source choice and exact hypotheses still require review.

**Step ledger:** `M0115-N-FACTORIZATION-STEP-01..03`.

**Boundary:** A projective-only factorization may not narrow the frozen target.

**Status vector:** `[H4, M4, R4]`.

### M0115-B-FACTOR

**Claim:** The factorization branches jointly prove the relative comparison.

**Role:** Owns all case splits and their recomposition.

**Inputs:** Both normalizations, immersion GRR, projection GRR.

**Proof route:** 1. Produce the factors. 2. discharge the immersion branch. 3.
discharge the projection branch. 4. use composition stability. 5. transport back
to f.

**Branch logic:** Every branch and exhaustiveness theorem is explicit.

**Formal map:** Planned child-to-parent certificate.

**Trust boundary:** Current graph records only an unverified source
decomposition.

**Step ledger:** `M0115-B-FACTOR-STEP-01..03`.

**Boundary:** No branch receives closure before an exact composer exists.

**Status vector:** `[H4, M4, R4]`.

### M0115-C-DEFORMATION

**Claim:** The deformation or graph-factorization spaces and maps used by the
proof exist in the required category.

**Role:** Supplies the geometric construction behind the reduction.

**Inputs:** Frozen schemes, morphism, and source construction.

**Proof route:** 1. Construct the graph. 2. form the deformation/blowup data. 3.
identify open and closed pieces. 4. define comparison maps.

**Branch logic:** Each constructed component owns a well-definedness condition.

**Formal map:** Planned exact signature.

**Trust boundary:** Pinned mathlib has adjacent scheme infrastructure only.

**Step ledger:** `M0115-C-DEFORMATION-STEP-01..03`.

**Boundary:** Object construction alone proves no characteristic-class identity.

**Status vector:** `[H4, M4, R4]`.

### M0115-C-NORMAL

**Claim:** The deformation data has every regularity, compatibility, and
choice-independence invariant consumed downstream.

**Role:** Makes the construction legal for the immersion/projection engines.

**Inputs:** `M0115-C-DEFORMATION`, domain hypotheses.

**Proof route:** 1. Prove well-definedness. 2. establish regularity/flatness. 3.
identify normal data. 4. prove naturality. 5. prove independence of choices.

**Branch logic:** Failed invariants block their dependent branch.

**Formal map:** Planned exact signature.

**Trust boundary:** No imported theorem is credited by name alone.

**Step ledger:** `M0115-C-NORMAL-STEP-01..03`.

**Boundary:** Hidden construction invariants may not be called routine.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-CHERN

**Claim:** The exact Chern character is additive, descends to K_0, and is
compatible with every operation used by the proof.

**Role:** Core characteristic-class engine.

**Inputs:** K_0, Chow, and operation semantics.

**Proof route:** 1. Define on representatives. 2. prove additivity. 3. descend
through relations. 4. prove naturality and normalization identities.

**Branch logic:** Different K_0 models require explicit transport.

**Formal map:** Planned exact signature.

**Trust boundary:** No external Chern theorem was located or imported.

**Step ledger:** `M0115-L-CHERN-STEP-01..03`.

**Boundary:** A named `chernCharacter` function is not this theorem.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-TODD

**Claim:** Tangent and normal bundle relations yield the required Todd-class
identities.

**Role:** Supplies the characteristic correction in both branches and root.

**Inputs:** Domain smoothness, Chow model, operations.

**Proof route:** 1. Construct tangent classes. 2. prove exact-sequence formulas.
3. establish multiplicativity. 4. identify source, target, and normal factors.

**Branch logic:** Absolute and relative Todd conventions require checked maps.

**Formal map:** Planned exact signature.

**Trust boundary:** The anchor audit found no pinned Todd-class API.

**Step ledger:** `M0115-L-TODD-STEP-01..03`.

**Boundary:** An abstract `toddClass` operation supplies no identity.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-PROJECTION

**Claim:** Proper Chow pushforward commutes with cap action in the exact form
needed to move Todd factors.

**Role:** Connects relative comparison to the absolute formula.

**Inputs:** Chow homology, cap action, proper pushforward.

**Proof route:** 1. State the exact projection formula. 2. verify grading. 3.
prove it on cycles. 4. descend to rational equivalence and Q-coefficients.

**Branch logic:** Source and target factors remain typed separately.

**Formal map:** Planned exact signature.

**Trust boundary:** No current proof body exists.

**Step ledger:** `M0115-L-PROJECTION-STEP-01..03`.

**Boundary:** Generic functoriality cannot replace the cap-product theorem.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-IMMERSION

**Claim:** GRR holds for the exact regular closed-immersion branch, with its
normal-bundle Todd correction.

**Role:** First terminal geometric engine.

**Inputs:** Deformation data, invariants, Chern and Todd engines.

**Proof route:** 1. Identify the normal bundle. 2. compute K-theory
pushforward. 3. compare Chern characters. 4. insert the Todd correction. 5.
transport to the branch formula.

**Branch logic:** Regularity is explicit and not inferred from a name.

**Formal map:** Planned exact signature.

**Trust boundary:** A major theorem package, never a primitive citation.

**Step ledger:** `M0115-L-IMMERSION-STEP-01..03`.

**Boundary:** It proves only its declared branch until recomposed.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-PROJECTION_CASE

**Claim:** GRR holds for the exact smooth/projective-bundle projection branch.

**Role:** Second terminal geometric engine.

**Inputs:** Construction, Chern/Todd engines, projection formula.

**Proof route:** 1. Normalize the projection. 2. compute pushforward on
generators. 3. compare characteristic classes. 4. extend additively. 5. deliver
the branch formula.

**Branch logic:** Generators and extension must cover the complete K_0 input.

**Formal map:** Planned exact signature.

**Trust boundary:** A major theorem package requiring its own source and body.

**Step ledger:** `M0115-L-PROJECTION_CASE-STEP-01..03`.

**Boundary:** A projective-bundle computation is not the general theorem.

**Status vector:** `[H4, M4, R4]`.

### M0115-L-COMPOSE

**Claim:** Relative GRR comparisons compose along the selected factorization.

**Role:** Recombines geometric branches into a comparison for f.

**Inputs:** Operation functoriality and Chow projection formula.

**Proof route:** 1. Expand both comparisons. 2. use K-theory pushforward
composition. 3. use Chow pushforward composition. 4. apply the projection
formula. 5. normalize Todd factors.

**Branch logic:** Both factors are consumed; unused branches are modeling
errors.

**Formal map:** Planned exact signature.

**Trust boundary:** Current decomposition has no exact Lean certificate.

**Step ledger:** `M0115-L-COMPOSE-STEP-01..03`.

**Boundary:** Categorical composition alone does not prove GRR compatibility.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-MATHLIB

**Claim:** Every used pinned mathlib declaration and source byte is classified.

**Role:** Formal import boundary.

**Inputs:** Exact module and declaration closure.

**Proof route:** 1. Resolve imports. 2. hash sources. 3. extract declarations.
4. classify terminal bodies and axioms.

**Branch logic:** Adjacent substrate receives no GRR credit.

**Formal map:** `AnchorAudit.lean` support probes.

**Trust boundary:** Current wrappers are support only.

**Step ledger:** `M0115-X-MATHLIB-STEP-01..03`.

**Boundary:** Pinned imports do not imply a terminal theorem.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-EXTERNAL

**Claim:** Any future external GRR result is exact or has a consumer-checked
transport and a placeholder-free trusted body.

**Role:** External formal-proof boundary.

**Inputs:** Provider bytes, fingerprints, body identity, receipts, license.

**Proof route:** 1. Normalize statements. 2. inspect body. 3. bind provider
bytes. 4. implement consumer wrapper. 5. re-elaborate and validate locally.

**Branch logic:** Exact and checked-transport relationships are distinct.

**Formal map:** None accepted; Atlas candidate is rejected.

**Trust boundary:** Provider acceptance never transfers.

**Step ledger:** `M0115-X-EXTERNAL-STEP-01..03`.

**Boundary:** A placeholder or name match supplies zero proof credit.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-SOURCE

**Claim:** Every material transition has a pinpoint primary-source mapping and
independent fidelity review.

**Role:** Human-source H-axis overlay.

**Inputs:** SGA 6/Fulton edition, locators, assumptions, errata.

**Proof route:** 1. Fix edition. 2. locate each lemma. 3. map assumptions. 4.
record corrections. 5. obtain independent review.

**Branch logic:** Broad citations cannot close individual obligations.

**Formal map:** Source crosswalk remains intake-level.

**Trust boundary:** Human review is separate from kernel evidence.

**Step ledger:** `M0115-X-SOURCE-STEP-01..03`.

**Boundary:** This architecture does not claim H0.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-PROVENANCE

**Claim:** Every eventual wrapper resolves to its terminal proof body and full
dependency origin.

**Role:** Prevents aliases and wrappers from duplicating proof credit.

**Inputs:** Declaration graph, source bytes, revisions, receipts.

**Proof route:** 1. Resolve wrapper. 2. find terminal declaration. 3. hash body.
4. traverse dependencies. 5. classify trust closure.

**Branch logic:** Shared terminal bodies count once.

**Formal map:** No accepted root body exists.

**Trust boundary:** Evidence/provenance edge only.

**Step ledger:** `M0115-X-PROVENANCE-STEP-01..03`.

**Boundary:** The graph intentionally has no root provenance edge yet.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-EVIDENCE

**Claim:** Every validation result binds exact inputs, command, output, and
invalidation state.

**Role:** Evidence authority overlay.

**Inputs:** Structured recipes, hashes, logs, environment, attestations.

**Proof route:** 1. Freeze recipe. 2. execute without shell/network. 3. capture
complete output. 4. bind covered IDs. 5. record freshness.

**Branch logic:** Exit zero and semantic acceptance are separate.

**Formal map:** Obligation-tree receipt and later phase receipts.

**Trust boundary:** Worker evidence remains provisional.

**Step ledger:** `M0115-X-EVIDENCE-STEP-01..03`.

**Boundary:** This phase supplies no proof-validation receipt.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-TRUST

**Claim:** Foundation, TCB, hermetic replay, and independent verification all
close for the eventual root body.

**Role:** Release trust overlay.

**Inputs:** Full provenance closure and deterministic evidence bundle.

**Proof route:** 1. enumerate TCB. 2. compare axioms. 3. cold build. 4. offline
replay. 5. independent runner/verifier.

**Branch logic:** Warm worker elaboration is nonrelease evidence.

**Formal map:** Later validation and release specifications.

**Trust boundary:** Current canonical `.lake` symlink is implementation-time
only.

**Step ledger:** `M0115-X-TRUST-STEP-01..03`.

**Boundary:** No E0/E1 or release-grade trust is claimed.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-READABLE

**Claim:** Every required node has a unique, coherent reconstruction accepted by
an independent reader.

**Role:** Readability R-axis overlay.

**Inputs:** This outline, expanded future proof process, formal maps, sources.

**Proof route:** 1. Preserve claim/role/inputs. 2. expand mathematical steps. 3.
bind formal declarations. 4. state trust and boundary. 5. independent review.

**Branch logic:** Reader-facing decomposition cannot become proof premises.

**Formal map:** This file is an architecture draft only.

**Trust boundary:** Machine checks structure, not mathematical prose adequacy.

**Step ledger:** `M0115-X-READABLE-STEP-01..03`.

**Boundary:** No R0 review exists.

**Status vector:** `[H4, M4, R4]`.

### M0115-X-WORKFLOW

**Claim:** Proof, validation, and release run in exact dependency order with
freshness and revocation handling.

**Role:** Workflow-state overlay.

**Inputs:** V2 checklist, phase receipts, master gates.

**Proof route:** 1. Accept predecessors. 2. execute proof nodes. 3. validate. 4.
review independently. 5. publish atomically or roll back.

**Branch logic:** Worker `[_]` and master `[x]` never collapse.

**Formal map:** Task IDs in `typed-graphs.json`.

**Trust boundary:** Scheduler alone writes task state.

**Step ledger:** `M0115-X-WORKFLOW-STEP-01..03`.

**Boundary:** This worker changes no authoritative checkbox.

**Status vector:** `[H4, M4, R4]`.

### M0115-T-RELATIVE

**Claim:** For every admissible D and alpha, identify the intermediate Chow
class supplied by the target Todd-action branch with Chow pushforward of the
source Chern/Todd expression.

**Role:** First open terminal premise of checked assembly.

**Inputs:** Factor branch, Chern engine, projection formula, composition engine.

**Proof route:** 1. Factor f. 2. prove both geometric cases. 3. compose. 4.
transport to the selected K_0 and Chow models.

**Branch logic:** Both factored cases and their recomposition are mandatory.

**Formal map:** `RelativeComparisonPackage`.

**Trust boundary:** Declaration is a proposition only; no inhabitant exists.

**Step ledger:** `M0115-T-RELATIVE-STEP-01..03`.

**Boundary:** It does not construct or identify the target Todd-capped class;
that witness belongs to its sibling branch.

**Status vector:** `[H4, M4, R4]`.

### M0115-T-TODD_ACTION

**Claim:** For every admissible D and alpha, construct an intermediate Chow
class identified with the exact target Todd-capped Chern character.

**Role:** Second open terminal premise of checked assembly.

**Inputs:** Todd identities and Chow projection formula.

**Proof route:** 1. identify the tangent/Todd relation. 2. cap the target factor.
3. construct `IntermediateComparisonData`. 4. expose its target-side equality.

**Branch logic:** The target-side witness is produced without assuming the
source-side relative identification.

**Formal map:** `TargetToddActionPackage`.

**Trust boundary:** Declaration is a proposition only; no inhabitant exists.

**Step ledger:** `M0115-T-TODD_ACTION-STEP-01..03`.

**Boundary:** It cannot independently prove the relative comparison.

**Status vector:** `[H4, M4, R4]`.

### M0115-T-FORMULA

**Claim:** `D.Formula alpha` holds for every datum satisfying the full frozen
hypothesis package.

**Role:** Exact terminal equality consumed by root assembly.

**Inputs:** `M0115-T-RELATIVE`, `M0115-T-TODD_ACTION`.

**Proof route:** 1. obtain target-identified intermediate data. 2. apply the
relative package to that exact data. 3. compose both equalities into the exact
formula.

**Branch logic:** Both children are explicitly consumed.

**Formal map:** `FormulaPackage` and
`formula_package_of_relative_and_todd`.

**Trust boundary:** Composition is checked but children remain uninhabited.

**Step ledger:** `M0115-T-FORMULA-STEP-01..03`.

**Boundary:** Conditional composition gives no machine closure to its premise or
parent.

**Status vector:** `[H4, M4, R4]`.

### M0115-T-ASSEMBLE

**Claim:** The exact terminal formula package yields the public canonical root.

**Role:** Final child-to-root composition certificate.

**Inputs:** `M0115-T-FORMULA`.

**Proof route:** 1. introduce the frozen binders. 2. pass the complete
hypothesis conjunction. 3. apply the package to alpha. 4. return the exact
expanded target.

**Branch logic:** The sole declared child is consumed.

**Formal map:** `AssembledRootPackage` and
`assembled_root_package_of_formula_package`.

**Trust boundary:** Lean checks the interface under `--trust=0`; no root body is
constructed.

**Step ledger:** `M0115-T-ASSEMBLE-STEP-01..03`.

**Boundary:** Root closure remains false.

**Status vector:** `[H4, M3, R4]`.

## Open Cut Sets

The minimal modeled machine cut set is
`{M0115-T-RELATIVE, M0115-T-TODD_ACTION}`. Closing it will still not establish
theorem completion until provenance, source, trust, evidence, readability,
hermetic validation, independent review, and release gates close. The current
architecture accepts zero closed obligations, zero terminal proof-body IDs, and
zero external reuse decisions.
