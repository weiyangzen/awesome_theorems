# THM-M-0056 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named Weyl's
inequality. The repository supplies only the gloss "perturbation theory for eigenvalues of
Hermitian matrices," attributes it to Hermann Weyl in 1912, and labels it verified. That label is
untrusted inventory metadata, not an exact proposition, source audit, or machine-proof receipt.

The gloss does not select one theorem. Standard finite-matrix readings include the upper additive
eigenvalue inequality, its lower companion, both families together, and the operator-norm bound on
each ordered eigenvalue under a Hermitian perturbation. They require different conclusions and
index premises. The catalog also omits the scalar field, finite dimension, eigenvalue ordering and
multiplicity convention, norm, and zero-dimensional and endpoint cases. Intake therefore does not
silently choose the most familiar variant.

Weyl's 1912 primary paper was inspected from a public-domain scan. Its Section 1, Satz I, gives and
proves related upper and lower inequalities for symmetric integral kernels in Weyl's reciprocal
Fredholm eigenparameter notation. It is an important historical source-family lead, but it is not
literally the catalog's finite complex Hermitian-matrix wording. A versioned modern Hermitian-matrix
paper gives the upper additive inequality, and Terence Tao's notes display upper, lower, and norm
perturbation variants. These leads support `H1`, not `H0`: catalog-to-source identity, the
kernel-to-matrix passage, exact variant selection, transcription, corrections, immutable admission,
and independent review remain open.

Pinned mathlib supplies ordered Hermitian eigenvalues, eigenvectors, the spectral theorem, and
Rayleigh-quotient addition and norm bounds. `IntakeProbe.lean` authenticates those interfaces. A
bounded source search found no exact eigenvalue-of-sum or Weyl perturbation declaration and no
indexed Courant-Fischer/minimax bridge. The probe is adjacent infrastructure, not the target or a
proof body.

The provisional theorem-family intake vector is `[H1, M4, R4]`; the root vector remains
unclassified until a canonical statement and obligation are frozen. `instance.json` is the
structured scope authority, while `task-dag.json` leaves all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
