# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9929-9934` supplies exactly the title `叉形分岔`, attribution to
many mathematicians, the twentieth century, the gloss `对称性破缺的分岔`, importance "high," and
status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, formula, definition, binder, hypothesis, conclusion, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37047-37072` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, AMS, 2012, Section 6.5, printed page 200, was inspected as an authoritative modern
discovery source. It presents the scalar system `x' = mu*x - x^3` (equation (6.31)) and says that it
has one stable fixed point for `mu <= 0`, which becomes unstable and splits into two stable fixed
points at `mu = 0`; it names this a pitchfork bifurcation. Problem 6.17 asks the reader to draw the
phase plots and prove the example's claims. The surrounding text expressly offers prototypical
examples instead of developing a general bifurcation theory.

The author-hosted preliminary PDF had SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. A three-page
`pdftotext -f 210 -l 212 -layout` extract had 10,444 bytes and SHA-256
`04561dcd8b4a1e8fb443641acdb1c076338057325449cf8264f3cc0e1a8dd299`. The catalog does not cite
this source. Its example does not decide whether the target is that elementary scalar result or a
general symmetry-breaking theorem, and no immutable source admission, complete proof mapping, or
independent review is credited.

The official errata PDF observed during intake had SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`. A text search found no
entry keyed to pitchfork, bifurcation, equation (6.31), or printed page 200. That negative lookup
does not upgrade the source to accepted evidence; a future source admission must repeat the errata
audit and independent review against immutable inputs.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `叉形分岔` | scalar normal-form example, local theorem, equivariant branching result, or qualitative classification | no single declaration follows from the name | theorem family, not a unique proposition |
| "symmetry" | often invariance under `x -> -x`, but possibly an abstract group action | involution or group action plus equivariance predicate | group, action, and scope absent |
| "breaking" | appearance of two non-invariant, symmetry-related equilibria from a symmetric branch | branch functions, nontriviality, orbit relation, parameter-side condition | meaning and quantifiers absent |
| "bifurcation" | local branch existence, change in count or stability, or normal-form equivalence | exact `Prop`, ordered binders, local neighborhoods, genericity and nondegeneracy hypotheses | result and boundary absent |
| many mathematicians / twentieth century | broad historical context | provenance metadata only | no source or pinpoint theorem |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no H or M credit |

## Example-to-general-theorem boundary

The inspected scalar family fixes a particular polynomial, real one-dimensional phase space, real
parameter, critical value zero, supercritical sign, and a stability conclusion. A general local
pitchfork theorem instead needs a family of maps or vector fields, regularity, symmetry, a simple
critical mode or reduction, transversality, a nonzero cubic or corresponding coefficient, and a
precise local equivalence and branch conclusion. These are not alternate spellings of one target.
No checked implication or equivalence between them is available at intake.

The elementary equilibrium equation alone also does not prove the source's dynamical stability
claims. Conversely, proving stability for the specific cubic does not establish a normal-form or
equivariant branching theorem. Treating a plotted pitchfork diagram or a predicate that assumes
the branch structure as the theorem would be circular.

## Neighbor and substitution boundary

The surrounding catalog separately names generic bifurcation theory (`THM-M-1358`), saddle-node
(`THM-M-1359`), Hopf (`THM-M-1360`), and transcritical (`THM-M-1361`) bifurcations. Their different
normal forms, critical spectra, branch counts, and stability conclusions cannot be substituted.
Chaos theory (`THM-M-1363`) and structural stability (`THM-M-1366`) also remain distinct targets.

## Source gate

There is no authoritative mathematical source selected by the repository. Before leaving `H5`, an
accountable reviewer must redirect the phenomenon label to one corrected exact proposition,
preserve an immutable primary or authoritative source, record edition and theorem/section/page,
transcribe all incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary,
and exceptional cases, audit errata, justify its relation to the scalar example and all neighboring
targets, and obtain independent approval of the source-to-statement mapping.

`H5` here does not assert that pitchfork bifurcation theory is false. It records that the repository
gloss does not determine a truth-valued target that a Lean kernel could check. No H0 crosswalk can
be completed until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `deriv`, `ContDiff`, `IsIntegralCurve`, `Flow`, and `Function.IsFixedPt`. These are possible
substrate for future source-selected encodings, not a pitchfork statement or proof. A bounded
case-insensitive search for `pitchfork`, `bifurcat`, or `symmetry.?break` over pinned mathlib and
repo-local Lean sources found only an unrelated physics target's symmetry-breaking prose, with no
pitchfork or bifurcation occurrence. The later immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
