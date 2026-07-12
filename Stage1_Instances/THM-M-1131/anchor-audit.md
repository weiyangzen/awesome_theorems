# Anchor audit record

Item: `S56-M-1131-ANCHOR_AUDIT`  
Base revision: `451cecc55d7bd202b72564a5fcbe6968711cb1ea`  
Audit date: 2026-07-12

## Decision

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies checked
Frechet-derivative identities for constant scalar multiplication and negation. These are relevant
to rewriting the divergence of `q = -conductivity * gradient T`. Its integral divergence theorem
is useful only for a different weak or boundary formulation. No declaration in the pinned source
scan states the frozen pointwise implication, so these anchors are proof-enabling substrate rather
than terminal closure.

The credible external PDE candidate `weiran-sun/pde` was inspected at immutable commit
`0b37f095c5ac3571084f5ea47f0435884452d86a`. Its
`Heat.heatKernel_solves_heat_eq` proves that one explicit one-dimensional heat kernel solves a
source-free heat equation. It has a real proof body, but it does not mention heat flux, Fourier's
constitutive law, or local energy balance and cannot be transported to the arbitrary-field target.
It also uses Lean 4.23.0-rc2 and mathlib `90c0e1...`, not this repository's pinned environment.
Importing it would therefore add compatibility work without closing any exact obligation.

The exact local artifact remains a proposition definition without a proof body. The root stays at
`M3 / formalization_debt`: no exact external closure was found, hence no repo-local integration debt
was created. Anonymous repository searches are bounded evidence only and do not prove that no Lean
formalization exists anywhere.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` using the
existing canonical `.lake` artifacts. No dependency update, build, clone, fetch, or installation
ran.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1131/AnchorAudit.lean` | 0 | six retained pinned declarations elaborated and printed |
| scoped `rg` over tracked Lean and pinned mathlib for Fourier/heat/conduction aliases | 0 | exact local statement plus adjacent heat-equation material; no exact terminal body |
| `git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a1783...a95`, tree `bdc39a...2b` |
| `sha256sum` on retained mathlib sources, license, local statement, and external immutable files | 0 | hashes recorded in `anchor-audit.json` |
| GitHub repository API searches for heat-equation and Fourier-conduction Lean projects | 0 | both returned `total_count=0`, `incomplete_results=false`; response hash recorded |
| immutable raw-source scan of `weiran-sun/pde` HeatKernel module | 0 | adjacent `Heat.heatKernel_solves_heat_eq`; no admission or axiom declaration in that module |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1131` | 0 | rank 336, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1131/anchor-audit.json` | 0 | structured audit artifact parsed |
| forbidden-term scan of `AnchorAudit.lean` | 1 | expected no-match exit; no proof gap declaration |
| `git diff --check -- Stage1_Instances/THM-M-1131 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This anchor-audit node is self-tested pending master acceptance. It audits mathlib and one credible
external Lean 4 PDE candidate at immutable revisions; it does not freeze the obligation registry,
prove the target, clear H1/R3, complete the full audit, or claim theorem completion.
