# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:2027-2032` records:

- title: `切比雪夫不等式`;
- attribution: Pafnuty Chebyshev;
- year: 1867;
- gloss: `随机变量偏离期望的概率上界` (an upper bound on the probability that a random variable
  deviates from its expectation);
- importance: high;
- untrusted formalization status: `已验证`.

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula, ordered
binders, assumptions, definitions, proof boundary, correction history, reviewer, or formal
artifact. `Docs/Stage0_Blueprint.md:7792-7817` repeats the probabilistic gloss while explicitly
leaving the formal system, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. These records establish target identity but
not H0, an exact proposition, or proof evidence.

## Duplicate catalogue record

`Docs/researches/math_theorems.md:7245-7250` separately records `THM-M-0992` with the same title,
attribution, year, importance, status, and the near-identical gloss `偏离期望的概率上界`. The target
manifest places it in probability theory and gives it the legacy slot `S1-M-272`; `THM-M-0282`
has no legacy slot and remains categorized as real analysis. Category and legacy scheduling do not
override either literal source statement.

The existing `THM-M-0992` crosswalk says that `THM-M-0282` is the deterministic sum inequality.
No supporting repository source was located, and the claim contradicts the quoted authoritative
row. It is therefore rejected as a scope authority. Whether the two probability entries should be
deduplicated or deliberately maintained as distinct encodings is a master-owned catalogue decision
and a hard statement-identity blocker for this intake.

## Inspected human-source lead

P.-L. de Tchebychef, *Des valeurs moyennes*, *Journal de Mathématiques Pures et Appliquées*, second
series 12 (1867), printed pages 177-184, French translation from Russian by N. de Khanikof, was
inspected through NUMDAM's Gallica/BNF scan. The retrieved 9-page, 498,189-byte PDF has SHA-256
`e651494a4b2710e4c81cc10be402c230507043aae9dca4575eb17bc93f141f02` and is available from
`https://www.numdam.org/item/JMPA_1867_2_12__177_0.pdf`.

Printed page 177 defines mathematical expectation for a discrete quantity and states an interval
probability theorem for a sum `x + y + z + ...`, using the expectations of the quantities and their
squares. The interval is centered at the sum of the expectations and scaled by the square root of
the sum of second moments minus squared expectations; its probability is greater than
`1 - 1 / alpha^2`. The proof occupies printed pages 177-182. Printed pages 182-183 derive the
arithmetic-average form, page 183 states convergence in probability under uniformly bounded first
and second moments, and page 184 gives Bernoulli's theorem as a special case.

This inspection strongly confirms that the source family is probabilistic and does not support the
deterministic similarly-sorted-sums reinterpretation. It does not yet prove that the catalogue's
short gloss selects a single-variable modern variance theorem rather than the historical sum or
average theorem.

The printed theorem calls the quantities arbitrary, but pages 178-181 enumerate joint cases with
product weights `p_lambda q_mu r_nu ...`; the proof therefore uses mutual independence without
stating it. The unrestricted sum theorem is false for dependent quantities, for example two copies
of the same nonconstant centered random variable. The theorem also says the bound holds for every
`alpha`, while the displayed interval ordering and `1 / alpha^2` require its positive/nonzero domain
to be fixed. Its conclusion is a strict lower bound on an inside-interval event; transport to
mathlib's non-strict upper bound on a closed tail requires an exact complement and event-boundary
audit.

The French item is a translation from Russian by N. de Khanikof and says it is extracted from
*Recueil des Sciences mathématiques*, volume II. The Russian original/translation relationship,
all incorporated definitions, corrections and errata, and historical priority genealogy including
Bienayme must be audited rather than assuming uncontested 1867 priority. These issues, the modern
measure-theoretic transport, proof-node crosswalk, and absent independent review keep the source at
`H1`, not H0. The single-variable specialization avoids the hidden independence defect but still
needs an approved source-to-catalogue selection.

## Clause crosswalk

| Catalogue clause | Human/source question | Prospective Lean surface | Intake decision |
|---|---|---|---|
| random variable | probability-space, codomain, measurability, and moment premises absent | `X : Omega -> Real`, `[IsProbabilityMeasure mu]`, `MemLp X 2 mu`, or a weaker measurability package | probability family fixed; binders open |
| expectation | source definition and existence convention absent | `mu[X]` / Bochner integral | exact premise and notation transport open |
| deviation probability | threshold, strictness, and event convention absent | `mu {omega | c <= abs (X omega - mu[X])}` | closed two-sided event is a candidate only |
| upper bound | formula omitted | `ENNReal.ofReal (variance X mu / c ^ 2)` or `evariance X mu / c ^ 2` | real versus extended variance open |
| 1867 attribution | NUMDAM/Gallica French translation and printed pages 177-184 inspected | no Lean content | Russian original/translation, Bienayme priority, modern assumptions, errata, node map, and independent review open |
| `已验证` | no evidence accompanies the label | no declaration selected | no proof credit |

## Pinned Lean candidates, not credited

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Moments.Variance` contains:

- `ProbabilityTheory.meas_ge_le_variance_div_sq`: for a finite measure, a real-valued `X` with
  `MemLp X 2 mu`, and `0 < c`, bounds the closed deviation event by
  `ENNReal.ofReal (variance X mu / c ^ 2)`. For source correspondence it must at least be
  specialized to a probability measure; its unnormalized integral is not the catalogue's
  probabilistic expectation for a general finite measure;
- `ProbabilityTheory.meas_ge_le_evariance_div_sq`: for an almost-everywhere strongly measurable
  real-valued `X` and nonzero `c : NNReal`, gives the related extended-variance bound.

`IntakeProbe.lean` verifies that both declarations elaborate in the existing pinned environment
and records their axiom reports. This is adjacent API evidence only. Source identity, exact target
selection, normalized expression, checked transports, terminal proof-body provenance, dependency
and trust closure, and acceptance remain downstream.

The repository's historical `S1_M_272.lean` and the current `THM-M-0992` statement use these APIs.
They are discovery evidence for the duplicate theorem family, not inherited state for
`THM-M-0282`.

## Required closure

Before H0 or the Lean statement gate, an accountable reviewer must approve a lawful immutable
source edition and pinpoint locator, every premise and definition, exact conclusion and proof
boundary, hidden independence and `alpha` domains, Russian-original/translation and priority
genealogy, correction/errata disposition, and the mapping to one unambiguous target ID. A formal
reviewer must then encode that same proposition with minimal pinned imports, freeze the
elaborated expression and environment fingerprints, compile every credited transport, and execute
all required statement mutations.
