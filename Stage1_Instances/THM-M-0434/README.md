# THM-M-0434 rev-5.6 intake

This is the `planned` rev-5.6 instance for Ngo Bao Chau's Fundamental Lemma. The terse catalog
phrase `基本引理的证明` is resolved at intake to the Lie-algebra Fundamental Lemma proved in Ngo's
2010 primary paper. This choice must still receive source and statement review; it does not inherit
credit from the legacy slot.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Ngo's source-normalized Lie-algebra Fundamental Lemma | Exact theorem subcase, notation, and hypotheses require statement-phase transcription |
| Arithmetic regime | Positive characteristic and the stated sufficiently-large residual-characteristic transfer to characteristic zero | The bound and transfer theorem must not be erased |
| Geometric objects | reductive/endoscopic data, regular semisimple matching, integral models | No concrete Lean API is selected |
| Analytic objects | orbital integrals, stable sums, Haar measures, transfer factors, unit functions | All definitions and normalization bridges are open |
| Related form | group Fundamental Lemma | A separate reduction/transport is required; it is not silently identified with the root |
| Legacy Lean | `S1_M_083.lean` structures and `StatementShapeWithHyperspecialModel` | Discovery input only; its abstract functions make the implication wrapper tautological rather than the source theorem |
| Foundations | Lean 4 kernel, pinned mathlib, accepted classical/quotient/measure policy | Toolchain, imports, TCB, and expression fingerprint remain open |

The proof architecture is provisionally: exact source transcription; concrete group/endoscopy API;
matching and regular-semisimple loci; measures and orbital integrals; transfer-factor normalization;
geometric/Hitchin comparison; local-to-global and characteristic transfer; terminal composition. Stable
obligation IDs and all typed graphs belong to the later obligation-tree phase.

## Intake verdict

Lifecycle is `planned`, with provisional vector `[H1, M4, R3]`. The first failed theorem gate is the
exact statement gate: no faithful Lean expression, environment fingerprint, checked transport, or
mutation evidence exists. The theorem is not complete.

Validation commands and their exact outcomes are recorded in `validation.md`.
