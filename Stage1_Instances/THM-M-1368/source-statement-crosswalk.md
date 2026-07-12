# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9971-9976` supplies exactly the title `Morse-Smale系统`, Marston
Smale, 1961, the gloss `结构稳定系统的特征` ("characteristics of structurally stable systems"),
importance "high," and status `已验证`. The same six lines are duplicated at
`Docs/researches/math_theorems.md:10222-10227`. Git blame attributes both uncited records to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37209-37234` repeats the gloss while explicitly leaving the target formal
system and foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic statement that a closed result is known
is not source or kernel evidence. The rev-5.6 manifest retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

The repository supplies no bibliography, theorem/page locator, system definition, ordered binders,
hypotheses, conclusion, incorporated definition chain, proof boundary, errata, or reviewer. The
gloss is also logically ambiguous: a class may be structurally stable without being an unrestricted
characterization of every structurally stable system.

## Primary-source leads

Crossref metadata for DOI `10.2307/1970311` identifies Stephen Smale, *On Gradient Dynamical
Systems*, *The Annals of Mathematics* 74(1), July 1961, starting at page 199. The fixed Scholarpedia
revision's bibliography gives the full range 199-206. The year matches the catalog, and "Stephen
Smale" makes it a plausible lead while exposing the catalog's literal "Marston Smale" first-name
discrepancy. The inspected JSTOR and Project
Euclid endpoints did not yield the full paper in this worker environment, so no theorem text,
number, complete assumptions, proof boundary, correction status, or statement equivalence was
verified. Metadata alone is not `H0` and the paper is not adopted as the root.

Later source metadata exposes a separate structural-stability lineage. J. Palis and S. Smale,
*Structural stability theorems*, *Proceedings of Symposia in Pure Mathematics* 14 (1970), pages
223-231, DOI `10.1090/pspum/014/0267603`, is a later result. J. Palis, *On Morse-Smale dynamical
systems*, *Topology* 8(4) (1969), pages 385-404, DOI `10.1016/0040-9383(69)90024-X`, is another
later lead. Their dates prevent intake from silently treating a later structural-stability theorem
as the precise content of the catalog's 1961 record.

## Inspected expository discriminator

Michael Shub's reviewed article *Morse-Smale systems*, *Scholarpedia* 2(3):1785 (2007), DOI
`10.4249/scholarpedia.1785`, was inspected at immutable revision `132702` (2013-04-24,
MediaWiki SHA-1 `b7834472e9b6267870cd897331e111fc2e97a1f6`). It defines Morse-Smale diffeomorphisms or
one-parameter groups using finitely many hyperbolic periodic orbits, coverage by their stable and
unstable manifolds, and pairwise transversality. In a separate section it states that Morse-Smale
dynamical systems are structurally stable and attributes that theorem to Palis and Smale. Its
bibliography separately lists Smale's 1961 gradient paper and the 1970 structural-stability paper.

This reviewed secondary source is useful precisely because it distinguishes a definition, a later
theorem, and the gradient/Morse-theory lineage. It cannot select the repository target, replace a
primary source, or supply `H0`.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `system` | diffeomorphism, vector field, or one-parameter flow | map, `Flow`, or manifold vector field/integral curves | time model and regularity absent |
| Morse-Smale | finite hyperbolic critical elements plus transverse stable/unstable manifolds, with variant conventions | new predicates over periodic orbits, derivatives, invariant splittings, and manifolds | definition not supplied by catalog |
| `structurally stable` | `C1`-near maps topologically conjugate, or nearby vector fields orbit equivalent | topology on systems plus conjugacy/orbit-equivalence relation | topology and equivalence absent |
| `characteristics` | definition, sufficient criterion, iff characterization, genericity, decomposition, or Morse inequalities | one exact `Prop` with fixed conclusion clauses | root conclusion absent |
| Smale / 1961 | gradient-dynamics historical lead | provenance only | full primary passage unavailable and unmapped |
| `已验证` | untrusted inventory label | no Lean declaration or proof object | no H or M credit |

## Source and neighbor gate

The statement phase must lawfully preserve one complete primary edition; select an exact result and
proof boundary; transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
and boundary case; reconcile 1961 gradient results with later Morse-Smale and structural-stability
terminology; check corrections and errata; justify the boundary against `THM-M-1366`,
`THM-M-1367`, and the hyperbolic-dynamics targets; and obtain independent review. It must then
freeze and mutation-test the identical Lean expression. Until then the canonical mathematical and
Lean targets remain null and the received catalog record remains `H5`; this classification does not
apply to properly stated Morse-Smale theorems.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
generic adjacent ODE, flow, invariant-set, periodic-point, manifold-integral-curve, and derivative
APIs. A bounded exact-topic search found no Morse-Smale or structural-stability declaration in
repo-local or pinned-mathlib Lean sources. This is discovery only; the precommitted exhaustive
anchor audit and external-project review remain open.
