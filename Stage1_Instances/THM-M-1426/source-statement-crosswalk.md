# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10418-10423` supplies exactly the title
`多值随机动力系统`, the attribution "many mathematicians," the period "21st century," the gloss
`非唯一解的随机系统`, importance "high," and status `已验证`. All six lines were introduced by
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record contains no citation or
theorem statement.

`Docs/Stage0_Blueprint.md:38780-38805` repeats the gloss and explicitly leaves exact definitions and
premises, proof process, dependencies, equivalent forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and resets this target
to `L0 / rework_required`.

## Primary source-selection candidate

Publisher metadata and an institutional-repository copy identify Tomas Caraballo, Jose A. Langa,
and Jose Valero, "Global Attractors for Multivalued Random Dynamical Systems," *Nonlinear Analysis:
Theory, Methods & Applications* **48**(6), 805-829 (2002), DOI
`10.1016/S0362-546X(00)00216-9`. The inspected 28-page, 251443-byte PDF has SHA-256
`3d708a8b27e6d889c5b6b929a1a3d9702383fc0f0be9ca41ccd4be38fbbf2269`.

The abstract and introduction make this a strong semantic candidate: they describe an MRDS as a
measurable multivalued flow satisfying a cocycle property and motivate it by stochastic equations
whose solutions are not unique. Section 2.1, Definition 1 (printed page 3) fixes one concrete MRDS
definition. But the paper does not identify one inevitable catalog theorem. It also contains
Proposition 2 and Theorem 3 on limit sets and random attractors, Theorem 8 on generating an MRDS,
Theorems 12 and 16 on attractors for inclusions, and Theorem 17 for a reaction-diffusion example.

The catalog does not cite this paper, choose Definition 1 or any theorem, adopt the paper's exact
spaces and almost-sure convention, or distinguish the general framework from the neighboring
random-attractor target. The paper is therefore source-selection and ambiguity evidence only. Its
proof dependencies, corrections and errata, exact archival policy, catalog identity, and
independent review are not accepted, so it supplies no H0 or canonical-statement credit.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `多值` / "multivalued" | one initial condition may relate to several solution states | a set-valued map or relation, action on points/sets, and value nonemptiness/closure convention | concept named; representation open |
| `随机` / "random" | measurable dependence on a sample and a measure-preserving base flow | measurable/probability space, measure, driving action, exceptional-set scope | all data and conventions open |
| `动力系统` / "dynamical system" | identity and cocycle/concatenation laws over time | time type, base shift, multifunction composition, equality or inclusion law | no exact law selected |
| "nonunique solutions" | solution set of a stochastic equation or inclusion | equation, solution concept, existence and concatenation relation | motivation only; no equation or theorem |
| "many mathematicians" / 21st century | a literature family | immutable source identity and node-by-node premise mapping | no author, edition, theorem/page, proof, errata, or reviewer |
| `已验证` | untrusted inventory metadata | inspectable human proof or kernel receipt would be required | no H or M credit |

## Candidate-paper crosswalk

| Candidate passage | Mathematical role | Lean needs | Why it is not canonical at intake |
|---|---|---|---|
| Definition 1, printed p. 3 | measurable `G : R+ x Omega x X -> C(X)` with identity and cocycle equality | Polish/metric state, measurable multifunction, nonempty closed values, time/base flow, lifted relation composition | a definition, not a truth-valued theorem; catalog does not select its conventions |
| Proposition 2, printed pp. 4-6 | compactness, invariance, and attraction of omega-limit sets under `(H1)-(H2)` | absorbing random compact set, semicontinuity, pullback limit set, Hausdorff semidistance | one substantive result among several; exact hypotheses and proof boundary not audited |
| Theorem 3, printed pp. 7-9 | existence, uniqueness, minimality, and measurability of a global random attractor | compact-valued MRDS, deterministic bounded-set measurability, union of limit sets, completed-measure transport | overlaps neighboring `THM-M-1425` and is not selected by the catalog |
| Theorem 8 | a stochastic inclusion generates an MRDS | operator/inclusion solution theory, compact semigroup, measurable multivalued flow | model-dependent construction with a deep imported premise boundary |
| Theorems 12, 16, 17 | global random attractors for general and reaction-diffusion inclusions | Hilbert/PDE, subdifferential, compactness, dissipativity, stochastic forcing | distinct application theorems and attractor results, not the bare catalog gloss |

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must justify the
catalog-to-source identity, preserve and hash an immutable primary source, select one exact
truth-valued theorem rather than a topic or definition, transcribe every incorporated definition,
ordered binder, hypothesis, conclusion, almost-sure convention, and exceptional case, map its proof
dependencies and corrections or errata, and explain the boundary with `THM-M-1424` and
`THM-M-1425`. A second qualified reviewer must approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Data.Rel`
provides `SetRel`, `SetRel.comp`, `SetRel.image`, and `SetRel.image_comp`; the ergodic API provides
`MeasurePreserving` and iteration. A bounded name search over repository and pinned-mathlib Lean
sources found no target-specific declaration for a multivalued or set-valued random dynamical
system, multivalued random flow/cocycle, or random differential inclusion.

The relation APIs do not supply multifunction measurability, random cocycles, nonunique stochastic
solution concatenation, or any candidate theorem. The canonical module, expression, expression
hash, checked transports, and statement mutations remain null. No H0, M0, readable-proof closure,
audit completion, or theorem completion is claimed.
