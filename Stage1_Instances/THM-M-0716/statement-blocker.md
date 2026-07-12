# Statement-phase blocker

Item: `S56-M-0716-STATEMENT`  
Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`  
Checked: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The exact-statement gate is blocked before a canonical Lean declaration can be created. The only
repository wording is `原始递归函数与部分递归函数` ("primitive recursive functions and partial
recursive functions"). It names two function classes but contains no mathematical relation and
therefore is not a proposition. The accompanying attribution to Kurt Godel and year 1931 do not
identify an edition, theorem or definition number, page, exact transcription, or errata record.

Several non-equivalent propositions fit the wording: every primitive recursive function is
computable; every such total function is partial recursive after coercion; partial recursive
functions arise by adding unbounded minimization to primitive recursion; or primitive recursive
functions form a proper subclass of a larger computability class. The record also leaves open the
domain and codomain, unary versus coded finite arity, total versus partial codomain, and divergence
semantics. Selecting any one of these would broaden or substitute the source rather than elaborate
its exact target.

The nearby Stage0 entries do not disambiguate this item. `THM-C-0022` separately states that
primitive recursive functions are a proper subset of Turing-computable functions, while
`THM-C-0023` separately states an equivalence involving mu-recursive functions. Importing either
claim into `THM-M-0716` would collapse distinct repository targets without source evidence.

Pinned mathlib provides all of `Nat.Primrec`, `Primrec`, `Nat.Partrec`, `Partrec`,
`Primrec.to_comp`, and `Computable.partrec`. The existing `IntakeProbe.lean` elaborates those APIs
with the pinned environment. This establishes only that candidate encodings are available; it
cannot select the missing relation, and no proof body or candidate theorem is credited.

First failed gate: rev-5.6 section 5 exact canonical mathematical claim, before Lean target
elaboration, expression hashing, checked transports, or semantic mutation tests. Machine status
remains `M4`; lifecycle remains `planned`; no audit or theorem completion is claimed.

## Retry condition

Retry only after an immutable primary-source artifact, or an independently accepted exact
transcription, supplies and reviews all of the following:

- an edition and theorem/definition/section/page locator, with errata status;
- the exact relation asserted between primitive and partial recursive functions;
- ordered binders, domains, codomains, arity/coding convention, and hypotheses;
- the total-to-partial coercion and divergence conventions, where applicable;
- the exact conclusion and the treatment of boundary or degenerate cases.

Only then can the source wording be crosswalked to one Lean proposition and tested with minimal
pinned imports, a normalized-expression fingerprint, checked alternate encodings, and the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

## Commands and results

All commands ran in the worker clone. The canonical `.lake` artifacts were reused read-only. No
dependency update, build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0716` | 0 | rank 755; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD` | 0 | `3a479c703900e8096e6b239e7bf5b0da25472b8a` |
| `git status --short` | 0 | preflight showed only the existing untracked canonical `Formalizations/Lean/.lake` link |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes `651c8acc...b1d2` and `321626c8...d81` |
| `rg -n -C 8 '原始递归函数与部分递归函数|递归函数' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | confirmed the proposition-free source phrase and separate, more specific computability targets; found no exact source transcription |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0716/IntakeProbe.lean)` | 0 | seven candidate computability APIs elaborated; no canonical target was selected |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0716 -g '*.lean'` | 1 | expected no-match exit; no prohibited Lean placeholder or axiom declaration found |
| `git diff --check -- Stage1_Instances/THM-M-0716 .stage1-worker-selftest.json` | 0 | no whitespace errors in the owned artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test receipt correctly absent for the blocked phase |

No `.stage1-worker-selftest.json` is emitted because the assigned exact-statement phase is blocked,
not genuinely self-tested. Creating a convenient candidate declaration merely to obtain a passing
Lean command would violate the no-substitution gate.
