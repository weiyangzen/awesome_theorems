# Exact-statement gate: blocked

Item: `S56-M-0697-STATEMENT`  
Theorem: `THM-M-0697`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `一阶逻辑的完备性` ("completeness of first-order logic"), accompanied
by attribution and year metadata. Stage0 leaves the exact definitions, premises, formal system,
logical foundation, proof route, and machine artifact open. The intake accordingly identifies a
theorem family and primary-source discovery leads, but selects neither an immutable pinpoint
statement nor a proof calculus.

At least three familiar but non-identical root forms remain possible:

1. every logically valid sentence is provable;
2. for every theory `T` and sentence `phi`, semantic consequence from `T` implies derivability from
   `T`;
3. every syntactically consistent theory has a model.

Moving between these forms requires fixed negation and consistency definitions, a named finitary
calculus, and checked deduction, compactness, or contrapositive bridges. The metadata also does not
fix equality, sentences versus formulas with free variables, assignments, nonempty models,
finite contexts versus arbitrary theories, ordered binders, universes, or empty and inconsistent
boundary cases. These choices change the proposition. Selecting a standard textbook variant would
therefore invent or substitute mathematics rather than elaborate the exact requested theorem.

The canonical human statement fails before minimal imports, an elaborated expression fingerprint,
checked alternate transports, or meaningful removed-hypothesis, changed-domain, binder-scope, and
boundary mutations can be established. No abstract derivability predicate, desired conclusion as
a hypothesis, placeholder, axiom, compactness substitute, or weakened empty-theory case was added.
Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports only `Mathlib.ModelTheory.Satisfiability` and checks pinned
first-order language, sentence, theory, model, satisfiability, satisfaction/consequence, and
semantic compactness declarations. A bounded search of pinned mathlib found no first-order
proof-system derivability API or theorem from semantic consequence to derivability. The probe was
re-elaborated to confirm that the semantic substrate and pinned executable are available; it is
not a completeness statement and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical `.lake`
artifacts were used read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0697` | 0 | rank 738, planned, legacy artifacts unaccepted, theorem incomplete |
| repository search for the theorem ID and Chinese/English completeness labels | 0 | found only underspecified catalog/Stage0 metadata and the fail-closed intake; no source-frozen proposition |
| pinned-mathlib searches for first-order derivability, provability, proof systems, deduction, and completeness | 0 overall | semantic and unrelated completeness text was found, but no first-order proof calculus or semantic-to-syntactic completeness declaration |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0697/IntakeProbe.lean` | 0 | all eight semantic-substrate checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0697 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in Lean source |

There is no applicable `lake env lean <canonical-target>.lean` command: the source-frozen
expression does not exist. Manufacturing an interface that assumes an arbitrary derivability
relation or the desired implication would be fake statement evidence.

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition, transcribe one
exact theorem with all incorporated definitions and assumptions, dispose of errata, select its
proof calculus and consequence conventions, and independently approve the mapping. A later
statement run can then encode that same claim, minimize pinned imports, serialize and hash the
elaborated expression, compile checked alternate transports, and run all four mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
