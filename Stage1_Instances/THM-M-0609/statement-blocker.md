# Exact-statement gate: blocked

Item: `S56-M-0609-STATEMENT`  
Theorem: `THM-M-0609`  
Base revision: `63728668acb87acd4bab7e755151dce89dc1eeb4`

## First failed gate

The repository record does not identify a mathematical proposition. It supplies only the title
"Floer homology", Andreas Floer, the year 1988, and the gloss "an invariant in symplectic geometry
and low-dimensional topology". That wording leaves the theory, geometric objects, coefficient
system, grading, analytic hypotheses, auxiliary data, and kind of invariance unspecified. These
choices change both the binders and the conclusion, so they cannot be recovered by elaboration.

The three primary-source candidates recorded by the accepted intake do not resolve this ambiguity.
Selecting a construction or invariance result from one of them would add information absent from
the catalogue. In particular, selecting Lagrangian-intersection theory would silently overlap the
separate `THM-M-0611` target, while selecting instanton theory would overlap `THM-M-0610`. A generic
statement spanning all Floer theories would instead broaden incompatible analytic constructions.
The rev-5.6 hard-stop rule therefore applies: the source statement cannot be identified without
inventing missing mathematics.

## Lean statement consequence

No faithful canonical Lean expression exists until the source claim is disambiguated. The pinned
mathlib snapshot also contains no source file mentioning Floer theory, pseudoholomorphic curves,
almost-complex geometry, a symplectic-manifold API, or Hamiltonian orbit/diffeomorphism machinery.
Its general homological-complex API cannot encode the missing geometric and analytic content by
itself.

Introducing caller-supplied types and predicates for a Floer complex and its invariance would
assume exactly the content at issue. Replacing the target with ordinary chain-complex homology,
Morse homology, or a formal `d^2 = 0` fact would be a weakened substitute. Consequently this phase
creates no `.lean` declaration and claims no minimal-import set, elaborated-expression fingerprint,
checked transport, mutation result, proof credit, audit completion, or theorem completion. Machine
debt remains `M4`.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` artifacts
were read only. No dependency update, build, clone, or fetch was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0609` | 0 | Rank 646, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository search for `THM-M-0609` and the Chinese and English catalogue labels | 0 | Located only the generic catalogue record, blueprint projections, and accepted intake dossier |
| pinned-mathlib source search for Floer and the required symplectic/analytic vocabulary | 1 | No matching Lean source file |

There is no applicable `lake env lean <target>.lean` command: the source does not determine the
expression such a file would contain. Elaborating an invented predicate shell would not validate
the assigned exact target.

## Retry condition

The catalogue owner or a source-review phase must identify one exact primary-source proposition,
including immutable edition, theorem/page locator, Floer variant, ordered binders, geometric and
analytic hypotheses, coefficients, grading, auxiliary choices, and conclusion, while explaining
its boundary from `THM-M-0610` and `THM-M-0611`. A later statement run must then map those notions
to pinned Lean definitions, find the minimal imports, preserve and hash the elaborated expression
and environment fingerprint, compile any claimed transports, and distinguish the required removed-
hypothesis, changed-domain, binder-scope, and boundary mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
