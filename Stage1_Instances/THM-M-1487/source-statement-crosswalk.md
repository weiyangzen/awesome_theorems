# THM-M-1487 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10868-10873` supplies exactly the title `卷积神经网络`, the
attribution `Yann LeCun`, the year `1989`, the gloss `图像处理的神经网络`, importance "high," and
status `已验证`. Git provenance places all six uncited lines in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, architecture,
equation, theorem, binder, hypothesis, conclusion, proof, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:40432-40457` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof or observation, dependency graph,
alternate statements, axiom policy, machine status, and artifact links open. Its generic
closed-result and leaf-audit wording is planning metadata, not evidence. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| convolutional | weight sharing over translated local receptive fields, discrete convolution, or cross-correlation | indexed kernel, spatial action, padding/stride convention, and layer map | no convention supplied |
| neural network | a parameterized composition of affine/local operators and activations | architecture, shapes, parameters, activation, and composition | no network selected |
| image processing | classification, recognition, segmentation, filtering, or feature extraction | input/output types, task semantics, labels, transformations, and loss | no task or image model supplied |
| Yann LeCun / 1989 | historical attribution | immutable source edition and pinpoint proposition | no source locator supplied |
| `已验证` | untrusted screening label | accepted source or kernel receipt would be required | no H or M credit |

The gloss cannot populate a canonical domain, ordered binders, hypotheses, conclusion, alternate
encodings, excluded cases, or Lean expression fingerprint.

## Historical source lead, not an admitted theorem source

Crossref metadata was inspected on 2026-07-13 for DOI
`10.1162/neco.1989.1.4.541`: Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. E. Howard,
W. Hubbard, and L. D. Jackel, "Backpropagation Applied to Handwritten Zip Code Recognition,"
*Neural Computation* 1(4), December 1989, pages 541-551, MIT Press.

The metadata matches the catalog author, year, and image-processing theme, but the catalog does
not cite this article and compresses its seven authors to one attribution. An author-hosted
11-page scan was retrieved with SHA-256
`378c00b2b3e2f461b79848ef88f671eefdf1dcfde28ad945d15751bccc91fff1`. Page 541 frames task
constraints and recognition success; pages 542-544, sections 3.1-3.3, describe a `16 x 16` input,
ten outputs, local receptive fields, shared weights, `5 x 5` kernels, and feature maps as nonlinear
subsampled convolutions; pages 546-550 report architecture and trained-network measurements and
conclusions. These are source-family and empirical-boundary observations, not a source-selected
mathematical theorem or proof. No exact proposition, complete incorporated-definition and
assumption map, analytical proof boundary, corrections, or independent review was credited. The
lead is discovery evidence and establishes neither a canonical statement nor `H0`.

## Neighbor boundary

The catalog separately schedules neural networks (`THM-M-1484`), backpropagation
(`THM-M-1485`), deep learning (`THM-M-1486`), recurrent neural networks (`THM-M-1488`), and
Transformers (`THM-M-1489`). Those records confirm that this generic image-network gloss must not
be silently widened to all neural networks or narrowed to backpropagation, recurrence, attention,
or an arbitrary deep architecture. No neighbor's evidence is inherited.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Data.Holor`
provides multidimensional indexed arrays, slices, tensor products, and CP-rank facts;
`Mathlib.Data.Matrix.Mul` provides finite dot products and matrix-vector operations; and
`Mathlib.Analysis.SpecialFunctions.Sigmoid` provides one scalar activation and analytic facts.
`IntakeProbe.lean` checks representative declarations in the pinned environment.

These APIs do not define a CNN architecture, discrete image convolution/cross-correlation layer,
training or prediction semantics, or target conclusion. Mathlib's analytic function convolution
is likewise not a CNN model. A bounded exact-topic search over repo-local Lean and pinned mathlib
found no convolutional-neural-network terminal declaration; the only neural-network wording was a
comment describing holor terminology. This is intake discovery, not an exhaustive external anchor
audit, global absence claim, or proof evidence.

## Source exit gate

Before leaving `H5`, accountable reviewers must redirect the model-family label to one corrected,
truth-valued proposition; preserve an immutable primary or approved authoritative edition; select
an exact definition/theorem/section/page and analytical rather than empirical proof boundary; map
every architecture component, convolution convention, domain, ordered binder, hypothesis,
constant, conclusion, and boundary case; reconcile neighboring targets; audit corrections; and
obtain independent machine-learning, source, and statement review.

Only then may the statement phase freeze minimal imports, elaborate and preserve the identical
Lean expression and environment fingerprint, compile checked transports, and mutation-test a
removed hypothesis, changed domain, changed binder scope, and boundary case. Until then no exact
statement, H0, M0, R0, proof, audit completion, or theorem completion is claimed.
