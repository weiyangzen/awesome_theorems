# THM-M-1235 frozen obligation tree

The registry freezes 15 semantic obligations before any closure metric is
credited. The checked Lean certificate consumes exact existence and uniqueness
packages and returns the canonical root. It does not prove either package.

## Proof architecture

- `M1235-ROOT` requires `M1235-T-ASSEMBLE`.
- `M1235-T-ASSEMBLE` requires exact existence and uniqueness packages.
- Existence requires finite-horizon normalization, approximate-motion
  construction, vorticity and circulation estimates, compactness and limit
  passage, and verification of conditions `(I)`-`(VIII)`.
- Uniqueness requires the two-motion stability estimate and equality of all
  five source functions.
- Definitions, boundary cases, foundation/trust, primary-source crosswalk, and
  terminal-body provenance are separate non-credit overlays.

## Node boundaries

### m1235-root
Exact target from `Statement.lean`; open at `M3`.

### m1235-s-definitions
Native analytic expansion and checked transport are required; the existing
named `Prop` fields are a frozen interface, not proofs of PDE facts.

### m1235-s-boundary
Bounded/exterior analytic-boundary cases and source regularity assumptions may
not be replaced by a whole-plane, torus, weak-solution, or zero-time theorem.

### m1235-s-foundation
Classical and TCB policy remains open pending terminal bodies.

### m1235-n-finite-horizon
The arbitrary finite positive horizon must be related to the historical global
claim without asserting an unproved compatible solution on `[0, infinity)`.

### m1235-c-approximation
Approximate motions and all construction invariants remain open.

### m1235-l-vorticity
Vorticity transport, circulation, decay, and Holder estimates remain open.

### m1235-l-compactness
Compactness, subsequence extraction, and limit passage remain open.

### m1235-l-conditions
Verification of every source condition `(I)`-`(VIII)` remains open.

### m1235-t-existence
The exact `WolibnerExistencePackage` interface is frozen but unproved.

### m1235-l-uniqueness-estimate
The source stability estimate for two motions remains open.

### m1235-t-uniqueness
The exact `WolibnerUniquenessPackage` interface is frozen but unproved.

### m1235-t-assemble
`root_of_existence_and_uniqueness` is a kernel-checked conditional composition;
it receives only local composition credit.

### m1235-x-source
Node-specific pages, numbered arguments, assumptions, and errata require
independent human review. Bibliographic identification is not H0.

### m1235-x-provenance
Terminal proof-body and transitive provenance coverage remains open.

The structured registry and graphs are authoritative. All leaf budgets are at
most 100, but the bound is only a split threshold and supplies no H0, M0, or R0
credit. The minimal open root cut set is existence plus uniqueness. Audit and
theorem completion are both false.
