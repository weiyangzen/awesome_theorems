# THM-M-0058 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item
`冯·诺依曼迹不等式` (von Neumann trace inequality). The repository supplies the attribution
John von Neumann, the year 1937, and only the gloss `矩阵迹的最大值不等式` ("maximum-value
inequality for a matrix trace"). Its `已验证` label is explicitly untrusted under rev-5.6.

The theorem name identifies a classical result family, but the received wording is not a
binder-complete proposition. It does not specify the scalar field, dimensions, square versus
rectangular matrices, transpose versus conjugate transpose, absolute value versus real part,
singular-value indexing and ordering, the inequality direction, or whether an extremal equality is
part of the root. Choosing the familiar singular-value formula at intake would silently fill in all
of those missing mathematical choices.

An unverified historical lead encountered during discovery is a 1937 John von Neumann paper commonly
cited in later literature under the title *Some matrix-inequalities and metrization of matrix-space*.
This worker did not authenticate its full bibliographic metadata or obtain an immutable primary
passage, theorem/page locator, definitions, proof boundary, or errata record.
Later exact restatements likewise require admission and independent review. The title and familiar
formula are therefore discovery leads, not an accepted canonical statement or H0 evidence.

Pinned mathlib provides adjacent interfaces: matrix trace, finite-dimensional linear-map trace, and
ordered singular values. `IntakeProbe.lean` elaborates those APIs at the pinned revision. A bounded
topic search found no declaration relating trace to singular values. The probe neither defines a
canonical target nor proves an inequality.

The provisional theorem-family intake vector is `[H1, M4, R4]`: a classical theorem and historical
source lead are identifiable, but exact source fidelity is open; no usable formal theorem artifact
was located; and no source-faithful readable proof route exists. The root vector itself remains
unclassified until a canonical statement fingerprint and root obligation are frozen. All six
downstream phases remain open. No exact statement, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
