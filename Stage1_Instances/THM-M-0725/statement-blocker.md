# Exact-statement gate: blocked

Item: `S56-M-0725-STATEMENT`  
Theorem: `THM-M-0725`  
Worker base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source record. Its entire
mathematical wording is the title `指数时间层次` (provisionally, "exponential time hierarchy") and
the gloss `指数时间复杂性类` ("exponential-time complexity classes"). The record attributes the topic
only to many mathematicians in the 1970s. It gives no proposition, primary source, theorem number,
page, machine model, cost model, ordered binders, hypotheses, or conclusion. Stage0 explicitly
leaves the precise definitions, prerequisites, proof route, dependencies, axioms, and machine
artifact to be supplied.

The metadata remains compatible with inequivalent roots:

- a deterministic time-hierarchy separation instantiated at two exponential bounds;
- a nondeterministic time-hierarchy separation, with different hypotheses and diagonalization;
- a definition or characterization of `EXPTIME` or `NEXPTIME` as a union over time bounds;
- an alternation- or oracle-defined exponential hierarchy and an inclusion, equality, union, or
  collapse statement about its levels.

These choices change the quantified languages, encodings, machine semantics, bound family,
constructibility and growth conditions, reduction notion, and conclusion. Even within a time
hierarchy reading, the source does not choose the two bounds or state the separation hypotheses.
Selecting a familiar version, including `P != EXPTIME`, would invent or substitute mathematics.
The catalogue's `已验证` field is untrusted metadata and supplies no statement or proof credit.

Consequently section 5.1 fails at canonical human-claim identity. There is no exact expression to
serialize or hash, no minimal import to establish, no alternate encoding to transport, and no
sound removed-hypothesis, changed-domain, binder-scope, or boundary-case mutation suite. The
statement node remains open at `M4`; audit and theorem completion remain false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports
`Mathlib.Computability.TuringMachine.Computable` and checks mathlib's finite Turing-machine,
step-bounded output, arbitrary-time computation, and polynomial-time specialization APIs. It was
re-elaborated in the pinned environment. Those declarations are possible encoding ingredients,
not an exponential-time class or hierarchy theorem, and the probe receives no statement or proof
credit. Narrow repository and pinned-mathlib name searches found no `EXPTIME`, exponential-time
class, exponential hierarchy, or time-hierarchy declaration for this target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Exact validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0725` | 0 | rank 762, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| source search for `指数时间层次` and `指数时间复杂性类` in `Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` | 0 | found only the underspecified duplicated metadata and open Stage0 fields |
| repository search for `EXPTIME`, exponential-time/hierarchy names, and time-hierarchy names | 0 | target intake prose/probe plus one unrelated comment; no exact formal target |
| pinned-mathlib search for `EXPTIME`, exponential-time/hierarchy names, and time-hierarchy names | 0 | only an unrelated performance comment; no theorem-specific declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0725/IntakeProbe.lean` | 0 | all six candidate computation API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0725 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in owned Lean source |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition, select and
transcribe one exact proposition, dispose of errata, and independently approve the mapping. The
selection must freeze the language and encoding, deterministic/nondeterministic/alternating/oracle
machine model, runtime and input-length semantics, exact bound family, constructibility and growth
hypotheses, reduction or inclusion relation, ordered quantifiers, conclusion, and all small-input
and rounding cases. A later statement run can then encode that same claim, minimize pinned imports,
fingerprint the elaborated expression, check transports, and run all four required mutation
classes.

This is the first failed gate, not completion of the statement phase. The assigned phase is not
genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
