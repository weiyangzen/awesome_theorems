# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:6229-6234` contains exactly the title `相变现象`, the
Erdos/Renyi attribution, year 1960, gloss `随机图的相变`, importance `高`, and status
`已验证`. `Docs/Stage0_Blueprint.md:23171-23196` repeats this metadata while explicitly leaving
the exact definitions and premises, proof route, dependencies, equivalent formulations, axioms,
and machine artifact open. The manifest preserves the status only as `source_status_untrusted`.

The catalog also contains `THM-M-1113` (`随机图相变`) with the gloss `随机图的相变现象`,
the same authors, and the same year. This semantic near-duplicate is a scope-boundary fact, not a
license to combine target IDs or transfer its dossier state.

## Inspected primary source

P. Erdos and A. Renyi, "On the Evolution of Random Graphs," *A Matematikai Kutato Intezet
Kozlemenyei* / *Publications of the Mathematical Institute of the Hungarian Academy of Sciences*,
volume 5, series A, issues 1-2 (1960), journal pages 17-61. The inspected official scan came from
`https://www.renyi.hu/~p_erdos/1960-10.pdf`; it has 45 PDF pages, 5,680,595 bytes, and SHA-256
`374daa0f45a834733e61622c5942a5f1dd4362bda1fff850b2c3ec01de9397da`. No source bytes were
added to the repository.

Pinpoint observations from the scan:

- Page 17 defines `Gamma(n,N)` as the uniform law over labelled simple graphs with `n` vertices and
  exactly `N` edges, gives an equivalent edge-addition process, and defines "almost all" by a
  probability limit equal to one.
- Theorem 7a and its remark, pages 47-49, give the logarithmic greatest-tree scale away from the
  critical value and explain when it is also the greatest component.
- Theorem 7c, pages 49-50, bounds the greatest tree at `N ~ n/2` between
  `n^(2/3)/omega_n` and `n^(2/3) omega_n` in probability for every slowly diverging `omega_n`.
- Section 9, page 52, explicitly summarizes the greatest component as order `log n`, `n^(2/3)`,
  and `n` for `N(n)/n -> c` below, at, and above `1/2`, calling the change a double jump.
- Theorem 9b, page 56, states supercritical convergence in probability of the greatest-component
  fraction to `G(c)` for `c > 1/2`; page 57 describes, up to `o(n)` vertices, isolated trees plus a
  single giant component.

This inspection identifies a primary source family and makes the catalog ambiguity precise. It is
not `H0`: no independent reviewer has selected one root, audited every incorporated premise and
proof boundary, or checked corrections and errata.

## Claim crosswalk

| Catalog or source phrase | Source component | Required Lean component | Intake status |
|---|---|---|---|
| `random graph` | uniform fixed-edge `Gamma(n,N)` on labelled simple graphs (p. 17) | finite vertex type and an exact fixed-cardinality graph measure | source model identified; no pinned Lean encoding selected |
| `phase transition` | Section 9 double jump of greatest-component order (p. 52) | a three-regime asymptotic proposition over component sizes | candidate synthesis identified; root not selected |
| subcritical regime | Theorem 7a plus earlier component classification | largest-component cardinality and logarithmic probability bounds | dependencies and exact conclusion not frozen |
| critical regime | Theorem 7c and surrounding results (pp. 49-50) | quantified `n^(2/3)`-scale bounds with auxiliary sequences | candidate theorem identified; exact transcription/review open |
| supercritical regime | Section 9, especially Theorems 9a and 9b (pp. 52-56) | largest-component fraction, limiting probability, and optional uniqueness/structure | candidate theorem identified; root strength open |
| critical value | `N(n)/n -> 1/2` | historical parameterization or a checked map to average degree / `G(n,p)` | transport not credited |
| `已验证` | catalog inventory label | none | rejected as source or kernel evidence |

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs` defines the independent-edge measure
`SimpleGraph.binomialRandom`. Its historical note explicitly says that the Erdos-Renyi model in the
1960 source is closely related but different. The same file contains elementary endpoint and
singleton-mass facts and an unrelated `proof_wanted` about the edge-count distribution. Module
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Finite` exposes finite connected-component APIs.

`IntakeProbe.lean` verifies that nine adjacent declarations elaborate together. A bounded exact-
topic search found no pinned mathlib or repository-local Lean phase-transition declaration. This is
intake feasibility evidence only, not the downstream exhaustive anchor audit and not a claim of
global absence.

## Unblocking crosswalk

Before statement work or `H0`, accountable reviewers must select the exact primary-source root and
edition; hash every admitted source; record the complete definition, premise, conclusion,
dependency, proof-boundary, correction, and erratum mapping; decide the relation to `THM-M-1113`
without sharing credit; and independently approve every model, parameter, quantifier, probability,
component-size, uniqueness, and boundary choice. Only then may a worker elaborate the corresponding
Lean target and any checked model transport.
