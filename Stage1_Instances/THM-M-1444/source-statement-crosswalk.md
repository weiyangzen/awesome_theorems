# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10546-10551` supplies exactly the title
`Banach不动点定理`, Stefan Banach, 1922, the gloss `压缩映射的不动点`, high importance, and status
`已验证`. Git history attributes those uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no bibliography, theorem locator, complete
premise list, conclusion, proof, errata, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:39271-39296` repeats the same data while explicitly leaving the target
formal system, foundations, exact definitions and premises, proof path, dependencies, equivalent
forms, axiom use, machine state, and artifact links open. Rev-5.6 consequently preserves
`已验证` only as `source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected historical source lead

Stefan Banach, *Sur les opérations dans les ensembles abstraits et leur application aux équations
intégrales*, *Fundamenta Mathematicae* **3** (1922), 133-181, DOI
`10.4064/fm-3-1-133-181`, was inspected in a publisher-hosted 49-page image scan bearing the Polish
Virtual Mathematics Library watermark. The observed PDF SHA-256 is
`87c9b019a592cb2c16755db15e54b0df2a2a43c4769cc0df8aca4d9514b75445`.

Theorem 6 appears on printed page 160, with its proof continuing on page 161. It assumes:

1. `U(X)` is a continuous operation in `E`, with its counter-domain contained in `E`;
2. there is a number `0 < M < 1` such that for all `X'`, `X''`,
   `|U(X') - U(X'')| <= M |X' - X''|`.

Its displayed conclusion is existence of an `X` satisfying `X = U(X)`. The proof starts from an
arbitrary `Y`, forms successive iterates, uses the geometric contraction estimate to obtain norm
convergence, and uses continuity to get the fixed point. Theorem 7, beginning on printed page 161,
applies the result to an operator equation; it is not the target theorem.

This inspection supports `H1`, not `H0`. The repository does not cite or select the paper; the scan
is not vendored, and repeated publisher downloads can be byte-variable; its archival stability and
license treatment need review; the source's earlier
axioms and terminology for `E`, every incorporated definition, translation decisions, proof-node
mapping, errata, and an independent source review are not yet accepted. In particular, uniqueness,
modern metric-space generality, and explicit convergence/error conclusions must not be inserted
into the source theorem merely because they are familiar consequences or library APIs.

## Literal crosswalk

| Catalog/source element | Mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| Banach fixed-point theorem | one contraction-mapping fixed-point proposition | one exact `Prop` plus checked transports | theorem family identified; exact root open |
| contraction mapping | factor below one and a distance/norm inequality | `ContractingWith K f` or an approved expansion | encoding and factor type open |
| fixed point | existence of `X` with `X = U X` in Theorem 6 | preserve literal equality or use `Function.IsFixedPt` with checked equality-symmetry transport | existence family preserved; transport not yet checked |
| source `E` | at-least-two-element real normed linear setting with Cauchy completeness on printed pp.134-136 | real normed-space, `CompleteSpace`, and `Nontrivial` instances | candidate mapping identified; full incorporated definitions and review open |
| self-operation | counter-domain of `U` contained in `E` | endomap or `Set.MapsTo`/subtype map | carrier choice open |
| continuity | explicit Theorem 6 premise | `Continuous U` or derived lemma | retain/remove decision open |
| `0 < M < 1` | positive strict contraction constant | `K : NNReal` and `K < 1`, or real factor | checked transport absent |
| `已验证` | untrusted catalog field | H/M evidence would require receipts | no proof credit |

## Pinned Lean candidates

| Candidate | Checked pinned role | Why it is not selected at intake |
|---|---|---|
| `ContractingWith.exists_fixedPoint` | complete `EMetricSpace`; start `x` with finite `edist x (f x)`; fixed point, iterate convergence, and geometric bound | substantially richer conclusion and an extended-distance component premise |
| `ContractingWith.exists_fixedPoint'` | complete forward-invariant subset variant with start point, convergence, and bound | subset and restriction encoding not selected by the catalog or source crosswalk |
| `ContractingWith.fixedPoint_isFixedPt` | fixedness of the chosen point in a nonempty complete `MetricSpace` | conclusion is tied to a noncomputable library definition; exact root identity is unreviewed |
| `ContractingWith.fixedPoint_unique` | uniqueness of the library fixed point | uniqueness is not the displayed conclusion of source Theorem 6 |
| `ContractingWith.tendsto_iterate_fixedPoint` | convergence from every starting point | convergence belongs to the proof and modern theorem family but is not yet selected as root conclusion |
| a priori/a posteriori estimate APIs | quantitative geometric error bounds | no catalog or accepted source mapping selects either bound |

The declarations above are discovery evidence from the pinned dependency, not accepted anchors or
proof bodies for `THM-M-1444`. A later anchor audit must inventory exact types, provenance, axioms,
terminal bodies, imports, license, and source fit at immutable revisions.

## Source gate

Before statement acceptance, accountable reviewers must choose the exact root; map the complete
source setting, ordered binders, hypotheses and conclusion; decide whether uniqueness, convergence,
and estimates are root conclusions or downstream nodes; audit corrections and translation; and
approve the source-to-Lean relationship. Only then may the statement phase elaborate a canonical
expression, fingerprint its environment, check alternate encodings, and run mutations.
