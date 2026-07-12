# Exact Lean statement gate: blocked

Item: `S56-M-0363-STATEMENT`  
Theorem: `THM-M-0363`  
Base revision: `64b3d9781c233011aa06d7899ba7c31e8ef481ee`

## Decision

The pinned Lean environment cannot presently elaborate the exact theorem without first adding a
substantial, source-faithful formalization of real-variable `H^1(R^n)`, `BMO(R^n)` modulo
constants, Riesz transforms, and their normed-space and pairing interfaces. No exact target
declaration is therefore claimed, and the statement node is blocked rather than self-tested.

The primary announcement was inspected during this run: Charles Fefferman,
"Characterizations of bounded mean oscillation", *Bulletin of the American Mathematical Society*
77 (1971), 587-588, DOI `10.1090/S0002-9904-1971-12763-5`. On page 587, Theorem 1 says that BMO is
the dual of `H^1(R^n)`. The preceding paragraph defines BMO using locally integrable functions and
the supremum, over cubes, of average absolute oscillation, identifying functions whose difference
is constant. The paragraph following Theorem 1 regards `H^1` as the `L^1` functions whose Riesz
transforms all lie in `L^1`. The stated pairing is the integral, initially for a dense subspace of
smooth rapidly decreasing `H^1` functions.

That source identifies the theorem family much more sharply than the repository slogan, but the
required concrete Lean objects do not exist in the pinned mathlib source. Searches found no BMO,
bounded-mean-oscillation, real Hardy-space, or analytic Riesz-transform declaration. Generic
`LocallyIntegrable`, `MemLp`, integration, Schwartz-map, and continuous-linear-map APIs do exist,
as checked by `StatementProbe.lean`; they do not define either Banach space or the representation
map. Creating abstract types named `H1` and `BMO`, assuming their equivalence, or replacing the
result by a generic dual-space tautology would be a prohibited substituted theorem.

Even before implementing those missing foundations, an exact formal target must resolve details
that the two-page announcement leaves implicit or delegates to its references: the precise `H^1`
norm and completion/model, the normalization of every Riesz transform, the topology and norm on
BMO modulo constants, almost-everywhere representative equality, the construction and continuity
of the integral pairing from the dense test subspace, and whether "is the dual" is asserted
isometrically or only up to equivalent norms. These choices affect the elaborated proposition and
cannot be invented from the repository metadata.

Accordingly the ordered Lean binders, canonical expression fingerprint, minimal target imports,
checked alternate-form transports, and removed-hypothesis/domain/binder-scope/boundary mutation
suite required by rev-5.6 section 5.1 cannot truthfully be emitted. Machine state remains `M4`.
No `sorry`, axiom, proxy predicate, abstract interface, broadened claim, or special-case substitute
was introduced. The intake dependency also remains provisional (`[_]`) pending master acceptance.

## Environment fingerprint

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Inspected AMS PDF SHA-256:
  `7352edb3d25ffcfd7473ad738751b5e0d8e7dccd13540b45a57647289405524d`.

## Narrow validation evidence

Commands ran in this worker clone using only the existing canonical pinned `.lake` artifacts. No
Lake update/build, dependency fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0363` | 0 | rank 681, planned, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0363/StatementProbe.lean` | 0 | the five generic infrastructure declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `rg -n 'BMO|BoundedMeanOscillation|HardySpace|RieszTransform|Riesz transform' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching concrete analytic API in pinned mathlib; exit 1 means no match |
| `curl -L -A 'Mozilla/5.0' --max-time 30 -o /tmp/fefferman1971.pdf 'https://www.ams.org/journals/bull/1971-77-04/S0002-9904-1971-12763-5/S0002-9904-1971-12763-5.pdf'` followed by `pdftotext -layout /tmp/fefferman1971.pdf /tmp/fefferman1971.txt` | 0 | retrieved the two-page primary announcement and exposed Theorem 1 and its adjacent definitions for inspection |
| `sha256sum /tmp/fefferman1971.pdf` | 0 | source digest recorded above |

## Retry condition

Select and inspect a complete authoritative source that fixes the implicit norm and normalization
choices, then implement or pin concrete Lean definitions of Euclidean BMO modulo constants,
real-variable `H^1` via normalized Riesz transforms, the dense test subspace, and the extended
integral pairing. A later statement run can then freeze the exact binders and expression, minimize
imports, compile the source-form transports, and mutation-test all four required dimensions.

Until those conditions and the dependency gate are met, statement acceptance, audit completion,
and theorem completion are false. Because the assigned phase is not genuinely self-tested, no
`.stage1-worker-selftest.json` is emitted.
