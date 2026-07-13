# THM-M-1481 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10826-10831` supplies exactly the title `模拟退火`, the
attribution Scott Kirkpatrick, the year 1983, the gloss `全局优化的随机方法`, importance
"high," and status `已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, ordered binder, hypothesis, conclusion, proof, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:40270-40295` repeats the gloss while explicitly leaving the formal
system, exact definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The stable ID `THM-M-1481` is repository scheduling identity, not a source identifier. The initial
generated Stage0 record used a pre-deduplication number; commit
`c61be3c80710c07c5f7626e3404e51f40ecb39a6` assigned the current ID. The target manifest and
execution DAG later introduced its rev-5.6 membership and tasks. None of these generated identities
adds mathematical content or source authority.

## Historical source lead

Scott Kirkpatrick, C. Daniel Gelatt Jr., and Mario P. Vecchi, *Optimization by Simulated
Annealing*, Science 220(4598), 671-680, 13 May 1983, DOI
`10.1126/science.220.4598.671`, PMID `17813860`, is the strong historical lead matching the
catalog attribution and year. Crossref and the NLM PubMed record were observed on 2026-07-13. An
11-page, 581,070-byte course-hosted JSTOR scan was also inspected at
`https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TemperAnneal/KirkpatrickAnnealScience1983.pdf`;
its SHA-256 is
`d0fedd367a09e978538839da68f32f91ec3f9713d1a7c7a2ac783e28e250b6b0`.
The extracted 98,776-byte text has SHA-256
`6789a7b5566f3e7e46e0029610550bdcaf0630d977f6d6cd507cd4fbe009f8d6`.
The scan carries a JSTOR personal/noncommercial-use notice and was therefore not vendored.

Pages 671-673 present a heuristic framework rather than a general theorem. Page 671 warns that
there is no guarantee that a heuristic for one NP-complete problem works for another. Page 672
gives the Metropolis rule: accept nonpositive cost changes and accept a positive change with a
Boltzmann exponential probability; it says the system evolves into a Boltzmann distribution, but
does not state the state-space, proposal, irreducibility, or limiting hypotheses needed for a
formal theorem. Page 673 describes slow staged cooling, each stage long enough to approach steady
state. Page 679 lists four design ingredients, permits schedules developed by trial and error, and
reports that numerical studies suggest good-quality results.

This inspected primary-source lead still does not establish `H0`. The catalog does not cite the
article and omits two authors; the article does not select one exact general global-optimization
proposition matching the gloss; no complete theorem/assumption/proof/errata crosswalk or independent
review exists. The publisher endpoint separately returned HTTP 403.

## Later exact-theorem lead

Bruce Hajek, *Cooling Schedules for Optimal Annealing*, Mathematics of Operations Research 13(2),
311-329, May 1988, DOI `10.1287/moor.13.2.311`, is a later statement-selection lead. Crossref's
publisher-deposited abstract says the paper gives a necessary and sufficient cooling-schedule
condition for convergence in probability to the global-minimum set; for
`T(t) = c / log(1 + t)`, it reports the threshold `c` as the suitably defined depth of the
deepest nonglobal local minimum.

The publisher body was unavailable, and no definitions, theorem locator within the article,
complete hypotheses, proof, corrections, or independent review were admitted. More importantly,
the repository says 1983 and Scott Kirkpatrick. Replacing that broad historical method entry with
Hajek's 1988 finite-setting theorem requires an explicit target decision and cannot be done
silently.

## Clause crosswalk

| Repository element | Possible source component | Required Lean component | Intake result |
|---|---|---|---|
| `模拟退火` | temperature-controlled stochastic search inspired by physical annealing | exact state/process/kernel/schedule definitions | method family only |
| "randomized" | proposal moves plus probabilistic acceptance, often time-inhomogeneous | probability space, kernel sequence, acceptance law, process construction | absent |
| "global optimization" | concentration or convergence to the set of global cost minimizers | objective, minimizer set, convergence mode, quantifier order | absent |
| Kirkpatrick / 1983 | likely Science article, actually with Gelatt and Vecchi | immutable source edition, exact passage, correction audit | strong lead; not admitted |
| later cooling theorem | schedule/barrier conditions for convergence in probability | finite landscape, graph, depth, schedule and exact conclusion | narrower lead; not source-identical |
| `已验证` | catalog status | accepted human proof and kernel receipts would be required | no H or M credit |

## Source gate

Before the target can leave `H5`, accountable reviewers must redirect it to one corrected,
truth-valued proposition; preserve an immutable primary source; freeze every definition, domain,
binder, hypothesis, conclusion, schedule and boundary case; map each source premise and proof step;
inspect corrections and errata; and justify why that proposition represents `THM-M-1481`. A
second qualified reviewer must approve the mapping. Human-proof status must then be classified
afresh rather than inherited from `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` checks generic Markov-kernel, invariant-measure, reversibility,
irreducibility, and finite-minimum interfaces. The reversible-implies-invariant theorem concerns a
single Markov kernel; it does not construct an annealing chain or prove cooling convergence. A
bounded source search found no exact simulated-annealing, annealing, cooling-schedule, or Metropolis
declaration. This is intake discovery only, not the downstream immutable anchor audit or a claim
about all Lean projects.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and statement mutations remain null. No H0, M0, R0, audit completion, or theorem completion is
claimed.
