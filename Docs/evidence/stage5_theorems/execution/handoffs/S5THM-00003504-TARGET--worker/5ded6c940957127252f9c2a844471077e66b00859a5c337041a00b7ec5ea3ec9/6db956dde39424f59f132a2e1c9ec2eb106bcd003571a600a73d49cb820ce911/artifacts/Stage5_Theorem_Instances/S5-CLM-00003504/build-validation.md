# Build validation

The three target Lean files were checked with the pinned `leanprover/lean4:v4.29.0`
toolchain and `--trust=0` against the canonical Lake environment. The local
files elaborate when using the available Mathlib surface. An exact provider
import cannot be resolved by the current manifest because `FormalConjectures`
has no built library in the canonical search path; this is an integration
precondition for Master, not a proof receipt. No network or cache mutation was
used.
