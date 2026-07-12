# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:9810-9815` supplies exactly the title
`Hartman-Grobman定理`, the attribution Philip Hartman/David Grobman, the year 1960, the gloss
`双曲平衡点的局部线性化`, importance "high," and status `已验证`. All six lines originate in
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and contain no citation.

`Docs/Stage0_Blueprint.md:36588-36613` projects the record as `THM-M-1345` while marking the exact
definitions and premises, proof history, dependencies, equivalent formulations, axioms, machine
status, and artifact links open. Neither repository file is a primary mathematical source. The
manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`; the label supplies no H or M credit.

## Inspected primary historical candidate

Philip Hartman, "A lemma in the theory of structural stability of differential equations,"
*Proceedings of the American Mathematical Society* 11(4), August 1960, pages 610-620, DOI
`10.1090/S0002-9939-1960-0121542-7`, was inspected from the publisher PDF. Theorem (II) is on page
615 and its proof continues through page 618. The exact inspected PDF has SHA-256
`f633e1c7f25336d13b0fae201361393003995d99e1d7ee17e6bccf0246d997f9`.

The paper's setup is `x' = T x + F(x)`, with `F(x) = o(|x|)` as `x -> 0`, a constant real matrix
`T`, and every eigenvalue `gamma_j` satisfying `Re(gamma_j) != 0`. Theorem (II) assumes `F` is
`C2` near zero and states that, for the solution map `T^t : x |-> xi(t,x)`, there is a continuous
one-to-one map `R` from a neighborhood of zero onto a neighborhood of zero such that `R T^t
R^{-1}` is `u |-> exp(T t) u`. The introduction explicitly says the map sends solution paths to
linear solution paths while preserving parametrization. Section 8 records a `C1` variant only when
all eigenvalue real parts have the same sign.

This candidate supplies H1 discovery evidence, not H0. The catalogue does not cite it; the paper's
incorporated local-solution conventions and exact neighborhood/time quantifiers have not yet been
converted into a canonical binder list; no Hartman-specific errata or corrigenda audit or
independent source-to-target review is complete; and the target statement has not been approved as Hartman's historical `C2` theorem
rather than a modern `C1` formulation.

## Inspected modern candidate

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), DOI `10.1090/gsm/140`, Theorem 9.9 on page
264, gives a modern continuous-time formulation. The exact inspected author-hosted preliminary PDF
has SHA-256 `362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`.

It supposes that `f` is a differentiable vector field with zero as a hyperbolic fixed point, writes
`Phi(t,x)` for its flow and `A = df_0`, and obtains a homeomorphism `phi(x) = x + h(x)` with `h`
bounded such that `phi o exp(tA) = Phi_t o phi` near zero. The same book separately states a
discrete-map formulation as Theorem 10.4, page 286. The modern candidate corroborates the theorem
family and exposes variant boundaries, but is not catalogue-selected or independently reviewed and
does not override the historical candidate's explicit `C2` premise.

The inherited Chapter 6 context is also material: the book works with `f` of class `C^k`, `k >= 1`,
on an open subset of finite-dimensional real space, and Theorem 6.1 supplies an open maximal local
flow domain. Those incorporated assumptions must be transcribed rather than replacing the source
flow with an arbitrary abstract global `Flow`.

The official errata PDF was also inspected at SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`. It contains
proof-relevant corrections in this section: page 265 must use bounded continuous functions in the
sup-norm Banach space; page 266 repairs an invalid equation in the proof of Lemma 9.7 and supplies
the argument forcing the residual map to vanish; and page 268 corrects the boundedness formula for
the conjugacy displacement. These corrections are recorded but not yet mapped node by node into an
accepted source reconstruction, so the candidate remains H1 rather than H0.

## Component crosswalk

| Catalogue component | Historical candidate | Prospective Lean surface | Intake result |
|---|---|---|---|
| Hartman-Grobman theorem | Hartman 1960, Theorem (II), page 615 | one exact declaration with source-bound binders | primary candidate located; target selection open |
| hyperbolic equilibrium | origin for `x' = T x + F(x)`; every eigenvalue of `T` has nonzero real part | fixed-point equation plus complexified spectrum or equivalent splitting | exact encoding/equivalence and arbitrary-point transport open |
| local linearization | continuous one-to-one neighborhood map conjugating `T^t` to `exp(tT)` | neighborhoods, homeomorphism/local homeomorphism, flow and linear-flow maps | neighborhood and time quantifiers not frozen |
| local nonlinear system | `F=o(|x|)`, `F` `C2` near zero | finite-dimensional state, differentiability/little-o and local ODE solution interface | domain and incorporated ODE assumptions open |
| topological conjugacy | paths mapped preserving parametrization | conjugacy equation for every admissible real time | must not weaken to orbit equivalence or time-one conjugacy |
| 1960 / Hartman and Grobman | Hartman paper matches year and one named author; repository gives no Grobman source | provenance documentation only | Grobman genealogy and catalogue intent still unaudited |
| `已验证` | published proof exists in the inspected candidate | accepted H crosswalk and kernel receipt would be separate | no H0 or M credit |

## Source gate

Before the statement node can close, an accountable reviewer must choose an immutable authoritative
statement, transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
neighborhood/time condition, and exceptional case, audit errata, and decide the historical `C2`
versus modern regularity boundary. A second reviewer must approve that mapping and its separation
from the map theorem, stable manifold theorem, indirect stability method, and structural stability.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, adjacent ODE, flow,
derivative, fixed-point, homeomorphism, semiconjugacy, spectrum, and matrix-exponential APIs exist.
A pinned `Flow.IsSemiconjugacy` witness is global and requires a continuous surjection; it cannot
directly express the source's local neighborhood conjugacy without restriction and transport work.
A bounded exact-topic search of the repo-local Lean tree and pinned mathlib found no declaration
named for Hartman-Grobman and no exact hyperbolic-equilibrium topological-conjugacy result. This is
an intake search, not a complete immutable external-project audit. No exact declaration, proof
body, axiom report, statement fingerprint, checked transport, or machine closure is credited.
