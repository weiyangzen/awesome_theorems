# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:10453-10458` supplies exactly the title `Douady-Hubbard
theorem`, Adrien Douady and John Hubbard, 1982, the gloss `Mandelbrot set connectedness`, high
importance, and status `已验证` ("verified"). All six catalog lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record contains no definition, formula,
publication, theorem locator, premises, proof, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:38915-38940` repeats the gloss and explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent statements, axioms, machine
status, and artifact links open. Its generic closed-result and theorem-tree wording is planning
text, not source evidence. The rev-5.6 manifest preserves the catalog status only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The research inventory also contains an exact metadata duplicate at lines 1878-1883, projected as
the separate target `THM-M-0261`. That duplication does not determine which source edition or
formal encoding either target owns and grants no shared proof credit.

## Primary-source candidates

The leading historical candidate is Adrien Douady and John H. Hubbard, *Itération des polynômes
quadratiques complexes*, C. R. Acad. Sci. Paris, Série I, volume 294 (1982), pages 123-125,
zbMATH Open document `3758648`, Zbl `0483.30014`. Bibliographic discovery describes the quadratic
family, the filled Julia set, the Mandelbrot parameter set defined by boundedness of the critical
orbit, and the result that the Mandelbrot set is connected. This is a strong candidate, but the
catalog does not cite it and this intake has not admitted an immutable full text, exact French
passage, complete premise/proof mapping, errata audit, or independent review.

An expanded candidate is Douady and Hubbard's *Étude dynamique des polynômes complexes*,
Publications Mathématiques d'Orsay 84-02 and 85-04. The inspected English Orsay notes describe
results obtained in 1981-82, define `P_c(z) = z^2 + c`, define `M` by connectedness of the filled
Julia set, state that `M` is compact and connected in Chapter 1, and later derive "The set M is
connected" as Corollary 8.3(a) from Theorem 8.1's conformal isomorphism
`Phi : Complex \\ M -> Complex \\ closedUnitDisk`. The same chapter explicitly labels local
connectedness of `M` as conjectural. The web copy was used only for bounded source discovery; its
edition relationship, translation, definitions, proof boundary, corrections, and independent
review remain open, so it is not `H0`.

## Component crosswalk

| Source component | Mathematical component to freeze | Prospective Lean component | Intake status |
|---|---|---|---|
| `P_c(z) = z^2 + c` | normalized quadratic family over the complex plane | `fun z : Complex => z ^ 2 + c` | generic arithmetic substrate only; canonical term open |
| critical point `0` | the distinguished critical orbit, including iterate zero | `n |-> (f c)^[n] 0` using `Function.iterate` | iteration API probed; binder and normalization open |
| orbit does not escape | bounded critical orbit or failure to tend to infinity | `Bornology.IsBounded (Set.range ...)` or an equivalent filter/escape predicate | boundedness API probed; equivalence and boundary open |
| Mandelbrot set `M` | set of parameters satisfying the selected critical-orbit predicate | set comprehension in `Complex` | definition and source transport not frozen |
| connected | ordinary connectedness, including the source's nonemptiness convention | `IsConnected M`, possibly split into nonempty and `IsPreconnected` obligations | predicates probed; exact root not elaborated |
| conformal map `Phi` | analytic bijection of the complements, normalized at infinity | a future complex-analytic equivalence plus exact complement/topology data | source proof route only; no matching Lean interface credited |
| Corollary 8.3(a) | connectedness consequence of Theorem 8.1 | checked composition from analytic obligations to the root | pinpoint candidate; proof graph not frozen |
| local connectedness | stronger MLC claim explicitly separated from connectedness | must remain a distinct proposition | excluded from this target |
| `已验证` ("verified") | untrusted catalog metadata | no Lean declaration or proof object | explicitly rejected as evidence |

## Source gate

Before `H0`, accountable reviewers must preserve and hash an immutable primary edition, approve
the exact theorem/corollary and every incorporated definition, transcribe all assumptions and
conventions, map the 1982 note to any expanded source used for proof reconstruction, check
translation, corrections, and errata, and independently approve every row of the source-to-target
crosswalk. The duplicate target must be reconciled without merging identities or evidence by
assumption.

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks representative complex,
iteration, range, boundedness, connectedness, preconnectedness, and compactness APIs. A bounded
pinned-source and repo-local search found no exact topic declaration. This result is not a global
absence claim and not the downstream immutable anchor audit.

Before statement credit, a formal reviewer must approve one exact source-faithful Lean expression,
minimal imports, its environment and elaborated-expression fingerprints, checked transports, and
mutations for removed hypotheses, changed domain, changed binder scope, and boundary cases. Until
then the root remains `[H1, M4, R3]`; no proof search or completion claim is legal.
