# THM-M-0299 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the singular-integral boundedness
theorem. The repository supplies only the gloss `奇异积分的L^p有界性` ("`L^p` boundedness of
singular integrals"), attributes it to Alberto Calderon and Antoni Zygmund in 1952, and labels it
verified. Under rev-5.6 that label is untrusted inventory metadata, not an exact source statement or
proof evidence.

The title identifies a classical theorem family, but the gloss does not select a convolution or
general Calderon-Zygmund operator, the ambient space, kernel hypotheses, principal-value or
truncation convention, initial domain, exponent range, endpoint policy, or the form and constant of
the conclusion. Each choice changes the proposition. Intake therefore records familiar strong-type
formulations only as search leads and does not silently promote one to the canonical target.

Crossref metadata for Calderon and Zygmund's 1952 paper *On the existence of certain singular
integrals*, DOI `10.1007/BF02392130`, was inspected. It identifies *Acta Mathematica* 88 (1952),
pages 85-139, and is a strong bibliographic lead matching the catalog attribution and date. The
article text was not retrievable in this worker environment, no exact theorem or proof passage was
inspected, and source-to-claim mapping, corrections, and independent review remain open. This
supports provisional `H1`, not `H0`.

Pinned mathlib provides generic measure, Bochner integration, `MemLp`, `Lp`, and continuous-linear-
map interfaces. A bounded exact-topic search found no named singular-integral, Calderon-Zygmund,
Hilbert-transform, Riesz-transform, or maximal-truncation declaration. `IntakeProbe.lean`
authenticates only adjacent generic APIs; it does not define an operator, select a target, or prove
boundedness.

The provisional vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical statement, H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
