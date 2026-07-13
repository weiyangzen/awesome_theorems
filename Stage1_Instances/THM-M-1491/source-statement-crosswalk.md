# THM-M-1491 source-statement crosswalk

## Repository Record

`Docs/researches/math_theorems.md:10896-10901` is the complete catalog record. It supplies the
title `凸优化`, the collective attribution `众多数学家`, the period `20世纪`, the gloss
`凸函数的优化`, importance `高`, and status `已验证`. All six lines originate at repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That is repository provenance, not a
primary mathematical source.

The record contains no bibliography, objective, domain, feasible set, convexity definition,
quantifiers, hypotheses, conclusion, proof, correction history, or formal declaration.
`Docs/Stage0_Blueprint.md:40540-40565` repeats the gloss while explicitly leaving the formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Rev-5.6 consequently retains `已验证` only
as `source_status_untrusted`.

## Literal Crosswalk

| Catalog component | Missing mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `凸函数` | function domain/codomain, scalar field, convex domain, convex versus strict/strong convexity, total versus extended value | types, structures, `ConvexOn`/related predicate, objective function | absent; no binders accepted |
| `优化` | minimization/maximization orientation, feasible set, optimum notion, existence versus characterization versus algorithm | `IsMinOn`, infimum/argmin, constraints, convergence or complexity proposition | absent; no conclusion accepted |
| implicit constraints | constraint families, equality/inequality forms, qualifications and boundary cases | indexed functions and feasibility predicate | absent |
| implicit theorem status | exact truth-valued result and all hypotheses | one elaborated `Prop` with ordered binders | absent; topic family only |
| attribution and century | primary work, edition, theorem/page, historical identity and corrections | versioned human-source record | untrusted metadata only |
| `已验证` | human proof mapping, formal system, declaration, immutable revision and kernel receipt | exact source crosswalk and checked module/declaration | no credit |

## Human-Source Lead

Stephen Boyd and Lieven Vandenberghe, *Convex Optimization*, Cambridge University Press, 2004,
author-hosted PDF `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`, was observed on
2026-07-13 with SHA-256
`40d976c83c18cce1900eff8c41bd5ad408c102b813af39d05ff85678ccf8d76e`.
Chapter 4, printed pages 127-139, first defines general optimization terminology, then defines
standard-form convex optimization at section 4.2.1, and at section 4.2.2 proves that every locally
optimal point of such a problem is globally optimal.

This is an authoritative modern definition and proof lead, but it does not resolve the catalog
identity. The catalog does not cite the book, does not choose the section 4.2.2 theorem rather than
the many other results in the field, and supplies no independent source review. The remote PDF is
not vendored or admitted as release evidence, and edition/correction review and a source-to-Lean
definition transport remain open. No `H0` is claimed.

## Formal Discovery Boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Convex.Extrema` contains
`IsMinOn.of_isLocalMinOn_of_convexOn`, which turns a local minimum on a convex set of a convex
function into a global minimum, and `IsMinOn.of_isLocalMin_of_convex_univ`, its whole-space
variant. `IntakeProbe.lean` elaborates both declarations and prints their axioms.

These declarations closely match the source lead's section 4.2.2 result, but that agreement does
not disambiguate the catalog. They do not prove minimizer existence, strict-convexity uniqueness,
KKT, duality, or an algorithm, and no wrapper is credited. The bounded search and API probe are
intake discovery only, not the downstream exhaustive anchor/provenance audit or proof evidence.

## Retry Condition

The statement phase may proceed only after accountable reviewers admit one immutable proposition,
freeze every semantic choice in `scope-map.md`, map the edition, pinpoint locator, incorporated
definitions, ordered binders, hypotheses, conclusion, proof, corrections, and boundary cases, and
independently approve why that proposition is this repository target. A later statement run must
then elaborate exactly that Lean target with minimal pinned imports, serialize its expression and
environment fingerprints, compile every credited transport, and execute the required removed-
hypothesis, changed-domain, binder-scope, and boundary mutations.
