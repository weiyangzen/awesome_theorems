# THM-M-1257 rev-5.6 intake

This directory is the `planned` instance for Lewy's nonsolvability counterexample. The Stage0 label
"some linear PDEs have no solution" is only a discovery summary; it is not sufficiently precise to
serve as the formal target.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Lewy's explicit 1957 smooth, complex, first-order linear PDE and its failure of local solvability | The exact operator, forcing term, neighborhood quantifiers, and solution regularity require transcription from the primary paper |
| Analytic setting | Open neighborhoods of the origin in three real variables; complex-valued coefficients and unknown | No claim about all linear PDEs, global solvability, or boundary-value problems |
| Statement forms | Explicit counterexample and the corresponding non-surjectivity statement on local germs | Equivalence is not credited until definitions and a Lean transport are checked |
| Formal surface | A future Lean definition of the differential operator, local solution predicate, and explicit forcing term | No repo-local or upstream declaration has been identified or credited |
| Foundations | Lean 4 kernel plus pinned mathlib analysis APIs | Toolchain, imports, function spaces, classical principles, and TCB closure remain open |

The canonical claim and exclusions are structured in `intake.json`. The primary-source identity,
claim-component mapping, and unresolved transcription questions are recorded in
`source_statement_crosswalk.md`.

## Open task DAG

1. `STATEMENT`: obtain a stable primary-source copy; record its hash; transcribe the exact operator,
   forcing term, locality, and solution class; then elaborate the unweakened Lean target.
2. `ANCHOR_AUDIT`: search pinned mathlib and credible Lean projects for the exact analytic APIs and
   any terminal proof, recording negative as well as positive results.
3. `OBLIGATION_TREE`: freeze typed definition, analytic-estimate, contradiction, provenance, trust,
   evidence, and workflow nodes before proof metrics are observed.
4. `PROOF`: implement or immutably integrate every required body without changing the theorem.
5. `VALIDATION`: run exact-type, kernel, axiom, provenance, composition, hermetic, and independent
   checks.
6. `RELEASE`: reconcile accepted receipts and separately decide audit and theorem completion.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `M4` is deliberate: the
repository's one-line source summary omits statement-critical data, so inventing a Lean expression
would broaden or substitute the theorem. The first failed gate is exact source-statement freeze.
No theorem completion, machine closure, or inherited "verified" credit is claimed.

## Validation

The commands and exact results for this intake are recorded in `validation.md`. They validate
manifest membership, repository structure, JSON syntax, and dossier-local hygiene only; no Lean
kernel check is applicable because this phase introduces no Lean declaration.
