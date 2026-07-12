# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9936-9941` supplies exactly the title `混沌理论`, attribution to
many mathematicians, the twentieth century, the gloss `确定性系统的混沌行为`, importance `high`, and
status `已验证`. Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source ID,
definition, theorem/page locator, binder, hypothesis, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37074-37099` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`. The ODE category and
statement-first lane were generated from inventory metadata; neither adds a mathematical premise.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, DOI `10.1090/gsm/140`, was inspected as an
authoritative modern discovery source. Section 11.3, preliminary-edition internal pages 295-297
(PDF pages 306-308), first says that defining chaos is difficult and different authors use
different definitions. It discusses sensitive
dependence plus transitivity, then selects Devaney's definition for a continuous discrete map
`f : M -> M` on an infinite metric space: transitivity and density of periodic points. Lemma 11.3
then derives sensitive dependence from that selected notion.

The catalog does not cite Teschl, Devaney, or Lemma 11.3. The passage concerns one discrete-map
definition and implication, not a theorem named "chaos theory" covering every deterministic system.
It therefore discriminates possible scope but is not adopted as the root and receives no H0 credit.

The author-hosted preliminary PDF observed during intake had 4,133,331 bytes and SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. The reproducible command
`pdftotext -f 306 -l 308 -layout <temporary-source-pdf> <temporary-extract>` produced an 11,217-byte
extract with SHA-256 `f2507f426dfe0b5ac293f49b9101ad516fe5ee1b32a5335d8486031b5a0461d9`.
The author-linked current errata PDF says its locators refer to printed-version pagination; mapping
the preliminary pages to that edition remains open. It had SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e` and materially corrects the
matching printed-page-298 transitivity definition to quantify over **nonempty** open sets, changes
`W^s` to `W^+`, and adds a no-isolated-points assumption to Problem 11.3. Any future source admission must incorporate
these corrections and undergo independent review. Temporary files and mutable URLs are discovery
inputs, not an immutable accepted source packet.

## Component crosswalk

| Catalog component | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `混沌理论` | a broad field with multiple incompatible definitions and theorem families | no single declaration follows from a field name | not a stable proposition |
| deterministic system | a self-map, action, semiflow, flow, ODE solution operator, or stochastic-free model | function/action/`Flow`, phase and time types, invariant domain, regularity | all absent |
| chaotic behavior | Devaney, sensitivity, entropy, Li-Yorke, mixing, horseshoe, or another property | exact predicate plus ordered binders, structures, hypotheses, and result | definition and conclusion absent |
| many mathematicians / twentieth century | broad historical context | provenance metadata only | no source or pinpoint theorem |
| ODE category | inventory classification | does not imply a smooth real ODE target | no premise credit |
| `已验证` | untrusted inventory field | inspectable source proof and kernel receipt would be required | no H or M credit |

## Quantifier and substitution boundary

The gloss has no logical verb or quantifier. Reading it as "all deterministic systems are chaotic"
is false for identity and constant dynamics. Reading it existentially requires choosing a system
and a chaos definition. Reading it definitionally produces no theorem. Rewriting it as Devaney's
definition, chaos-implies-sensitivity, positive-entropy-implies-chaos, a horseshoe/shift theorem, or
a named-system result would change rather than transcribe the source.

The immediately following records separately own the Lorenz system (`THM-M-1364`) and Smale
horseshoe (`THM-M-1365`); structural stability (`THM-M-1366`) is also separate. Topological entropy
(`THM-M-1403`) and measure-theoretic entropy (`THM-M-1404`) have their own targets. None may be
silently selected as this root, and no proof credit is shared.

## Source gate

There is no authoritative mathematical proposition selected by the repository. Before leaving
`H5`, an accountable reviewer must redirect the field label to one corrected exact proposition,
preserve an immutable primary or authoritative source, record edition and theorem/section/page,
transcribe all incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
and exceptional cases, incorporate errata, justify every neighbor boundary, and obtain independent
approval of the source-to-statement mapping.

`H5` here does not assert that chaos theory or its standard theorems are false. It records that the
repository's subject label and phenomenon gloss are not a truth-valued target a Lean kernel can
check. No H0 crosswalk can be completed until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks generic flow/invariance, periodic-point, topological-transitivity, and topological-entropy
interfaces. These use materially different encodings and form possible substrate only. A bounded
case-insensitive search for `chaos`, `chaotic`, `Devaney`, and `sensitive dependence` under pinned
`Mathlib/Dynamics` returned no match. A separate repo-local target-specific search for `Devaney`,
`sensitive dependence`, `deterministic systems`, `chaotic behavior`, `chaos theory`, or `IsChaotic`
also returned no match. Unrelated uses of "chaos" are outside this target search.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
