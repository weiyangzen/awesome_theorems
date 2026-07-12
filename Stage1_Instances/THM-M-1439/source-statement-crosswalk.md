# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10509-10514` supplies exactly the title `Lyubich证明`, Mikhail
Lyubich, 1999, the gloss `Feigenbaum猜想的解析证明`, importance "high", and status `已验证`. Git
blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no theorem statement,
bibliography, definitions, assumptions, quantifiers, conclusion, or proof boundary.

`Docs/Stage0_Blueprint.md:39131-39156` repeats the gloss while leaving the formal system,
foundation, background, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generated assertion that a closed
result exists is not primary-source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The adjacent records matter: `THM-M-1437` is `Feigenbaum普适性` (Feigenbaum universality), and
`THM-M-1438` is Lanford's computer-assisted proof. Intake may not collapse those roots into this
proof-label record or borrow their eventual evidence.

## Inspected primary-source lead

Mikhail Lyubich, *Feigenbaum-Coullet-Tresser universality and Milnor's Hairiness Conjecture*,
*Annals of Mathematics* (2) **149** (1999), no. 2, 319-420, DOI `10.2307/120968`, is an exact
bibliographic and temporal match. The author-posted arXiv version `math/9903201v1` was inspected as
a 102-page immutable PDF (SHA-256
`8e32496391ceed7fa03e5ac5846ded6ecff1b379a01032444fac05c649bca9e0`).

The abstract says that the paper proves the Feigenbaum-Coullet-Tresser conjecture on hyperbolicity
of the bounded-type renormalization transformation and thereby gives the first computer-free proof
of universal parameter scaling. Pages 320-321 describe the conjecture as uniqueness and
hyperbolicity of a renormalization fixed point, then extend it to bounded combinatorics. Pages
321-323 separately state the Hyperbolicity, Hairiness, Self-Similarity, Universality, HD, and QC
theorems. In particular, the Hyperbolicity Theorem has three material conclusions, while the
Universality Theorem is a distinct asymptotic scaling statement.

This primary source identifies the result family and confirms why the catalog gloss is ambiguous;
it does not itself authorize this worker to correct the catalog root. An accountable, independent
source review must select the canonical theorem and map its full definition chain, assumptions,
proof dependencies, corrections, and errata before H0 or statement closure.

## Component crosswalk

| Repository element | Primary-source component | Required Lean component | Intake assessment |
|---|---|---|---|
| `Lyubich证明` | a proof contribution, not a proposition | one exact canonical `Prop` | subject is proof-labelled; root open |
| `Feigenbaum猜想` | in the paper, chiefly hyperbolicity of a renormalization transformation, with stationary and bounded-type forms | exact operator, domain, invariant set, hyperbolic splitting and quantifiers | catalog does not choose a form |
| `解析证明` | computer-free proof using complex-analytic renormalization machinery | proof provenance and dependency graph, not part of the theorem type unless explicitly encoded | proof method cannot identify the target |
| Mikhail Lyubich / 1999 | exact-match Annals/arXiv primary paper | immutable edition and source identity | strong discovery identity; independent admission open |
| `已验证` | untrusted inventory label | reviewed source packet and kernel receipt would be required | no H or M credit |

## Candidate-root crosswalk

| Candidate root | Material content | Why not canonical at intake |
|---|---|---|
| Introduction Hyperbolicity Theorem | compact invariant renormalization horseshoe; shift conjugacy and uniform hyperbolicity; stable hybrid leaves; analytic transverse unstable leaves | multi-clause theorem with a substantial definition chain not reproduced by the catalog |
| Stationary Feigenbaum case | a renormalization fixed point and its hyperbolicity/one-dimensional unstable direction | narrower than the paper's bounded-type headline and overlaps the Lanford boundary |
| Introduction Universality Theorem | transverse analytic family, unique nearby parameter sequence, universal asymptotic scaling | consequence of hyperbolicity and closest to the word "universality", but logically distinct |
| Section 9 bounded-type universality | exponential parameter convergence and transverse-family ratio estimate | different statement and constants from the stationary theorem |
| Whole paper/result package | hyperbolicity plus hairiness, self-similarity, universality, HD, and QC results | a conjunction manufactured from multiple named theorems, not one catalog statement |

## Source gate

Before the target can leave `H5`, an accountable reviewer must issue a source correction selecting
one truth-valued proposition, preserve the primary edition, identify exact theorem/page and every
incorporated definition, transcribe ordered binders, hypotheses and all conclusion clauses, map
supporting assumptions and proof dependencies, check corrections and errata, and justify the
boundary against `THM-M-1437` and `THM-M-1438`. A second qualified reviewer must approve that
mapping. The corrected proposition's H state must then be classified afresh.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks generic complex, analytic, iteration, semiconjugacy, compactness, connectedness, and
continuous-linear-map APIs. A bounded source-name search found no Feigenbaum/Coullet/Tresser,
quadratic-like-germ, hybrid-class, Mandelbrot-copy renormalization, or target Lyubich declaration in
repo-local or pinned mathlib Lean sources.

The canonical module, declaration/expression, elaborated-expression hash, checked transports, and
statement mutations remain null. The probe and search are intake feasibility evidence only, not a
complete formal-candidate audit and not H0, M0, or readable-proof closure.
