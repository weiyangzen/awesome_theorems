# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1878-1883` supplies exactly the title `曼德博集合连通性`,
Adrien Douady and John Hubbard, 1982, the gloss `Mandelbrot集的连通性`, high importance, and
status `已验证` ("verified"). All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the current record blob is
`b78ec1f48495aa5747ef252665ab58e418d195e4`. It contains no definition, formula, publication,
theorem locator, premises, proof, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:7220-7245` repeats the gloss and explicitly leaves exact definitions and
premises, proof route, dependencies, equivalent statements, axioms, machine status, and artifact
links open. Its generic closed-result and theorem-tree wording is planning text, not evidence. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

The research inventory contains an exact metadata duplicate at lines `10453-10458`, projected as
the separate target `THM-M-1431`. Duplication does not choose the source edition or formal encoding
for either ID and grants no shared proof or receipt credit.

## Primary-source discovery

The historical candidate is Adrien Douady and John H. Hubbard, *Iteration des polynomes
quadratiques complexes*, C. R. Acad. Sci. Paris, Serie I, volume 294 (1982), pages 123-125,
Zbl `0483.30014`. The expanded Orsay notes cite it as `[DH1]` and are consistent with the catalog
authors and year. This intake has not admitted an immutable copy of the C. R. note, transcribed its
exact French passage, or completed a premise/proof/errata review, so it is not `H0` evidence.

An expanded discovery source is Adrien Douady and John H. Hubbard, *Etude dynamique des polynomes
complexes*, Publications Mathematiques d'Orsay 84-02 and 85-04, English notes dated 2006. The
downloaded 178-page PDF had SHA-256
`287d476f039253509a6c058dc99869a097343f8983504a13b5e3690bc739569d`. Its Chapter 1 says that
`P_c(z) = z^2 + c`, defines `K_c` by non-escape, defines `M` as the parameters for which `K_c` is
connected, and says `M` is compact and connected. Chapter 8, Theorem 8.1 constructs
`Phi : C \\ M -> C \\ D`; Corollary 8.3(a) states exactly "The set M is connected." The notes
separately label local connectedness of `M` as conjectural. This is pinpoint discovery, not accepted
`H0`: publication/translation identity, all incorporated definitions, proof boundary, corrections,
errata, and an independent reviewer remain open.

## Component crosswalk

| Source component | Mathematical component to freeze | Prospective Lean component | Intake status |
|---|---|---|---|
| `P_c(z) = z^2 + c` | normalized quadratic family over the complex plane | `fun z : Complex => z ^ 2 + c` | arithmetic substrate checked; canonical term open |
| critical point `0` and first value `c` | distinguished critical orbit and indexing convention | `(fun z : Complex => z ^ 2 + c)^[n] 0` or shifted orbit from `c` | iteration API checked; start and binder open |
| orbit does not escape | bounded critical orbit or failure to tend to infinity | `Bornology.IsBounded (Set.range ...)` or a filter/escape predicate | boundedness API checked; transport and boundary open |
| filled Julia set `K_c` | points with non-escaping orbit | future set comprehension in `Complex` | source definition located; no Lean definition frozen |
| Mandelbrot set `M` | parameters satisfying the selected critical-orbit/filled-Julia predicate | future set comprehension in `Complex` | definition and equivalence chain open |
| connected | ordinary connectedness with the intended nonempty convention | `IsConnected M`, possibly split into nonempty and `IsPreconnected` | predicates checked; exact root not elaborated |
| Theorem 8.1 | conformal isomorphism of complements | future complex-analytic equivalence and complement/topology data | source proof route only; no local interface credited |
| Corollary 8.3(a) | connectedness consequence of Theorem 8.1 | checked composition from analytic obligations to the root | exact source sentence located; proof graph not frozen |
| local connectedness | explicitly stronger conjectural claim | distinct proposition, excluded from this target | exclusion confirmed |
| `已验证` | untrusted catalog metadata | no Lean declaration or proof object | rejected as evidence |

## Formal-source discovery

Pinned Lean is `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. A bounded local search found no exact-topic
declaration. `IntakeProbe.lean` checks representative complex, iteration, boundedness, and
connectedness APIs; it states no target theorem.

Immutable remote inspection of `girving/ray` revision
`0ca7b1e746b2911557ac76f56259068cfd1423ab` found `Ray/Mandelbrot.lean` (raw SHA-256
`f5d04806d2f7ead1379ba8c97b7de60b6f22d5f3aed32f3410d824c469823db8`). It defines
`mandelbrot` by failure of the norm of the orbit starting at `c` to tend to infinity, proves
`mandelbrot_eq_multibrot`, and declares `isConnected_mandelbrot : IsConnected mandelbrot`.
Upstream uses Lean `v4.27.0-rc1` and mathlib
`725c803ee924f55342e93f2c75976051ab902b54`. The source is absent from the local dependency
closure and was not cloned, built, or kernel-checked here. It has not passed this target's exact
source mapping or downstream anchor audit, so it receives discovery credit only, not `M1` or proof
credit.

## Open source and statement gates

Before `H0`, accountable reviewers must preserve and hash an accepted primary edition, approve the
exact theorem/corollary and every incorporated definition, transcribe assumptions and conventions,
relate the 1982 note to any expanded proof source, disposition translation/corrections/errata, and
independently approve every crosswalk row. They must also reconcile `THM-M-0261` and `THM-M-1431`
without merging identity or evidence by assumption.

Before statement credit, a formal reviewer must approve one exact source-faithful Lean expression,
minimal imports, elaborated-expression and environment fingerprints, checked transports, and
mutations for a removed hypothesis, changed domain, changed binder scope, and boundary cases. Until
then the root remains `[H1, M4, R3]`; no proof or completion claim is legal.
