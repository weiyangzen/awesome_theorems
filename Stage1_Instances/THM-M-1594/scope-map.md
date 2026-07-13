# Scope map

## Received target

| Field | Frozen intake value | Consequence |
|---|---|---|
| ID | `THM-M-1594` | Stable repository identity only |
| Name | `Turbo码` / Turbo codes | Names a technology and code family, not a proposition |
| Attribution | Claude Berrou / Alain Glavieux, 1993 | Catalog metadata; the matching 1993 paper also names P. Thitimajshima |
| Gloss | `接近香农限的码` | Undefined “near”, limit, channel, rate, metric, decoder, and quantifiers |
| Catalog status | `已验证` | Explicitly untrusted; grants no H, M, or R credit |
| Lifecycle | `planned` | No accepted execution state is permitted |

## Proposition choices that remain open

An admitted source must select exactly one root. Candidate families below are discovery categories,
not alternative statements already accepted for this target.

| Candidate root family | Data that must be fixed | Why it cannot be silently selected |
|---|---|---|
| Encoder construction or algebraic correctness | constituent recursive systematic convolutional encoders, generator representation, state initialization, interleaver, termination, puncturing, rate | A construction or identity is not a near-capacity performance theorem |
| SISO/MAP/BCJR component-decoder correctness | trellis, channel likelihood, a priori/extrinsic convention, tie and zero-probability policy | Component optimality is not correctness or convergence of iterative turbo decoding |
| Iterative decoder property | update schedule, number of iterations or stopping rule, fixed-point/convergence notion | No such result or assumptions are selected by the catalog |
| Finite performance point | exact code and interleaver, channel, SNR convention, block length, decoder, iterations, BER/FER, confidence and arithmetic | Simulation or measurement is not an analytic theorem or kernel proof |
| Analytic error or distance bound | code ensemble, interleaver distribution, decoder, weight/distance spectrum, probability order, constants | Later analytic results are distinct from the 1993 design/performance report |
| Asymptotic threshold or capacity claim | channel family, rate sequence, block-length sequence, decoder, error criterion, limit order, quantitative gap | A general coding theorem or later capacity result cannot replace a turbo-code-specific claim |

## Domains and binders to freeze

- alphabets, bit and state types, constituent-code memory, polynomial or transition conventions;
- finite information, parity, and transmitted-word index types and all length relations;
- deterministic interleaver or random interleaver ensemble and its probability space;
- termination, tail-biting, puncturing, systematic/parity transmission, and resulting rate;
- discrete channel or AWGN model, signal mapping, energy/noise and SNR or decibel conventions;
- hard or soft decoder, exact real or approximate arithmetic, schedule, iteration count, and ties;
- bit-error or block/frame-error event, averaging order, and probability measure;
- fixed versus varying parameters, quantifier order, limit mode, constants, and “near” tolerance;
- theorem, hypothesis, heuristic, numerical computation, simulation, or experimental boundary.

Until these are source-selected, ordered binders, hypotheses, conclusion, alternate encodings,
transports, and excluded cases remain empty rather than invented.

## Degenerate and boundary cases to resolve

- zero information or block length, empty alphabets, memory zero, identity or invalid interleavers;
- un-terminated, zero-tail, tail-biting, and incompatible constituent or puncturing lengths;
- rate zero or one, puncturing all parity symbols, catastrophic or nonrecursive encoders;
- noiseless and extreme-noise endpoints, zero likelihoods, decoding ties, and nontermination;
- zero iterations versus one or unbounded iterations and flooding versus serial schedules;
- bit versus frame error, average versus maximal error, ensemble average versus existence or
  high-probability claims, and strict versus non-strict numeric gaps;
- finite measured results versus exact-real inequalities and asymptotic limit claims.

No case is excluded at intake because no proposition has yet been selected.

## Neighbor and substitution boundaries

- `THM-M-1579` owns the channel-capacity topic; its definition or evidence is not inherited.
- `THM-M-1580` owns the general noisy-channel coding theorem; it cannot serve as a turbo-code root.
- `THM-M-1585` owns the coding-theory umbrella; it provides no theorem credit here.
- `THM-M-1593` and `THM-M-1595` separately own LDPC and polar-code families.
- `THM-C-0384` is a distinct, out-of-scope computer-science catalog record and cannot broaden or
  select this rev-5.6 target.
- Generic `hammingDist`, `PMF`, `Kernel`, `gaussianReal`, or `DFA` APIs are substrate, not a turbo
  theorem. A definition, diagram, structure field, assumed decoder oracle, simulation, or floating-
  point trace is likewise not the requested root.

## Required decision

The integration lane must redirect this family gloss to one corrected, independently reviewed,
immutable-source proposition. Only then may the statement node choose minimal imports, elaborate an
exact expression, record its environment fingerprint, check transports, and mutation-test domain,
hypothesis, binder-scope, and boundary decisions.
