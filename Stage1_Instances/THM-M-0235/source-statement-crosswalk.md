# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1696-1701` supplies exactly the title "open mapping theorem,"
the attribution "many mathematicians," the nineteenth century, the gloss "nonconstant
holomorphic functions are open maps," high importance, and status `已验证` ("verified"). All six
lines entered the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record
contains no author or work citation, edition, theorem/page, definitions, assumptions, proof
boundary, corrections, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:6518-6543` repeats the gloss but explicitly leaves precise definitions
and premises, proof route, dependencies, equivalent formulations, axioms, machine status, and
artifact links open. Its generated claim that closure is believed to exist supplies no source or
proof evidence. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

The corpus also contains the different functional-analysis statement "a surjective bounded linear
operator is an open map." Its deduplicated Stage1 target is `THM-M-0276`. The complex-analysis
category and holomorphic wording make that theorem an explicit non-substitute for `THM-M-0235`.

## Source status

The classical complex theorem is historically established, so the recognizable family is
provisionally `H1`, not an open mathematical problem. Jiří Lebl, *Guide to Cultivating Complex
Analysis: Working the Complex Field*, version 1.9 (July 11, 2026), was inspected as a named
authoritative modern source lead at Git tag `v1.9`, commit
`a4d25d9ba37a486a5a020219eb8bd4e6602fd14c`. The release archive has SHA-256
`1d50a21c5e07e3b6d77b13b01974480ad9d3d29281513cd1e09fe9e2789b4c33`; its
`ca.tex` has SHA-256 `a99ed1bfceca960f98abd08e7d3c4f20d907b2fa392c211b522c06283ac61935`.

Definition 1.1 (PDF page 13; source around lines 970-988) defines a domain as an open connected
subset of `ℂ`, with a footnote that sets are generally considered nonempty although empty-domain
results are often vacuous. Theorem 5.5.1 (PDF pages 144-145; source around lines 11730-11760) states
that if `f : U → ℂ` is holomorphic and nonconstant on a domain, then `f(V)` is open for every open
`V ⊂ U`, and gives a complete proof through local nonconstancy, a closed disk, a boundary lower
bound, and Rouché's theorem. This is a strong source and proof lead closely matching the catalog.

It is not `H0`: the catalog does not cite Lebl, the optional nonemptiness convention must be made
explicit, the source's function-on-domain presentation needs a checked ambient/subtype Lean
transport, corrections and errata have not been dispositioned, proof nodes have not been mapped to
a frozen obligation registry, and no independent source review is recorded.

## Crosswalk

| Repository phrase | Mathematical decision | Prospective Lean component | Intake status |
|---|---|---|---|
| "holomorphic function" | ambient complex function and its domain | `f : ℂ → ℂ`, `U : Set ℂ`, plus a source-matched differentiability or analyticity predicate | function/domain binders and predicate open |
| implicit "domain" | open, connected, normally nonempty complex domain | `IsOpen U` with `IsConnected U`, or source-checked equivalents using `U.Nonempty` and `IsPreconnected U` | omitted by catalog; definition chain required |
| "nonconstant" | not constant on the selected domain | `¬ ∃ w, ∀ z ∈ U, f z = w` or a checked equivalent | encoding and empty-domain behavior open |
| "open map" | images of domain-open sets are open in `ℂ` | `∀ s ⊆ U, IsOpen s → IsOpen (f '' s)` or `IsOpenMap` for a subtype restriction | relative/total encoding open |
| whole-plane form | an entire nonconstant function is a total open map | `AnalyticOnNhd ℂ f Set.univ` and `IsOpenMap f` | valid candidate specialization, not selected root |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as evidence |

The source-to-Lean mapping remains open specifically at domain nonemptiness, source `f : U → ℂ`
versus mathlib's ambient `g : E → ℂ`, `IsConnected` versus `IsPreconnected`, source holomorphicity
versus `AnalyticOnNhd`, and the source's domain-open subsets versus the pinned ambient-set image
form. These gaps explain H1 without weakening or substituting the theorem.

## Pinned formal candidates

The pinned file `Mathlib.Analysis.Complex.OpenMapping` is itself titled "The open mapping theorem
for holomorphic functions" and records the intended constant-or-open family. The intake probe
authenticates these interfaces:

- `AnalyticOnNhd.is_constant_or_isOpen`: closest connected-set candidate; its right disjunct is
  relative to `U`, while the left disjunct states constancy on `U`.
- `AnalyticOnNhd.is_constant_or_isOpenMap`: whole-plane corollary with total `IsOpenMap`.
- `AnalyticAt.eventually_constant_or_nhds_le_map_nhds`: local neighborhood alternative used by
  the global route.
- `DifferentiableOn.analyticOnNhd` and `analyticOnNhd_iff_differentiableOn`: candidate bridges
  between ordinary complex differentiability and analytic-on-neighborhood language on open sets.

The module and declarations are immutable at the recorded mathlib revision, but they remain
`M3` intake candidates. Exact source identity, elaborated expression equality, minimal imports,
checked transports, declaration/body provenance, placeholder and axiom closure, and integration
acceptance belong to downstream phases. No proof body is credited by this dossier.

## Required downstream decision

The statement phase must not select the convenient whole-plane corollary merely because it yields
`IsOpenMap f` directly. It must first admit and independently review a source statement, decide
the domain convention and relative-open conclusion, then elaborate that exact proposition. The
anchor audit can subsequently determine whether one pinned declaration or a checked wrapper closes
the accepted target without broadening or narrowing it.
