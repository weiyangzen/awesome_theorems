# Scope map

## Preserved source scope

- Objects: a sequence of harmonic functions.
- Claimed behavior: convergence, under assumptions absent from the repository record.
- Attribution and date: Axel Harnack, 1887, as unverified secondary metadata.
- Mathematical setting: differential equations / partial differential equations.

This is the entire justified scope. In particular, the word "convergence" alone does not imply
pointwise, compact-open, locally uniform, norm, or derivative convergence.

## Decisions required before statement freeze

The statement phase must identify a primary theorem and freeze the ambient scalar field and
dimension, connected open domain, definition of harmonicity, sequence indexing, positivity or
monotonicity hypotheses, local boundedness hypothesis (if any), mode and codomain of convergence,
the divergence alternative, harmonicity and finiteness of the limit, and empty/disconnected or
zero-dimensional boundary cases. Quantifier order and whether boundedness at one point suffices
must be mapped literally from the selected source.

## Explicit exclusions

- Substituting the common increasing-sequence dichotomy without source evidence.
- Substituting a normal-family theorem for locally bounded harmonic functions.
- Substituting Harnack's inequality, a maximum principle, or convergence of holomorphic functions.
- Treating pointwise convergence as locally uniform convergence without a proved bridge.
- Treating the metadata label `已验证` or a nearby theorem's Lean file as evidence for this target.
