# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0308`, the label "extension theorem," the attribution Sergei
Sobolev, the year 1936, and the gloss "extension of Sobolev functions." Importance "high" and
status `已验证` are catalog metadata, not source or kernel evidence. Intake preserves only the
Sobolev-function extension family.

A common reading is the existence of a bounded linear operator from a Sobolev space on a regular
domain to the corresponding whole-space Sobolev space whose restriction agrees with the input.
That sentence is a scope locator, not the selected theorem.

## Proposition-changing decisions

An approved source selection must freeze:

- the exact historical or modern theorem, edition, incorporated definitions, assumptions, proof
  boundary, corrections, errata, and relation to the catalog attribution and date;
- Euclidean space or manifold, ambient dimension, domain openness and boundedness, boundary
  regularity, Lipschitz/cone/extension-domain condition, and the ambient and restricted measures;
- real, complex, scalar, or vector-valued functions, including all required Banach-space
  hypotheses;
- integer, first-order, higher-order, fractional, homogeneous, or inhomogeneous Sobolev model,
  and `W^{k,p}` versus `W_0^{k,p}`;
- the complete ranges and endpoints of `k`, `s`, and `p`, including `p = 1` and `p = infinity`;
- whether the result supplies one operator for the entire space or an extension for each function,
  and whether it is linear, bounded, continuous, positive, local, or support-controlled;
- the exact restriction/agreement relation on the domain: equality of representatives, almost
  everywhere equality, equality of equivalence classes, or equality of weak derivatives;
- the norm or seminorm estimate, extension constant, and every parameter on which it may depend;
- ordered binders, quantifier dependencies, universes, coercions, quotient representatives,
  typeclass assumptions, and every boundary or degenerate case.

These choices change the proposition and sometimes its truth.

## Candidate families not credited

- A bounded linear extension operator `W^{k,p}(Omega) -> W^{k,p}(Real^n)` for a Lipschitz or other
  source-approved extension domain, with restriction equal to the original class and a norm bound.
- A first-order `W^{1,p}` extension result, which may have different endpoint and domain hypotheses.
- A fractional Sobolev extension theorem or a homogeneous-space extension theorem.
- Zero extension for `W_0^{k,p}` or for functions satisfying a source-selected trace condition.
- A per-function existence statement without a single bounded linear extension operator.

These are a resolution ledger only. Intake asserts none as the root.

## Explicit exclusions

Zero extension on a zero-boundary space cannot replace a general-domain extension operator.
Whitney, Tietze, Hahn-Banach, Kirszbraun, measure, distribution, or holomorphic extension theorems
are different targets. A reflection construction for smooth functions alone does not establish a
Sobolev-space theorem. A structure field or hypothesis named `domainExtensionPackage` merely
assumes the missing work and is not a proof.

The neighboring `THM-M-0303` and legacy-backed `THM-M-1237` dossiers concern Sobolev embedding,
not extension; their statements and evidence are not inherited. The distinct `THM-M-0307` trace
target may eventually share a boundary package, but a trace result does not supply this root.

## Boundary cases

The eventual source target must decide empty and whole-space domains; dimension zero and one;
unbounded, disconnected, rough, measure-zero, or non-extension domains; zero functions and zero
spaces; `p = 1` and `p = infinity`; order zero; fractional endpoints; real versus complex scalars;
and representative dependence. It must also distinguish support preservation from bounded support
growth and state whether the extension acts uniformly over a family of domains.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib contains `MeasureTheory.Lp`, `MemLp`,
continuous linear maps, and Gagliardo-Nirenberg-Sobolev inequalities for smooth compactly
supported functions. A repo-local legacy Sobolev-embedding artifact records
`domainExtensionPackage` only as an open proposition. These are adjacent interfaces, not a
Sobolev extension-space definition, extension operator, restriction theorem, or norm estimate.
The later statement and anchor-audit phases must determine exact imports, expression identity,
formal candidates, and terminal proof provenance.
