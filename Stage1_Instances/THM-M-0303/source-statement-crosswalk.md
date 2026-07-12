# Source-statement crosswalk

## Repository record and provenance

The retained source record is `Docs/researches/math_theorems.md:2174-2179`, in Analysis / Real
Analysis. It supplies exactly:

- title `索伯列夫嵌入定理`;
- proposer Sergei Sobolev;
- year 1936;
- gloss `Sobolev空间到连续函数空间的嵌入`;
- importance "high"; and
- formalization status `已验证`.

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. No citation, edition, theorem/page, definitions,
assumptions, proof, errata record, or formal artifact accompanies them. Stage0 repeats the gloss at
`Docs/Stage0_Blueprint.md:8359-8384` while explicitly leaving exact definitions and premises,
equivalent forms, axioms, proof path, and existing machine artifacts as `待补充` (to be supplied).

The source inventory also contains a byte-identical Chinese entry at lines 2393-2398. Repository
generation deduplicates that exact signature and retains the earlier Real Analysis entry. A third
record at lines 9038-9043 differs only in its mixed English/Chinese title, survives as the distinct
target `THM-M-1237`, and has no authority over this target. This provenance explains the identity
collision; it does not resolve it.

## Statement-component crosswalk

| Repository component | Required mathematical source detail | Required Lean component | Intake disposition |
|---|---|---|---|
| "Sobolev space" | exact `W^{k,p}`, homogeneous/inhomogeneous or fractional definition; domain, measure, values, derivative notion, quotient convention | concrete Sobolev membership and almost-everywhere representation | unresolved |
| "embedding" | continuous linear inclusion, set inclusion, existence of representative, quantitative estimate, or a bundle of these | exact map or proposition and norm inequality | unresolved |
| "continuous-function space" | `C^0`, bounded continuous, continuous on the closure, or Holder space; target norm/topology | `Continuous`, `ContinuousOn`, boundedness, or `HolderOnWith` with exact domain | unresolved |
| omitted parameter condition | relation among order, exponent, and dimension; endpoint policy | ordered binders and explicit inequalities | blocking |
| omitted domain condition | whole space, bounded Lipschitz/extension domain, manifold, or local chart | domain structure and extension/restriction hypotheses | blocking |
| omitted representative clause | existence, almost-everywhere agreement, uniqueness, boundary values | quotient-to-function bridge | blocking |
| `已验证` | no cited human or machine evidence | no declaration or proof credit | explicitly rejected |

## Human-source candidates

The separate `THM-M-1237` dossier names L. C. Evans, *Partial Differential Equations*, second
edition (AMS, 2010), Section 5.6.3, Theorem 6 and its subsequent Sobolev consequence, and R. A.
Adams and J. J. F. Fournier, *Sobolev Spaces*, second edition (Academic Press, 2003), as discovery
leads for a supercritical bounded-domain formulation. They were not inspected from an immutable
edition for this target. The catalog cites neither work and does not select that formulation.

Before ordinary theorem execution or `H0`, an accountable reviewer must select a stable primary or authoritative edition and an
exact theorem/page/formula, capture its definitions and complete assumptions, check corrections or
errata, map every statement clause and proof boundary to this target, reconcile the duplicate
catalog identities, and obtain independent review. The current catalog-target classification is
`H5`, not `H0`: the received wording is not a stable proposition to which human proof debt can yet
attach. This does not classify any corrected, source-selected Sobolev theorem as false or open.

## Lean discovery crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow probe checks:

| Pinned declaration | What it establishes | Why it is not the target |
|---|---|---|
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one` | a first-order GNS inequality for compactly supported `C^1` functions | no weak Sobolev class or continuous-representative conclusion |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq` | the equality-exponent `L^p` derivative estimate | subcritical norm control, not supercritical continuity |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le` | a bounded-support weakened-exponent estimate | still a smooth-function norm inequality |
| `MeasureTheory.eLpNorm_le_eLpNorm_fderiv` | the bounded-support base estimate | no source-selected Sobolev embedding or representative bridge |
| `HolderOnWith.continuousOn` | positive Holder control implies continuity on the same set | consumes Holder control; it does not produce it from Sobolev hypotheses |

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_175.lean` elaborates in the pinned environment and
contains wrappers around these anchors plus abstract statement interfaces. Its header identifies
`THM-M-1237`, and essential Sobolev, exponent, domain, representative, and estimate content remains
partly proposition-valued. It is discovery evidence only. There is no target-specific Lean file or
legacy slot for `THM-M-0303`.

## First blocker and retry condition

The first failed downstream gate is exact source-statement identity. A statement worker must receive
an approved source and duplicate-target decision fixing every domain, order, exponent, regularity,
representative, target-space, estimate, and boundary choice above. Only then can it author the exact
Lean expression, minimize imports, serialize its elaborated expression and environment fingerprint,
check alternate encodings, and mutation-test hypotheses, domains, binder scope, and boundary cases.

Until then, the formal target stays null and machine debt stays `M4`. No source acceptance,
statement acceptance, proof, audit completion, or theorem completion is claimed.
