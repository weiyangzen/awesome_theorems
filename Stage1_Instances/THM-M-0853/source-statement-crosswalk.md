# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:6257-6262` records only the title `Dirac定理`, proposer Gabriel
Dirac, year 1952, the gloss `Hamilton圈存在的度条件`, high importance, and status `已验证`.
`Docs/Stage0_Blueprint.md:23279-23304` repeats this metadata while explicitly leaving exact
definitions and premises, proof path, equivalent forms, axioms, machine-checked status, and artifact
links open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The six-line catalog record originated at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It gives no publication, edition, theorem number,
page, exact degree threshold, graph convention, proof boundary, correction record, or reviewer.

## Historical primary-source lead

Crossref bibliographic metadata identify G. A. Dirac, "Some Theorems on Abstract Graphs,"
*Proceedings of the London Mathematical Society*, series 3, volume 2, issue 1 (1952), pages 69-81,
DOI `10.1112/plms/s3-2.1.69`. This independently confirms a likely publication-level source for
the named theorem family and supports provisional `H1` classification.

zbMATH Open record `3073652` independently gives author code `dirac.gabriel-andrew`, identifying
the catalog's abbreviated Gabriel Dirac as Gabriel Andrew Dirac, and agrees on title, third series,
volume 2, pages 69-81, year, and DOI. This remains bibliographic corroboration, not article text.

It is not an `H0` packet. The publisher full text was not available to this intake, so no exact
theorem/page passage, original definitions, ordered assumptions, conclusion, incorporated lemmas,
proof boundary, corrections, or errata were inspected or preserved. No independent source reviewer
has approved a translation or premise-by-premise mapping. The broad page range and DOI are
bibliographic locators, not a pinpoint statement crosswalk.

MathWorld's secondary entry "Dirac's Theorem" states the conventional normalization: a simple
graph with `n >= 3` vertices and every vertex degree at least `n/2` has a Hamiltonian cycle, and it
cites Dirac's 1952 paper. This corroborates the candidate family and its usual boundary; as a
secondary web source it cannot replace the primary-text and independent-review requirements.

## Component crosswalk

| Repository or conventional phrase | Mathematical component to freeze | Required Lean surface | Intake status |
|---|---|---|---|
| `Dirac定理` | graph-theoretic theorem identity, not the several unrelated Dirac families | source-approved namespace/name only after proposition identity | historical family recognized; exact source passage open |
| Hamiltonian cycle exists | a spanning simple cycle under the source convention | `SimpleGraph.IsHamiltonian` or an explicit `Walk.IsHamiltonianCycle` plus checked relationship | pinned predicates probed; canonical choice open |
| degree condition | pointwise degree or minimum degree, exact inequality, and all graph hypotheses | `SimpleGraph.degree`, `SimpleGraph.minDegree`, and checked conversion lemmas | APIs probed; no threshold selected |
| half the graph order | real/rational inequality or an exact integral rounding convention | `n <= 2 * d`, `(n + 1) / 2 <= d`, or another reviewed encoding | odd-order rounding unresolved |
| usual order boundary | finite graph with at least three vertices | `3 <= Fintype.card V` or source-equivalent encoding | conventional candidate only; not source-admitted |
| `已验证` | untrusted inventory metadata | no Lean proposition or evidence component | explicitly rejected as source or proof credit |

## Lean candidate boundary

The conventional mathematical reading can be represented by candidate shapes such as:

```text
3 <= card V -> card V <= 2 * G.minDegree -> G.IsHamiltonian
3 <= card V -> (forall v, card V <= 2 * G.degree v) -> G.IsHamiltonian
```

A ceiling-style minimum-degree form may instead use `(card V + 1) / 2 <= G.minDegree`. The weaker
floor form `card V / 2 <= G.minDegree` differs when `card V` is odd and must not be silently
credited. These expressions are intake candidates, not the canonical claim.

At pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` elaborates the adjacent degree and
Hamiltonicity APIs and all candidate proposition shapes. A bounded name/content search of pinned
mathlib found no graph-theoretic Dirac theorem or declaration connecting the half-order degree
condition to Hamiltonicity. That negative result is scoped discovery evidence only, not the
downstream immutable anchor audit and not an absence claim about external Lean projects.

Before statement credit, a source reviewer must preserve and approve an immutable proposition-level
source, pinpoint its definitions and theorem passage, map every binder/premise/conclusion and
boundary convention, and audit corrections and errata. A formal reviewer must then approve the
same elaborated Lean target, its serialized expression/environment fingerprint, checked transports,
and required mutations. Until then the root remains provisional `H1/M3/R4` with no proof credit.
