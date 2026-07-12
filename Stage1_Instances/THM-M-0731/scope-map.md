# Scope map

## Included topic boundary

- Algorithms or machines with an explicit finite random source.
- A source-specified success criterion: one-sided or two-sided error, average or worst case.
- The exact deterministic simulator, advice, or pseudorandom generator promised by the source.
- All resource bounds and uniformity, constructivity, hardness, and distributional assumptions.

## Ambiguities to resolve at statement freeze

1. **Finite seed fixing:** for a fixed input or finite input set, an averaging argument selects a
   seed. This need not give one uniform efficient deterministic algorithm.
2. **Non-uniform simulation:** a randomized complexity class is simulated using advice or circuits,
   for example the distinct claim commonly written `BPP subseteq P/poly`.
3. **Conditional uniform derandomization:** a hardness assumption yields a pseudorandom generator
   and a deterministic simulation with specified overhead.
4. **Unconditional uniform derandomization:** a class equality such as `BPP = P`, which cannot be
   silently inferred from the generic label.

The source phase must select an immutable source and freeze the machine model, input encoding,
random-bit model, acceptance thresholds, time/space bounds, uniformity, quantifier order, advice,
and assumptions. It must cover empty inputs, zero random bits, threshold equality, promise-problem
behavior, and whether the deterministic object may depend on input length or on each input.

## Explicit exclusions

- Treating exhaustive enumeration of random seeds as preservation of polynomial running time.
- Replacing a uniform simulator by a separate good seed or circuit for each input length.
- Replacing an unconditional theorem by a hardness assumption, or dropping such an assumption.
- Substituting `BPP subseteq P/poly`, a PRG construction, or an expectation-preserving estimator
  merely because each is called derandomization in some context.
- Packaging the desired deterministic algorithm as a hypothesis and projecting it back.
- Treating the inventory label `已验证` as source or machine-proof evidence.

No canonical Lean target is frozen at intake because the repository record supplies no proposition.
