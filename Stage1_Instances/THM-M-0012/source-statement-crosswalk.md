# THM-M-0012 Source-Statement Crosswalk

## Repository record

`Docs/researches/math_theorems.md:107-112` names the fundamental theorem of algebra, attributes it
to Carl Friedrich Gauss in 1799, and states that every nonconstant polynomial over the complex
numbers has a root. `Docs/Stage0_Blueprint.md:447-460` repeats the claim but explicitly leaves its
exact definitions, premises, proof route, logical foundation, and formal artifact open. The target
manifest carries `已验证` only as untrusted source metadata. None of these records is a primary
proof source or machine-completion receipt.

The catalog wording entered the repository at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the pinned blob containing it is recorded in
`instance.json`. This freezes provenance of the repository wording, not its historical accuracy.

## Primary-source boundary

The Gauss 1799 attribution is a historical source lead only. This intake did not select or inspect
an immutable edition of the dissertation, locate a theorem or page, reconcile its formulation and
proof assumptions with the modern polynomial claim, inspect corrections or errata, or obtain an
independent review. It therefore supports `H1`, not `H0`. A later source packet must record the
edition, page-level statement and proof boundary, assumptions, definition of root/nonconstant,
errata search, complete node mapping, and reviewer.

## Component crosswalk

| Catalog component | Frozen human meaning | Candidate Lean component | Intake status |
|---|---|---|---|
| "polynomial over the complex field" | conventionally, univariate `f` with complex coefficients and a complex root domain; arity is not explicit in the catalog | `f : Polynomial Complex` | candidate carrier identified; source ratification and canonical binder open |
| "nonconstant" | excludes every constant polynomial, including zero | candidate `0 < f.degree` or exclusion of `Polynomial.C` images | exact encoding and equivalence open |
| "has a root" | there exists a complex `z` where evaluation is zero | `exists z : Complex, Polynomial.IsRoot f z` | exact encoding open |
| Gauss / 1799 | historical attribution in the catalog | no formal component | primary edition and fidelity audit open |
| `已验证` | catalog status label | no formal component | explicitly untrusted; no H/M credit |

## Pinned formal candidates, not credited

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Complex.Polynomial.Basic` declares:

```text
Complex.exists_root {f : Complex[X]} (hf : 0 < degree f) :
  exists z : Complex, IsRoot f z
```

The same module installs `Complex.isAlgClosed`, while
`Mathlib.FieldTheory.IsAlgClosed.Basic` exposes the generic `IsAlgClosed.exists_root`. These are
highly relevant candidates. Intake deliberately does not claim their normalized identity with the
canonical root, audit the terminal proof body, or derive `M0-W`. The later statement and anchor
audit nodes own those gates.

## Non-substitution boundary

Positive degree and exclusion of constants appear conventionally equivalent over complex
polynomials, and `IsRoot` is conventionally evaluation at zero, but names and intuition do not
establish rev-5.6 statement identity. Those relationships require kernel-checked transports under
the same pinned environment. Algebraic closedness and splitting forms additionally require an
explicit directional mapping back to root existence and may not be assumed as premises. Until
those checks and source review occur, no H0, M0, or exact-statement claim is made.
