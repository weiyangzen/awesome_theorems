# Exact-statement gate: blocked

Item: `S56-M-0666-STATEMENT`  
Theorem: `THM-M-0666`  
Base revision: `3bbec7282e62d6123372fda54f8eb18cd839d643`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
only mathematical wording is "special points in o-minimal structures" under the eponym
"Pila-Zannier theorem". This names a method and a family of unlikely-intersection applications,
not a proposition with fixed domains, hypotheses, binders, or conclusion.

The ambiguity is material inside this repository. `THM-M-0465` has the same Chinese title but the
different gloss "proof of the Manin-Mumford conjecture". The 2008 Pila-Zannier paper identified at
intake is a plausible primary source for that other record, but it has not been accepted as the
source of this target's broader o-minimal/special-point wording. Borrowing its Manin-Mumford result
would merge two separately scheduled targets. Choosing an Andre-Oort, Zilber-Pink, special-point
finiteness, non-density, or methodological reduction statement would instead invent a variant.

The missing choices alter the proposition rather than its notation:

- the ambient algebraic, Shimura, or definable object and its base field;
- the o-minimal structure, definability language, and uniformization or period map;
- whether "special" means torsion, CM, Shimura-special, or another arithmetic locus;
- irreducibility, connectedness, dimension, and algebraic-part conventions;
- height and complexity normalizations and bounded-height finiteness assumptions;
- Galois-orbit, counting, and functional-transcendence inputs;
- whether the conclusion is finiteness, non-density, or containment in finitely many special
  subvarieties, including empty and zero-dimensional cases.

Consequently there is no canonical human proposition from which to derive minimal imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. Encoding an arbitrary `Special` predicate or
assuming the desired arithmetic-geometric inputs would be a broadened placeholder, not the exact
theorem. No Lean declaration, axiom, `sorry`, weakened special case, or substitute theorem was
introduced. Machine debt remains `M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing pinned environment is usable: Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 hashes are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

A narrow pinned-mathlib source search found model-theory infrastructure and generic torsion APIs,
but no Pila-Zannier, o-minimal, special-point, Manin-Mumford, torsion-coset, or unlikely-intersection
declaration under the searched terms. This negative feasibility result is not an anchor audit and
does not replace the missing source statement. There is no applicable
`lake env lean <canonical-target>.lean` command because the proposition to elaborate has not been
identified. The canonical `.lake` artifacts were read only; no update, build, clone, fetch, or
dependency mutation was run.

## Validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0666` | 0 | rank 710, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the ID, titles, English wording, and Pila-Zannier names | 0 | found the two inequivalent metadata records and intake discovery material; no exact source-frozen proposition or Lean target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| pinned-mathlib `rg` search for Pila-Zannier, special points, o-minimality, Manin-Mumford, torsion cosets, and unlikely intersections | 1 | no theorem-specific match (`rg` exit 1 means no match) |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary source, select and
transcribe one exact theorem/page with all incorporated definitions and assumptions, audit errata,
explain its non-duplication or explicit relationship to `THM-M-0465`, and obtain independent
approval. The review must freeze every ambient object, specialness predicate, definability and
height convention, ordered binder, hypothesis, conclusion, and degenerate case listed above. A
later statement run can then implement that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression, check alternate transports, and run
all four required mutation classes.

This is the first failed gate and does not complete the statement node or any later node. The
assigned phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
