# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10847-10852` records only the title `神经网络`, proposer
`众多数学家`, time `20世纪`, gloss `人工神经网络`, importance `高`, and status `已验证`. It supplies no bibliography,
formula, definitions, quantifiers, hypotheses, conclusion, proof, corrections, or formal artifact.
All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that establishes repository provenance, not a
primary mathematical source.

`Docs/Stage0_Blueprint.md:40351-40376` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic claims about known closure are legacy
discovery text and receive no rev-5.6 credit. The target manifest retains `已验证` only as
`source_status_untrusted`.

## Crosswalk

| Catalog component | Missing mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `人工` | scalar and computation model; exact versus floating point | scalar type, computability and TCB policy | absent |
| `神经网络` | architecture, layers, widths, parameters, biases, activation and evaluator | structures/functions over finite index types, matrices or linear maps | absent; no definition accepted |
| implicit input/output behavior | domains, codomains, target functions, data and loss | typed functions, sets, measures and objectives | absent |
| implicit theorem | representation, approximation, training, generalization, capacity, or other conclusion | an exact `Prop` with ordered binders | absent; family only |
| `众多数学家` / `20世纪` | source identity, edition, exact locator and corrections | immutable source revision and node crosswalk | untrusted metadata only |
| `已验证` | proof body, formal declaration, dependency revision and kernel evidence | exact module/declaration plus receipt | no credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Data.Matrix.Mul` provides `Matrix.mulVec` and its algebraic lemmas, while
`Mathlib.Analysis.SpecialFunctions.Sigmoid` provides `Real.sigmoid` and analytic properties such
as positivity, strict monotonicity, continuity, and derivatives. These are plausible ingredients
for some encodings, but they specify no architecture, parameter semantics, network evaluator,
source statement, or neural-network theorem.

A bounded case-insensitive search over repo-local Lean, pinned mathlib, and the pinned external
package found only an incidental documentation use of “neural network” in `Mathlib.Data.Holor` and
no exact neural-network declaration. This is discovery-only evidence, not an exhaustive anchor
audit or a global absence proof. Generic Stone-Weierstrass results likewise receive no credit
without a source-approved statement and checked semantic transport.

## Retry condition

The statement phase may proceed only after accountable reviewers select one immutable
truth-valued source proposition, freeze every architecture, activation, domain, parameter,
function-class, norm/loss, quantifier, conclusion, computation, and boundary choice in
`scope-map.md`, map the exact source locator and incorporated definitions/proof/corrections, and
approve why it is this repository target. A fresh statement worker must then elaborate exactly
that claim with minimal pinned imports and run hypothesis, domain, binder-scope, and boundary
mutations.
