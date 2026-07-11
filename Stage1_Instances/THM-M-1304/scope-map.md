# Scope map

## Preserved source scope

- Topic label: paracomposition.
- Informal operation: paradifferentiation associated with composition of functions.
- Repository attribution: Jean-Michel Bony, 1981; not independently verified.
- Discipline: partial differential equations / paradifferential calculus.

This is the entire scope supported by repository-local source metadata. It is
not yet a theorem statement.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze: the exact
paracomposition construction; scalar or vector domain and codomain; dimension;
Littlewood-Paley decomposition and quantization conventions; homogeneous or
inhomogeneous spaces; Sobolev, Holder, Besov, or other regularity indices;
regularity and invertibility assumptions on the composing map; the expression
being compared; target norm; loss or gain of derivatives; constants and their
dependencies; local versus global setting; support and boundary assumptions;
and endpoint, low-frequency, zero-function, and identity-map cases.

## Explicit exclusions

- Ordinary chain rule, Taylor expansion, or differentiation of `f ∘ g`.
- Bony's paraproduct decomposition by itself.
- A definition of a paracomposition operator without a substantive theorem.
- Any convenient continuity estimate selected only because mathlib exposes it.
- The untrusted metadata value `已验证` as human or kernel evidence.

No Lean encoding is frozen at intake because doing so before source
identification could silently substitute one of several inequivalent results.
