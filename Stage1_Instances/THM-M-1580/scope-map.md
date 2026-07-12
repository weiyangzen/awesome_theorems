# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1580`, the title `香农噪声信道编码定理`, the gloss
`信道编码的存在性`, attribution to Claude Shannon, and the year 1948. Importance `high` and
status `已验证` are catalog metadata, not human-source or kernel evidence.

The title and gloss identify the reliable-communication result family but not one truth-valued
root. A later statement phase may select a proposition only from an immutable, independently
reviewed source mapping and must preserve the neighboring and duplicate-record boundaries.

## Candidate interpretations not credited

1. Shannon 1948, Section 13, Theorem 11 as a complete source-channel theorem, including its
   below-capacity coding existence, above-capacity equivocation achievability, and converse.
2. Only Theorem 11's reliable-coding existence clause, after resolving its printed `H <= C`
   boundary against the proof's strict rate inequality.
3. Shannon 1948, Theorem 12: for fixed nontrivial error bound `q`, the asymptotic rate of the
   largest reliably distinguishable equal-probability signal subset equals channel capacity.
4. The modern finite discrete memoryless channel theorem: every rate strictly below
   mutual-information capacity admits block codes whose decoding error tends to zero.
5. A strong or weak converse, a source-channel separation theorem, or a conjunction of direct and
   converse claims.

These have different domains, binders, error notions, boundary behavior, and proof obligations.
None is selected, asserted, or credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact theorem number, edition, incorporated definitions, proof boundary, and whether a
  historical or modern formulation is canonical;
- a source-channel theorem versus a channel-code theorem, and whether separation is part of the
  target or a dependency;
- finite-state channels with memory, stationary memoryless channels, or another channel class;
- input/output alphabets, nonemptiness and finiteness, measurable structures, state space,
  transition probabilities, initial state, stationarity, and ergodicity assumptions;
- source alphabet and process, entropy-rate existence, time/symbol normalization, and whether the
  source is fixed or quantified;
- capacity as Shannon's maximum information rate, a supremum of mutual information, or an
  operational limit, including logarithm base and whether the optimum is attained;
- code shape, deterministic or stochastic encoder, block length, message-set size, decoder,
  allowed delay, common randomness, feedback, and any cost constraint;
- symbol-error frequency, average or maximal block error, equivocation, almost-sure or expected
  error, and their checked relationships;
- strict `R < C`, printed `H <= C`, equality at capacity, or an epsilon/backoff formulation;
- whether existence holds for some block length or all sufficiently large lengths, the exact
  quantifier order for rate and error tolerances, and asymptotic limit versus limsup/liminf; and
- every universe, ordered binder, hypothesis, conclusion, alternate encoding, and boundary case.

## Degenerate and boundary cases

The selected source must resolve empty or singleton input, output, source, state, and message
alphabets; zero-capacity and noiseless channels; deterministic, completely noisy, reducible, or
nonergodic channels; zero entropy sources; unattained capacity suprema; rate zero, negative rate,
exact equality with capacity, and rates above capacity; block lengths zero and one; message sets of
size zero or one; error tolerance zero, one, or outside the probability interval; zero-probability
transitions; logarithm of zero; maximum versus supremum; decoder ties; and average-to-maximal-error
expurgation.

## Neighbor and substitution exclusions

- `THM-M-1577` (information theory), `THM-M-1578` (Shannon entropy), `THM-M-1579` (channel
  capacity), and `THM-M-1581` (noiseless coding theorem) are separate roots and provide no
  inherited statement or proof credit.
- The uncataloged Stage0 computer-science records `THM-C-0362` (channel coding theorem),
  `THM-C-0363` (noisy-channel coding theorem), `THM-C-0366` (capacity converse), and
  `THM-C-0367` (joint source-channel coding) are boundary evidence, not rev-5.6 instances or
  substitutes.
- Binary entropy, Kullback-Leibler divergence, a Markov-kernel structure, Hamming distance,
  Kraft-McMillan, or existence of a capacity-achieving input distribution is substrate, not a
  reliable-code existence theorem.
- A structure or hypothesis that stores the desired encoder, decoder, reliability, or capacity
  result provides no proof.
- A binary symmetric channel example, repetition code, finite computation, simulation, numerical
  optimizer, or unchecked external declaration cannot replace a source-selected general theorem.
- The untrusted `已验证` label and API probe supply no source-fidelity or proof credit.

## Formal boundary

Pinned mathlib exposes probability mass functions, Markov kernels, KL divergence and its chain
rule, binary entropy, uniquely decodable source codes, and Hamming distance. It does not currently
expose a located mutual-information, channel-capacity, block-code reliability, or Shannon
noisy-channel theorem API under the bounded intake search. The probe authenticates adjacent
interfaces only and neither defines nor proves the target.
