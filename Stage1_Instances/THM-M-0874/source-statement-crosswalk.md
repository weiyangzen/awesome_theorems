# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:6404-6409` supplies the title `Babai算法`, attribution Laszlo
Babai, year 2015, gloss `图同构的准多项式算法`, importance `高`, and status `已验证`. An identical
duplicate occurs at lines 11551-11556. Git history attributes both uncited records to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no graph encoding, algorithm,
machine or cost model, exact bound, theorem locator, proof, correction record, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:23846-23871` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic closed-result planning text is not evidence.
Rev-5.6 retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Babai v2 source lead

Laszlo Babai, *Graph Isomorphism in Quasipolynomial Time*, arXiv `1512.03547v2`, 19 January
2016, was inspected as an 89-page author paper. The observed PDF has SHA-256
`b6393ff36f4ff1c9646d7b9c5ea9ef78cfb222d52634ffdef2f05fa77daa9c62`.
Section 1.1.1 on PDF page 4 defines a quasipolynomially bounded function by constants `c, C` with
`f(n) <= exp(C (log n)^c)` for all sufficiently large `n`. Theorem 1.1.1 states that String
Isomorphism can be solved in quasipolynomial time. Corollary 1.1.2 gives Graph Isomorphism and
Coset Intersection. The intervening paragraph defines Graph Isomorphism as deciding whether two
graphs are isomorphic and describes the reduction of graphs on `n` vertices to binary strings on
unordered vertex pairs.

The STOC 2016 extended abstract, DOI `10.1145/2897518.2897542`, pages 684-697, is a
bibliographic match but predates the correction. Neither v2 nor STOC alone is accepted as the final
proof source.

## Correction and post-fix leads

Babai's author update of 9 January 2017 records that Helfgott found an error invalidating the v2
quasipolynomial timing analysis, that Babai replaced the problematic recursive Split-or-Johnson
call and restored the claim, and that an updated arXiv posting was still in preparation. The
observed HTML has SHA-256
`d96a4083ffd3b0b6931500f13e81a33ecb3ec5ab9eebadb64c2fca476faf42ca`.

The linked four-page note, *Fixing the UPCC case of Split-or-Johnson*, dated 14 January 2017, has
observed SHA-256 `e4438bf10d131f4642bee9aa29dfbd9fc133776705c85c3fe3d466da38b95653`.
It explains the bad recursion and replacement, but also says another error in the Design Lemma
algorithm required a forthcoming update. It is therefore one repair component, not a complete
standalone corrected edition.

Harald Andres Helfgott, Jitendra Bajpai, and Daniele Dona, *Graph isomorphisms in
quasi-polynomial time*, arXiv `1710.04574v1`, 12 October 2017, is a detailed post-fix Bourbaki
exposition. The observed 67-page PDF has SHA-256
`f16a953a084a4bc4b77e30b5d0fb35557a566d5d869bf42de155400466b9f2d2`.
Its introduction defines the String Isomorphism and Graph Isomorphism tasks, explains the
graph-to-string reduction, states String Isomorphism as Theorem 1.1 and Graph Isomorphism as
Corollary 1.2, and says that Helfgott found the timing error, Babai repaired it, and the proof is
now correct. This is a strong post-fix reconstruction and review lead. It does not by itself satisfy
rev-5.6 `H0`: the full incorporated-definition, correction, assumption, and proof-node crosswalk
and an accepted independent review receipt remain open.

## Component crosswalk

| Catalog/source component | Pinpoint source meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| graph isomorphism | v2 Cor. 1.1.2; post-fix Cor. 1.2 | decision predicate over encoded finite graph pairs, related to `G ≃g H` | graph and encoding contract open |
| algorithm | explicit deterministic String Isomorphism route plus graph reduction | bundled machine/transition, total output, correctness theorem | no implementation or exact target |
| quasipolynomial | v2 p.4 bound; post-fix `exp(O(log n)^(O(1)))` | quantified natural time bound with real/asymptotic bridge | constants, rounding, threshold, and size variable open |
| graph-to-string reduction | binary strings indexed by unordered vertex pairs under induced symmetric-group action | encoding and checked bidirectional correctness/overhead | only prose source lead |
| v2 proof | Theorem 1.1.1 and Cor. 1.1.2 | source nodes for formal obligations | timing analysis was invalidated |
| repaired proof | UPCC note plus corrected Design Lemma material and post-fix exposition | separately owned correction and composition obligations | full bundle/node crosswalk open |
| `已验证` | uncited inventory label | accepted H/M receipts would be required | no source or proof credit |

## Pinned Lean boundary

`IntakeProbe.lean` checks `SimpleGraph.Iso`, `Language`, `ManyOneReducible`,
`Turing.TM2OutputsInTime`, and `Turing.TM2ComputableInTime` at the pinned revision. These APIs
can support pieces of a future encoding. They supply no finite graph serialization, GI language,
resource-bounded graph-to-string reduction, quasipolynomial predicate, Babai procedure, correctness
theorem, or terminal proof body. `TM2ComputableInPolyTime` is polynomial-specific and does not
silently express the required quasipolynomial bound.

A bounded case-insensitive search of repo-local Lean and pinned mathlib found no source or
documentation matching Babai, String Isomorphism, Coset Intersection, or quasipolynomial time; the
generic phrase "graph isomorphism" occurs only around ordinary graph isomorphism APIs. This is an
intake observation, not the later immutable exhaustive anchor audit.

## Source and statement gate

Before statement execution, accountable source and algorithms reviewers must select and preserve
a lawful complete corrected source bundle, map every incorporated definition, binder, assumption,
algorithmic transition, bound, reduction, correction, proof node, and boundary case, and approve
the exact human claim. A formal reviewer must then freeze the graph/input and machine/cost models,
one minimal-import Lean expression, its environment fingerprint, checked transports, and the four
required mutation classes. Until those gates pass, `H1`, `M4`, and `R4` are truthful provisional
classifications and no statement or proof credit is claimed.
