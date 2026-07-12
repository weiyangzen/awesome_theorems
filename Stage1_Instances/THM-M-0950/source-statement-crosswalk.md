# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6938-6943` supplies exactly the title `Polymath项目`, attribution
to many mathematicians, year 2009, the gloss `密度Hales-Jewett定理的组合证明`, importance "high,"
and status `已验证`. All six lines entered at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, theorem number,
definitions, ordered binders, hypotheses, conclusion, or proof boundary.

`Docs/Stage0_Blueprint.md:25903-25928` repeats that gloss while leaving exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
open. Rev-5.6 retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Repository element | Primary-source meaning | Required formal component | Intake result |
|---|---|---|---|
| `Polymath项目` | the first Polymath collaboration and its publication, not a proposition | exact selected declaration plus proof-provenance policy | open |
| "density Hales-Jewett theorem" | qualitative Theorem 1.4 is the likely conclusion | exact finite alphabet, word, density, line, and threshold encoding | candidate only |
| "combinatorial proof" | the new elementary/finitary proof route, distinct from the earlier ergodic proof | typed proof graph, source-node crosswalk, and checked composition | no proof-route credit |
| many mathematicians / 2009 | collaboration attribution and project start/public preprint year | immutable edition, authorship/provenance boundary, errata and review | plausible source matched |
| `已验证` | untrusted inventory metadata | accepted source and kernel receipts would be required | no H or M credit |

## Primary source

D. H. J. Polymath, "A new proof of the density Hales-Jewett theorem," *Annals of Mathematics*
175(3), 2012, pp. 1283-1327, DOI `10.4007/annals.2012.175.3.6`. The inspected publisher PDF has 45
pages, 554622 bytes, and SHA-256
`b7f68cc3e49357ddb836b542519164e9846010d9224dc7d942fe571f4cd9f2df`. The publication page names
D. H. J. Polymath and links that PDF. The matching immutable preprint is arXiv `0910.3926v2`,
dated 2010-02-16; the project/preprint began in 2009.

The source's introductory definitions on pp. 1283-1285 use `[k] = {1, ..., k}`, words in `[k]^n`,
and nondegenerate combinatorial lines described by a partition of `[n]` into fixed-coordinate sets
`X_1, ..., X_k` and a nonempty wildcard set `W`.

No independent source reviewer, accepted errata audit, or complete proof-to-node mapping exists, so
the source is not classified H0.

## Numbered-result crosswalk

| Source locator | Source clause | Formal obligations if selected | Status |
|---|---|---|---|
| Theorem 1.4, p. 1285 | qualitative density Hales-Jewett for every positive `k` and real `delta > 0` | encode density in `[k]^n`, a positive threshold, all larger `n`, arbitrary dense `A`, and a nondegenerate line | likely conclusion; not selected |
| Theorem 1.5, p. 1285 | tower-height bound of order `1/delta^2` for `k = 3`; Ackermann-scale comparison for `k >= 4` | define tower/Ackermann functions and replace informal big-O/comparability prose with exact sourced constants or bounds | stronger candidate; not selected |
| Abstract, p. 1283 | announces the elementary proof and the `k = 3` quantitative consequence | provenance/readable route and exact theorem links | summary only |
| Sections 2-8 | finitary proof architecture, including density-increment and induction machinery | source-node registry, all material premises, and checked composition | downstream proof/source audit only |

The published abstract and Theorem 1.5 use `O(1/delta^2)`. A live arXiv API summary observed during
intake used a conflicting exponent, so it is not statement authority; the immutable v2 source and
published text must control any quantitative target.

## Neighbor boundary

`THM-M-0949` is separately cataloged as `密度Hales-Jewett定理`, with the gloss "existence of a
combinatorial line." `THM-M-0950` instead names the Polymath project and its combinatorial proof.
The two may eventually reference a shared semantic proposition, but intake state, evidence,
receipts, proof credit, and target ownership remain separate. The integration/source reviewer must
decide whether 0950 selects a stronger quantitative proposition or requires the Polymath proof
provenance for a proposition also owned by 0949.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.HalesJewett` defines `Combinatorics.Line` and proves ordinary coloring
Hales-Jewett as `Combinatorics.Line.exists_mono_in_high_dimension`. Its own TODO notes that explicit
coordinate bounds are absent. `Mathlib.Data.Finset.Density` supplies `Finset.dens`. Bounded exact-
topic searches located no density-Hales-Jewett, DHJ, or Polymath theorem.

`IntakeProbe.lean` checks these adjacent APIs and two prospective predicates only. It supplies no
canonical expression, expression hash, checked alternate encoding, theorem declaration, proof
body, anchor-audit result, or proof credit.

## Source gate

Before `S56-M-0950-STATEMENT`, accountable reviewers must select one exact numbered source result
or provenance-sensitive package, bind every incorporated definition and premise to immutable
locators, resolve `THM-M-0949` ownership, audit corrections and the quantitative-exponent conflict,
and independently approve the source mapping. Only then may the statement phase freeze minimal
imports, the elaborated expression and environment fingerprints, checked transports, and required
mutations.
