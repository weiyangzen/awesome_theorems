# THM-M-0696 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for completeness of classical propositional
logic. The Stage0 label `已验证` is untrusted discovery metadata and supplies no proof or acceptance
credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Semantic consequence implies syntactic derivability: `Gamma entails phi -> Gamma derives phi` | The atom type, context representation, connectives, valuation semantics, and calculus must be selected and elaborated in the statement phase |
| Logic | Finitary, two-valued classical propositional logic | Intuitionistic, modal, many-valued, infinitary, and first-order logics are excluded |
| Semantics | All Boolean valuations; a valuation satisfying every premise in `Gamma` must satisfy `phi` | Lean's ambient `Prop` is not silently identified with object-language syntax or derivability |
| Syntax | One standard, explicitly encoded proof calculus, such as Hilbert, natural deduction, or sequent calculus | Completeness is calculus-relative; an arbitrary derivability predicate or a tactic success claim is not the theorem |
| Context | General premise consequence is the intended root | Empty-context tautological completeness is only an alternate form until a deduction/finite-context transport is checked |
| Proof architecture | Likely routes include truth-table induction, disjunctive normal form, maximal consistent sets, or translation between calculi | Architecture is not frozen and no obligation or proof closure is credited |
| Foundations and TCB | Lean 4 kernel and the pinned mathlib environment | Imports, expression fingerprint, actual axioms, transitive dependencies, computation boundary, and TCB remain open |

The choice of calculus is intentionally not guessed from the short Stage0 slogan. The canonical
human claim is narrow enough to reject nearby theorems, while `intake.json` keeps the concrete Lean
expression open until the statement phase can freeze all syntax and binder choices.

## Intake verdict

Lifecycle is `planned`. Root debt is provisionally `[H1, M4, R3]`: a primary historical source
candidate exists, no exact Lean target has been elaborated, and no independently reviewed readable
reconstruction exists. `task-dag.json` is an all-open dossier projection; the repository master DAG
remains authoritative.

The intake is self-tested pending master acceptance. Human-source fidelity, exact statement,
anchor audit, obligations, proof, trust, reproducibility, and release gates remain open. The theorem
is not complete.

## Validation

Exact intake-only commands and results are recorded in `validation.md`. They establish manifest
membership, standard consistency, JSON syntax, dossier-local references, and the availability of
the pinned Lean executable only. They do not elaborate or prove the theorem.
