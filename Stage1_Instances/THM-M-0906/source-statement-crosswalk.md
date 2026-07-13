# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6628-6633` supplies exactly the title `列表着色`, attribution
`Vizing/Erdős/Rubin/Taylor`, year 1976, gloss `列表色数的理论` ("the theory of the list chromatic
number"), importance "high," and status `已验证`. Git blame attributes all six uncited lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, definitions, domains, quantifiers, hypotheses, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:24710-24735` repeats the gloss while explicitly leaving the target formal
system, logical foundation, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. The rev-5.6 target manifest preserves
`已验证` only as untrusted metadata and resets this target to `L0 / rework_required`.

No mathematical source cited by the repository selects a theorem. The attribution and year are
therefore retained as untrusted catalog provenance, not accepted historical or H0 evidence.

## Clause crosswalk

| Repository phrase | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `列表着色` | list coloring of vertices, edges, or another incidence object | a proper coloring plus membership in an allowed-color assignment | object and coloring mode absent |
| `列表色数` | least `k` for which a graph is `k`-choosable | a minimum in `Nat`, `ENat`, or another cardinality type | definition, finiteness, and nonattainment convention absent |
| `理论` | a body of definitions and many theorems | no single `Prop` | not a truth-valued root |
| Vizing/Erdős/Rubin/Taylor | historical attribution lead | source provenance only | no edition, title, locator, or statement supplied |
| 1976 | historical date lead | source revision field only | no matching source admitted |
| `已验证` | untrusted inventory status | would require source and kernel receipts | no H or M credit |

## Candidate theorem families not selected

The repository wording could be associated with definitions of list coloring and choosability,
existence of the list chromatic number for finite graphs, comparisons between ordinary and list
chromatic numbers, bounds in terms of degree or degeneracy, exact values for special graph classes,
or characterizations of low-choosability graphs. It might also be read historically as referring
to foundational work by the named authors. None of these readings is selected by the received
record. Naming one would broaden or substitute the target rather than crosswalk it.

A bounded web metadata search during intake did not produce an exact source that can be admitted
for the catalog record. Search results and encyclopedia pages are E5 discovery material at most;
they are not used to raise H status. The statement phase must locate a lawful immutable primary or
authoritative edition, audit its exact statement, premises, definitions, proof boundary, corrections
and errata, and obtain independent source review.

## Neighbor crosswalk

The nearby catalog sequence separately assigns the Dinitz conjecture to `THM-M-0904`, Galvin's
theorem to `THM-M-0905`, the Alon-Tarsi theorem to `THM-M-0907`, Thomassen's planar-graph theorem to
`THM-M-0908`, and Voigt's planar counterexample result to `THM-M-0909`. Their specificity is evidence
that this target is an umbrella topic, not permission to merge their claims, sources, proofs, or
status into it. Any future overlap requires explicit master scope reconciliation and checked
implication or equivalence transports.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SimpleGraph.Coloring` supplies `SimpleGraph.Coloring`,
`SimpleGraph.Colorable`, `SimpleGraph.chromaticNumber`, and ordinary-coloring lemmas.
`IntakeProbe.lean` checks those interfaces and finite-set/cardinality substrate. A bounded search of
the repository's `Formalizations/Lean` tree and pinned mathlib found no obvious list-coloring,
choosability, choice-number, or list-chromatic declaration. Ordinary coloring lacks a per-vertex
allowed-color assignment and is not an exact candidate.

These observations are scoped discovery evidence only. They are not a complete immutable external
anchor audit and not a global absence theorem. The probe declares no target, transport, axiom, or
proof body.

## Source gate

Before leaving `H5`, accountable reviewers must correct or disambiguate the repository record to
one truth-valued proposition, preserve an immutable approved source, map every binder, hypothesis,
conclusion, definition, side condition, boundary case, attribution, and erratum, and independently
approve fidelity to `THM-M-0906`. Only then may the statement phase select minimal imports,
serialize the elaborated expression and environment hashes, check alternate encodings, and run the
required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
