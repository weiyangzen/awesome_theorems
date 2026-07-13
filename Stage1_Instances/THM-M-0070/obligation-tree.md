# THM-M-0070 frozen obligation tree

Item: `S56-M-0070-OBLIGATION_TREE`

The denominator is frozen from the exact Lean target, immutable anchor inventory, official
MathComp capstone, transitive BG/PF source packages, and the audited Lean-port roadmap. The
available exact Lean declaration is a placeholder and the exact MathComp theorem is a different
kernel object. Neither receives Lean proof credit.

## Checked route and boundary

The only locally checked proof path is `M0070-ROOT -> M0070-T-ROOT -> M0070-T-ADAPTER ->
M0070-X-LEAN-BODY`. `ObligationTree.lean` verifies exact conditional composition; the last node
is deliberately open. The MathComp route is a logical architecture rooted at
`M0070-X-COQ-SOURCE`, not a `proof_requires` path. Its section packages must be recursively split
and translated before proof acceptance. A 2,084-entry source declaration index records every
named declaration beneath those packages. Their split ceilings are not proof-length or closure
claims.

## Obligation ledger

<a id="m0070-root"></a>
### `M0070-ROOT` - root

Every finite multiplicative group whose natural-number cardinality is odd is solvable.

- Formal target: `Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget`
- Output: The exact frozen finite odd-order solvability proposition.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M3/R4`; risk `critical`; split ceiling `8`
- Premises: ["M0070-S-BOUNDARY", "M0070-S-ENCODINGS", "M0070-S-FOUNDATION", "M0070-S-INTERFACE", "M0070-T-ROOT", "M0070-X-COQ-SOURCE"]
- Inference: `Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-ROOT-STEP-01", "premise_ids": ["M0070-S-BOUNDARY", "M0070-S-ENCODINGS", "M0070-S-FOUNDATION", "M0070-S-INTERFACE", "M0070-T-ROOT", "M0070-X-COQ-SOURCE"], "inference_or_boundary": "Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget", "output_claim": "The exact frozen finite odd-order solvability proposition.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-s-interface"></a>
### `M0070-S-INTERFACE` - definition

Preserve the universe, Group and Finite binders, Nat.card oddness premise, and IsSolvable conclusion in their frozen order.

- Formal target: `Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget`
- Output: The exact formal context and conclusion without a special-group restriction.
- Eligibility: machine `required`, human source `not_applicable`, readable `required`
- Current debt: `H1/M0-L/R4`; risk `critical`; split ceiling `16`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-S-INTERFACE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget", "output_claim": "The exact formal context and conclusion without a special-group restriction.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-s-boundary"></a>
### `M0070-S-BOUNDARY` - branch

Include the trivial group and all finite noncommutative odd-order groups while excluding no odd cardinality and adding no nontriviality premise.

- Formal target: `Statement.lean boundary witnesses and four mutation classes`
- Output: The complete source-faithful degenerate and domain boundary policy.
- Eligibility: machine `required`, human source `not_applicable`, readable `required`
- Current debt: `H1/M0-L/R4`; risk `high`; split ceiling `20`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Statement.lean boundary witnesses and four mutation classes`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-S-BOUNDARY-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Statement.lean boundary witnesses and four mutation classes", "output_claim": "The complete source-faithful degenerate and domain boundary policy.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-s-encodings"></a>
### `M0070-S-ENCODINGS` - transport

Relate Finite/Nat.card to Fintype.card, Odd to congruence modulo two, and IsSolvable to eventual triviality of the derived series.

- Formal target: `oddOrderSolvabilityTarget_iff_fintypeCardTarget; oddOrderSolvabilityTarget_iff_modTwoTarget; oddOrderSolvabilityTarget_iff_derivedSeriesTarget`
- Output: Three checked bidirectional encoding transports.
- Eligibility: machine `required`, human source `not_applicable`, readable `required`
- Current debt: `H1/M0-L/R4`; risk `high`; split ceiling `18`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `oddOrderSolvabilityTarget_iff_fintypeCardTarget; oddOrderSolvabilityTarget_iff_modTwoTarget; oddOrderSolvabilityTarget_iff_derivedSeriesTarget`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-S-ENCODINGS-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "oddOrderSolvabilityTarget_iff_fintypeCardTarget; oddOrderSolvabilityTarget_iff_modTwoTarget; oddOrderSolvabilityTarget_iff_derivedSeriesTarget", "output_claim": "Three checked bidirectional encoding transports.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-s-foundation"></a>
### `M0070-S-FOUNDATION` - certificate

Fix the Lean kernel, classical choice, quotient, extensionality, import, computation, and accepted TCB policies for any terminal translation.

- Formal target: `planned transitive Lean foundation and TCB certificate`
- Output: A release-grade foundation decision without mathematical proof credit.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `40`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned transitive Lean foundation and TCB certificate`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-S-FOUNDATION-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned transitive Lean foundation and TCB certificate", "output_claim": "A release-grade foundation decision without mathematical proof credit.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-n-minimal-induction"></a>
### `M0070-N-MINIMAL-INDUCTION` - normalization

Reduce a hypothetical nonsolvable odd-order finite group by well-founded induction on cardinality to a minimal simple odd-order counterexample.

