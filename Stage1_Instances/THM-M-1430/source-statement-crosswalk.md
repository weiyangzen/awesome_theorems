# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10446-10451` supplies exactly the title `Mandelbrot集`, Benoit
Mandelbrot, 1980, the gloss `复二次多项式的参数空间`, importance "high," and status
`已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; no bibliography or theorem statement accompanies
them.

`Docs/Stage0_Blueprint.md:38888-38913` repeats the gloss while explicitly leaving the exact
definition and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. The rev-5.6 manifest carries `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `Mandelbrot集` | a subset of complex quadratic parameter space | an exact set predicate or a proposition about it | object name only; no proposition |
| "complex quadratic polynomials" | commonly the monic centered family `z^2 + c`, but also conjugate quadratic coordinates | fixed family, parameter/phase types, and checked coordinate transports | all open |
| "parameter space" | parameters classified by a dynamical property, commonly bounded critical orbit | exact membership predicate and set encoding | classification property not stated |
| Benoit Mandelbrot / 1980 | historical attribution and year | pinpoint immutable source provenance | no edition, theorem, page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspected human proof and kernel receipt would be required | no H or M credit |

The usual bounded-critical-orbit definition is not silently promoted from mathematical convention
to repository authority. In particular, the source does not state whether the orbit begins with
`0` or `c`, how boundedness is encoded, or what property of the resulting set is to be proved.

## Bibliographic discovery boundary

Crossref metadata identifies a plausible work matching the attribution and year: Benoit B.
Mandelbrot, "Fractal aspects of the iteration of z -> lambda z(1-z) for complex lambda and z,"
*Annals of the New York Academy of Sciences* 357(1) (1980), pages 249-259, DOI
`10.1111/j.1749-6632.1980.tb29690.x`. This is bibliographic discovery evidence only. The attempted
publisher full-text retrieval returned HTTP 403, so no immutable source copy, exact passage,
incorporated definitions, proposition, assumptions, proof boundary, or errata was inspected. The
paper's logistic-family coordinates also require a checked crosswalk before they could authorize a
`z^2 + c` encoding. It receives no H credit and is not the canonical claim.

## Neighbor boundary

The immediately following catalog target, `THM-M-1431`, explicitly states
`Mandelbrot集的连通性` and attributes the Douady-Hubbard theorem. This separation is affirmative
evidence that connectedness must not be substituted for the object/topic record here. Likewise,
the adjacent complex-dynamics, Julia-set, Fatou-set, Yoccoz, and Brjuno records remain separate.

## Source gate

Before ordinary theorem-proof execution can leave `H5`, an accountable reviewer must either:

1. approve a target correction that supplies one stable truth-valued proposition, or
2. redirect this record to an explicitly non-theorem object-definition lane.

For a theorem correction, the reviewer must preserve and hash an immutable primary source, select
an exact edition and theorem/page/section, transcribe all incorporated definitions, ordered
binders, hypotheses, conclusion, and boundary cases, inspect proof dependencies and errata, and
justify why it belongs to `THM-M-1430` rather than `THM-M-1431` or another neighboring target. An
independent qualified reviewer must approve that source-to-statement map before H0 is possible.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded source-name
search found no occurrence of "Mandelbrot" or "complex dynamics" and no relevant quadratic
parameter-space declaration. `IntakeProbe.lean` confirms only that complex numbers, function
iteration, norms, ranges, and `Bornology.IsBounded` are available.

A bounded remote source inspection found one credible future audit candidate, the `girving/ray`
repository at immutable revision `0ca7b1e746b2911557ac76f56259068cfd1423ab`. Its
`Ray/Mandelbrot.lean` defines `mandelbrot` by non-escape of the orbit starting at `c` under
`z ↦ z^2 + c`, proves equality with `multibrot 2`, and then proves connectedness of the set and
its complement. The inspected file has SHA-256
`f5d04806d2f7ead1379ba8c97b7de60b6f22d5f3aed32f3410d824c469823db8`; its upstream toolchain
is Lean `v4.27.0-rc1` with mathlib revision
`725c803ee924f55342e93f2c75976051ab902b54`. It is not in the local dependency closure and was
not cloned, built, or kernel-checked here. It therefore receives discovery credit only, not M1 or
proof credit. Its definition does not turn the catalog object label into a theorem, while its
connectedness result belongs the distinct `THM-M-1431` unless an approved target decision says
otherwise.

The canonical module, expression, expression hash, checked transports, and statement mutations
remain null.

No H0, M0, readable-proof closure, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
