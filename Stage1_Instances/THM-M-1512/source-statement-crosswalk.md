# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records the title `纳什存在性定理`, John Nash, the year 1950,
and the complete gloss `纳什均衡的存在性` (existence of Nash equilibrium). It supplies no
bibliography, game definition, quantifiers, hypotheses, conclusion-level formula, proof, errata,
or formal artifact. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is repository provenance, not an accepted
mathematical source revision.

`Docs/Stage0_Blueprint.md` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof path, dependencies, equivalent formulations,
axioms, and machine artifacts open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`.

The neighboring catalog record `THM-M-1511` is titled `纳什均衡` and has the broader gloss
`非合作博弈的均衡`. It is a separate target and supplies no statement or proof credit here.

## Inspected primary-source lead

John F. Nash, Jr., *Equilibrium Points in N-Person Games*, **Proceedings of the National Academy
of Sciences** 36 (1950), no. 1, printed pages 48-49, DOI
`10.1073/pnas.36.1.48`. A two-page scan exposed through PubMed Central was inspected outside the
repository; its SHA-256 was
`5bf21fdad1ab15779fb1d816298ba338b6d30d854938c15e4f41df1b6659ed85`.
Crossref independently confirms the title, author, journal, date, volume, issue, pages, and DOI.

The scan identifies the historical theorem family and its short proof, but it is not admitted as
`H0`: the repository does not cite or explicitly select it, the incorporated definitions and
assumptions have not been reviewed against a canonical formal statement, no errata search or
translation review is accepted, and no independent source reviewer is assigned.

## Crosswalk

| Source/catalog component | Mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| catalog: existence of Nash equilibrium | an existential theorem, not merely the definition of equilibrium | `Exists profile, IsNashEquilibrium game profile` after definitions are frozen | family identified; proposition absent from catalog |
| Nash p. 48: each player has finitely many pure strategies | finite pure-strategy carrier per player | dependent finite types or finite nonempty sets | source lead inspected; exact binders and nonemptiness encoding open |
| Nash p. 48: a payment vector for each pure profile | normal-form payoff table | `(i : Player) -> PureProfile -> Real` or checked equivalent | candidate source clause; codomain and coercions not frozen |
| Nash pp. 48-49: mixed strategies are probability distributions | simplex of distributions on each pure-strategy set | `stdSimplex Real (Pure i)` or `PMF (Pure i)` | both adjacent APIs exist; representation and transport open |
| Nash p. 49: payoffs are expected polylinear forms | finite expected-payoff extension | finite sum over pure profiles weighted by a product of probabilities | definition and continuity proof open |
| Nash p. 49: a profile counters another | each component is a highest-payoff response to the other components | best-response correspondence on the mixed-profile product | terminology mapped only at prose level |
| Nash p. 49: self-countering means equilibrium | simultaneous best responses | fixed point or all-player no-profitable-deviation predicate | equivalence must be kernel-checked later |
| Nash p. 49: countering values are convex and graph is closed | Kakutani hypotheses for the correspondence | `Convex`, graph closedness or upper hemicontinuity, nonempty values | prospective proof nodes only |
| Nash p. 49: fixed point, hence equilibrium | existence of a mixed-strategy equilibrium | exact root existential | no formal target or proof credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks `stdSimplex`, `convex_stdSimplex`, `isCompact_stdSimplex`, `PMF`, and generic
upper-hemicontinuity and fixed-point predicates. A bounded case-insensitive name search over
repo-local Lean and pinned mathlib found no Nash-equilibrium, mixed-strategy, best-response, or
game-theory declaration matching this target, and no Kakutani fixed-point terminal theorem.
Unrelated uses of "payoff" and combinatorial games are not candidates.

This is intake discovery only, not the downstream exhaustive anchor audit and not an absence claim
about all external Lean projects. A later bounded external search located the immutable project
`math-xmum/Brouwer` at commit `c02205edf347ad45f0d62db85497598ba2c4291e`. Its
`Gametheory/Nash.lean` defines finite games, simplex-valued mixed strategies, mixed payoff and
`mixedNashEquilibrium`, then states and proves `ExistsNashEq : Exists sigma : G.mixedS,
mixedNashEquilibrium sigma`. The source file SHA-256 is
`734911160e5fec94607d343c36228b0064de083d6a9b412b9dbe8b66bd962c4b`.

That candidate is an `E3` discovery anchor only. It targets Lean 4.31.0 and mathlib
`fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, is absent from this repository's pinned dependency
closure, and was not built or axiom-audited here. Its proof uses a single-valued Nash map and a
project-local Brouwer/Scarf route rather than Nash's 1950 Kakutani correspondence route, so an exact
claim transport and terminal provenance audit are required. The visible `sorry` text in the Nash
file occurs in line or block comments, but a static scan is not a kernel or transitive trust
receipt. It remains for `ANCHOR_AUDIT`; it does not justify M1 or any proof credit at intake.

No canonical Lean target, expression fingerprint, checked alternate encoding, obligation registry,
proof body, or machine debt reduction is credited.

## Retry condition

The statement phase may proceed only after an accountable reviewer selects an immutable source
proposition, freezes every row and boundary decision in `scope-map.md`, completes the
edition/definition/assumption/conclusion/errata crosswalk, and approves why it is the repository
target rather than a familiar substitute. It must then elaborate the exact Lean target with fixed
imports and options and run the required domain, hypothesis, binder-scope, and boundary mutations.
