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
accepted complete proof source. Its standing convention at TeX line 36 restricts the scalar field
to `Real` or `Complex`; its Banach-space definition at line 52 incorporates completeness; its
bounded-operator notation is introduced before the theorem; and its open-map definition is
immediately adjacent. Those passages now select the exact statement proposal. It is still not H0:
the printed Baire-cover typo needs a source correction or independently reviewed repair; the
catalog does not cite the notes; the full notation chain lacks independent review; catalog
attribution/year are not mapped to a primary historical source; and the general pinned theorem has
not been transported to the selected closed real-and-complex root. The provisional human status
therefore remains H2.

## Crosswalk

| Repository/source phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "bounded linear operator" | an everywhere-defined continuous linear operator | ordinary same-field `f : E ->L[Real] F` and `f : E ->L[Complex] F` | frozen bundled encoding |
| implicit scalar field | standing convention uses real or complex scalars | closed conjunction of the `Real` and `Complex` cases | frozen without open-class broadening |
| "Banach spaces" | both normed spaces are complete | `NormedAddCommGroup`, `NormedSpace`, and `CompleteSpace` on both `E` and `F` | frozen from source definition chain |
| "surjective" / "onto" | every codomain point has a preimage | `Function.Surjective f` | frozen encoding |
| "open map" | every open domain set has open image | `IsOpenMap f` | frozen with checked definitional expansion |
| semilinear generalization | compatible scalar-field equivalence | `f : E ->SL[sigma] F` plus inverse/isometry instances | pinned generalization, not selected root |
| `已验证` | untrusted inventory label | no proposition or proof object | rejected as evidence |

The source-to-Lean statement gap is now closed provisionally by
`Stage1Instances.THM_M_0276.BanachOpenMappingTarget`. The remaining formal gap is downstream: a
checked specialization of the stronger semilinear theorem, terminal-body provenance, and trust
closure have not been audited or credited.

## Pinned formal candidates

The pinned module `Mathlib.Analysis.Normed.Operator.Banach` contains:

- `ContinuousLinearMap.isOpenMap`: the direct surjective-to-open theorem.
- `ContinuousLinearMap.exists_approx_preimage_norm_le`: Baire-category approximation step.
- `ContinuousLinearMap.exists_preimage_norm_le`: controlled exact-preimage step.
- `ContinuousLinearMap.isQuotientMap`: a surjective continuous open-map corollary.
- `LinearEquiv.continuous_symm`: the bijective bounded-inverse consequence.

`IntakeProbe.lean` authenticates these pinned APIs and representative axiom reports. They remain
M3 candidates. `Statement.lean` separately records the exact source-selected root with the single
direct import `Mathlib.Analysis.Complex.Basic`, its elaborated expression and environment
fingerprints, an expanded-open-map transport, and structural mutations. The same-field/semilinear
proof transport, terminal-body provenance, placeholder and trust closure, and integration
acceptance remain downstream. No proof body is credited by this dossier.

## Required downstream decision

The integration lane must re-elaborate and decide whether to accept the provisional statement
receipt. Independent source work must resolve the printed proof gap and primary-history mapping
before H0. The anchor audit can then determine whether checked Real and Complex specializations or
another exact wrapper around the pinned semilinear declaration close the accepted target. It must
not substitute the broader semilinear theorem, the narrower bijective inverse result, or an
incomplete-space variant for the frozen root.
