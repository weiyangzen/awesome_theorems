# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the title `康托尔-伯恩斯坦-施罗德定理`, attributes it to
Georg Cantor, Felix Bernstein, and Ernst Schroeder, dates it to 1898, and states `两个集合互相单射则等势`
(`two sets that inject into each other are equipotent`). The Stage0 record repeats this statement.
The rev-5.6 manifest carries `已验证` only as `source_status_untrusted`.

This is enough to identify the ordinary theorem and freeze its semantic scope, but it is not H0
source evidence. The repository gives no primary edition, theorem/page locator, original wording,
assumption analysis, proof boundary, errata search, or independent review. The historical spelling
and attribution are not independently accepted by this intake.

## Statement crosswalk

| Repository phrase | Mathematical content | Provisional Lean content | Intake status |
|---|---|---|---|
| "two sets" | arbitrary sets, no size relation assumed | `alpha : Type u`, `beta : Type v` | scope frozen; canonical declaration open |
| "inject into each other" | maps in both directions, each one-to-one | `f : alpha -> beta`, `g : beta -> alpha`, `Function.Injective f`, `Function.Injective g` | pinned API elaborated |
| "equipotent" | a bijection exists | `exists h : alpha -> beta, Function.Bijective h` | pinned candidate type elaborated |
| `已验证` | untrusted inventory status | no proposition or proof object | explicitly rejected as evidence |

Set membership is not part of the mathematical claim; treating each set as the type of its
elements is the standard extensional encoding. No `Set` ambient carrier or subtype membership
hypothesis is required. Empty sets remain within scope.

## Pinned Lean discovery

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.SetTheory.Cardinal.SchroederBernstein` exposes:

- `Function.Embedding.schroeder_bernstein`, whose checked type takes injections both ways and
  returns a bijection;
- `Function.Embedding.antisymm`, the bundled embeddings/equivalence form; and
- `Function.Embedding.schroeder_bernstein_of_rel`, a stronger relational variant.

The bounded intake probe checks these declarations and a local proposition spelling of the
repository claim. This records a highly plausible repo-local closure route but is not the required
immutable anchor audit: proof-body provenance, exact imports, axiom closure, license/SBOM, and
candidate eligibility remain downstream work.

## Source work still required

The anchor/source audit must select and independently inspect an immutable authoritative edition,
record theorem or page, exact assumptions and terminology, check relevant errata, and map each
source proof node to the frozen statement. Until that review is accepted, status remains H3 rather
than H0.

