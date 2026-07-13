# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1581`, the title `香农无噪声编码定理`, the gloss
`数据压缩的极限`, attribution to Claude Shannon, and the year 1948. Importance `high` and status
`已验证` are catalog metadata, not human-source or kernel evidence.

The title and gloss identify the classical lossless source-coding family but not one truth-valued
root. A later statement phase may select a proposition only from an immutable, independently
reviewed source mapping and must preserve the neighboring and duplicate-record boundaries.

## Candidate interpretations not credited

1. Shannon 1948, Section 9, Theorem 9 in its historical form: a source of entropy rate `H` and a
   constrained noiseless channel of capacity `C` admit nonsingular encoding at average source-symbol
   rate arbitrarily close to `C / H`, with a converse above `C / H`.
2. The finite one-symbol `D`-ary prefix-code bound `H_D(X) <= E[length] < H_D(X) + 1`.
3. The lower bound on average length for every finite uniquely decodable code, perhaps paired with
   a separate prefix-code construction.
4. An asymptotic lossless block source-coding theorem for an iid, stationary ergodic, finite-state,
   or general source.
5. A fixed-to-fixed typical-set or almost-lossless coding theorem with vanishing error.

These formulations have different objects, binders, boundary behavior, direct/converse content,
and proof obligations. None is selected, asserted, or credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact theorem, edition, incorporated definitions, proof boundary, corrections, and errata;
- a historical source-to-constrained-channel theorem versus a modern source-code theorem;
- the source alphabet and process: finite iid, finite-order Markov, stationary ergodic, Shannon's
  finite-state source, or another class;
- entropy as one-symbol Shannon entropy or an entropy rate, logarithm base, units, existence and
  finiteness assumptions, and normalization per symbol or per unit time;
- the output alphabet, symbol durations or costs, channel constraints and capacity definition, or
  whether the channel is absent and only a `D`-ary code is quantified;
- block, variable-length, prefix, instantaneous, uniquely decodable, nonsingular, or invertible
  code; deterministic versus randomized encoding; and decoder and delay requirements;
- average length, expected duration, worst-case length, code rate, compression ratio, or channel
  source-symbol rate as the quantity bounded;
- exact lossless decoding versus vanishing block error and the governing probability measure;
- achievability only, converse only, or both, including strict inequalities, epsilon placement,
  integer rounding, and whether optimal codes must attain the boundary;
- the quantifier order for tolerances and block lengths and whether claims hold for some or all
  sufficiently large block lengths; and
- every universe, ordered binder, hypothesis, conclusion, alternate encoding, and boundary case.

## Degenerate and boundary cases

The selected source must resolve empty and singleton source or code alphabets; output alphabet
cardinality zero or one; deterministic sources and entropy `H = 0`; empty support; zero-probability
symbols; zero or infinite entropy; channel capacity `C = 0`; `C / H` when `H = 0`; zero-duration
signals and zero symbol costs; source blocks of length zero; empty codewords; empty, singleton, or
non-surjective codes; logarithm base one and logarithm of zero; equality at the entropy or capacity
boundary; unattained infima; integer floors and ceilings; and zero or unit error tolerance.

## Neighbor and substitution exclusions

- `THM-M-1577` (information theory), `THM-M-1578` (Shannon entropy), `THM-M-1579` (channel
  capacity), and `THM-M-1580` (noisy-channel coding theorem) are separate roots and provide no
  inherited statement or proof credit.
- The Stage0 computer-science record `THM-C-0361` (`信源编码定理`, gloss `无损压缩的熵下界`)
  is a related boundary record outside the rev-5.6 target set, not an accepted duplicate or a
  statement source for this target.
- `InformationTheory.UniquelyDecodable` and `kraft_mcmillan_inequality` are genuine coding
  substrate but do not define source probabilities, entropy, average length, achievability, or
  Shannon's complete theorem.
- Binary entropy, a probability mass function, or an arbitrary code-length inequality cannot
  replace a source-selected theorem.
- A structure or hypothesis that stores the desired code, decoder, or rate result provides no
  proof, and finite examples, simulation, or numerical optimization cannot prove the general root.
- The untrusted `已验证` label and the discovery probe supply no source-fidelity or root proof
  credit.

## Formal boundary

Pinned mathlib exposes `PMF`, scalar binary and q-ary entropy functions, uniquely decodable word
sets, and the Kraft-McMillan inequality. It does not expose a located discrete-source entropy API,
expected code length, source encoder/decoder package, constrained noiseless-channel capacity, or
Shannon source-coding theorem under the bounded intake search. The probe authenticates only the
listed interfaces and neither defines nor proves the target.
