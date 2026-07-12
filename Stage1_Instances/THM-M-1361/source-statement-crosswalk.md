# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9922-9927` supplies exactly the title `跨临界分岔`, attribution to
many mathematicians, the twentieth century, the gloss `平衡点交换稳定性的分岔`, importance "high,"
and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, equation, definition, binder, hypothesis, conclusion, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37020-37045` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generic planning sentence about a known closed result
is not source evidence. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

There is also a historical identifier boundary: before Stage0 deduplication commit
`c61be3c80710c07c5f7626e3404e51f40ecb39a6`, the generated projection labeled this record
`THM-M-1401`; the current manifest labels it `THM-M-1361`. The current manifest identity is
authoritative. A historical theorem ID without the record content and revision is not a stable
source locator.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `跨临界分岔` | a definition, explicit example, local theorem, or normal-form classification | one exact `Prop` and ordered binders | result kind absent |
| "equilibria" | a selected dynamical system and two source-defined equilibrium branches | vector field or map plus `Function.IsFixedPt` or an equation predicate | system and branches absent |
| "exchange" | branch identities on both sides of a critical parameter and a comparison rule | parameter order/neighborhoods, branch functions, and side conditions | orientation and branch labels absent |
| "stability" | Lyapunov, asymptotic, exponential, spectral, or discrete-time stability | a source-selected stability predicate and orbit semantics | stability notion absent |
| "bifurcation" | a critical value and local qualitative-change or normal-form conclusion | exact locality, regularity, genericity, and nondegeneracy data | assumptions and conclusion absent |
| many mathematicians / twentieth century | broad historical context | provenance metadata only | no source or pinpoint result |
| `已验证` | untrusted inventory field | source proof and kernel receipt would be required | no H or M credit |

The noun phrase does not quantify over a system or assert an implication. Treating the familiar
transcritical theorem as implicit would still require choosing materially different premises and
conclusions.

## Inspected discovery source

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), Section 6.5, printed pages 199-200, was
inspected in the author's preliminary version made available with the publisher's permission. It
is an authoritative modern discovery lead, not the uncited catalog's accepted source.

| Source locator | Source component | Prospective target component | Intake disposition |
|---|---|---|---|
| p. 199, one-dimensional derivative criterion and Problem 6.15 | negative state derivative gives local exponential stability; positive derivative gives instability | a selected scalar stability predicate and proof bridge | adjacent criterion; proof is delegated to a problem |
| p. 200, equation (6.32) | scalar autonomous family `x' = mu*x - x^2` | one explicit real ODE encoding | candidate example only |
| p. 200, sentence after (6.32) | fixed points collide and exchange stability at `mu = 0` | branch identities and two-sided stability clauses | candidate phenomenon description, not a binder-complete theorem |
| p. 200, Problem 6.17 | asks the reader to prove the displayed example statements | a possible human proof task | not a supplied complete proof |

The same sentence after (6.32) says that there are "two stable fixed points" for nonzero `mu` and
then says they exchange stability. For the displayed vector field, the equilibria are `x = 0` and
`x = mu`; the state derivatives there are respectively `mu` and `-mu`. Under the criterion stated
on the preceding page, exactly one is stable and the other unstable for each nonzero parameter,
with their roles reversed across zero. The inspected official errata contains no text match for
this passage. This apparent typo or unresolved inconsistency prevents verbatim source admission;
intake neither corrects it by fiat nor turns its likely intended reading into the catalog target.

The observed PDF SHA-256 was
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. A 6,874-byte extract of
printed pages 199-200 had SHA-256
`72cf623f3faffe4eb6df0d1ad7ca173bb3c5157e03bd4cb07840ee2f08911e9f`. The observed official
errata PDF had SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`.
The catalog does not cite this source; no immutable source admission, complete assumption and proof
mapping, resolved correction record, or independent review is credited.

## Candidate-theorem boundary

The explicit scalar example, a general transcritical existence theorem, a smooth normal-form
classification, and a definition of the phenomenon are distinct targets. A general theorem may
need a persistent equilibrium branch and source-specific derivative, transversality, quadratic,
and locality conditions that do not occur in the catalog. A normal-form theorem additionally needs
precise coordinate and parameter-change equivalence. Conversely, proving the displayed polynomial
example would not prove either general result.

The neighboring catalog records separately name generic bifurcation theory (`THM-M-1358`),
saddle-node (`THM-M-1359`), Hopf (`THM-M-1360`), and pitchfork (`THM-M-1362`) bifurcations. This
separation forbids substituting those branch patterns or sharing their future proof credit.

## Source gate

There is no authoritative mathematical proposition selected by the repository. Before leaving
`H5`, an accountable reviewer must redirect the phenomenon gloss to one corrected exact claim,
preserve an immutable primary or authoritative source, record edition and theorem/section/page,
resolve or formally delimit the source wording issue, transcribe all incorporated definitions,
ordered binders, hypotheses, conclusion, proof boundary, and exceptional cases, audit errata,
reconcile neighboring targets, and obtain independent approval of the source-to-statement mapping.

`H5` here does not assert that transcritical bifurcation theorems are false. It records that the
repository's phrase is not a truth-valued target that a Lean kernel could check.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `ImplicitFunctionData.implicitFunction`, `IsIntegralCurve`, `Flow`,
`Function.IsFixedPt`, `HasFDerivAt`, and `ContDiff`. These are possible substrate for a future
source-selected encoding, not a transcritical statement or proof. A bounded case-insensitive search
for `bifurcat` or `transcritical` over pinned mathlib and repo-local Lean sources returned no match.
The later immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
