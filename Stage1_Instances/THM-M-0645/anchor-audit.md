# Lean 4 anchor audit

Item: `S56-M-0645-ANCHOR_AUDIT`  
Audit date: 2026-07-12  
Base revision: `5c0a4aafae91449d16f106bf558339d46b60f39b`

## Exact audit boundary

The audited root is `Stage1Instances.THM_M_0645.CompletenessTarget`, expression SHA-256
`76fbce831cb0d1669af8754a6c4f3c3d45d0e4fbbab1532e0140104937c7ea68`. It uses mathlib
sentences and semantics and concludes an inhabitant of the concrete `Derivation` type in
`Statement.lean`. A result about propositional logic, semantic compactness, model-theoretic
completeness of one theory, or another untransported proof calculus is not exact closure.

## Pinned mathlib

The locally available mathlib checkout is exactly
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (Lean 4.29.0). Its `ModelTheory` tree supplies the
object layer used by the statement: `Language`, `Sentence`, `Structure`, realization, theories,
satisfiability, and semantic consequence. The `Theory.IsComplete` declarations in
`Mathlib.ModelTheory.Satisfiability` mean that any two models of a theory are elementarily
equivalent. They are not syntactic proof completeness.

A scoped search of all Lean sources under pinned `Mathlib/ModelTheory` and `Mathlib/Logic` found
no derivation calculus or terminal theorem converting validity to derivability. Mathlib is
therefore classified `object_layer_only`, not a proof anchor.

## Repository-local candidate

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean` defines a calculus for the Craig
interpolation target and marks `SemanticToDerivabilityBridge` as the missing completeness bridge.
The file explicitly states that no inhabitant is supplied. Its calculus also differs from the
frozen target's equality and natural-deduction rules. It is a useful nonterminal boundary, not a
terminal candidate.

## External candidate

`FormalizedFormalLogic/Foundation` has a substantive first-order completeness development at
immutable revision `87d4dd68835a6c1eb8448b9c392d9ca51fe08d63`:

| Field | Audited value |
|---|---|
| Module | `Foundation.FirstOrder.Completeness.CounterModel` |
| Source | `Foundation/FirstOrder/Completeness/CounterModel.lean` |
| Source SHA-256 | `daa486fd8f6f8adaf34972aa61ef7ccaa93aa239556ec95def5bf57af09492d5` |
| Terminal declaration | `LO.FirstOrder.Theory.Proof.complete` |
| Type as written upstream | `T ⊨[Struc.{max u w} L] phi -> T ⊢ phi` |
| Companion declarations | `small_satisfiable_of_consistent`, `Proof.small_complete`, `Proof.complete_iff`, `Proof.complete_on_eq_models` |
| Proof route | unprovability gives consistency of `insert (not phi) T`; completeness builds a model and obtains a counterexample |
| Toolchain | `leanprover/lean4:v4.31.0` |
| Pinned mathlib | `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` |
| License | Apache-2.0 |

The terminal source contains no textual `sorry` or `admit`. That narrow observation is not a
transitive trust audit: this worker did not fetch/build the project or inspect its complete axiom
closure. Its language, sequent proof system, equality assumptions, semantic consequence relation,
and universes differ from this dossier's exact target. Its Lean/mathlib 4.31 dependency set also
does not match the pinned 4.29 environment.

Consequently the candidate is `external_upstream_anchor_only`. It cannot receive M0 credit. A
future proof phase must either provide a local proof or integrate Foundation at an immutable pin,
check its terminal closure, and prove a kernel-checked transport into the exact local `Derivation`.

## Search limitations

GitHub's unauthenticated code-search API returned HTTP 403 because its rate limit was exhausted.
The external search therefore used the project's own immutable README link, repository tree, raw
source, manifest, toolchain, and license. No dependency clone/fetch or `.lake` mutation was run.
The negative finding is restricted to the recorded local and pinned-mathlib source searches; it is
not a claim that no other Lean project exists.

## Verdict

The node-specific candidate audit is complete and self-tested, pending master acceptance. No proof
anchor is selected. Machine status remains `not_repo_local_closed` and root debt remains `M4`.
The external candidate creates an explicit integration opportunity/blocker, not theorem closure.
This phase claims audit completion only; theorem completion is false.
