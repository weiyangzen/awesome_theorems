# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10875-10880` records only the title `循环神经网络`, proposer
`众多数学家`, time `20世纪`, gloss `序列处理的神经网络`, importance `高`, and status `已验证`. It
supplies no bibliography, formula, definitions, quantifiers, hypotheses, conclusion, proof,
corrections, or formal artifact. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that establishes repository provenance, not a
primary mathematical source.

`Docs/Stage0_Blueprint.md:40459-40484` repeats the gloss while explicitly leaving the formal
system, foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claim that a closed result is known is
planning metadata and receives no rev-5.6 credit. The manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Catalog component | Possible mathematical component | Prospective Lean surface | Intake result |
|---|---|---|---|
| recurrent | a feedback state update with time-shared parameters | typed state transition or list/finitary fold | no recurrence or sharing rule supplied |
| neural network | affine maps, biases, activations, gates, parameters | matrices/linear maps and coordinatewise functions | no cell architecture accepted |
| sequence | finite list, fixed-length vector, stream, or indexed family | `List`, `Vector`, `Nat ->`, or `Fin T ->` input | time carrier, horizon, and boundary open |
| processing | evaluation, prediction, transduction, approximation, stability, memory, or learning | an exact `Prop` with ordered binders | no truth-valued relationship stated |
| many mathematicians / twentieth century | source identity, edition, exact locator, corrections | immutable source revision and node crosswalk | untrusted metadata only |
| `已验证` | human proof or machine evidence | exact source review or module/declaration receipt | no credit |

The gloss cannot determine domains, parameters, recurrence, initial state, task, hypotheses,
conclusion, quantifier order, constants, arithmetic policy, or boundary cases.

## Historical source-family lead

Crossref metadata identifies Jeffrey L. Elman, *Finding Structure in Time*, *Cognitive Science*
14(2), 179-211 (1990), DOI `10.1207/s15516709cog1402_1`. It is a plausible historical lead for a
simple recurrent architecture and sequence-processing experiments, but the catalog cites neither
Elman nor this paper and says only "many mathematicians" and "twentieth century." No exact
definition, theorem, analytical proposition, assumptions, proof boundary, correction record, or
source-to-catalog identity is admitted. This metadata is `E5` discovery evidence, not H0.

## Non-substitution boundary

Encoding an Elman cell from memory, proving by induction that a fold implements it, or selecting a
universal-approximation, contractivity, fading-memory, gradient, or training theorem would add
mathematics absent from the source. LSTM, GRU, bidirectional, and stacked architectures have
different state and gate equations. A sequence-classification experiment is not a mathematical
theorem. Neighboring generic neural-network, backpropagation, deep-learning, CNN, and Transformer
targets provide no inherited scope or proof credit.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Data.Matrix.Mul` provides `Matrix.mulVec` and algebraic lemmas,
`Mathlib.Analysis.SpecialFunctions.Sigmoid` provides `Real.sigmoid` and analytic facts, and
`Mathlib.Data.List.Basic` provides fold lemmas. `IntakeProbe.lean` checks representative
declarations and selected axiom reports. These interfaces specify no RNN model, evaluator, source
statement, or theorem.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found only an incidental
documentation mention of neural networks in `Mathlib.Data.Holor`, not a recurrent-network target
declaration. This is feasibility evidence, not an exhaustive immutable candidate audit or global
absence proof.

## Retry condition

The statement phase may proceed only after accountable reviewers select one immutable truth-valued
source proposition, map the exact locator and every incorporated definition, assumption, proof
boundary, correction, and erratum, and freeze the recurrence, spaces, time carrier, sequence
semantics, parameters, activation/gates, initial state, task, norm/loss, hypotheses, conclusion,
quantifiers, computation boundary, and degenerate cases. A fresh statement worker must then
elaborate exactly that claim with minimal pinned imports and run removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations.

Until then no exact statement, H0, M0, R0, proof, audit completion, or theorem completion is
claimed.
