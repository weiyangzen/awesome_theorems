# Exact-statement gate: blocked

Item: `S56-M-0723-STATEMENT`  
Theorem: `THM-M-0723`  
Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title `多项式层次` ("polynomial hierarchy") and the gloss
`复杂性类的层次结构` ("hierarchical structure of complexity classes"). The record attributes the
topic to Larry Stockmeyer in 1976, but gives no primary-source edition, theorem/page, exact
proposition, definitions, ordered binders, hypotheses, or conclusion. Stage0 explicitly leaves the
exact definitions, assumptions, proof route, dependencies, axioms, and machine artifact open.

The intake identifies Stockmeyer's paper *The polynomial-time hierarchy* only as a discovery
locator. It does not inspect and accept a pinpoint result. Several inequivalent roots remain
compatible with the metadata:

1. the definition of the hierarchy as a union of finite levels;
2. an alternating or quantified-predicate characterization of a fixed level;
3. containment between adjacent levels or containment of the hierarchy in PSPACE;
4. a conditional collapse theorem;
5. completeness of a specified problem for a specified level and reduction;
6. strictness or noncollapse, which is not an unconditional proved theorem.

These readings also require choices of alphabet and encoding, language or decision-problem
carrier, deterministic/nondeterministic/oracle/alternating machine semantics, input-size and cost
model, polynomial-bound convention, level-zero indexing, complement convention, reduction type,
uniformity, and degenerate cases. Choosing any one of them would invent or substitute mathematics.
Consequently there is no canonical expression to fingerprint, no minimal import set for that
expression, and no sound removed-hypothesis, changed-domain, binder-scope, or boundary mutation.
The rev-5.6 exact-statement gate therefore fails before proof evidence may be inspected.

`IntakeProbe.lean` was re-elaborated only to distinguish an available pinned Lean environment from
a missing mathematical statement. Its import of `Mathlib.Computability.Language` checks the
generic `Language` carrier and membership/extensionality API. It is not the target statement and
receives no statement or proof credit. A bounded exact-name search found no polynomial-hierarchy
or `ComplexityClass` API in pinned mathlib. Mathlib does contain some deterministic Turing-machine
time and polynomial-time substrate, but that does not select or encode any of the roots above.

## Validation evidence

Validation ran on 2026-07-12 (Asia/Shanghai) inside this worker clone. The existing canonical
`.lake` link and artifacts were used read-only. No update, build, dependency clone, or fetch was
run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1 through 1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0723` | 0 | rank 760; planned; legacy artifacts unaccepted; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0723/IntakeProbe.lean)` | 0 | `Language`, `Membership.mem`, and `Language.ext` elaborated |
| repository `rg` search for the theorem ID, Chinese title/gloss, English title, and candidate paper | 0 | found only underspecified source metadata, open Stage0 fields, and intake discovery material; no source-frozen proposition |
| `rg -n -i 'polynomial[ -]time hierarchy\|polynomial hierarchy\|PolynomialHierarchy\|ComplexityClass' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match exit in the bounded pinned-mathlib search |
| `rg -n 'ComputableInPolyTime\|ComputableInTime\|TM2OutputsInTime' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability --glob '*.lean'` | 0 | located generic deterministic complexity substrate, not a polynomial-hierarchy statement |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0723 -g '*.lean'` | 1 | expected no-match exit; no prohibited Lean placeholder or axiom |

## Retry condition and status boundary

An accountable source review must preserve and hash an immutable primary-source edition, select
and transcribe one exact proposition with all incorporated definitions and assumptions, audit
errata, and independently approve the mapping. It must freeze every computational-model,
encoding, cost, polynomial-bound, oracle/alternation, indexing, complement, reduction, uniformity,
quantifier, and boundary convention relevant to that proposition. A later statement run can then
encode that same claim, minimize pinned imports, serialize and hash the elaborated expression,
check alternate transports, and execute all four required mutation classes.

Verdict: `blocked`. The lifecycle remains `planned`; the root remains `[H3, M4, R4]`;
`audit_complete: false`; `theorem_complete: false`. No statement receipt or acceptance is claimed.
The assigned deliverable did not pass its gate, so no `.stage1-worker-selftest.json` is emitted.
