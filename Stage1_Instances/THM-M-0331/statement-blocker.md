# Exact-statement gate: blocked

Item: `S56-M-0331-STATEMENT`  
Theorem: `THM-M-0331`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "one-parameter unitary groups and self-adjoint operators"; a
duplicate physics inventory says only "the exponential relation between unitary groups and
self-adjoint operators." The accepted intake correctly records that these identify Stone's
theorem family but do not freeze one proposition.

Choosing the standard formulation from memory would invent missing mathematics. The gloss remains
compatible with the group-to-generator theorem, the generator-to-group converse, the full
correspondence, or the characterization of the generator domain by a strong derivative at zero.
Those roots differ in ordered binders, continuity topology, generator domain and equality,
uniqueness, derivative normalization, and whether the convention is `exp(i t A)` or
`exp(-i t A)`. The inventory fixes none of them and supplies no edition, theorem/page, incorporated
definitions, assumptions, errata, or independently reviewed source mapping.

Consequently there is no canonical human claim from which to derive minimal imports, a serialized
elaborated expression, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation tests. Section 5.1's exact-statement gate fails before proof or
formal-anchor evidence may be inspected. The machine state remains `M4`; statement elaboration,
audit completion, and theorem completion are false.

## Pinned Lean boundary

`IntakeProbe.lean` imports the pinned inner-product-space adjoint and partial-linear-map modules. It
checks that the environment contains `LinearPMap`, domains and closedness, `IsSelfAdjoint` and its
dense-domain consequence, unitary continuous operators, and `Continuous`. These are useful
encoding ingredients but do not select or assert any Stone theorem proposition, so the probe gets
no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0331` | 0 | rank 824; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese name, and both Chinese glosses | 0 | found only the two underspecified inventory glosses and Stage0 open fields; no exact proposition |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0331/IntakeProbe.lean` | 0 | eight substrate API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0331 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in target Lean files |
| `python3 -m json.tool Stage1_Instances/THM-M-0331/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0331` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact proposition with all incorporated definitions and assumptions,
dispose of errata, and independently approve the mapping. A later statement run can then encode
that same claim, minimize its pinned imports, fingerprint the elaborated expression, check alternate
transports, and run all four required statement mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
