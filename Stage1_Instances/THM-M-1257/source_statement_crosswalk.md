# Source-statement crosswalk

## Identified source

Hans Lewy, "An example of a smooth linear partial differential equation without solution",
*Annals of Mathematics*, Second Series, volume 66 (1957), pages 155-158. This bibliographic
identification is sufficient for intake discovery, not for `H0`: an immutable scan, page-level
transcription, assumption mapping, and errata search have not been accepted.

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| An explicit smooth first-order complex linear differential operator exists | Lewy 1957, pp. 155-158; exact displayed formula still needs verified transcription | future structure/function defining `L` on functions over `Real^3` | Source identified, but coefficients and sign/conjugation conventions are not frozen |
| A smooth forcing term is specified | Lewy 1957 construction; exact formula and quantifier scope still need verified transcription | future explicit `f` | Statement-critical object remains open; it must not be replaced by an arbitrary witness |
| `L u = f` has no local solution near the origin | Lewy 1957 principal nonsolvability conclusion | future negated local-solution predicate | Function space, derivative sense, neighborhood quantifiers, and equality notion remain open |
| The result refutes general local solvability for smooth linear PDEs | Mathematical consequence of the explicit example | existential wrapper around the exact example | Headline consequence only; it cannot replace the stronger explicit construction |
| Germ/non-surjectivity formulation | Standard language for local solvability | future map on an appropriate germ space | Candidate reformulation; no source or Lean equivalence is yet checked |

## Statement-preservation rules

The later statement phase must preserve the explicit operator and forcing term, the three-real-
variable complex setting, the local neighborhood quantifiers, and the source's solution regularity.
Changing a coefficient sign or complex-conjugation convention is allowed only with a checked
coordinate/conjugation transport. Proving nonsolvability only for analytic solutions, only under
extra boundary conditions, or only on one fixed domain would not establish the source claim unless
the primary statement itself has exactly that scope.

The repository source label `已验证` is untrusted metadata and supplies neither source fidelity nor
machine-proof credit. No external formal theorem has been located at intake, and no negative claim
about its existence is made before the anchor-audit protocol runs.

## Required follow-up

- Acquire a stable primary-source artifact and record its content hash, edition, exact pages, and
  any corrections or errata.
- Transcribe the displayed operator, forcing term, theorem wording, regularity class, and locality
  quantifiers independently twice, resolving sign and coordinate conventions.
- Map every source assumption to ordered Lean binders and mutation-test omitted regularity,
  altered domains, fixed versus arbitrary neighborhoods, and coefficient changes.
- Identify the minimal pinned mathlib representation for derivatives, smoothness, distributions or
  classical solutions, and local equality before choosing the canonical Lean expression.

Current source status is `H1`, not `H0`. The statement is intentionally `M4` until the missing
mathematical data are recovered rather than guessed.
