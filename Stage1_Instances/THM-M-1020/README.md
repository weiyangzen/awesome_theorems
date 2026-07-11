# THM-M-1020 rev-5.6 intake

This directory is the `planned` intake instance for the repository entry named “Parseval恒等式”.
The only supplied mathematical wording is “特征函数的积分恒等式” (an integral identity for
characteristic functions). That wording is not an exact theorem: it omits the formula, Fourier
normalization, domains, scalar field, and analytic hypotheses. The intake therefore preserves the
ambiguity rather than choosing a broader or substituted Parseval theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Repository claim | The exact source phrase and its probability-theory classification | Metadata status `已验证` is untrusted and supplies no evidence |
| Human statement | Identify a primary source that fixes the characteristic-function identity | No canonical formula can yet be frozen |
| Candidate meanings | Fourier Plancherel; characteristic-function L2 identities; density/measure inner-product identities | Discovery families only, not alternate encodings or proof obligations |
| Lean statement | Eventually select a minimal pinned mathlib expression matching the sourced formula | Module, declaration, binders, hypotheses, and expression hash are open |
| Degenerate cases | Zero/finite/infinite measures, absence of densities, non-L2 characteristic functions, and normalization constants | Must be resolved by the exact source, not guessed |
| Foundations | Lean 4 kernel with a versioned measure/integration/Fourier dependency profile | TCB, classical-choice use, and computation profile remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The next phase is blocked until a primary source identifies the exact formula and assumptions.
After that, statement work must freeze ordered binders and boundary cases, elaborate the exact Lean
target, and mutation-test its domain, hypotheses, normalization, and constants.

## Intake verdict

Lifecycle is `planned`; root vector is `[H5, M4, R4]`. The first failed gate is exact-source
identification. This dossier is self-tested as an intake artifact only. It does not claim the
statement phase, an upstream mathlib anchor, or theorem completion.

## Validation

Commands and results are recorded in `validation.md`. They establish target membership, rev-5.6
structural consistency, JSON syntax, and dossier-local integrity only.
