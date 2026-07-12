# Exact-statement gate: blocked

Item: `S56-M-0715-STATEMENT`  
Theorem: `THM-M-0715`  
Worker base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
record gives the field label `可计算性理论` (computability theory), collective attribution, the
period "20th century", and only the circular gloss `可计算函数的理论` ("the theory of
computable functions"). It does not state a truth-valued proposition or identify a primary-source
edition, theorem, section, or page. Stage0 also leaves the exact definitions, premises, proof route,
equivalent formulations, axioms, and machine artifact open.

The phrase is compatible with many inequivalent claims, including closure properties of primitive
recursive functions, enumeration of partial-recursive functions, undecidability of halting,
existence of universal machines, and equivalence between recursive functions and a chosen Turing
machine model. The repository separately catalogues several such claims. Selecting one here, or
conjoining them into a survey theorem, would broaden or substitute the assigned target.

Even the intended objects are not fixed. The source does not choose total versus partial functions,
natural-number versus encoded higher-type domains, predicates versus functions, a machine model,
coding and divergence conventions, extensional equality, ordered binders, hypotheses, conclusion,
or boundary cases. Consequently there is no canonical mathematical claim to map to Lean, no
minimal import for that claim, and no elaborated kernel expression to serialize or hash. Checked
alternate-form transports and the required removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations are likewise undefined. This fails the rev-5.6 statement gate before
proof evidence may be inspected.

The existing `IntakeProbe.lean` was re-elaborated only to distinguish a working pinned Lean
environment from a missing proposition. Its eleven checks expose candidate recursive-function,
enumerability, halting, and Turing-machine APIs. They are vocabulary and feasibility evidence, not
a canonical target, and receive no statement or proof credit. No opaque predicate, assumed result,
`sorry`, `admit`, `axiom`, weakened special case, or broadened theorem was introduced.

## Validation record

Commands ran in this worker clone on 2026-07-12 (`Asia/Shanghai`). The existing canonical `.lake`
artifacts were used read-only. No update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1 through 1546; all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0715` | 0 | rank 754; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 8 'THM-M-0715\|可计算性理论\|可计算函数的理论\|Computability theory\|the theory of computable functions' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Stage1_Instances/THM-M-0715` | 0 | found the field-level catalogue text and open Stage0 fields, but no exact proposition for this target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0715/IntakeProbe.lean` | 0 | all eleven API checks elaborated; no canonical theorem target asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0715/instance.json` | 0 | intake instance JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0715/task-dag.json` | 0 | open task DAG JSON is syntactically valid |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0715 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom occurs in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0715` | 0 | no whitespace errors in tracked changes; the new blocker was also inspected directly |

The toolchain files hash in full to
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, respectively.

## Retry condition and status boundary

An accountable source reviewer must supply and independently inspect an immutable source passage
that selects one exact proposition. The review must freeze the computation model, domains,
function totality, encodings, operational and divergence semantics, equality notion, all ordered
binders and hypotheses, conclusion, and degenerate cases, and distinguish the claim from separately
catalogued computability results. A later statement run can then encode that same claim, minimize
its pinned imports, preserve and fingerprint the elaborated expression, check alternate transports,
and run all four mutation classes.

The first failed gate is exact source-statement identity. The statement node remains open at `M4`,
and the root remains `[H3, M4, R4]`; `audit_complete` and `theorem_complete` remain false. This
artifact records a truthful blocker, not completion of this or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json`
is emitted.
