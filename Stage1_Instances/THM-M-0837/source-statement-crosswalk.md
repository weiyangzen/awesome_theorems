# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6145-6150` supplies exactly the title
`Robertson-Sanders-Seymour-Thomas证明`, attribution `Robertson等`, year 1997, gloss
`四色定理的新证明`, importance `高`, and status `已验证`. All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. There is no citation, theorem number, definition,
binder, hypothesis, conclusion, or proof-artifact locator.

`Docs/Stage0_Blueprint.md:22847-22872` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Source-family meaning | Required Lean component | Intake result |
|---|---|---|---|
| `Robertson-Sanders-Seymour-Thomas证明` | a named proof and provenance family | exact proposition plus declared proof-provenance contract | open |
| `四色定理的新证明` | ordinary 4CT conclusion, new proof architecture, and associated algorithm are all plausible | one selected root and checked composition | open |
| Robertson et al. / 1997 | strong match to the JCTB article | immutable edition, exact locators, definitions, assumptions, corrections, and review | bibliographic lead only |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no H or M credit |

The word "proof" cannot silently become the generic Four-Colour proposition, because that loses
the proof-route identity and overlaps `THM-M-0833`. It also cannot silently become a theorem about
the existence, novelty, validity, or formal verification of a proof object.

## Source leads

The matching 1997 bibliographic record is Neil Robertson, Daniel P. Sanders, Paul Seymour, and
Robin Thomas, "The Four-Colour Theorem," *Journal of Combinatorial Theory, Series B* 70(1), 1997,
2-44, DOI `10.1006/jctb.1997.1750`. Crossref metadata and the author-maintained bibliography agree.
The publisher article body was not retrieved successfully, so its complete statement, definitions,
proof, and corrections were not inspected here.

Robin Thomas's author-maintained page, "The Four Color Theorem," summarizes the RSST proof and
algorithm. The inspected 16056-byte HTML snapshot has SHA-256
`c096ff0c8b5da0bb9267071b83f65679bb7ce5a54b16b3fcbdde0502c1e8d83f`. It defines the map-colouring
motivation and gives graph-theoretic configuration terminology, but it is a summary page, not the
accepted primary proof source.

The authors' 1996 announcement, "A New Proof of the Four-Colour Theorem," was visually inspected
from a 203692-byte, nine-page PDF with SHA-256
`df597ecb200d7fcfecbebd00ce5d79c13e9e106fd47b39c9b9ddca225baeaca3`. Formula extraction is
garbled, so the intake records only visually checked discovery facts rather than claiming an exact
machine transcription. The author page cites printed pages 17-25, while current Crossref metadata
reports 17-26; that pagination discrepancy remains unresolved.

## Clause crosswalk

| Source locator | Visually inspected or author-summary clause | Lean obligations if selected | Status |
|---|---|---|---|
| Announcement abstract and section 1 | every finite loopless planar graph admits a proper vertex-colouring with at most four colours | finite graph and planarity encoding, colouring, general-input reduction, and map/graph transport | candidate only |
| (2.1) | every minimal counterexample is an internally 6-connected triangulation | minimality, plane triangulation, internal connectivity, and reduction proof | supporting candidate only |
| (2.2), also author-page Theorem 1 | no good configuration appears in a minimal counterexample | 633-object identity, appearance, reducibility, safe reducers, program/certificate boundary | candidate only |
| (2.3), also author-page Theorem 2 | every internally 6-connected triangulation contains a good configuration | charges, 32 rules, cartwheels, finite degree cases, program/certificate boundary | candidate only |
| (3.1) | each of the 633 good configurations is D- or C-reducible with a safe reducer | exact data, integer semantics, program correctness, outputs, and composition to (2.2) | computation boundary only |
| (4.4) | every relevant internally 6-connected triangulation has a good configuration in the vicinity of a vertex | formalized case language, rules, data, verifier, and composition to (2.3) | computation boundary only |
| section 5 | the proof yields a quadratic algorithm for four-colouring planar graphs | input/output types, total correctness, recursion, triangulation, cost model, and complexity proof | candidate only |

The inspected sources derive the Four-Colour Theorem by combining the minimal-counterexample fact
with (2.2) and (2.3). That source architecture does not decide whether the repository root is the
conclusion, the source-specific route, its clause suite, or the algorithm.

## Computer-proof boundary

The author sources describe two computer-verified parts, integer arithmetic, independent programs,
and residual compiler and hardware trust. The authors' 2014 arXiv records `1401.6481`, "Reducibility
in the Four-Color Theorem," and `1401.6485`, "Discharging cartwheels," say that two lemmas in the
1997 article were asserted computer-verified rather than proved there and point to ancillary files.
No such file or result is admitted, pinned, executed, or kernel-checked by this intake.

## Neighbor and source gates

Before `S56-M-0837-STATEMENT` can freeze a canonical target, accountable and independent reviewers
must select one exact root, identify all incorporated definitions and clauses, resolve the
generic/provenance relationship to `THM-M-0833`, keep Appel-Haken and Gonthier evidence separate,
settle edition and pagination issues, audit corrections, and freeze the human/computation/trust
boundary. H5 then requires an explicit redirect or corrected stable proposition before ordinary
theorem execution.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded searches over
repo-local Lean and pinned mathlib found no exact Four-Colour, RSST, reducibility, unavoidability,
or simple-graph planarity target. `IntakeProbe.lean` checks only graph-colouring interfaces.

No canonical module, declaration or expression, expression hash, environment fingerprint, checked
alternate encoding, source-specific computation, proof body, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
