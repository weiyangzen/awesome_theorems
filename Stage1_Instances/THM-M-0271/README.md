# THM-M-0271 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Fubini's theorem. The repository
attributes the result to Guido Fubini in 1907 and supplies only the gloss `重积分与累次积分的关系`
("the relationship between multiple and iterated integrals"). Its `已验证` label is untrusted
metadata under rev-5.6, not an exact source statement, a source audit, or proof evidence.

The gloss identifies a classical theorem family but omits proposition-changing choices. It does
not select Lebesgue, Bochner, or Riemann integration; scalar or Banach-valued functions; the
measure spaces and finiteness hypotheses; product-versus-iterated equality or order exchange;
integrability and measurability assumptions; almost-everywhere section claims; or boundary cases.
Choosing one familiar formulation at intake would silently narrow or broaden the received claim.

The zbMATH Open record for JFM `38.0343.02` identifies Guido Fubini's 1907 paper *Sugli integrali
multipli*, pages 608-614, and preserves a contemporary German review of a planar scalar Lebesgue
formulation. The primary paper itself was not inspected, and the review is not a complete primary
proof source or independent source-to-target audit. It is therefore a strong historical source
lead supporting `H1`, not `H0` evidence.

Pinned mathlib contains strong formal candidates in `Mathlib.MeasureTheory.Integral.Prod`.
`IntakeProbe.lean` authenticates product-integral, both iterated-integral orders, order-swap, and
section-integrability interfaces plus representative axiom reports. The actual types are abstract
Bochner statements over s-finite measures and include a non-complete-codomain convention that must
not be silently identified with the historical scalar theorem. No candidate receives proof credit
before an approved source statement and checked transport are frozen.

The provisional root vector is `[H1, M3, R4]`: a historically proved family and strong source lead
are known; pinned formal statement/proof candidates exist; but exact source identity, canonical
statement, source-to-Lean transport, and source-faithful readable reconstruction remain open.
`instance.json` is the structured scope authority, and `task-dag.json` keeps all six downstream
phases open. No H0, M0, R0, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
