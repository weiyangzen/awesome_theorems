# THM-M-0235 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the complex-analytic open mapping
theorem. The repository supplies only the gloss "nonconstant holomorphic functions are open
maps," attributes it to many mathematicians in the nineteenth century, and labels it `已验证`
("verified"). Under rev-5.6 that label is untrusted inventory metadata, not a source audit, an
exact Lean proposition, or proof evidence.

The gloss identifies a classical theorem family, but it omits proposition-changing choices. It
does not fix the complex domain, say whether "domain" includes nonemptiness, openness, and
connectedness, define nonconstancy on that domain, or distinguish an open map from the restricted
claim that open subsets of the domain have open images in the complex plane. The whole-plane
entire-function form is a specialization, not a neutral interpretation of the received claim.

Pinned mathlib contains direct open-mapping declarations in
`Mathlib.Analysis.Complex.OpenMapping`. In particular,
`AnalyticOnNhd.is_constant_or_isOpen` gives the constant-or-open alternative on a preconnected
set, while `AnalyticOnNhd.is_constant_or_isOpenMap` gives the whole-domain version. The local
`AnalyticAt.eventually_constant_or_nhds_le_map_nhds` is an ingredient, not the global theorem.
`IntakeProbe.lean` authenticates these interfaces and representative axiom reports only. No
candidate is transported to an exact source-selected root at intake.

Jiří Lebl's author-published *Guide to Cultivating Complex Analysis*, version 1.9, was inspected as
an authoritative modern source lead at its immutable Git tag. Definition 1.1 defines a domain as
an open connected subset of `ℂ`, and Theorem 5.5.1 states the matching domain-relative open
mapping theorem with a complete proof. The catalog does not cite this source, its optional
nonemptiness convention and function-on-subtype presentation still require an approved Lean
crosswalk, and no independent source review is recorded. It therefore supports H1, not H0.

The provisional vector is `[H1, M3, R4]`: the historically proved theorem family is identifiable,
and a complete named source lead is pinned, but catalog-source identity, complete assumption
crosswalk, corrections/errata disposition, and independent review remain open; usable exact-topic
pinned interfaces exist, but the canonical statement and checked transport are not frozen; and no
source-faithful proof reconstruction exists for an exact root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the unresolved statement and source boundary, and
`task-dag.json` keeps all six downstream phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
