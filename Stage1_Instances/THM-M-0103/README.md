# THM-M-0103 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`豪斯多夫-杨定理` (Hausdorff-Young theorem). The repository supplies only the gloss
`傅里叶变换的范数不等式` (a norm inequality for the Fourier transform), attribution to Felix
Hausdorff and William Young, the year 1923, and an untrusted `已验证` label. It does not supply a
binder-complete proposition.

## Intake result

The title points to the Hausdorff-Young family, but it does not decide among Fourier series on the
circle, the Euclidean Fourier transform, or a locally compact abelian or finite-group formulation.
It also omits the Haar measures and Fourier normalization, exponent and conjugate-exponent
conventions, scalar codomain, function-space completion, endpoint treatment, and norm constant.
Those choices change the proposition, so this intake does not invent them.

The catalog separately assigns `THM-M-0295` to `豪斯多夫-杨不等式` with the more specific gloss
`傅里叶变换的L^p估计`. It is a distinct Stage1 target and is not authority to broaden, merge, or
silently substitute this target. The likely semantic duplication must be adjudicated before an
exact source statement is selected.

## Source and formal boundary

Bibliographic metadata identifies Hausdorff's 1923 paper *Eine Ausdehnung des Parsevalschen Satzes
uber Fourierreihen* and Young's 1913 paper *On the Determination of the Summability of a Function by
Means of its Fourier Constants* as primary-source leads. Neither full source has been admitted or
crosswalked to an exact repository claim, and no correction, translation, or independent source
review is complete. They therefore support only a provisional `H1` classification.

`IntakeProbe.lean` checks pinned Fourier-transform endpoint APIs: an `L1` transform/norm bound and
the `L2` Plancherel isometry. A bounded lexical search found no named Hausdorff-Young or
Riesz-Thorin declaration at the pinned mathlib revision. Endpoint infrastructure does not prove an
unselected intermediate-exponent theorem, and the search is not an exhaustive anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H1, M4, R4]`. All six downstream tasks remain open. No exact statement, H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
