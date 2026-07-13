# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1626-1631` is the complete repository source record:

- title: `最大模原理`;
- attribution: Karl Weierstrass;
- year: 1875;
- statement: `全纯函数的模在内部不能达到最大值`;
- importance: high;
- formalization status: `已验证`.

All six lines originate unchanged at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no work title, edition, theorem or page,
stable external identifier, definition chain, complete assumptions, exception, proof text,
correction record, reviewer, or formal artifact. `Docs/Stage0_Blueprint.md:6248-6273` repeats the
gloss while explicitly leaving precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, logic dependencies, machine status, and artifact links open.

The catalog attribution and year are provenance leads only. No primary or authoritative source is
admitted at intake, and `已验证` is untrusted inventory metadata. The recognizable historically
proved family is therefore provisionally `H1`, not `H0`.

## Authoritative secondary-source lead

The immutable Encyclopedia of Mathematics entry *Maximum-modulus principle*, revision 54115
(12 October 2023), was inspected at
`https://encyclopediaofmath.org/index.php?title=Maximum-modulus_principle&oldid=54115`. The observed
18,821-byte response had SHA-256
`347e19aadf4fdecc15504939127d62f2939dfe5d9a749bb456baece83a7ee161`. It explicitly assumes a
nonconstant holomorphic function on an open domain, distinguishes the no-local-maximum form from
the equivalent non-attainment-of-supremum form, and states the bounded closure-continuous boundary
consequence separately. Its references include L. V. Ahlfors, *Complex Analysis*, McGraw-Hill
(1979), page 241, Zbl `0395.30001`.

This is a named, versioned secondary-source discriminator and downstream bibliography lead, not
an H0 packet. The cited Ahlfors passage was not admitted or crosswalked, and the entry does not
validate the catalog's Weierstrass/1875 attribution. Exact source selection, premise and conclusion
mapping, correction review, and independent review remain open.

## Clause crosswalk

| Catalog phrase | Candidate mathematical readings | Pinned Lean surface | Intake status |
|---|---|---|---|
| "holomorphic function" | scalar holomorphic map on a complex domain, or a map between complex normed spaces; regularity local near a point or global on a set | `DifferentiableAt`, `DifferentiableOn`, and eventual differentiability appear in `AbsMax` declarations | domain, codomain, and regularity scope open |
| "modulus" | complex absolute value or norm of a vector-valued map | `norm \u2218 f` | scalar/vector relationship and strict convexity open |
| "interior" | a point of an open domain, a neighborhood-local condition, or interior relative to a larger set | `c \u2208 U`, `IsOpen U`, or neighborhood filter `\ud835\udca9 c` | meaning and binder placement open |
| "attain a maximum" | `IsLocalMax (norm \u2218 f) c`, `IsMaxOn (norm \u2218 f) U c`, or a closure/boundary maximum | local and setwise candidates both exist | local/global and set choice open |
| "cannot" | explicit nonconstant hypothesis implies no interior maximum, or an attained maximum implies constancy | local eventual equality and global `EqOn` conclusions exist | direction and conclusion open |
| omitted constant case | constants attain maxima everywhere | both local and global pinned results conclude a form of constancy rather than unconditional impossibility | literal catalog wording is not accepted as a proposition |
| `已验证` | untrusted catalog status | no expression or accepted receipt | no H/M/R credit |

## Pinned formal provenance lead

The pinned dependency lock selects mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Its file
`Mathlib/Analysis/Complex/AbsMax.lean` has Git blob
`e8ff6a7da9e9b0324d2928a77d464b7fd40ff5fa` and SHA-256
`d2edf586cb228ff792f12bb6dac10cd449eb7f0aa45074c812768c336dd4ef8d`. The file overview says
explicitly that several statements with different domain, codomain, and conclusion assumptions are
called the maximum modulus principle.

Representative candidates are:

| Declaration | Mathematical role | Exactness boundary |
|---|---|---|
| `Complex.norm_eventually_eq_of_isLocalMax` | local maximum plus nearby complex differentiability implies local norm constancy | general codomain; norm, not value, conclusion |
| `Complex.eventually_eq_of_isLocalMax_norm` | local maximum plus nearby differentiability implies local value constancy | requires a complex normed codomain that is strictly convex as a real normed space (`StrictConvexSpace ℝ F`) |
| `Complex.norm_eqOn_of_isPreconnected_of_isMaxOn` | a maximum on an open preconnected domain implies norm constancy on it | global `IsMaxOn`; norm conclusion |
| `Complex.eqOn_of_isPreconnected_of_isMaxOn_norm` | the connected-domain assumptions imply value constancy | adds strict convexity; plausible scalar global form |
| `Complex.exists_mem_frontier_isMaxOn_norm` | a bounded-set maximum can be located on the frontier | boundary existence form, not the interior root |
| `Complex.norm_le_of_forall_mem_frontier_norm_le` | a frontier norm bound propagates to the closure | boundary inequality form, not the interior root |

`IntakeProbe.lean` checks these identifiers and representative axiom reports in the pinned
environment. This establishes usable formal interfaces only. Intake does not resolve their source
identity, exact elaborated-expression relationship, terminal proof bodies, transitive dependencies,
trust closure, or which variant belongs to the root. No candidate is credited as `M0-*`.

## First failed source gate

No immutable primary or authoritative theorem passage has been completely mapped to the catalog
claim and independently reviewed. In particular, there is no source authority for repairing the
literal constant-function defect, choosing local or global maximum, fixing the domain and
codomain, or selecting norm or value constancy. Until that source contract exists, choosing one
pinned declaration would substitute missing mathematics rather than freeze the received target.
