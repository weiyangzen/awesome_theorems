# THM-M-0294 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item
`普朗歇尔定理` (Plancherel theorem). The repository gives Michel Plancherel, the year 1910, the
gloss `L^2函数的傅里叶变换等距性` (isometry of the Fourier transform for `L^2` functions), and
an untrusted `已验证` label. It does not give a binder-complete proposition or proof evidence.

## Intake result

The gloss identifies the classical Plancherel family but leaves proposition-changing choices open:
the spatial domain, scalar or Hilbert-valued codomain, Fourier kernel and sign, `2 * pi` and measure
normalizations, the carrier for almost-everywhere classes, and whether the root asserts only norm
preservation or also inner-product preservation, inversion, or surjectivity.

The corpus separately assigns `THM-M-0342` to another Plancherel record, under harmonic analysis,
with the nearly identical gloss `L^2傅里叶变换的等距性`. That sibling has substantial provisional
Lean artifacts, but it remains a distinct rev-5.6 target. This worker does not merge the records,
transfer receipts, or use the sibling statement as authority for this real-analysis target.

## Source and formal boundary

The catalog attribution and Crossref record point to the 1910 article *Contribution a l'etude de la
representation d'une fonction arbitraire par des integrales definies*, Rendiconti del Circolo
Matematico di Palermo 30, pages 289-335, DOI `10.1007/BF03014877`, as a strong primary-work lead.
Crossref also anomalously lists Mittag Leffler as an additional author. The article text, definitive
authorship, and exact theorem passage were not admitted or independently reviewed, so this is `H1`
discovery rather than `H0` evidence.

Pinned mathlib directly exposes `MeasureTheory.Lp.fourierTransformₗᵢ`,
`MeasureTheory.Lp.norm_fourier_eq`, and `MeasureTheory.Lp.inner_fourier_eq` for finite-dimensional
real inner-product domains and complex Hilbert codomains. `IntakeProbe.lean` checks these interfaces
and a scalar Euclidean specialization. They are strong exact-topic candidates, not a frozen target,
source transport, or accepted proof for `THM-M-0294`.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M3, R4]`: a published primary-work lead is known but the exact source mapping is
open; direct pinned statement/proof interfaces and a sibling formalization exist but no exact root
is selected; and no accepted source-faithful readable proof is available. `instance.json` is the
scope authority, and `task-dag.json` keeps all six downstream phases open. No H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
