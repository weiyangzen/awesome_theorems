# Source-statement crosswalk

| Claim component | Human source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Stopped generator identity | E. B. Dynkin, *Markov Processes*, Vol. I, Springer, 1965, the generator/stopping-time formula traditionally called Dynkin's formula | Root expectation equality | Primary historical monograph identified, but theorem/page, edition scan, assumptions, and errata are not yet pinned: `H2` |
| Modern generator-domain formulation | S. N. Ethier and T. G. Kurtz, *Markov Processes: Characterization and Convergence*, Wiley, 1986, Chapter 4 treatment of generators and martingale problems | Process, generator domain, and martingale bridge | Secondary formulation family identified; exact proposition and hypothesis crosswalk remain open |
| `f` and `A f` terms | Generator-domain observable and its generator image | Measurable functions and integrability proofs | Exact codomain and integral API are deliberately not invented at intake |
| Stopping time `tau` | Source-dependent bounded/localized stopping time | Filtration, stopping-time predicate, stopped process | Boundedness versus uniform-integrability/localization variant must be selected from the pinned source |
| Deterministic time | Specialize `tau` to constant `t` | Boundary theorem/test | Consequence only; it cannot replace the stopped formula |
| Martingale form | `f(X_t)-f(X_0)-integral_0^t Af(X_s) ds` | Candidate bridge to optional stopping | Equivalence needs all filtration and integrability hypotheses checked in Lean |

The repository contributes only the Chinese title `Dynkin公式` and gloss `马尔可夫过程的生成元`.
Those words underdetermine the exact theorem. This intake therefore records the conventional
stopped-process claim but does not assert exact fidelity (`H0`/`H1`) or machine eligibility.

The source-audit phase must pin immutable bibliographic artifacts and pinpoint theorem numbers or
pages, transcribe the ordered assumptions, check corrections/errata, and map each premise to the
formal statement. The statement phase must not use a deterministic-time or discrete-time analogue
as a broadened or substituted target.
