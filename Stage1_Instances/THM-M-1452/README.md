# THM-M-1452 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Lanczos算法`
(Lanczos algorithm). The entire catalog gloss is `大型稀疏矩阵的特征值` ("eigenvalues of large
sparse matrices"), attributed to Cornelius Lanczos in 1950. That is a computational topic, not a
truth-valued proposition with ordered binders, hypotheses, and a conclusion. The attribution,
date, and `已验证` label are untrusted catalog metadata, not source or proof evidence.

The 1950 primary-paper lead is C. Lanczos, "An Iteration Method for the Solution of the Eigenvalue
Problem of Linear Differential and Integral Operators," *Journal of Research of the National
Bureau of Standards* 45(4), Research Paper 2133, pages 255-282, DOI
`10.6028/jres.045.026`. Its section VII gives the symmetric minimized-iteration recurrence and its
orthogonality discussion; section XIV summarizes a wider procedure. It does not supply a numbered
theorem identical to the catalog gloss, and the catalog does not identify a section, formula,
matrix domain, recurrence, starting-vector premise, breakdown convention, invariant, output, or
accuracy claim. The observed official PDF is a mutable external lead and is not admitted as H0.

This intake therefore freezes the ambiguity rather than inventing a theorem. The provisional root
vector is `[H5, M4, R4]`. `H5` classifies the catalog wording as not yet a stable proposition; it
does not refute standard exact-arithmetic Lanczos results. `M4` records that no source-identical
formal target is usable, while `R4` records that no proof reconstruction can attach to an
unidentified root. Ordinary statement and proof execution remain blocked until an independently
reviewed source correction selects one exact proposition.

Pinned mathlib provides Hermitian-matrix spectral results and general Gram-Schmidt interfaces.
`IntakeProbe.lean` authenticates selected adjacent APIs, but none states a Lanczos recurrence,
Krylov-subspace invariant, tridiagonalization result, Ritz-value guarantee, or finite-precision
claim. All six dependent phases remain open in `task-dag.json`. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
