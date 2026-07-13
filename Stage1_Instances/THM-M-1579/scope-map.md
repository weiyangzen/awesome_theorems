# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1579`, the title `信道容量`, the gloss `信道的最大传输速率`,
attribution to Claude Shannon, and the year 1948. Importance `high` and status `已验证` are catalog
metadata, not human-source or kernel evidence.

The noun and gloss identify a channel-capacity family but not one truth-valued root. A later
statement phase may select a proposition only from an immutable, independently reviewed source
mapping and must preserve neighboring target boundaries.

## Candidate interpretations not credited

1. Shannon 1948, Part I, Section 1's definition of discrete noiseless capacity as
   `lim_(T -> infinity) log N(T) / T`, where `N(T)` counts allowed duration-`T` signals.
2. Part I, Section 1, Theorem 1: a determinant/largest-real-root formula for the capacity of a
   finite-state constrained noiseless channel.
3. Part II, Sections 11-12's definition of noisy discrete capacity as the maximum, over possible
   input information sources, of input entropy rate minus equivocation.
4. Section 14, Theorem 12: for a fixed nontrivial error bound `q`, the asymptotic logarithmic rate
   of the largest reliably distinguishable equal-probability signal subset equals capacity.
5. Part IV, Section 24's continuous bandlimited-channel definition as an asymptotic normalized
   maximum of a mutual-information integral.
6. A modern finite-alphabet discrete memoryless channel definition using a supremum or maximum of
   mutual information, or an existence theorem for a capacity-achieving input distribution.

These choices have different domains, binders, hypotheses, conclusions, boundary behavior, and
proof obligations. Some are definitions and some are theorems. None is selected, asserted, or
credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- whether the target is a definition, existence claim, equality/characterization, operational
  theorem, or computation formula; direct coding, converse, and manufactured conjunctions are
  excluded as neighboring or broadened scopes;
- the exact edition, theorem or definition locator, incorporated definitions, proof boundary,
  correction status, and whether a historical or modern formulation is canonical;
- noiseless constrained, finite-state noisy discrete, memoryless discrete, continuous bandlimited,
  or another channel class;
- input, output, state, and signal alphabets or spaces; finiteness, nonemptiness, measurability,
  stationarity, ergodicity, memory, feedback, and cost constraints;
- signal duration, block length, symbol versus second normalization, logarithm base, rate codomain,
  and whether time takes discrete or real values;
- capacity as a limit, maximum, or supremum; the relevant entropy, equivocation, mutual-information,
  distinguishability, code, decoder, and error definitions; and whether the optimum is attained;
- limit existence versus limsup/liminf, the exact quantifier order, and all topology, convergence,
  compactness, continuity, and finite-state assumptions needed by the selected result; and
- every universe, ordered binder, hypothesis, conclusion, alternate encoding, and boundary case.

## Degenerate and boundary cases

The selected source must resolve empty or singleton alphabets and state spaces; an empty allowed
signal language; zero-duration symbols; no admissible input sources; zero-capacity, noiseless,
deterministic, completely noisy, reducible, or nonergodic channels; zero or infinite entropy and
capacity; unattained suprema; block lengths zero and one; error tolerance zero or one; decoder
ties; zero-probability transitions; logarithm of zero; and failure or nonexistence of each claimed
limit or maximum.

For Theorem 12 in particular, the selected source must preserve or explicitly revise the conditions
`q != 0` and `q != 1`, equal-probability selected signals, most-probable-cause decoding, and the
definition of `N(T,q)`. For Theorem 1 it must fix the finite-state graph, allowed transitions,
symbol durations, determinant matrix, and the existence and selection of its largest real root.

## Neighbor and substitution exclusions

- `THM-M-1577` (information theory), `THM-M-1578` (Shannon entropy), `THM-M-1580` (noisy-channel
  coding theorem), and `THM-M-1581` (noiseless coding theorem) are separate roots and provide no
  inherited statement or proof credit.
- The Stage0 computer-science records for channel coding, noisy-channel coding, capacity converse,
  joint source-channel coding, and Gaussian channel capacity are boundary evidence, not rev-5.6
  instances or substitutes.
- Shannon's Theorem 11 is a reliable-coding/source-channel theorem and belongs naturally to the
  separately cataloged noisy-channel target; it cannot silently replace this capacity item.
- Binary entropy, Kullback-Leibler divergence, a Markov-kernel structure, Hamming distance,
  Kraft-McMillan, a binary symmetric channel example, or a numerical optimizer is substrate or a
  special case, not the received root.
- A structure or hypothesis that stores a capacity value, maximizing input, operational equality,
  decoder, or reliability result supplies no proof of its existence or correctness.
- Simulation, floating-point optimization, an unchecked external declaration, or the untrusted
  `已验证` label supplies no source-fidelity or proof credit.

## Formal boundary

Pinned mathlib exposes probability mass functions, Markov kernels, KL divergence and a chain rule,
binary entropy, uniquely decodable source codes, and Hamming distance. The bounded intake search
located no mutual-information or channel-capacity declaration in pinned mathlib or repository-local
Lean. A repo-local audit string names `abenenson/channel-capacity` at immutable commit
`a212a605d3ec5a23034e0c40f51b2b92d594efa5`; the string itself is not a declaration or proof
credit, and the referenced external project is only an unaudited downstream candidate lead. The
probe authenticates adjacent pinned interfaces only and neither defines nor proves the target.
