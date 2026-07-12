# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names the Breuil-Conrad-Diamond-Taylor theorem, dates it to 2001,
and glosses it as `所有椭圆曲线的模性` (modularity of all elliptic curves). Stage0 restates this as
"all elliptic curves are modular" but leaves definitions, hypotheses, proof route, and artifacts
open. The manifest's `已验证` is explicitly untrusted metadata.

## Primary source

Christophe Breuil, Brian Conrad, Fred Diamond, and Richard Taylor, *On the modularity of elliptic
curves over Q: wild 3-adic exercises*, Journal of the American Mathematical Society **14** (2001),
843-939, DOI `10.1090/S0894-0347-01-00370-8`, electronically published 15 May 2001.

The introduction, printed page 843, states Theorem A verbatim: "If E/Q is an elliptic curve, then E
is modular." Printed pages 845-846 define modularity through six equivalent conditions. These
include equality of `L(E,s)` with an eigenform L-series, the weight-2 level-`N(E)` refinement,
modularity of the associated `l`-adic representations, and modular parametrizations from `X_1(N)`.
The paper directs the formal theorem statements to section 2.2. The downloaded author-hosted PDF
used for this intake has SHA-256
`1e34130e55a0ef39d7ef2566cc7d518e2b69048dece36328a0b6530e92044cf2`.

## Crosswalk

| Source component | Exact human meaning | Required Lean component | Intake status |
|---|---|---|---|
| `E/Q` | an elliptic curve over the rationals | a nonsingular elliptic/Weierstrass curve over `Rat`, plus representation invariance | carrier API probed; encoding choice open |
| "modular" condition (1) | `L(E,s)=L(f,s)` for an eigenform | elliptic-curve and eigenform L-series | infrastructure not identified in bounded pinned search |
| condition (2) | eigenform has weight 2 and level `N(E)` | conductor, level, weight, normalized eigenform | infrastructure not identified |
| conditions (3)-(4) | one/all l-adic representations are modular | Tate module and continuous Galois representation | infrastructure not identified |
| conditions (5)-(6) | nonconstant modular parametrization, with (6) over `Q` at conductor level | modular curve `X_1(N)`, morphism, nonconstancy | infrastructure not identified |
| Theorem A | every `E/Q` satisfies these equivalent conditions | universal root plus checked equivalence transports | human claim frozen; Lean target open |

The definition's equivalences rely on earlier results of Carayol, Shimura, Faltings, and Mazur as
described on printed page 845; the later source audit must turn these citations and the paper's
three proof cases into node-specific records and inspect errata. Thus this intake is `H1`, not `H0`.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow probe imports
`Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass` and checks `WeierstrassCurve`, its
`IsElliptic` typeclass, discriminant, and `j`-invariant. A scoped source search found elliptic-curve
infrastructure but no target-specific modularity predicate. The probe is only evidence that part of
the domain can be represented; it is not a replacement statement, anchor audit, or proof.
