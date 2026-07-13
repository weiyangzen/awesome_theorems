# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1985-1990` supplies exactly the title "open mapping theorem,"
Stefan Banach, 1929, the gloss "a surjective bounded linear operator is an open map," high
importance, and `已验证` ("verified"). The identical record at lines 2260-2265 is removed by the
target generator's exact-field deduplication. All twelve lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Neither copy has a work citation, edition, theorem
or page, definitions, exact assumptions, proof boundary, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:7630-7655` repeats the gloss while leaving precise premises, proof route,
dependencies, equivalent formulations, axioms, machine status, and artifact links open. The
rev-5.6 target manifest retains `已验证` only as `source_status_untrusted` and resets this theorem to
`L0 / rework_required`.

## Source lead and H boundary

Liran Rotem's Technion Winter 2020 functional-analysis lectures, typed by Elad Tzorani, were
inspected at immutable repository commit `6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc`. The notes fix
their normed spaces over `ℝ` or `ℂ`; define an open map as one sending every open set to an open
set; and state Theorem 2.2.11 (PDF page 29, TeX lines 1133-1198): if `X,Y` are Banach spaces and
`T` is an onto bounded linear operator, then `T` is open. The following proof intends to use Baire
category, rescaling, and a convergent series of approximate preimages. However, TeX line 1152
prints `⋃ n, T(B_X(0,1))`, repeating the unit ball, and lines 1154-1156 likewise refer to its
closure. The later rescaling step at lines 1165-1169 uses `B(0,n)`, showing that the intended
standard cover is `⋃ n, T(B_X(0,n))`. As printed, the displayed Baire inference is invalid; the
obvious repair is not accepted silently at intake.

This is a versioned, exact-topic modern statement and recognizable proof-route lead, not an
accepted complete proof source. It is not H0: the printed Baire-cover typo needs a source correction
or independently reviewed repair; the catalog does not cite the notes; the notation `L(X,Y)` and
its incorporated boundedness convention need a reviewed definition chain; catalog attribution/year
are not mapped to a primary historical source; and the real/complex textbook form has not been
transported to the more general pinned Lean interface. Because the only inspected proof source has
a known printed gap and no accepted repair, the provisional human status is H2.

## Crosswalk

| Repository/source phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "bounded linear operator" | an everywhere-defined continuous linear operator | `f : E ->L[𝕜] F`, or a linear map plus a checked continuity/boundedness bridge | exact encoding open |
| implicit scalar field | source lead uses real or complex scalars | `𝕜 = ℝ` or `𝕜 = ℂ`; a general `NontriviallyNormedField` form is broader | root field open |
| "Banach spaces" | both normed spaces are complete | `NormedAddCommGroup`, `NormedSpace`, and `CompleteSpace` on both `E` and `F` | omitted by catalog; source lead supplies it |
| "surjective" / "onto" | every codomain point has a preimage | `Function.Surjective f` or checked `range f = ⊤` | encoding open |
| "open map" | every open domain set has open image | `IsOpenMap f` | direct prospective match; exact expression unfrozen |
| semilinear generalization | compatible scalar-field equivalence | `f : E ->SL[sigma] F` plus inverse/isometry instances | pinned generalization, not selected root |
| `已验证` | untrusted inventory label | no proposition or proof object | rejected as evidence |

The central source-to-Lean gap is not whether an exact-topic theorem exists. It is whether the
accepted root should be the real/complex same-field textbook statement or mathlib's semilinear
generalization, and how the source's bounded-operator and open-map definitions transport to the
chosen encoding without broadening or narrowing the claim.

## Pinned formal candidates

The pinned module `Mathlib.Analysis.Normed.Operator.Banach` contains:

- `ContinuousLinearMap.isOpenMap`: the direct surjective-to-open theorem.
- `ContinuousLinearMap.exists_approx_preimage_norm_le`: Baire-category approximation step.
- `ContinuousLinearMap.exists_preimage_norm_le`: controlled exact-preimage step.
- `ContinuousLinearMap.isQuotientMap`: a surjective continuous open-map corollary.
- `LinearEquiv.continuous_symm`: the bijective bounded-inverse consequence.

`IntakeProbe.lean` authenticates these pinned APIs and representative axiom reports. They remain
M3 candidates. Exact source identity, minimal imports, elaborated expression and environment
fingerprints, checked same-field/semilinear transport, terminal-body provenance, placeholder and
trust closure, and integration acceptance belong to downstream phases. No proof body is credited
by this dossier.

## Required downstream decision

The statement phase must admit and independently review a precise source formulation, fix the
scalar and completeness boundary, and elaborate that exact proposition. It must not silently use
the broader semilinear theorem, the narrower bijective inverse result, or an incomplete-space
variant. The anchor audit can then determine whether a checked specialization or wrapper around
the pinned declaration closes the accepted target.
