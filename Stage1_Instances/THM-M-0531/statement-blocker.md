# Exact-statement gate: blocked

Item: `S56-M-0531-STATEMENT`  
Theorem: `THM-M-0531`  
Base revision: `9c62e277cad936290d63af79d788d97dd17bf4cf`

## Decision

The exact Lean 4 target cannot be truthfully elaborated. The authoritative repository record says
only "universal coefficient theorem" and "relation between homology groups and cohomology groups."
It supplies no source, numbered theorem, coefficient convention, degree convention, hypotheses,
maps, naturality claim, or splitting claim. Stage0 explicitly marks the exact definitions and
premises as still to be supplied.

The accepted intake chooses the cohomological branch only provisionally and leaves all of the
following proposition-changing choices open:

- a theorem for free chain complexes versus its specialization to singular or cellular chains;
- integral homology with an arbitrary abelian coefficient group versus another base ring;
- reduced versus unreduced (co)homology, and the meaning of the degree `n = 0` term;
- the exact arrows in `0 -> Ext(H_(n-1), G) -> H^n -> Hom(H_n, G) -> 0`;
- naturality in the chain complex/space, coefficients, or both;
- existence of a splitting versus inclusion of a chosen splitting, and the required
  non-naturality qualification.

Hatcher, *Algebraic Topology* (2002), Section 3.1, Theorem 3.2, printed p. 195, is only the intake's
unreviewed discovery lead. No immutable source packet, assumption-level crosswalk, errata review,
or independent source acceptance exists. Selecting that familiar formulation now would invent the
missing statement rather than elaborate an exact repository target. The homological tensor/Tor
form belongs to the distinct `THM-M-0004` scope and is not a permissible substitute.

The pinned mathlib revision exposes `AlgebraicTopology.singularHomologyFunctor` and the categorical
`Ext` functor, as demonstrated by `IntakeProbe.lean`, but repository and pinned-mathlib searches
found no selected ordinary singular-cohomology object or terminal topological universal
coefficient declaration. In particular, the two available APIs do not by themselves type the
middle cohomology term or the UCT arrows. Introducing an arbitrary cohomology object, arbitrary
maps, or a structure containing exactness/splitting as fields would assume the theorem and would be
placeholder statement evidence.

Consequently the phase fails first at exact human-claim identity and then at the missing compatible
formal object model. Minimal imports, an elaborated-expression fingerprint, checked transports,
and meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations cannot be
frozen. Machine status remains `M3`; no canonical declaration or proof credit is claimed.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
symlink was reused read-only. No update, build, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0531` | 0 | Rank 588, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0531/IntakeProbe.lean` | 0 | Printed the typed singular-homology and `Ext` substrate declarations only |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| repository and pinned-mathlib `rg` searches for universal-coefficient and ordinary singular-cohomology declarations | 0/1 | Found audit prose and substrate only; no exact terminal target (`1` denotes no mathlib match) |

There is no applicable `lake env lean Statement.lean` check: no exact expression exists. The probe
is deliberately not represented as the requested elaboration.

## Retry condition

An accountable source reviewer must select an immutable exact theorem and freeze the chain/space
model, base ring and coefficient object, degree and reducedness conventions, ordered binders,
arrows, naturality variables, splitting strength, and `n = 0` behavior. A compatible pinned Lean
API must then define the chosen cohomology term and all objects and arrows. A later statement run
can minimize imports, elaborate and fingerprint that expression, compile checked transports, and
run all four required mutation classes.

The assigned phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted. This artifact advances no downstream node and makes no
theorem-completion claim.
