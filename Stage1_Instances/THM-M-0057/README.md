# THM-M-0057 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Hoffman-Wielandt theorem. The
repository supplies only the gloss `正规矩阵特征值的扰动` ("perturbation of the eigenvalues of
normal matrices"), attributes it to A. J. Hoffman and H. W. Wielandt in 1953, and labels it
`已验证`. Under rev-5.6 those fields are untrusted inventory metadata, not a source audit, exact
Lean proposition, or proof receipt.

The gloss identifies the classical finite complex normal-matrix perturbation family, but it does
not state the inequality. It does not fix the matrix size and index type, define normality, choose
eigenvalue enumerations with algebraic multiplicity, quantify the matching permutation, define the
Frobenius norm, select the norm or squared form, or settle the zero-dimensional case. Intake does
not silently supply those proposition-changing clauses.

The original paper was identified bibliographically as A. J. Hoffman and H. W. Wielandt, "The
variation of the spectrum of a normal matrix," *Duke Mathematical Journal* 20(1) (1953), 37-39,
DOI `10.1215/S0012-7094-53-02004-3`. Its full text was not available for inspection in this worker
environment. A later paper by Xuefeng Xu and Chen-Song Zhang, arXiv `1612.05759v2`, was inspected.
Its abstract and introduction explicitly state the familiar inequality for two normal complex
matrices and cite the original paper, but it is a secondary source and does not establish the
catalog-to-primary-source crosswalk or `H0`.

Pinned mathlib supplies `IsStarNormal`, Frobenius matrix norms, matrix spectrum/eigenspace APIs,
and a fully indexed eigenvalue function plus spectral theorem for Hermitian matrices.
`IntakeProbe.lean` authenticates representative declarations. A bounded exact-topic search found
no Hoffman-Wielandt declaration or general-normal-matrix eigenvalue matching theorem. Hermitian
spectral infrastructure is a specialization and possible ingredient, not the requested normal
matrix result.

The provisional theorem-family assessment is `[H1, M4, R4]`: a classical published theorem and a
precise secondary source lead are known, but the primary statement and catalog mapping are not
accepted; no usable exact formal artifact is credited; and no source-faithful reconstruction is
available. `instance.json` is the structured scope authority and `task-dag.json` keeps all six
downstream phases open. No exact target, H0, M0, R0, accepted state, audit completion, theorem
completion, or master acceptance is claimed.
