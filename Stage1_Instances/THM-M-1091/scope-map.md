# Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Repository root | Chapman-Kolmogorov equation, glossed as the semigroup property of transition probabilities | The gloss identifies the equation family but not a time model or exact theorem edition |
| State space | One measurable state space with transition kernels from states to probability measures | Standard-Borel, countability, topology, and universe choices are unspecified |
| General time form | For `s <= t <= u`, direct transition `P(s,u)` equals composition through `t` | The indexing structure and source assumptions establishing the family are open |
| Homogeneous discrete form | For a kernel `K`, `K^(m+n) = K^m` followed by `K^n` | Pinned mathlib provides this candidate; adopting it as the root needs a source-scope decision |
| Integral form | `P(s,u)(x,A) = integral P(t,u)(y,A) dP(s,t)(x,dy)` for measurable `A` | Orientation, measurability, and equality conventions must match the selected kernel API |
| Probability normalization | Classical transition kernels have probability-measure outputs | Mathlib's power theorem is more general than Markov kernels; a source-faithful wrapper may need `IsMarkovKernel` assumptions |
| Boundary cases | Zero elapsed time, `m = 0`, `n = 0`, degenerate spaces, killed processes | Each must be fixed and mutation-tested in the statement phase |

## Required statement decision

The source audit must identify an immutable mathematical edition and decide whether the root is
the general inhomogeneous three-time equation or the homogeneous discrete-time semigroup law.
If the latter is chosen, the statement phase must explain why the specialization is exact rather
than merely convenient, and must decide whether probability normalization is an explicit premise.
It must then freeze binder order, composition orientation, the measurable-set form, and checked
transports between kernel equality and integral equality.

## Explicit exclusions

- Kernel associativity alone; it supports iterated composition but is not by itself a transition
  family's Chapman-Kolmogorov consistency theorem.
- Defining `P(s,u)` to be the composition and proving the equation only by reflexivity unless that
  construction is the precise sourced theorem.
- Kolmogorov forward or backward differential equations, owned by neighboring targets.
- The Markov property itself, owned by `THM-M-1090`; deriving Chapman-Kolmogorov from a process law
  requires explicit conditional-law infrastructure.
- A finite-state matrix identity substituted for the measurable-kernel equation without a checked
  transport and source justification.
- Treating the repository label `已验证` or the mathlib theorem name as source fidelity, accepted
  proof provenance, or theorem completion.
