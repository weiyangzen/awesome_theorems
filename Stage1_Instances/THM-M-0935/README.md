# THM-M-0935 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
Dias da Silva-Hamidoune theorem. The repository supplies the authors, the year 1994, and only the
gloss `Erdős-Heilbronn猜想的证明` ("proof of the Erdos-Heilbronn conjecture"). Its nearby
`已验证` label is expressly untrusted inventory metadata, not an exact source statement, Lean
declaration, or proof receipt.

## Intake result

The bibliographic identity is strong: J. A. Dias da Silva and Y. O. Hamidoune, *Cyclic Spaces for
Grassmann Derivatives and Additive Theory*, *Bulletin of the London Mathematical Society* 26(2)
(1994), 140-146, DOI `10.1112/blms/26.2.140`. Crossref confirms the metadata, but the primary
article text was access-blocked and was not admitted or inspected theorem by theorem. The zbMATH
Open record includes a source-close summary of the general `m`-subset result, but not the paper's
internal theorem locator or its full premise and proof context.

Accessible scholarly sources expose an important scope fork. Balandraud's Theorem 2 and
Feher-Nagy's Theorem 3.1 call the general restricted `h`-fold sumset bound the Dias da
Silva-Hamidoune theorem:

`|h^A| >= min(p, h * (|A| - h) + 1)` for `A` in `F_p` and `0 <= h <= |A|` (or, in another source,
`1 <= h <= |A|`). The `h = 2` specialization is the classical Erdos-Heilbronn self-sumset bound
`|A dot+ A| >= min(p, 2 * |A| - 3)`. Other literature uses the theorem name for that specialization.
The catalog's proof gloss does not decide whether this target owns the general theorem, only the
conjecture-specializing case, or a checked relationship between them. Intake therefore records the
family and scope fork but does not invent a canonical root.

## Formal boundary

Pinned mathlib has `ZMod p`, `Finset.powersetCard`, finite sums, `Finset.subsetSum`, and ordinary
`ZMod.cauchy_davenport`. `IntakeProbe.lean` checks those adjacent APIs only. A bounded name and
statement search found no Dias da Silva-Hamidoune, Erdos-Heilbronn, or restricted fixed-cardinality
sumset theorem. Ordinary Cauchy-Davenport permits repeated/equal summands from two sets and cannot
replace the pairwise-distinct restricted theorem.

The provisional vector is `[H1, M4, R4]`: a published primary-paper identity and precise secondary
statement leads are known, but the exact primary theorem locator, parameter endpoints, incorporated
definitions, proof and errata boundary, catalog-to-source choice, and independent review remain
open; no usable exact formal artifact is located; and no readable proof reconstruction is admitted.
All six downstream phases remain open. No canonical statement, H0, M0, R0, accepted state, audit
completion, theorem completion, accepted receipt, or master acceptance is claimed.
