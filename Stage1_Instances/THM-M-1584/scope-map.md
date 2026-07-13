# Scope map

## Preserved theorem family

The intake preserves the Chaitin Omega theorem family named by the catalog. For a suitably universal
prefix-free or self-delimiting computing machine `U`, the measure of its halting domain, commonly
written `Omega_U`, is a real in `[0, 1]` and is not computable. None of the following candidate
ingredients is yet credited as the canonical proposition:

- finite binary programs, or programs over a source-specified finite alphabet;
- a partial machine semantics and its halting domain;
- a prefix-free or self-delimiting condition that makes the Kraft sum bounded;
- a universality or optimality condition on the machine;
- a real defined by a weighted sum or product-measure probability of the halting domain; and
- nonexistence of an effective approximation procedure meeting a source-selected error contract.

## Decisions required at statement freeze

1. Preserve one lawful complete primary edition, select the exact definition/result and proof
   boundary, map every incorporated premise and conclusion, audit corrections, and obtain
   independent source approval.
2. Decide the quantifier scope: every universal prefix-free machine, one explicitly fixed machine,
   existence of an uncomputable halting probability, or a characterization of all Omega reals.
3. Fix the machine model, program alphabet, encoding, initial input convention, partial evaluation,
   halting predicate, prefix-free/self-delimiting predicate, and universality notion.
4. Fix the probability construction: binary product measure or Kraft sum, logarithm/base convention,
   convergence proof, codomain (`Real`, `NNReal`, or another exact encoding), and checked transports.
5. Fix computability of reals: Cauchy-name, rational-approximation, digit-stream, Dedekind-cut, or
   another source-mapped representation, including modulus and endpoint conventions.
6. State whether lower semicomputability, Martin-Lof randomness, incompressibility, irreducibility
   of bits, formal-system incompleteness, or Diophantine encodings are premises, conclusions, later
   corollaries, or outside this root.
7. Freeze ordered binders and all typeclass, universality, prefix-free, convergence, and
   computability hypotheses; mutation-test removed hypotheses, changed domains, binder scope, and
   boundary cases.
8. Select foundation, TCB, computation, minimal-import, and checked-alternate-encoding profiles.

## Degenerate and boundary cases

Source review must dispose of an empty, finite, singleton, or non-prefix-free halting domain;
machines that never halt or halt on every admitted program; zero- or one-symbol alphabets; empty
programs; duplicate encodings; invalid programs; a nonuniversal machine with computable halting
probability; sums equal to `0` or `1`; dyadic reals with two binary expansions; approximation error
zero; negative or zero precision indices; and the distinction between lower semicomputability and
two-sided computability.

No case is excluded at intake. A structure or hypothesis that directly stores the desired
noncomputability, randomness, or halting oracle would make a later projection circular rather than
prove the theorem.

## Neighbor and substitution exclusions

- `THM-M-1582` (Kolmogorov complexity) and `THM-M-1583` (algorithmic information theory) are
  dependencies or neighboring families, not inherited scope or proof evidence.
- `THM-M-0707` (halting-problem undecidability) may support a future reduction but is not itself a
  halting-probability theorem; no status or proof credit is shared.
- A computable halting probability for a special nonuniversal machine is not the Chaitin theorem.
- Existence of any noncomputable real, undecidability of one digit, or noncomputability of a halting
  set is not a substitute for noncomputability of the selected `Omega_U` real.
- Martin-Lof randomness or algorithmic incompressibility is stronger/differently encoded unless an
  exact source root and checked implication are selected.
- Busy Beaver growth, Godel incompleteness, Diophantine equations, experimental digit computation,
  and numerical truncation are not interchangeable with the root.
- `Nat.Partrec.Code`, halting undecidability, unique decodability, and Kraft-McMillan are adjacent
  APIs only. Their existence does not define or prove Chaitin Omega.
- The repository's `verified` label, a DOI, source metadata, or an API probe supplies no source or
  machine-proof credit.

## Formal boundary

Pinned mathlib exposes partial-recursive program codes and evaluation, halting undecidability,
finite uniquely decodable codes, and the Kraft-McMillan inequality. The probe authenticates only
these adjacent interfaces. It does not define a universal prefix-free machine, its infinite halting
domain, an Omega real, computability of exact reals, or the desired noncomputability theorem. No
canonical Lean target, expression fingerprint, checked transport, mutation suite, or proof body is
claimed at intake.
