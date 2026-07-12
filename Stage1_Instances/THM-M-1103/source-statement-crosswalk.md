# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md` supplies the title "Hamiltonian Monte Carlo", Radford Neal, the
year 2011, and only the phrase "HMC algorithm". `Docs/Stage0_Blueprint.md` repeats that phrase while
leaving definitions, assumptions, proof route, axioms, and machine artifacts open. Its `已验证`
field is explicitly untrusted under rev-5.6. These records identify a method, not a theorem.

## Candidate primary expository source

- Radford M. Neal, "MCMC Using Hamiltonian Dynamics", in Steve Brooks, Andrew Gelman, Galin L.
  Jones, and Xiao-Li Meng (editors), *Handbook of Markov Chain Monte Carlo*, Chapman & Hall/CRC,
  2011, Chapter 5, pages 113-162.

This chapter matches the repository author and year and is the primary expository source candidate
for the algorithmic target. The exact proposition, page, definitions, assumptions, edition text,
and correction/errata history have not been independently inspected in this intake. The citation is
therefore a discovery anchor only and supplies no `H0` evidence.

## Crosswalk

| Repository/source element | Mathematical information currently fixed | Required Lean component | Intake result |
|---|---|---|---|
| "Hamiltonian Monte Carlo" | an MCMC method using augmented Hamiltonian dynamics | measurable phase space and an explicit Markov kernel | subject identified; theorem open |
| target distribution | desired marginal law for position | probability measure or normalized density and reference measure | required; conventions open |
| momentum augmentation | auxiliary law and kinetic energy | product measure, momentum distribution, Hamiltonian | likely method component; exact form open |
| Hamiltonian trajectory | deterministic proposal evolution | ODE flow or a discrete integrator | exact/discrete choice open |
| leapfrog/reversible integrator | practical approximate dynamics | finite-step map with checked reversibility and volume behavior | inclusion depends on selected result |
| Metropolis correction | accept/reject using energy change | measurable acceptance probability and corrected kernel | likely method component; convention open |
| correctness | invariance, reversibility, or convergence | one exact equality, detailed-balance identity, or limit theorem | conclusion unresolved |
| `已验证` | repository screening metadata | accepted source review or kernel receipt | no credit |

## Source and formal boundary

The source phrase does not determine whether the intended theorem concerns exact-flow measure
preservation, correctness of the Metropolized numerical proposal, a special Gaussian calculation,
or asymptotic convergence. These statements have different assumptions and conclusions; choosing
one merely because it is easy to encode would substitute mathematics.

No target-specific legacy slot or Lean module is identified by the manifest. A narrow repository
and pinned-mathlib name search during intake found no declaration specifically named for HMC; that
negative name search is not the required immutable anchor audit and does not rule out reusable
Hamiltonian, ODE, measure-preservation, or Markov-kernel infrastructure under other names.

Before `H0`, an independent reviewer must inspect a stable source copy, select and pinpoint the
exact theorem/result, record every referenced definition and assumption, check corrections, and
approve a row-by-row map to the canonical mathematical and Lean statements. The later anchor audit
must separately record exact modules, declarations, immutable revisions, proof bodies, axioms,
placeholders, and dependency feasibility for every formal candidate.
