# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1593`, the title `LDPC码`, the literal gloss
`低密度奇偶校验码` (low-density parity-check codes), the attribution to Robert Gallager, and the
year 1963. The importance and `已验证` fields are catalog metadata, not source-fidelity or Lean
evidence. The catalog names a coding-theory family, not one truth-valued statement.

## Candidate result families not credited

Gallager's monograph makes the following distinct result families plausible. None is selected or
credited by this intake:

1. Define a regular binary `(n, j, k)` low-density parity-check ensemble using a parity-check matrix
   with fixed column and row weights and derive its nominal rate.
2. Prove a typical minimum-distance lower bound linear in block length for a fixed regular ensemble,
   with a different low-column-weight boundary such as logarithmic behavior when `j = 2`.
3. Bound typical maximum-likelihood decoding error on a source-selected binary-input symmetric
   channel and compare the ensemble with random linear codes of a related rate.
4. Define Gallager's probabilistic iterative decoder and prove a finite-length or asymptotic error
   bound under exact channel, rate, degree, iteration, and independence conditions.
5. Prove a decoder hardware or data-handling complexity result under an explicit cost model.
6. Formalize a later irregular, nonbinary, density-evolution, threshold, or capacity-approaching
   theorem rather than Gallager's original regular binary results.

These claims are not interchangeable. In particular, the sparse-matrix definition is not itself a
performance theorem, and a kernel characterization of a linear code cannot discharge a distance or
decoding root.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from one immutable source passage:

- the selected theorem, edition, theorem/equation/page locator, incorporated definitions, proof
  boundary, errata decision, and independent review;
- binary versus `q`-ary alphabet, deterministic code versus random ensemble, regular versus
  irregular degrees, exact versus bounded row/column weights, and whether repeated parity checks or
  graph configurations are permitted;
- block length, check count, dimension and rate convention, divisibility and integrality
  constraints, parity-check rank assumptions, and whether codewords form the kernel of a specified
  linear map;
- the probability space and meaning of `typical`, `average`, or `with high probability`, including
  labeled versus quotient matrices/graphs and conditioning on rank or other events;
- Hamming weight and minimum-distance conventions, normalized versus absolute distance, strict
  versus non-strict inequalities, constants, and quantifier order;
- channel alphabet and transition law, symmetry convention, noise parameter, codeword prior, block
  versus bit error, and maximum-likelihood tie handling;
- exact decoder, message representation, update schedule, iteration count, stopping rule, failure
  event, independence/tree-neighborhood range, and randomness source;
- asymptotic regime, fixed and varying parameters, threshold domain, rate comparison, exponent or
  root-exponent meaning, and every dependency of constants; and
- whether computation is proof-producing, a checked finite enumeration, or merely experiment.

## Boundary cases to resolve

- zero block length, no checks, zero dimension, rate zero or one, empty alphabets, and inconsistent
  `n`, `j`, `k`, or check-count divisibility;
- `j = 0`, `j = 1`, `j = 2`, `j = 3`, `j >= 4`, `k <= j`, duplicate rows or columns, rank-deficient
  parity checks, disconnected Tanner graphs, and multiple edges;
- zero minimum distance, the zero codeword, nonzero-codeword versus pairwise-distance definitions,
  and normalized distance when the block length is zero;
- noiseless and maximally noisy channel endpoints, decoder ties, nontermination, repeated messages,
  and finite versus unbounded iterations;
- ensemble averages versus existence claims versus probability tending to one, and finite-length
  bounds versus asymptotic statements; and
- a proved result versus Gallager's explicitly stronger performance hypothesis or later empirical
  evidence.

## Excluded substitutions

- Defining an LDPC code or Tanner graph without proving a source-selected theorem.
- Proving only `x` is a codeword iff a parity-check matrix maps `x` to zero.
- A toy repetition, Hamming, cycle, or hand-picked sparse code used as the general result.
- A minimum-distance theorem substituted for a decoding theorem, or the reverse.
- A later capacity, density-evolution, threshold, expander-code, or belief-propagation result chosen
  merely because it is commonly associated with LDPC codes.
- A structure field, hypothesis, decoder oracle, numerical simulation, Monte Carlo estimate, or
  floating-point density-evolution output that assumes or approximates the conclusion.
- The duplicate Stage0 computer-science item `THM-C-0385` used to change this target's formal system,
  claim, status, or evidence.
- The catalog label `已验证` used as a primary source or proof receipt.

## Lean and trust boundary

Pinned mathlib provides `hammingDist`, `hammingNorm`, the `Hamming` type synonym, matrices, and
linear matrix-vector maps. Those APIs could support a future finite binary-code encoding. They do
not define an LDPC ensemble, channel, decoder, asymptotic performance proposition, or exact source
root. Exact imports, expression and environment fingerprints, alternate transports, mutation tests,
foundation and axiom policies, obligation registry, discovery inventory, proof architecture, and
release evidence remain downstream work.
