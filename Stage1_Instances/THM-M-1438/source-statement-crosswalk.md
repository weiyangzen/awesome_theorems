# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10502-10507` supplies exactly the title `Lanford证明`, Oscar
Lanford, 1982, the gloss `Feigenbaum猜想的计算机辅助证明`, importance "high," and status
`已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no citation, theorem number, definitions, binders,
hypotheses, or conclusion accompanies them.

`Docs/Stage0_Blueprint.md:39104-39129` repeats the gloss while leaving the exact definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and resets the target
to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Primary-source meaning | Required Lean component | Intake result |
|---|---|---|---|
| `Lanford证明` | a named proof/source family, not a numbered proposition | one exact declaration or explicitly selected conjunction | open |
| "Feigenbaum conjecture(s)" | the paper says "essentially all" of a family of conjectures | exact selected source clauses and composition | open |
| "computer-assisted proof" | rigorous finite-precision estimates with interval arithmetic, plus analytic deductions | certificate data, checker semantics, error bounds, TCB, and composition | no computation credit |
| Oscar Lanford / 1982 | source attribution and year | immutable edition, locator, incorporated definitions, errata, and review | plausible primary source inspected; independent review open |
| `已验证` | untrusted inventory metadata | accepted human-source and kernel receipts would be required | no H or M credit |

The singular Chinese gloss must not collapse the source's plural theorem suite into an unspecified
conjunction.

## Primary source

Oscar E. Lanford III, "A computer-assisted proof of the Feigenbaum conjectures," *Bulletin (New
Series) of the American Mathematical Society* 6(3), May 1982, DOI
`10.1090/S0273-0979-1982-15008-X`. Crossref reports pages 427-435. The inspected 638627-byte
publisher PDF has eight scan pages, SHA-256
`210cb7c561788fd8fab5fb2d5f7158619ef698a64fbb2ff0b5750185192ef045`, and visibly ends on
printed page 434; the next article in the issue starts on p. 435. Crossref's `427-435` is retained
as boundary-style metadata rather than physical article pagination. A bounded Crossref check
exposed no relation or update-to record, but that is not a full errata audit. No errata or
independent source review has been accepted.

The paper's printed pp. 427-429 define the map space, renormalization domain, operator, analytic
function spaces, bifurcation surface, and quadratic family used by its numbered results. Because
OCR is imperfect for formulas and Greek symbols, a later statement freeze must transcribe and
independently compare the visual source rather than treating extracted text as authority.

## Numbered-clause crosswalk

| Source locator | Source clause | Lean obligations if selected | Status |
|---|---|---|---|
| Theorem 1, p. 428 | an even analytic fixed point `g` exists on `{z : C \| \|z\| < sqrt(8)}`; its restriction is fixed by `T`; its Schwarzian derivative is negative on the real interval | encode the map space, domain, `T`, complex analyticity, restriction, fixed point, derivatives, and strict Schwarzian sign | candidate only |
| Proposition 2, p. 428 | neighborhood, smoothness, codomain, and compact-derivative infrastructure around `g` | encode the analytic Banach spaces, neighborhood, differentiability, Fréchet derivative, and compactness | supporting candidate only |
| Theorem 3, p. 428 | `DT(g)` is hyperbolic with a one-dimensional expanding subspace and a positive expanding eigenvalue | encode the exact Banach subspace, spectrum and unit circle, invariant splitting, dimension, simplicity, and positivity | candidate only |
| Theorem 4, p. 428 | `T^j g_j^*` belongs to the simple period-doubling surface for a positive integer `j` and source-specified `g_j^*` on the chosen local unstable manifold | encode invariant manifolds, starred point, bifurcation surface, iterate, and membership | candidate only |
| Theorem 5, p. 429 | near a parameter in the stated interval the quadratic-family point is in the domain of `T^j`, and its iterated curve crosses the local stable manifold transversally | encode the family, domain of the iterate, neighborhood quantifier, stable manifold, parameter bounds, iterate, and transversality | candidate only |
| Estimates 1 and 2, pp. 430-431 | strict operator and residual bounds imply fixed-point existence and hyperbolicity | encode exact coefficients, norms, interval enclosures, roundoff control, checker, and deductions | computation/proof boundary only |

The source states that Estimates 1 and 2 lead to Theorems 1 and 3 and that cone constructions
facilitate Theorems 4 and 5. On p. 433 it says a minimal set of estimates for Theorems 1 and 3
could be checked by hand with a nonprogrammable calculator. That observation neither selects the
catalog root nor constitutes Lean kernel evidence.

## Scope caveat inside the source

Immediately after Theorem 4, the paper says a transversal version of that unstable-manifold
crossing is almost certainly true but was not proved. Theorem 5 separately states a transversal
crossing for the quadratic-family curve and the stable manifold. These must not be conflated.

## Source gate

Before `S56-M-1438-STATEMENT` can freeze a canonical target, an accountable reviewer must select
one numbered theorem or exact conjunction, identify every incorporated definition and supporting
clause, retain the physical and metadata pagination boundary and audit any errata, transcribe all binders, hypotheses, conclusions,
and boundary conditions, and justify the relationship to neighboring `THM-M-1437` and
`THM-M-1439`. An independent qualified reviewer must approve that mapping before H0 is possible.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded name searches
over repo-local Lean and pinned mathlib found no matching Lanford/Feigenbaum theorem or
period-doubling renormalization development. `IntakeProbe.lean` confirms only adjacent general APIs
for analyticity, fixed points, continuous linear maps, compact operators, and spectra.

No canonical module, declaration or expression, expression hash, environment fingerprint, checked
alternate encoding, source-specific certificate, proof body, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.
