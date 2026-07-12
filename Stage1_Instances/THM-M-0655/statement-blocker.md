# Exact-statement gate: blocked

Item: `S56-M-0655-STATEMENT`  
Theorem: `THM-M-0655`  
Base revision: `8a4de324e430348fba945ccc31633dc565330377`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record contains only the Chinese title `联合一致性定理`, the attribution "many mathematicians", the
period "twentieth century", and the gloss `理论联合的相容性` (compatibility of the union of theories).
It supplies no primary source, numbered result, definitions, hypotheses, or quantifier order.

The accepted intake identifies Robinson's joint consistency theorem as a leading candidate, but
explicitly leaves that identification provisional. It also requires primary-source review to decide
whether this item duplicates or differs from the adjacent `THM-M-0654` Robinson consistency entry.
That unresolved distinction is material: the short gloss might refer to Robinson compatibility over
a common sublanguage, first-order compactness stated as finite satisfiability of a union, a directed
union result, or merely an informal compatibility principle. These are not interchangeable Lean
propositions.

Even within the Robinson interpretation, the record does not fix literal language inclusions versus
explicit language morphisms, a construction of the common and union signatures, translation of
sentences and theories, syntactic consistency versus semantic satisfiability, the polarity and
direction of the common-language separator condition, or the treatment of empty and inconsistent
theories. Selecting these choices would invent missing mathematics. In particular, the unrestricted
claim that separately satisfiable theories have a satisfiable union is false: two theories may force
opposite truth values for the same common-language sentence.

Consequently there is no canonical human claim from which to derive a minimal import, elaborated
expression fingerprint, checked alternate transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. No substitute theorem, abstract assumed
interface, `axiom`, `sorry`, or placeholder was introduced. Machine state remains `M4`; the
statement node and theorem completion remain open.

## Pinned Lean boundary

The pinned mathlib snapshot has general first-order logic support in
`Mathlib.ModelTheory.Semantics` and `Mathlib.ModelTheory.Satisfiability`. A narrow search found
`Theory.isSatisfiable_directed_union_iff` and special results about adjoining distinct constants.
Those declarations do not establish which mathematical theorem this metadata entry denotes and are
not the Robinson joint consistency statement. No declaration named for joint consistency, Robinson
consistency, or Craig interpolation was found by the scoped search. This is negative feasibility
evidence only, with no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0655` | 0 | rank 700, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the Chinese and English titles, gloss, Robinson candidate, and candidate paper | 0 | found only underspecified metadata, the provisional intake, and the separately owned adjacent dossier; no source-frozen proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| pinned-mathlib `rg` search for joint/Robinson consistency, interpolation, and satisfiable theory unions | 0 | only directed-union and special distinct-constant union results matched; no exact target declaration |

There is no applicable `lake env lean <target>.lean` validation because the exact expression does
not exist. Elaborating a chosen proxy or an interface that assumes the desired compatibility would
be fake statement evidence rather than the assigned deliverable.

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary or critical source,
identify an exact theorem and pinpoint pages, transcribe all incorporated definitions and
assumptions, dispose of errata, resolve the relationship with `THM-M-0654`, and independently
approve the source mapping. A later statement run can then encode precisely that claim, minimize
pinned imports, serialize and hash its elaborated expression, check alternate transports, and run
all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
