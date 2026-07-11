# THM-M-1523 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the catalogue item named "Mathematical
Foundations of Quantum Mechanics" (`量子力学的数学基础`). It begins at `L0 / rework_required` and
does not inherit proof credit from the legacy source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source wording | `希尔伯特空间形式` ("Hilbert-space formulation") | This is a topic/formalism, not yet a proposition with a truth value |
| Mathematical model | A complex Hilbert space; states, observables/operators, and an explicitly selected axiom package | No particular axiom system or operator class is silently selected |
| Candidate theorem families | spectral representation, variational statements, operator estimates, or consequences of stated quantum axioms | Candidates are discovery branches, not substitutes for the catalogue wording |
| Physical interpretation | Only consequences conditional on an explicit mathematical model | Experimental claims and correspondence rules are outside kernel-proof scope |
| Lean surface | Lean 4 plus pinned mathlib analysis/Hilbert-space/operator APIs | Exact module, declaration, imports, and expression fingerprint belong to the statement phase |
| Foundations | Lean kernel plus an accepted, versioned classical/choice/quotient policy | Exact foundation, TCB, and computation profiles remain open |

The statement phase must resolve the source ambiguity by locating an authoritative proposition (or
an explicit theorem-bearing axiom package) without turning the broad subject heading into a weaker
convenience theorem. Until then, spectral, variational, and uncertainty results are only candidate
scope branches.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed theorem gate is
exact-statement identity: the available source wording supplies no ordered binders, hypotheses, or
conclusion. No Lean theorem, source fidelity, machine closure, or theorem completion is claimed.

## Validation

The commands and exact outcomes in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases
remain outstanding.
