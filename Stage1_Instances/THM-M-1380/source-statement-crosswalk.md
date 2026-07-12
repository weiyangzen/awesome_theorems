# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10055-10060` supplies exactly the title `Jacobi定理`, Carl
Jacobi, 1837, the gloss `Hamilton-Jacobi方程的完全解`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem/page locator, formula, definition, binder, hypothesis, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37533-37558` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Inspected source-family discriminators

The strongest historical source lead located is C. G. J. Jacobi,
*Ueber die Reduction der Integration der partiellen Differentialgleichungen erster Ordnung
zwischen irgend einer Zahl Variablen auf die Integration eines einzigen Systemes gewoehnlicher
Differentialgleichungen*, *Journal fuer die reine und angewandte Mathematik* 17 (1837), pages
97-162, DOI `10.1515/crll.1837.17.97`. A GDZ scan identified as `PPN243919689_0017`,
`LOG_0012`, PURL `GDZPPN002141280`, was inspected; its 67-page PDF had SHA-256
`181ce79c830b5ca538509733f7128eef99009f3f88326de69688879bcd69fdef`. Printed page 114 discusses
a `vollstaendige Loesung` (complete solution) of a first-order PDE for a mechanical potential,
containing arbitrary constants `alpha_i`. It obtains integrals of the associated equations of
motion from parameter derivatives `partial V / partial alpha_i = beta_i`, spatial derivatives as
momenta, and a time derivative relation, with separate time-dependent and autonomous branches.
This is compelling attribution and theorem-family evidence, but the displayed formulas' complete
context, exact theorem boundary, assumptions, translation, corrections, and proof nodes have not
been fully transcribed or independently reviewed. The historical coordinate model is not silently
identified with a modern generic formulation. It is not `H0` evidence.

The permanent Encyclopedia of Mathematics revision `oldid=47166`, "Hamilton-Jacobi theory,"
was inspected as a modern statement-family discriminator. It calls Jacobi's theorem the result that
a complete integral `S(t,x,alpha)` of the Hamilton-Jacobi equation, depending on `n` parameters and
with nonzero determinant of the mixed derivative in `x` and `alpha`, yields a complete integral of
the associated Hamiltonian system through `partial_x S = p` and `partial_alpha S = beta`. It cites
L. A. Pars (1965) and V. I. Arnold (1978), but it is secondary, has no numbered theorem or proof,
and is not cited by the catalog. Its formulation is therefore not adopted as canonical.

David Tong, *Dynamics*, University of Cambridge Part II Mathematical Tripos lecture notes,
Section 4.7, "The Hamilton-Jacobi Equation," pages 121-124, was inspected as a modern discovery
source. Equations (4.184)-(4.185) state `p_i = partial W / partial q_i` and the time-dependent
Hamilton-Jacobi PDE. Equations (4.186)-(4.188) show, by differentiating the PDE, that the evolution
defined by the first Hamilton equation satisfies the second. Equations (4.189)-(4.190) separately
give the autonomous ansatz `W(q,t) = W0(q) - E*t`.

The author-hosted PDF observed on 2026-07-13 had SHA-256
`b65ba2b0399df6b02ca3850e5c69ee0255c3011a35664e80766349f521e43e80` and size 1,093,743 bytes.
The notes say that integration constants may be incorporated into a solution, but they do not call
this result "Jacobi theorem," define a complete integral, state the catalog claim as one theorem,
or supply the catalog's historical source. The catalog does not cite them. They discriminate
candidate meanings only; no immutable source admission, complete proof crosswalk, errata audit, or
independent review is credited.

Hans Samelson, "On Jacobi's Theorem in Hamilton-Jacobi Theory," *Rocky Mountain Journal of
Mathematics* 31(2), 2001, pages 619-623, DOI `10.1216/rmjm/1020171579`, supplies a directly
inspectable abstract. It describes Jacobi's theorem as saying that a complete integral of the
Hamilton PDE determines all trajectories of the Hamiltonian flow, and says its proof reduces to a
lemma about parameter derivatives of a one-parameter family of Hamilton-Jacobi solutions. This
strongly confirms the candidate family, but the complete article, exact formulas, hypotheses, and
proof boundary were not inspected. It remains `E5` discovery evidence, not a canonical statement,
proof crosswalk, or `H0` evidence.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `Jacobi定理` | complete-integral theorem, canonical-transformation theorem, trajectory theorem, or another eponym | no single declaration follows from the name | ambiguous eponym, not a unique proposition |
| Hamilton-Jacobi equation | `partial_t S + H(q, partial_q S, t) = 0`, subject to convention | derivatives on a product domain and an exact equality | domain, regularity, coordinates, and sign absent |
| "complete" | dependence on `n` independent parameters, nonsingular mixed derivative, or simply a solved PDE | parameter type/cardinality and an invertibility predicate | definition and quantifiers absent |
| "solution" | one function, a local family, a general integral, characteristic curves, or canonical coordinates | existence/uniqueness binders and exact conclusion | existence versus assumption and local/global scope absent |
| Carl Jacobi / 1837 | historical attribution | provenance metadata only | no catalog-selected primary locator |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no H or M credit |

## Candidate-to-canonical boundary

The Tong chain-rule result assumes a sufficiently differentiable PDE solution and derives Hamilton's
equations. A classical complete-integral theorem additionally parameterizes the solution family and
requires an independence condition, often expressed through a nonsingular mixed derivative. An
autonomous separated solution makes a different time-dependence assumption. None is merely a
notational spelling of the others, and no checked implications or equivalences are available at
intake.

Nor may "complete solution" be interpreted as a universal existence claim: global smooth complete
integrals can fail through singularities, caustics, topology, or lack of integrability. Conversely,
a structure that includes a complete integral as data would only restate an assumption if the
catalog intended an existence theorem.

## Source gate

There is no authoritative mathematical source selected by the repository. Before leaving `H5`, an
accountable reviewer must select or correct one exact proposition, preserve an immutable primary or
authoritative source, record edition and theorem/section/page, transcribe all incorporated
definitions, ordered binders, hypotheses, conclusion, proof boundary, and exceptional cases, audit
corrections and errata, reconcile the neighboring Hamilton-Jacobi and integrability targets, and
obtain independent approval of the source-to-statement mapping.

`H5` here does not assert that Hamilton-Jacobi theory is false. It records that the received title
and gloss do not determine a truth-valued target that a Lean kernel could check. No `H0` crosswalk
can be completed until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks `ContDiff`, `HasFDerivAt`, `fderiv`, product continuous-linear maps, and
`IsIntegralCurve`. These are possible substrate for a future source-selected encoding, not a
Hamilton-Jacobi statement or proof. A bounded case-insensitive search for `Hamilton-Jacobi`,
`HamiltonJacobi`, or `complete integral` over pinned mathlib and repo-local Lean found no exact-topic
declaration. The later immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No exact-statement
elaboration, formal absence theorem, proof, audit completion, or theorem completion is claimed.
