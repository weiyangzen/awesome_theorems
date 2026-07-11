# THM-M-1521 rev-5.6 intake

This is the `planned` dossier for the Poincare recurrence theorem. The source phrase "bounded
systems are recurrent" is not itself a sufficiently specified theorem. The frozen root is the
standard discrete, finite-measure, measure-preserving recurrence claim in `intake.json`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Almost-everywhere infinite return to each null-measurable set | Exact elaboration and fingerprint belong to the statement phase |
| Dynamics | One discrete self-map preserving the same finite measure | Continuous flows require a checked time-map transport |
| Measure theory | Arbitrary measurable space and finite invariant measure | No physical measure is manufactured by this theorem |
| Topological variant | Return to neighborhoods under the usual countability/measurability assumptions | Candidate strengthening, not part of the frozen root |
| Physical interpretation | Future application through a finite invariant measure-preserving model | Hamiltonian phase space, Liouville invariance, and finite energy shell remain formalization debt |
| Foundations | Lean 4 kernel and pinned mathlib | Toolchain, imports, axioms, and transitive TCB are not frozen yet |

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_180.lean` and mathlib names are
discovery inputs only. No old proof, pin, build result, or source label receives rev-5.6 credit.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next phase must elaborate the exact root, fingerprint its environment, check transports, and
mutation-test finiteness, preservation, measurability, binder scope, and almost-everywhere strength.

## Intake verdict

Lifecycle is `planned`, with provisional vector `[H1, M3, R3]`. The first failed theorem gate is the
exact statement gate. This intake is self-tested structurally but is not theorem completion.
