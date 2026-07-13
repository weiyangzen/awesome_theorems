# Source-statement crosswalk

## Repository record

| Catalog component | Repository evidence | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`: `Turbo码` | Future canonical namespace/declaration | Stable UID and subject only |
| Attribution/date | Claude Berrou / Alain Glavieux, 1993 | Provenance metadata | No work, edition, page, theorem, or equation is cited; matching paper has a third author |
| Literal claim | `接近香农限的码` | No expression | Noun phrase plus qualitative performance gloss, not a binder-complete proposition |
| Source status | `已验证` | No receipt | Explicitly untrusted; no source or machine credit |
| Exact premises/result | Marked `待补充` in Stage0 | Domains, binders, hypotheses, conclusion | Absent; canonical statement remains null |
| Proof/formal artifact | Marked `待补充` in Stage0 | Proof body, wrapper, or pinned dependency | Absent |

The separate catalog item `THM-C-0384` says `接近Shannon极限的码` and attributes the topic to
“Berrou等”. It is outside the 1546-target rev-5.6 set. It is duplicate subject metadata, not
authority to change this target's scope, formal system, statement, or evidence.

## Historical source-family lead

The strongest bibliographic match is C. Berrou, A. Glavieux, and P. Thitimajshima, “Near Shannon
limit error-correcting coding and decoding: Turbo-codes. 1,” *Proceedings of ICC '93*, volume 2,
pages 1064-1070, DOI `10.1109/ICC.1993.397441`. Crossref metadata confirms the title, three authors,
venue, volume, pages, and DOI. The catalog omits Thitimajshima. The observed Crossref response had
SHA-256 `6f41318b05a543742d3e89197c3b3d93644b90a8c78d109fce2a97b639b0a277`;
the observed Unpaywall response had SHA-256
`84fc3a15abece1efce02b7e619c9858109c6c3f79b2e4b22927b0c2c32c07dcb` and reported no open
repository copy.

This is discovery evidence, not H0. No primary text, exact theorem locator, complete assumptions,
proof boundary, corrections audit, or independent review was admitted. The title itself combines
coding, decoding, and a qualitative near-limit claim; it does not identify which one is the root.

A later explanatory source is C. Berrou and A. Glavieux, “Near optimum error correcting coding and
decoding: turbo-codes,” *IEEE Transactions on Communications* 44(10), 1261-1271 (1996), DOI
`10.1109/26.539767`. It is not automatically the repository's 1993 target.

## Distinct later analytic leads

| Source lead | Candidate subject | Intake boundary |
|---|---|---|
| S. Benedetto and G. Montorsi, “Unveiling turbo codes: some results on parallel concatenated coding schemes,” *IEEE Transactions on Information Theory* 42(2), 409-428 (1996), DOI `10.1109/18.485713` | Average-over-interleavers/error-bound analysis | Later analytic root; cannot be substituted without source authority |
| L. C. Perez, J. Seghers, and D. J. Costello Jr., “A distance spectrum interpretation of turbo codes,” *IEEE Transactions on Information Theory* 42(6), 1698-1709 (1996), DOI `10.1109/18.556666` | Distance-spectrum and spectral-thinning analysis | Different binders and conclusion from a finite performance report or capacity theorem |

These leads demonstrate source-family ambiguity. They do not establish that the catalog intended an
analytic bound, and no H0 proof crosswalk is claimed.

## Pinned Lean discovery surface

| Pinned module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.InformationTheory.Hamming`: `hammingDist`, `Hamming` | Finite word distance/weight substrate | API availability only |
| `Mathlib.Computability.DFA`: `DFA`, `DFA.eval` | Generic deterministic state evolution | Acceptor, not an output transducer or convolutional encoder |
| `Mathlib.Probability.ProbabilityMassFunction.Basic`: `PMF` | Discrete distributions | No code ensemble, channel, or decoding error |
| `Mathlib.Probability.Kernel.Basic`: `Kernel`, `IsMarkovKernel` | Generic stochastic kernels | No selected channel or capacity semantics |
| `Mathlib.Probability.Distributions.Gaussian.Real`: `gaussianReal` | Gaussian-noise substrate | No modulation, AWGN channel, SNR, decoder, or performance claim |

A bounded lexical scan of pinned mathlib and repo-local Lean found no terminal turbo-code,
recursive-systematic-convolutional encoder, interleaver, BCJR/MAP/SOVA decoder, BER/FER, SNR/dB, or
channel-capacity declaration. Negative lexical search is not an exhaustive anchor audit and proves
no global absence. `IntakeProbe.lean` only authenticates the generic APIs above at pinned revisions.

## Required source acceptance

Before statement execution, accountable reviewers must select one immutable primary-source
proposition and record a stable identifier, theorem/equation/section/page locator, exact definitions,
ordered premises and conclusion, proof dependencies, theorem-versus-experiment boundary, corrections
status, and independent review. The crosswalk must map every construction, channel, decoder, rate,
probability, error, asymptotic, constant, and degenerate-case convention into Lean. Until then the
received target is `H5`, the formal target is `M4`, and no theorem-completion claim is legal.
