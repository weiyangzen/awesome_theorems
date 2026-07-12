# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9901-9906` supplies exactly the title `分岔理论`, attribution to
many mathematicians, the twentieth century, the gloss `参数变化导致的定性变化`, importance "high,"
and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, formula, definition, binder, hypothesis, conclusion, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:36939-36964` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, AMS, 2012, Section 6.5, printed pages 199-200, was inspected as an authoritative
modern discovery source. It explains that small parameter changes may cause large qualitative
changes and calls their systematic study bifurcation theory. It then presents separate pitchfork,
transcritical, and saddle-node scalar ODE examples and observes, by the implicit-function theorem,
that a local change in the number of fixed points can occur only where both `f(x0, mu0) = 0` and
the state derivative vanishes. The author expressly says that he will not develop the theory there.

The author-hosted preliminary PDF had SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. A two-page
`pdftotext -f 210 -l 211 -layout` extract had 6,874 bytes and SHA-256
`72cf623f3faffe4eb6df0d1ad7ca173bb3c5157e03bd4cb07840ee2f08911e9f`. The catalog does not
cite this source. Its field description, examples, and necessary condition do not select one
omnibus proposition, and no immutable source admission, complete assumption and errata mapping,
or independent review is credited.

The official errata PDF observed during intake had SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`. A text search found no
entry keyed to bifurcation, printed pages 199-200, or equations (6.31)-(6.33). That negative lookup
does not upgrade the source to accepted evidence; a future source admission must repeat the errata
audit and independent review against immutable inputs.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `分岔理论` | a broad field containing many local and global results | no single declaration follows from a field name | not a stable proposition |
| "parameter variation" | a family of equations, maps, vector fields, or flows over a parameter space | parameter type, system family, domains, regularity, distinguished value | all absent |
| "qualitative change" | loss of equivalence, changed number or stability of invariant objects, new periodic orbit, or other behavior | a source-defined equivalence and invariant-object predicates | meaning and direction absent |
| bifurcation | value, point, branch, diagram, normal form, or classification theorem | exact `Prop`, ordered binders, genericity and nondegeneracy hypotheses | object and result absent |
| many mathematicians / twentieth century | broad historical context | provenance metadata only | no source or pinpoint result |
| `已验证` | untrusted inventory field | inspectable source proof and kernel receipt would be required | no H or M credit |

## Neighbor and substitution boundary

The immediately following catalog records separately name saddle-node (`THM-M-1359`), Hopf
(`THM-M-1360`), transcritical (`THM-M-1361`), and pitchfork (`THM-M-1362`) bifurcations. That
separation is affirmative evidence that none of these familiar codimension-one theorems may be
silently selected as the root of `THM-M-1358`. Chaos theory (`THM-M-1363`) and structural
stability (`THM-M-1366`) also remain distinct topics.

A definition of bifurcation, an equilibrium persistence lemma, a normal-form calculation, a
genericity statement, and a local or global classification theorem have different hypotheses and
conclusions. A numerical bifurcation diagram establishes none of them under the rev-5.6 proof
standard. The catalog chooses no member or conjunction of this family.

The gloss has no quantifier. A universal reading fails on a constant family, an existential reading
needs a chosen example or system, and a definitional reading only names a bifurcation. Rewriting it
as any one of those, or as a persistence, necessary-condition, or classification theorem, would
change rather than transcribe the source.

## Source gate

There is no authoritative mathematical source selected by the repository. Before leaving `H5`, an
accountable reviewer must redirect the topic label to one corrected exact proposition, preserve an
immutable primary or authoritative source, record edition and theorem/section/page, transcribe all
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, and exceptional
cases, audit errata, justify the relationship to every neighboring bifurcation target, and obtain
independent approval of the source-to-statement mapping.

`H5` here does not assert that bifurcation theory or its standard theorems are false. It records
that the repository's field label and phenomenon description are not a truth-valued target that a
Lean kernel could check. No H0 source crosswalk can be completed until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `ImplicitFunctionData.implicitFunction`, `IsIntegralCurve`, `Flow`,
`Function.IsFixedPt`, `HasFDerivAt`, and `ContDiff`. These are possible substrate for future
source-selected encodings, not a bifurcation statement or proof. A bounded case-insensitive search
for `bifurcat` over pinned mathlib and repo-local Lean sources returned no match. The later immutable
formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