- Formal target: `Coq:BGsection7.minSimpleOdd_ind (planned Lean translation)`
- Output: A minimal-simple-odd-group context or solvability of the original group.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `96`
- Premises: ["M0070-B-MINIMAL-COUNTEREXAMPLE", "M0070-BG-7", "M0070-C-MINIMAL-SIMPLE"]
- Inference: `Coq:BGsection7.minSimpleOdd_ind (planned Lean translation)`
- Outgoing use: ["M0070-T-COQ-CAPSTONE"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-N-MINIMAL-INDUCTION-STEP-01", "premise_ids": ["M0070-B-MINIMAL-COUNTEREXAMPLE", "M0070-BG-7", "M0070-C-MINIMAL-SIMPLE"], "inference_or_boundary": "Coq:BGsection7.minSimpleOdd_ind (planned Lean translation)", "output_claim": "A minimal-simple-odd-group context or solvability of the original group.", "outgoing_use_ids": ["M0070-T-COQ-CAPSTONE"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-b-minimal-counterexample"></a>
### `M0070-B-MINIMAL-COUNTEREXAMPLE` - branch

Separate the induction branch already closed by proper odd-order sections from the minimal nonsolvable simple counterexample branch.

- Formal target: `planned exhaustive branch theorem around minSimpleOdd_ind`
- Output: Exhaustive induction branches with the minimal branch isolated.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `82`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned exhaustive branch theorem around minSimpleOdd_ind`
- Outgoing use: ["M0070-N-MINIMAL-INDUCTION"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-B-MINIMAL-COUNTEREXAMPLE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned exhaustive branch theorem around minSimpleOdd_ind", "output_claim": "Exhaustive induction branches with the minimal branch isolated.", "outgoing_use_ids": ["M0070-N-MINIMAL-INDUCTION"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-c-minimal-simple"></a>
### `M0070-C-MINIMAL-SIMPLE` - construction

Package the carrier, odd order, nonsolvability, simplicity, and strict-cardinality induction hypotheses of a minimal counterexample.

- Formal target: `Coq:minSimpleOddGroupType and TheMinSimpleOddGroup (planned Lean structure)`
- Output: A well-formed minimal-simple odd group context used by local and character analysis.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `94`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Coq:minSimpleOddGroupType and TheMinSimpleOddGroup (planned Lean structure)`
- Outgoing use: ["M0070-N-MINIMAL-INDUCTION"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-C-MINIMAL-SIMPLE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Coq:minSimpleOddGroupType and TheMinSimpleOddGroup (planned Lean structure)", "output_claim": "A well-formed minimal-simple odd group context used by local and character analysis.", "outgoing_use_ids": ["M0070-N-MINIMAL-INDUCTION"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-l-no-minimal"></a>
### `M0070-L-NO-MINIMAL` - core_lemma

Derive a contradiction from every minimal simple odd-order group by combining Bender-Glauberman local analysis with Peterfalvi character theory.

- Formal target: `Coq:PFsection14.no_minSimple_odd_group (planned Lean translation)`
- Output: False in the minimal-simple-odd-group context.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-B-TYPE-PAIR", "M0070-C-CHARACTER-CONTEXT", "M0070-C-LOCAL-CONTEXT", "M0070-PF-14"]
- Inference: `Coq:PFsection14.no_minSimple_odd_group (planned Lean translation)`
- Outgoing use: ["M0070-T-COQ-CAPSTONE"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-L-NO-MINIMAL-STEP-01", "premise_ids": ["M0070-B-TYPE-PAIR", "M0070-C-CHARACTER-CONTEXT", "M0070-C-LOCAL-CONTEXT", "M0070-PF-14"], "inference_or_boundary": "Coq:PFsection14.no_minSimple_odd_group (planned Lean translation)", "output_claim": "False in the minimal-simple-odd-group context.", "outgoing_use_ids": ["M0070-T-COQ-CAPSTONE"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-b-type-pair"></a>
### `M0070-B-TYPE-PAIR` - branch

Split the final minimal-group analysis between the all-type-I alternative and the existence of a paired type-P configuration S,T.

- Formal target: `Coq:PFsection14.no_minSimple_odd_group case split via FTtypeP_pair_cases`
- Output: An exhaustive final structural alternative.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `72`
- Premises: ["M0070-B-ALL-TYPE1", "M0070-B-TYPE2-EXCLUSION"]
- Inference: `Coq:PFsection14.no_minSimple_odd_group case split via FTtypeP_pair_cases`
- Outgoing use: ["M0070-L-NO-MINIMAL"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-B-TYPE-PAIR-STEP-01", "premise_ids": ["M0070-B-ALL-TYPE1", "M0070-B-TYPE2-EXCLUSION"], "inference_or_boundary": "Coq:PFsection14.no_minSimple_odd_group case split via FTtypeP_pair_cases", "output_claim": "An exhaustive final structural alternative.", "outgoing_use_ids": ["M0070-L-NO-MINIMAL"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-b-all-type1"></a>
### `M0070-B-ALL-TYPE1` - branch

Contradict the alternative that every maximal subgroup lies in the type-I configuration.

- Formal target: `Coq:PFsection14.not_all_FTtype1`
- Output: False for the all-type-I branch.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `86`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Coq:PFsection14.not_all_FTtype1`
- Outgoing use: ["M0070-B-TYPE-PAIR"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-B-ALL-TYPE1-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Coq:PFsection14.not_all_FTtype1", "output_claim": "False for the all-type-I branch.", "outgoing_use_ids": ["M0070-B-TYPE-PAIR"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-b-type2-exclusion"></a>
### `M0070-B-TYPE2-EXCLUSION` - branch

For a paired S,T configuration, derive the type-II structure and exclude it through support coherence and the final character contradiction.

- Formal target: `Coq:PFsection14.FTtype2_exclusion`
- Output: False for the paired type-P branch.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-14"]
- Inference: `Coq:PFsection14.FTtype2_exclusion`
- Outgoing use: ["M0070-B-TYPE-PAIR"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-B-TYPE2-EXCLUSION-STEP-01", "premise_ids": ["M0070-PF-14"], "inference_or_boundary": "Coq:PFsection14.FTtype2_exclusion", "output_claim": "False for the paired type-P branch.", "outgoing_use_ids": ["M0070-B-TYPE-PAIR"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-c-local-context"></a>
### `M0070-C-LOCAL-CONTEXT` - construction

Construct the maximal-subgroup types, Fitting cores, complements, TI sets, and local configurations used by the final contradiction.

- Formal target: `Coq:BGsection10-16 local-analysis contexts (planned Lean structures)`
- Output: The complete local finite-group data consumed by Peterfalvi sections 8-14.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `96`
- Premises: ["M0070-BG-16"]
- Inference: `Coq:BGsection10-16 local-analysis contexts (planned Lean structures)`
- Outgoing use: ["M0070-L-NO-MINIMAL"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-C-LOCAL-CONTEXT-STEP-01", "premise_ids": ["M0070-BG-16"], "inference_or_boundary": "Coq:BGsection10-16 local-analysis contexts (planned Lean structures)", "output_claim": "The complete local finite-group data consumed by Peterfalvi sections 8-14.", "outgoing_use_ids": ["M0070-L-NO-MINIMAL"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-c-character-context"></a>
### `M0070-C-CHARACTER-CONTEXT` - construction

Construct class-function supports, Dade and cyclic-TI isometries, coherence data, and integral character expansions.

- Formal target: `Coq:PFsection1-7 character-theory contexts (planned Lean structures)`
- Output: The character-theoretic data and invariants consumed by the final sections.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-7"]
- Inference: `Coq:PFsection1-7 character-theory contexts (planned Lean structures)`
- Outgoing use: ["M0070-L-NO-MINIMAL"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-C-CHARACTER-CONTEXT-STEP-01", "premise_ids": ["M0070-PF-7"], "inference_or_boundary": "Coq:PFsection1-7 character-theory contexts (planned Lean structures)", "output_claim": "The character-theoretic data and invariants consumed by the final sections.", "outgoing_use_ids": ["M0070-L-NO-MINIMAL"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-t-coq-capstone"></a>
### `M0070-T-COQ-CAPSTONE` - terminal

Compose minimal-counterexample induction with nonexistence of a minimal simple odd-order group to obtain the MathComp theorem.

- Formal target: `Coq:odd_order.PFsection14.Feit_Thompson`
- Output: The exact Coq/MathComp odd-order solvability conclusion.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M3/R4`; risk `critical`; split ceiling `12`
- Premises: ["M0070-L-NO-MINIMAL", "M0070-N-MINIMAL-INDUCTION"]
- Inference: `Coq:odd_order.PFsection14.Feit_Thompson`
- Outgoing use: ["M0070-X-COQ-SOURCE"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-T-COQ-CAPSTONE-STEP-01", "premise_ids": ["M0070-L-NO-MINIMAL", "M0070-N-MINIMAL-INDUCTION"], "inference_or_boundary": "Coq:odd_order.PFsection14.Feit_Thompson", "output_claim": "The exact Coq/MathComp odd-order solvability conclusion.", "outgoing_use_ids": ["M0070-X-COQ-SOURCE"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-lean-body"></a>
### `M0070-X-LEAN-BODY` - bridge

Implement or approve a semantics-preserving placeholder-free Lean body for the exact frozen root; the Coq source alone cannot inhabit this obligation.

- Formal target: `Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody`
- Output: An authorized Lean kernel term of the exact translated-body type.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M3/R4`; risk `critical`; split ceiling `30`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody`
- Outgoing use: ["M0070-T-ADAPTER"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-LEAN-BODY-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody", "output_claim": "An authorized Lean kernel term of the exact translated-body type.", "outgoing_use_ids": ["M0070-T-ADAPTER"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-coq-source"></a>
### `M0070-X-COQ-SOURCE` - bridge

Reproduce and audit the immutable MathComp odd-order source and use it only as an architecture/provenance input until an approved Lean bridge exists.

- Formal target: `math-comp/odd-order@6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f:PFsection14.Feit_Thompson`
- Output: A checked other-prover source record with no Lean proof credit.
- Eligibility: machine `informational`, human source `required`, readable `required`
- Current debt: `H1/M3/R4`; risk `critical`; split ceiling `48`
- Premises: ["M0070-T-COQ-CAPSTONE"]
- Inference: `math-comp/odd-order@6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f:PFsection14.Feit_Thompson`
- Outgoing use: ["release or independent review gate"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-X-COQ-SOURCE-STEP-01", "premise_ids": ["M0070-T-COQ-CAPSTONE"], "inference_or_boundary": "math-comp/odd-order@6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f:PFsection14.Feit_Thompson", "output_claim": "A checked other-prover source record with no Lean proof credit.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-lean-placeholder"></a>
### `M0070-X-LEAN-PLACEHOLDER` - bridge

Track the exact external Lean statement as rejected until its terminal body is not a placeholder and compatible pins are integrated.

- Formal target: `ianklatzco/odd-order-lean@0f4a5daeaf6f26efd5af808ecd05e4744d8a2924:odd_order_solvable`
- Output: A rejection boundary; never a proof premise or numerator.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M5/R4`; risk `critical`; split ceiling `18`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `ianklatzco/odd-order-lean@0f4a5daeaf6f26efd5af808ecd05e4744d8a2924:odd_order_solvable`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-LEAN-PLACEHOLDER-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "ianklatzco/odd-order-lean@0f4a5daeaf6f26efd5af808ecd05e4744d8a2924:odd_order_solvable", "output_claim": "A rejection boundary; never a proof premise or numerator.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-t-adapter"></a>
### `M0070-T-ADAPTER` - terminal

Consume the exact translated Lean body without weakening, strengthening, or changing an encoding.

- Formal target: `Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody`
- Output: The exact canonical target as a conditional conclusion.
- Eligibility: machine `required`, human source `not_applicable`, readable `required`
- Current debt: `H1/M0-L/R4`; risk `critical`; split ceiling `4`
- Premises: ["M0070-X-LEAN-BODY"]
- Inference: `Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody`
- Outgoing use: ["M0070-T-ROOT"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-T-ADAPTER-STEP-01", "premise_ids": ["M0070-X-LEAN-BODY"], "inference_or_boundary": "Stage1Instances.THM_M_0070.ObligationTree.target_of_translatedOddOrderBody", "output_claim": "The exact canonical target as a conditional conclusion.", "outgoing_use_ids": ["M0070-T-ROOT"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-t-root"></a>
### `M0070-T-ROOT` - terminal

Consume the exact adapter output and return the complete frozen root.

- Formal target: `Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target`
- Output: The complete root conclusion with no added premise beyond the open body child.
- Eligibility: machine `required`, human source `not_applicable`, readable `required`
- Current debt: `H1/M0-L/R4`; risk `critical`; split ceiling `4`
- Premises: ["M0070-T-ADAPTER"]
- Inference: `Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target`
- Outgoing use: ["M0070-ROOT"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-T-ROOT-STEP-01", "premise_ids": ["M0070-T-ADAPTER"], "inference_or_boundary": "Stage1Instances.THM_M_0070.ObligationTree.terminalTarget_of_target", "output_claim": "The complete root conclusion with no added premise beyond the open body child.", "outgoing_use_ids": ["M0070-ROOT"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-i-solvable-group"></a>
### `M0070-I-SOLVABLE-GROUP` - bridge

Solvable-group infrastructure: Hall subgroups, pi-cores, coprime action, Fitting theory, chief factors, and minimal-normal elementary-abelian structure.

- Formal target: `planned Lean Layer 0a; Coq/MathComp finite-group substrate`
- Output: The finite solvable-group and local-analysis substrate required by BG sections.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `96`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned Lean Layer 0a; Coq/MathComp finite-group substrate`
- Outgoing use: ["M0070-BG-7", "M0070-BG-1", "M0070-I-FROBENIUS-WIELANDT"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-I-SOLVABLE-GROUP-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned Lean Layer 0a; Coq/MathComp finite-group substrate", "output_claim": "The finite solvable-group and local-analysis substrate required by BG sections.", "outgoing_use_ids": ["M0070-BG-7", "M0070-BG-1", "M0070-I-FROBENIUS-WIELANDT"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-i-character"></a>
### `M0070-I-CHARACTER` - bridge

Arithmetic character infrastructure: class functions, orthogonality, induction, integrality, virtual characters, isometries, inertia, and Galois action.

- Formal target: `planned Lean Layer 0b; Coq/MathComp character substrate`
- Output: The ordinary and virtual character-theory substrate required by PF sections.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned Lean Layer 0b; Coq/MathComp character substrate`
- Outgoing use: ["M0070-PF-1", "M0070-BG-2", "M0070-I-FROBENIUS-WIELANDT"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-I-CHARACTER-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned Lean Layer 0b; Coq/MathComp character substrate", "output_claim": "The ordinary and virtual character-theory substrate required by PF sections.", "outgoing_use_ids": ["M0070-PF-1", "M0070-BG-2", "M0070-I-FROBENIUS-WIELANDT"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-i-frobenius-wielandt"></a>
### `M0070-I-FROBENIUS-WIELANDT` - bridge

Frobenius-group structure, kernel results, semiregularity, and the Wielandt fixed-point order formula.

- Formal target: `Coq:wielandt_fixpoint plus Frobenius substrate (planned Lean translation)`
- Output: The Frobenius and fixed-point engines shared by BG and PF analysis.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `96`
- Premises: ["M0070-I-CHARACTER", "M0070-I-SOLVABLE-GROUP"]
- Inference: `Coq:wielandt_fixpoint plus Frobenius substrate (planned Lean translation)`
- Outgoing use: ["M0070-BG-3", "M0070-PF-9"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-I-FROBENIUS-WIELANDT-STEP-01", "premise_ids": ["M0070-I-CHARACTER", "M0070-I-SOLVABLE-GROUP"], "inference_or_boundary": "Coq:wielandt_fixpoint plus Frobenius substrate (planned Lean translation)", "output_claim": "The Frobenius and fixed-point engines shared by BG and PF analysis.", "outgoing_use_ids": ["M0070-BG-3", "M0070-PF-9"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-1"></a>
### `M0070-BG-1` - bridge

Translate and compose Bender-Glauberman section 1: p-length, p-stability, p-constraint, Puig series, and finite-group local-analysis definitions.

- Formal target: `Coq:BGsection1.v theorem package (planned Lean translation)`
- Output: The reviewed section-1 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-I-SOLVABLE-GROUP"]
- Inference: `Coq:BGsection1.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-2"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-1-STEP-01", "premise_ids": ["M0070-I-SOLVABLE-GROUP"], "inference_or_boundary": "Coq:BGsection1.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-1 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-2"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-2"></a>
### `M0070-BG-2` - bridge

Translate and compose Bender-Glauberman section 2: odd-order linear groups and the GL(2,p) representation bounds.

- Formal target: `Coq:BGsection2.v theorem package (planned Lean translation)`
- Output: The reviewed section-2 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-1", "M0070-I-CHARACTER"]
- Inference: `Coq:BGsection2.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-3"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-2-STEP-01", "premise_ids": ["M0070-BG-1", "M0070-I-CHARACTER"], "inference_or_boundary": "Coq:BGsection2.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-2 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-3"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-3"></a>
### `M0070-BG-3` - bridge

Translate and compose Bender-Glauberman section 3: Frobenius, Wielandt, regular-action, and metacyclic local structure.

- Formal target: `Coq:BGsection3.v theorem package (planned Lean translation)`
- Output: The reviewed section-3 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-2", "M0070-I-FROBENIUS-WIELANDT"]
- Inference: `Coq:BGsection3.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-4"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-3-STEP-01", "premise_ids": ["M0070-BG-2", "M0070-I-FROBENIUS-WIELANDT"], "inference_or_boundary": "Coq:BGsection3.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-3 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-4"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-4"></a>
### `M0070-BG-4` - bridge

Translate and compose Bender-Glauberman section 4: rank-two p-group and elementary-abelian local structure.

- Formal target: `Coq:BGsection4.v theorem package (planned Lean translation)`
- Output: The reviewed section-4 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-3"]
- Inference: `Coq:BGsection4.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-5"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-4-STEP-01", "premise_ids": ["M0070-BG-3"], "inference_or_boundary": "Coq:BGsection4.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-4 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-5"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-5"></a>
### `M0070-BG-5` - bridge

Translate and compose Bender-Glauberman section 5: narrow p-groups and their characteristic subgroups.

- Formal target: `Coq:BGsection5.v theorem package (planned Lean translation)`
- Output: The reviewed section-5 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-4"]
- Inference: `Coq:BGsection5.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-6"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-5-STEP-01", "premise_ids": ["M0070-BG-4"], "inference_or_boundary": "Coq:BGsection5.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-5 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-6"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-6"></a>
### `M0070-BG-6` - bridge

Translate and compose Bender-Glauberman section 6: factorization and transitivity inputs for the uniqueness analysis.

- Formal target: `Coq:BGsection6.v theorem package (planned Lean translation)`
- Output: The reviewed section-6 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-5", "M0070-BG-APPENDIX-AB"]
- Inference: `Coq:BGsection6.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-7"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-6-STEP-01", "premise_ids": ["M0070-BG-5", "M0070-BG-APPENDIX-AB"], "inference_or_boundary": "Coq:BGsection6.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-6 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-7"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-7"></a>
### `M0070-BG-7` - bridge

Translate and compose Bender-Glauberman section 7: minimal-simple-odd framework and Thompson transitivity.

- Formal target: `Coq:BGsection7.v theorem package (planned Lean translation)`
- Output: The reviewed section-7 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-6", "M0070-I-SOLVABLE-GROUP"]
- Inference: `Coq:BGsection7.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-N-MINIMAL-INDUCTION", "M0070-BG-8"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-7-STEP-01", "premise_ids": ["M0070-BG-6", "M0070-I-SOLVABLE-GROUP"], "inference_or_boundary": "Coq:BGsection7.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-7 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-N-MINIMAL-INDUCTION", "M0070-BG-8"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-8"></a>
### `M0070-BG-8` - bridge

Translate and compose Bender-Glauberman section 8: first uniqueness theorem for maximal local configurations.

- Formal target: `Coq:BGsection8.v theorem package (planned Lean translation)`
- Output: The reviewed section-8 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-7"]
- Inference: `Coq:BGsection8.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-9"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-8-STEP-01", "premise_ids": ["M0070-BG-7"], "inference_or_boundary": "Coq:BGsection8.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-8 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-9"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-9"></a>
### `M0070-BG-9` - bridge

Translate and compose Bender-Glauberman section 9: the uniqueness theorem chapter and its conjugacy consequences.

- Formal target: `Coq:BGsection9.v theorem package (planned Lean translation)`
- Output: The reviewed section-9 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-8"]
- Inference: `Coq:BGsection9.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-10"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-9-STEP-01", "premise_ids": ["M0070-BG-8"], "inference_or_boundary": "Coq:BGsection9.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-9 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-10"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-10"></a>
### `M0070-BG-10` - bridge

Translate and compose Bender-Glauberman section 10: sigma, alpha, beta, uniqueness, and maximal-subgroup machinery.

- Formal target: `Coq:BGsection10.v theorem package (planned Lean translation)`
- Output: The reviewed section-10 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-9"]
- Inference: `Coq:BGsection10.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-11"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-10-STEP-01", "premise_ids": ["M0070-BG-9"], "inference_or_boundary": "Coq:BGsection10.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-10 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-11"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-11"></a>
### `M0070-BG-11` - bridge

Translate and compose Bender-Glauberman section 11: the kappa-family hypotheses and structural consequences.

- Formal target: `Coq:BGsection11.v theorem package (planned Lean translation)`
- Output: The reviewed section-11 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-10"]
- Inference: `Coq:BGsection11.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-12"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-11-STEP-01", "premise_ids": ["M0070-BG-10"], "inference_or_boundary": "Coq:BGsection11.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-11 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-12"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-12"></a>
### `M0070-BG-12` - bridge

Translate and compose Bender-Glauberman section 12: type-F complements and the main local classification engine.

- Formal target: `Coq:BGsection12.v theorem package (planned Lean translation)`
- Output: The reviewed section-12 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-11"]
- Inference: `Coq:BGsection12.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-13"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-12-STEP-01", "premise_ids": ["M0070-BG-11"], "inference_or_boundary": "Coq:BGsection12.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-12 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-13"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-13"></a>
### `M0070-BG-13` - bridge

Translate and compose Bender-Glauberman section 13: prime and regular actions used by later maximal-subgroup types.

- Formal target: `Coq:BGsection13.v theorem package (planned Lean translation)`
- Output: The reviewed section-13 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-12"]
- Inference: `Coq:BGsection13.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-14"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-13-STEP-01", "premise_ids": ["M0070-BG-12"], "inference_or_boundary": "Coq:BGsection13.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-13 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-14"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-14"></a>
### `M0070-BG-14` - bridge

Translate and compose Bender-Glauberman section 14: kappa-complement structure and the section-14 local analysis.

- Formal target: `Coq:BGsection14.v theorem package (planned Lean translation)`
- Output: The reviewed section-14 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-13"]
- Inference: `Coq:BGsection14.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-15"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-14-STEP-01", "premise_ids": ["M0070-BG-13"], "inference_or_boundary": "Coq:BGsection14.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-14 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-15"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-15"></a>
### `M0070-BG-15` - bridge

Translate and compose Bender-Glauberman section 15: corrected local structure theorems feeding the final type classification.

- Formal target: `Coq:BGsection15.v theorem package (planned Lean translation)`
- Output: The reviewed section-15 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-14"]
- Inference: `Coq:BGsection15.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-BG-16"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-15-STEP-01", "premise_ids": ["M0070-BG-14"], "inference_or_boundary": "Coq:BGsection15.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-15 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-BG-16"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-16"></a>
### `M0070-BG-16` - bridge

Translate and compose Bender-Glauberman section 16: type F/P/P1/P2 and type I-V interface consumed by Peterfalvi analysis.

- Formal target: `Coq:BGsection16.v theorem package (planned Lean translation)`
- Output: The reviewed section-16 interface required by its downstream BG/PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-15"]
- Inference: `Coq:BGsection16.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-C-LOCAL-CONTEXT", "M0070-PF-8"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-16-STEP-01", "premise_ids": ["M0070-BG-15"], "inference_or_boundary": "Coq:BGsection16.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-16 interface required by its downstream BG/PF consumers.", "outgoing_use_ids": ["M0070-C-LOCAL-CONTEXT", "M0070-PF-8"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-appendix-ab"></a>
### `M0070-BG-APPENDIX-AB` - bridge

Translate p-stability and the Puig ZL-theorem from Bender-Glauberman appendices A and B.

- Formal target: `Coq:BGappendixAB.v theorem package`
- Output: The p-stability and Puig-factorization interface.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Coq:BGappendixAB.v theorem package`
- Outgoing use: ["M0070-BG-6"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-APPENDIX-AB-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Coq:BGappendixAB.v theorem package", "output_claim": "The p-stability and Puig-factorization interface.", "outgoing_use_ids": ["M0070-BG-6"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-bg-appendix-c"></a>
### `M0070-BG-APPENDIX-C` - bridge

Translate the finite-field norm and character estimate of Appendix C used only in Peterfalvi theorem 14.2.

- Formal target: `Coq:BGappendixC.prime_dim_normed_finField`
- Output: The arithmetic inequality excluding the final Galois configuration.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `Coq:BGappendixC.prime_dim_normed_finField`
- Outgoing use: ["M0070-PF-14"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-BG-APPENDIX-C-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "Coq:BGappendixC.prime_dim_normed_finField", "output_claim": "The arithmetic inequality excluding the final Galois configuration.", "outgoing_use_ids": ["M0070-PF-14"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-1"></a>
### `M0070-PF-1` - bridge

Translate and compose Peterfalvi section 1: preliminary virtual-character, algebraic-integer, and automorphism results.

- Formal target: `Coq:PFsection1.v theorem package (planned Lean translation)`
- Output: The reviewed section-1 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-I-CHARACTER"]
- Inference: `Coq:PFsection1.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-2"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-1-STEP-01", "premise_ids": ["M0070-I-CHARACTER"], "inference_or_boundary": "Coq:PFsection1.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-1 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-2"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-2"></a>
### `M0070-PF-2` - bridge

Translate and compose Peterfalvi section 2: the Dade isometry and reciprocity.

- Formal target: `Coq:PFsection2.v theorem package (planned Lean translation)`
- Output: The reviewed section-2 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-1"]
- Inference: `Coq:PFsection2.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-3"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-2-STEP-01", "premise_ids": ["M0070-PF-1"], "inference_or_boundary": "Coq:PFsection2.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-2 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-3"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-3"></a>
### `M0070-PF-3` - bridge

Translate and compose Peterfalvi section 3: cyclic-normalizer TI subsets and their isometry.

- Formal target: `Coq:PFsection3.v theorem package (planned Lean translation)`
- Output: The reviewed section-3 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-2"]
- Inference: `Coq:PFsection3.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-4"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-3-STEP-01", "premise_ids": ["M0070-PF-2"], "inference_or_boundary": "Coq:PFsection3.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-3 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-4"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-4"></a>
### `M0070-PF-4` - bridge

Translate and compose Peterfalvi section 4: the Dade isometry for the prime-TI subgroup configuration.

- Formal target: `Coq:PFsection4.v theorem package (planned Lean translation)`
- Output: The reviewed section-4 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-3"]
- Inference: `Coq:PFsection4.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-5"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-4-STEP-01", "premise_ids": ["M0070-PF-3"], "inference_or_boundary": "Coq:PFsection4.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-4 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-5"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-5"></a>
### `M0070-PF-5` - bridge

Translate and compose Peterfalvi section 5: the coherence framework for induced-character families.

- Formal target: `Coq:PFsection5.v theorem package (planned Lean translation)`
- Output: The reviewed section-5 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-4"]
- Inference: `Coq:PFsection5.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-6"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-5-STEP-01", "premise_ids": ["M0070-PF-4"], "inference_or_boundary": "Coq:PFsection5.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-5 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-6"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-6"></a>
### `M0070-PF-6` - bridge

Translate and compose Peterfalvi section 6: Sibley coherence and supporting estimates.

- Formal target: `Coq:PFsection6.v theorem package (planned Lean translation)`
- Output: The reviewed section-6 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-5"]
- Inference: `Coq:PFsection6.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-7"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-6-STEP-01", "premise_ids": ["M0070-PF-5"], "inference_or_boundary": "Coq:PFsection6.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-6 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-7"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-7"></a>
### `M0070-PF-7` - bridge

Translate and compose Peterfalvi section 7: inverse Dade and nonexistence of the preliminary odd-order configuration.

- Formal target: `Coq:PFsection7.v theorem package (planned Lean translation)`
- Output: The reviewed section-7 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-6"]
- Inference: `Coq:PFsection7.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-C-CHARACTER-CONTEXT", "M0070-PF-8"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-7-STEP-01", "premise_ids": ["M0070-PF-6"], "inference_or_boundary": "Coq:PFsection7.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-7 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-C-CHARACTER-CONTEXT", "M0070-PF-8"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-8"></a>
### `M0070-PF-8` - bridge

Translate and compose Peterfalvi section 8: FT-Dade instances and the bridge from BG type definitions.

- Formal target: `Coq:PFsection8.v theorem package (planned Lean translation)`
- Output: The reviewed section-8 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-16", "M0070-PF-7"]
- Inference: `Coq:PFsection8.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-9"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-8-STEP-01", "premise_ids": ["M0070-BG-16", "M0070-PF-7"], "inference_or_boundary": "Coq:PFsection8.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-8 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-9"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-9"></a>
### `M0070-PF-9` - bridge

Translate and compose Peterfalvi section 9: maximal subgroups of types II, III, and IV.

- Formal target: `Coq:PFsection9.v theorem package (planned Lean translation)`
- Output: The reviewed section-9 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-I-FROBENIUS-WIELANDT", "M0070-PF-8"]
- Inference: `Coq:PFsection9.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-10"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-9-STEP-01", "premise_ids": ["M0070-I-FROBENIUS-WIELANDT", "M0070-PF-8"], "inference_or_boundary": "Coq:PFsection9.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-9 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-10"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-10"></a>
### `M0070-PF-10` - bridge

Translate and compose Peterfalvi section 10: noncoherence and exclusion of type V.

- Formal target: `Coq:PFsection10.v theorem package (planned Lean translation)`
- Output: The reviewed section-10 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-9"]
- Inference: `Coq:PFsection10.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-11"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-10-STEP-01", "premise_ids": ["M0070-PF-9"], "inference_or_boundary": "Coq:PFsection10.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-10 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-11"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-11"></a>
### `M0070-PF-11` - bridge

Translate and compose Peterfalvi section 11: precise structure of maximal subgroups of types III and IV.

- Formal target: `Coq:PFsection11.v theorem package (planned Lean translation)`
- Output: The reviewed section-11 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-10"]
- Inference: `Coq:PFsection11.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-12"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-11-STEP-01", "premise_ids": ["M0070-PF-10"], "inference_or_boundary": "Coq:PFsection11.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-11 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-12"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-12"></a>
### `M0070-PF-12` - bridge

Translate and compose Peterfalvi section 12: type-I Frobenius structure and coherence consequences.

- Formal target: `Coq:PFsection12.v theorem package (planned Lean translation)`
- Output: The reviewed section-12 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-11"]
- Inference: `Coq:PFsection12.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-13"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-12-STEP-01", "premise_ids": ["M0070-PF-11"], "inference_or_boundary": "Coq:PFsection12.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-12 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-13"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-13"></a>
### `M0070-PF-13` - bridge

Translate and compose Peterfalvi section 13: the paired subgroups S and T and their symmetric character data.

- Formal target: `Coq:PFsection13.v theorem package (planned Lean translation)`
- Output: The reviewed section-13 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-PF-12"]
- Inference: `Coq:PFsection13.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-PF-14"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-13-STEP-01", "premise_ids": ["M0070-PF-12"], "inference_or_boundary": "Coq:PFsection13.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-13 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-PF-14"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-pf-14"></a>
### `M0070-PF-14` - bridge

Translate and compose Peterfalvi section 14: nonexistence of the minimal simple odd group and the final contradiction.

- Formal target: `Coq:PFsection14.v theorem package (planned Lean translation)`
- Output: The reviewed section-14 interface required by its downstream PF consumers.
- Eligibility: machine `required`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["M0070-BG-APPENDIX-C", "M0070-PF-13"]
- Inference: `Coq:PFsection14.v theorem package (planned Lean translation)`
- Outgoing use: ["M0070-L-NO-MINIMAL", "M0070-B-TYPE2-EXCLUSION"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-PF-14-STEP-01", "premise_ids": ["M0070-BG-APPENDIX-C", "M0070-PF-13"], "inference_or_boundary": "Coq:PFsection14.v theorem package (planned Lean translation)", "output_claim": "The reviewed section-14 interface required by its downstream PF consumers.", "outgoing_use_ids": ["M0070-L-NO-MINIMAL", "M0070-B-TYPE2-EXCLUSION"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-source"></a>
### `M0070-X-SOURCE` - source_boundary

Pinpoint every obligation to the complete Feit-Thompson, Bender-Glauberman, Peterfalvi, and formal-source proof boundaries, corrections, and errata.

- Formal target: `planned primary-source and formal-source crosswalk`
- Output: An independently accepted H0 node map.
- Eligibility: machine `not_applicable`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned primary-source and formal-source crosswalk`
- Outgoing use: ["release or independent review gate"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-X-SOURCE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned primary-source and formal-source crosswalk", "output_claim": "An independently accepted H0 node map.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-provenance"></a>
### `M0070-X-PROVENANCE` - certificate

Freeze every wrapper, terminal declaration, proof body, source blob, revision, dependency, and alias without duplicate credit.

- Formal target: `planned body-level provenance closure`
- Output: Complete transitive declaration and proof-body provenance.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `92`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned body-level provenance closure`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-PROVENANCE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned body-level provenance closure", "output_claim": "Complete transitive declaration and proof-body provenance.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-trust"></a>
### `M0070-X-TRUST` - certificate

Audit Lean and any supporting Coq kernels, axioms, artifacts, dependencies, unsafe/oracle boundaries, supply chain, and replay transitively.

- Formal target: `planned transitive trust closure`
- Output: An accepted cross-system trust and TCB decision.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `94`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned transitive trust closure`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-TRUST-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned transitive trust closure", "output_claim": "An accepted cross-system trust and TCB decision.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-license"></a>
### `M0070-X-LICENSE` - certificate

Verify CeCILL-B, Apache-2.0, mathlib, and every transitive source license and redistribution boundary.

- Formal target: `planned license and SBOM packet`
- Output: An accepted supply-chain license decision.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `30`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned license and SBOM packet`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-LICENSE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned license and SBOM packet", "output_claim": "An accepted supply-chain license decision.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-readable"></a>
### `M0070-X-READABLE` - certificate

Produce a complete independently reviewed readable reconstruction aligned with every high-risk local and character-theory package.

- Formal target: `planned long readable proof and review`
- Output: R0 coverage of the exact obligation denominator.
- Eligibility: machine `informational`, human source `required`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `98`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned long readable proof and review`
- Outgoing use: ["release or independent review gate"]
- Package state: `split_required_before_proof_acceptance`
- Structured ledger: [{"step_id": "M0070-X-READABLE-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned long readable proof and review", "output_claim": "R0 coverage of the exact obligation denominator.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

<a id="m0070-x-workflow"></a>
### `M0070-X-WORKFLOW` - certificate

Bind proof, validation, freshness, revocation, independent verification, deterministic evidence, and release receipts.

- Formal target: `planned rev-5.6 workflow evidence`
- Output: A dependency-legal release decision without mathematical proof credit.
- Eligibility: machine `informational`, human source `not_applicable`, readable `required`
- Current debt: `H1/M4/R4`; risk `critical`; split ceiling `56`
- Premises: ["EXACT-FROZEN-CONTEXT"]
- Inference: `planned rev-5.6 workflow evidence`
- Outgoing use: ["release or independent review gate"]
- Package state: `locally_bounded`
- Structured ledger: [{"step_id": "M0070-X-WORKFLOW-STEP-01", "premise_ids": ["EXACT-FROZEN-CONTEXT"], "inference_or_boundary": "planned rev-5.6 workflow evidence", "output_claim": "A dependency-legal release decision without mathematical proof credit.", "outgoing_use_ids": ["release or independent review gate"]}]
- Boundary: Frozen architecture or conditionally checked interface only; no external body, accepted root proof, H0, R0, or theorem completion.

## Root cut

The root remains `H1/M3/R4`. The first machine cut is `M0070-X-LEAN-BODY`. Source,
foundation, provenance, trust, license, readability, workflow, proof, validation, release,
and master acceptance remain open. No obligation in this registry is accepted closed.
