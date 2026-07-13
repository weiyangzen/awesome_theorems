# THM-M-0295 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`豪斯多夫-杨不等式` (Hausdorff-Young inequality). The repository supplies only the gloss
`傅里叶变换的L^p估计` (an `L^p` estimate for the Fourier transform), attribution to Felix
Hausdorff and William Young, the year 1923, and an untrusted `已验证` label. It does not supply a
binder-complete proposition.

## Intake result

The title identifies the Hausdorff-Young family but does not decide among Fourier series on the
circle, a Euclidean Fourier transform, or a finite-, compact-, discrete-, or locally compact
abelian-group formulation. It also omits both measures, Fourier normalization, scalar codomain,
input and conjugate exponents, function-space construction, endpoint treatment, and the inequality
constant. These choices change the proposition, so this intake does not invent them.

The catalog separately assigns `THM-M-0103` to `豪斯多夫-杨定理` with the gloss
`傅里叶变换的范数不等式`. It is a distinct Stage1 target and is not authority to broaden, merge,
or silently substitute this target. The likely semantic duplication requires integration-lane
adjudication before either record can select a canonical source statement.

## Source and formal boundary

Bibliographic metadata identifies Hausdorff's 1923 paper *Eine Ausdehnung des Parsevalschen Satzes
uber Fourierreihen* and Young's 1913 paper *On the Determination of the Summability of a Function by
Means of its Fourier Constants* as primary-source leads. Neither full source has been admitted or
crosswalked to the repository gloss; no exact result locator, correction search, translation
decision, or independent source review is complete. They support only a provisional `H1` state.

`IntakeProbe.lean` checks pinned Fourier endpoint APIs: an `L1` transform/norm bound and the `L2`
Plancherel isometry. A bounded lexical search found no named Hausdorff-Young or Riesz-Thorin
declaration at the pinned mathlib revision. Endpoint infrastructure does not prove an unselected
intermediate-exponent result, and this intake search is not an exhaustive anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional root vector
is `[H1, M4, R4]`; all six downstream tasks remain open. No exact statement, H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
