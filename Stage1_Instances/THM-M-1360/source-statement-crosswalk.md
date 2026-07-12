# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9915-9920` supplies exactly the title `Hopf bifurcation`, Eberhard
Hopf, 1942, the gloss `bifurcation in which periodic solutions arise`, importance `high`, and status
`verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:36993-37018` repeats the metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 target manifest preserves `verified`
only as untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no bibliography, theorem or page locator, differential equation, ordered
binders, hypotheses, conclusion, incorporated definitions, proof boundary, translation provenance,
errata, or reviewer. Its gloss therefore does not select one stable proposition.

## Historical source lead

A zbMATH Open record (`Zbl 0063.02065`, document `3104860`) identifies Eberhard Hopf,
*Abzweigung einer periodischen Loesung von einer stationaeren Loesung eines Differentialsystems*,
*Berichte ueber die Verhandlungen der Saechsischen Akademie der Wissenschaften zu Leipzig,
Mathematisch-Naturwissenschaftliche Klasse* 94, no. 1, pages 3-22, published 1943. An inspected
20-page scan has SHA-256
`f34a1b081ead783d8026c0f2f737ac342ac2bf55a9c6f706e921971728c9072f`; its title page records a
session on 19 January 1942, which is compatible with the catalog's date but also exposes a
presentation/publication distinction.

Visual inspection of the opening pages shows an analytic real-parameter differential-system
setting, an analytic stationary branch, exactly two purely imaginary critical characteristic
exponents at the distinguished parameter, and a nonzero real-part crossing derivative. Its theorem
describes a family of real periodic solutions, limiting period, isolation below a period cutoff,
and one-sided behavior. This is a strong primary-source-family lead, but the repository does not
cite this scan or identify its exact clause as the target. No complete transcription, translation,
assumption/proof-node mapping, correction search, immutable repository admission, or independent
review is supplied, so it is not `H0` and is not adopted as the canonical claim.

## Modern discriminators

Yuri A. Kuznetsov's reviewed Scholarpedia article, "Andronov-Hopf bifurcation," 1(10):1858
(2006), DOI `10.4249/scholarpedia.1858`, was inspected as an expository discriminator. The captured
HTML has SHA-256 `d6905eb073975f9260c22ebfa72279c234703ad3a2447548859fb80e4fc69482`.
It starts with a smooth one-parameter ODE on `R^n`, a nearby equilibrium family, and a conjugate
eigenvalue pair reaching the imaginary axis. Its two-dimensional normal-form result additionally
requires nonzero first Lyapunov coefficient and transversal crossing, distinguishes stable
supercritical from unstable subcritical cycles, and its higher-dimensional account uses a
two-dimensional center manifold and excludes other imaginary-axis spectrum. These stronger clauses
are not present in the catalog gloss.

Tadashi Kawanago, "The Hopf bifurcation theorem in Banach spaces," arXiv `2303.18000v3`, was
inspected as a materially different primary specialist variant. The 17-page PDF has SHA-256
`f999383e5358d9424080407302e23cac131ebb18ee978c4b378aba033684216b`. Theorem 2.1 works with a
closed linear operator on a real Banach space, periodic Hoelder function spaces, a `C^2` induced
nonlinearity map, simple eigenvalues at `+i` and `-i`, transversality, all-harmonic
nonresonance, and a resolvent
bound; it produces a locally exhaustive branch modulo phase shift. It explicitly targets settings
where no compact resolvent or generated `C0` semigroup is assumed. This is not the same formal
contract as the finite-dimensional normal-form theorem.

These sources discriminate the family but do not select the repository target. The historical
paper is a plausible source for the attribution; Scholarpedia is secondary exposition; and the
Banach-space paper is primary only for its own variant.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| differential system | smooth or analytic ODE on `R^n`, Banach evolution equation, PDE, or delay equation | state type, scalar field, vector field/operator, domain, solution predicate | all exact choices absent |
| stationary solution | fixed equilibrium or parameterized equilibrium branch | zero of vector field plus regularity in the parameter | branch and normalization absent |
| bifurcation parameter | real local parameter with oriented crossing | neighborhood, distinguished value, eigenvalue continuation, derivative | domain and crossing convention absent |
| imaginary pair | simple conjugate eigenvalues, possibly with other spectrum | complexification, eigenvalue/spectrum predicate, multiplicity and gap | simplicity and remaining spectrum absent |
| periodic solutions | parameterized functions, flow orbits, or equivalence classes modulo phase | `Function.Periodic`, integral-curve predicate, nonconstancy and period | carrier, period, phase quotient absent |
| arise | existence, branch regularity, local exhaustiveness, uniqueness, or normal-form equivalence | quantified neighborhoods and branch map | conclusion strength absent |
| side and stability | supercritical/subcritical; stable/unstable cycle and equilibrium | Lyapunov coefficient, orbital stability, parameter orientation | not mentioned |
| 1942 | presentation/session date or historical discovery date | provenance only | publication/source edition not fixed |
| `verified` | untrusted inventory label | no declaration or proof body | explicitly rejected as evidence |

## Neighbor and variant boundary

The immediately adjacent catalog records separately own general bifurcation theory, saddle-node,
transcritical, and pitchfork bifurcations. They do not determine the Hopf root. Scholarpedia also
distinguishes the discrete-time Neimark-Sacker analogue and infinite-dimensional PDE/DDE variants.
A special planar complex normal form, a high-dimensional center-manifold suspension, a Banach-space
branch theorem, and a degenerate theorem have different premises and conclusions; none may be
silently substituted for the terse catalog phrase.

## Required source admission

The statement phase must preserve and hash one lawful complete source edition, select an exact
result and proof boundary, transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, and boundary case, reconcile the 1942/1943 provenance, check translations, corrections,
and errata, and obtain independent review. It must then freeze and mutation-test the same exact Lean
expression. Until then the canonical mathematical and Lean targets remain null and the source
classification remains `H1`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic periodicity, ODE, flow, differentiability, eigenvalue, and spectrum APIs. A bounded
case-insensitive exact-topic search found no Hopf-bifurcation target in repo-local Lean or pinned
mathlib. This is discovery only; the precommitted exhaustive anchor audit and external-project
review remain open.
