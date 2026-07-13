# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10749-10754` supplies exactly:

- title: `CFL条件`;
- attribution and date: Courant/Friedrichs/Lewy, 1928;
- claim gloss: `双曲型方程的稳定性条件`;
- importance: high; and
- formal status: `已验证`.

All six lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.
They contain no bibliography, equation, definition, theorem locator, assumptions, conclusion, proof,
errata, reviewer, or formal declaration. `Docs/Stage0_Blueprint.md:40054-40079` repeats the gloss and
explicitly leaves exact definitions and premises, proof path, dependencies, equivalent forms,
axioms, machine status, and artifact links open.

## Primary-source family lead

R. Courant, K. Friedrichs, and H. Lewy, "Über die partiellen Differenzengleichungen der
mathematischen Physik," *Mathematische Annalen* 100(1) (1928), 32-74,
DOI `10.1007/BF01448839`. The inspected Göttingen digitization is PURL
`http://resolver.sub.uni-goettingen.de/purl?GDZPPN002272636`, work
`PPN235181684_0100`, range `LOG_0005`, 44 scan pages, SHA-256
`2aee594c9a7c3eef1ab28fee1e44333e0e29c621ba60f049d63de107aeb2a30f`.

This is a strong historical match, but it is not admitted as `H0`: the catalog never cites or
selects one result from it, the paper has multiple hyperbolic claims, a complete premise/proof
crosswalk and correction/errata audit are absent, and no independent source or translation review
has occurred.

## Crosswalk matrix

| Received or candidate content | Source locus | Future formal surface | Intake state |
|---|---|---|---|
| Courant/Friedrichs/Lewy, 1928 | article title page, printed p. 32 | provenance metadata only | matching source family, no theorem identity |
| Hyperbolic convergence depends on mesh-ratio inequalities determined by characteristics | introduction, printed p. 33 | ordered parameters and characteristic/grid relation | pinpointed lead, exact proposition open |
| Numerical and differential equations have distinct dependence regions | Part II, section 2, printed p. 61 | definitions of both domains of dependence | definition mapping open |
| Convergence generally fails when the discrete dependence region is too narrow | Part II, section 2, printed p. 61 | quantified necessity/nonconvergence conclusion | candidate root, not selected |
| Convergence holds in the other wave-grid regime under source-specific data hypotheses | Part II, section 3, printed pp. 62-65 | a separate sufficient convergence theorem | candidate root, not selected |
| `双曲型方程的稳定性条件` | repository gloss only | no faithful exact `Prop` yet | ambiguous and potentially misleading |
| Catalog `已验证` | repository metadata only | none | untrusted; no H/M credit |

The historical paper discusses convergence and dependence geometry. Turning that into a modern
generic "stability condition" would require an explicit, reviewed transport rather than a wording
shortcut. Necessity, sufficiency, stability, and convergence must remain distinct.

## Formal-source boundary

A bounded case-insensitive search of tracked Lean and pinned mathlib found no declaration matching
Courant-Friedrichs-Lewy, CFL, numerical domain of dependence, or a hyperbolic finite-difference CFL
condition. The pinned modules `Mathlib.Algebra.Group.ForwardDiff` and
`Mathlib.Analysis.InnerProductSpace.LaxMilgram` provide finite-difference algebra and an abstract
coercivity/stability-adjacent result. They contain no source-selected PDE scheme or CFL theorem.
`IntakeProbe.lean` authenticates the named APIs only; no anchor-audit completeness or absence claim
is made.

## Gate result

The source-statement identity gate remains open. Retry requires an accountable decision selecting
one immutable proposition (or an explicitly sourced conjunction), full mapping of definitions,
ordered assumptions and conclusion, corrections/errata and translation review, and independent
approval. Only then may the statement phase encode the exact target and test transports and
mutations.
