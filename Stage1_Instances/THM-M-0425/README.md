# THM-M-0425 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source entry "Hecke
L-functions". Historical Stage1 files are discovery inputs only and supply no
accepted proof or statement credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human claim | construction of the L-function attached to a Hecke character | The source inventory is too terse to determine character convention, conductor, infinity type, normalization, or analytic conclusion |
| Character data | a number field and a Hecke character, provisionally an idele-class character | Exact quotient, continuity, and finiteness hypotheses remain for the statement phase |
| L-function data | Dirichlet series and compatible Euler product in a convergence half-plane | Coefficients, local factors, bad primes, and convergence domain are not yet frozen |
| Analytic claims | none credited by this item | Continuation and functional equation belong to separate claims unless a primary source proves they are part of this target |
| Lean surface | existing `S1_M_079.lean` boundary structures and adjacent mathlib wrappers | These are legacy discovery candidates, not an elaborated canonical target or proof |
| Foundations | Lean 4 kernel plus pinned mathlib | Toolchain, imports, axioms, TCB, and computation profile require dependent phases |

The provisional root is deliberately narrower than THM-M-0426 (the functional
equation) but is not yet exact enough for Lean elaboration. The source wording
does not identify a single theorem, so intake preserves that ambiguity rather
than silently substituting a modern textbook theorem.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R3]`. The first failed gate is
the exact-source-statement gate: no edition/theorem/page-level primary anchor
has yet resolved the source entry into ordered hypotheses and a conclusion.
The dependent statement phase must not promote the legacy `StatementShape`,
whose proposition-valued structure fields make packages trivially inhabitable,
as the source theorem. The theorem is not complete.

## Validation

The exact commands and results for base revision
`1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06` are recorded in `validation.md`.
They validate membership and dossier structure only; no kernel closure is
claimed.
