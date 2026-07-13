# THM-M-0052 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Moore-Penrose generalized inverse. The repository says only that "every matrix has a unique
generalized inverse," attributes the entry jointly to Roger Penrose and Eliakim Moore, dates it to
1955, and labels it verified. That label is untrusted inventory metadata, not an exact proposition,
a source audit, or machine-proof evidence.

The gloss is not stable without a definition of "generalized inverse." An inner inverse satisfying
only `A * X * A = A` need not be unique. Penrose's 1955 theorem instead selects a unique matrix by
four equations involving conjugate transpose. The catalog does not state those equations, the
complex scalar domain, rectangular dimensions, or the multiplication and adjoint conventions.
Intake therefore records the intended Moore-Penrose family but does not silently turn the terse
gloss into a canonical proposition.

R. Penrose's primary article, *A generalized inverse for matrices*, was inspected from the
publisher-served PDF. Theorem 1 on printed pages 406-407 states and proves that four displayed
equations have a unique solution for every possibly rectangular complex matrix. This is a strong
primary-source lead. It remains `H1`, not `H0`, because the catalog gives no citation, its joint
Moore attribution and 1955 date have not been reconciled, no immutable source packet or correction
audit is admitted, the OCR-to-symbol transcription must be independently checked, and no reviewer
has accepted a clause-by-clause source-to-Lean mapping.

Pinned mathlib supplies rectangular matrices, multiplication, conjugate transpose, Hermitian
matrices, and square nonsingular inverses. Its nonsingular-inverse module explicitly says that it
does not consider pseudoinverses. A bounded repository and pinned-mathlib search found no
Moore-Penrose or matrix-pseudoinverse declaration. `IntakeProbe.lean` checks only those adjacent
interfaces and a square-invertible non-substitute; it does not declare or prove the target.

The provisional vector is `[H1, M4, R4]`. A complete primary human-proof lead has been inspected,
but exact source identity and review remain open; no exact usable formal target or proof body is
credited; and no accepted readable reconstruction exists. `instance.json` is the structured scope
authority and `task-dag.json` leaves all six downstream phases open. No H0, M0, R0, accepted state,
audit completion, theorem completion, or master acceptance is claimed.
