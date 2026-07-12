# THM-M-0575 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Bott periodicity theorem. The manifest's
untrusted source label says only "periodicity of K-theory" and does not distinguish several
standard theorems called Bott periodicity. Intake therefore selects complex topological K-theory
period two as the provisional root while keeping the exact-statement gate blocked until a primary
source formulation is transcribed without filling in omitted assumptions.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Exact root | Natural twofold periodicity of reduced complex topological K-theory by the Bott class | Space category, grading direction, and Bott normalization need a pinpoint source |
| K-theory model | Reduced complex topological K-theory with suspension and external product | No Lean model or declaration is selected |
| Bott input | Construction of a complex Bott class and its action | No construction or invertibility proof is credited |
| Equivalent topology | Double suspension and stable unitary loop-space formulations | These need checked representability and convention transports before statement credit |
| Boundaries | Point and sphere test cases; reduced/unreduced comparison | Special cases cannot replace the natural theorem |
| Excluded neighboring results | Real `KO` period eight, equivariant/operator/algebraic K-theory | Distinct roots, not broadenings of this item |
| Foundations | Lean 4 kernel plus versioned policies for topology, quotients, and classical choice | Profiles and dependency closure remain open |

The initial architecture names `BP-ROOT`, `BP-KMODEL`, `BP-BOTT`, `BP-INVERT`, `BP-NAT`, and
`BP-TRANSPORT`. These are scope labels only, not a frozen obligation registry and not closed proof
nodes. The dependent source-audit and obligation-tree phases must refine them after the statement
has a unique source-faithful meaning.

## Current boundary

The root is `[H1, M4, R3]`: the classical result and primary-source candidates are known, but the
repository wording is too short for `H0`; no exact Lean target or usable formal artifact has been
established; and this document is only an intake map. The manifest label `已验证` is discovery
metadata and supplies no machine-proof credit. Lifecycle is `planned`, and theorem completion is
false.

Exact validation commands and their limited meaning are recorded in `validation.md`.
