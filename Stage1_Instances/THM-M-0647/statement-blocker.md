# Exact-statement gate: blocked

Item: `S56-M-0647-STATEMENT`  
Theorem: `THM-M-0647`  
Base revision: `12d69b6951899a8e7de7ade1dfc86ce524d34a6e`

## Decision

The authoritative repository statement is only "an infinite model has elementarily equivalent
models of different cardinalities." It does not identify a primary-source theorem or page, quantify
a target cardinal, state a language-size bound, choose a direction, or fix model and universe
conventions. The accepted intake deliberately leaves open three materially different readings:

- existence of one elementarily equivalent model whose cardinality differs from the source model;
- existence at every infinite cardinal large enough for the language;
- a paired upward/downward or elementary-substructure formulation.

These readings cannot be silently substituted for one another. In particular, the all-cardinals
form is stronger than the literal existential gloss, while a bare unequal-cardinality witness does
not determine whether the intended result is upward or downward. Selecting one would invent the
missing quantifiers and hypotheses. Therefore there is no exact canonical human claim from which
to derive a minimal import, normalized expression hash, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Machine state remains
`M3`; statement completion and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.ModelTheory.Satisfiability` and checks
`FirstOrder.Language.exists_elementarilyEquivalent_card_eq`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the declaration quantifies over every cardinal `kappa`
with `aleph_0 <= kappa` and a lifted language-cardinality bound, and returns a bundled structure
`N` with `M ≅[L] N` and `#N = kappa`. The probe elaborates successfully, establishing that a close
candidate exists. It does not establish exact identity with the underspecified source claim and
receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the pinned mathlib
revision above. The worker clone's existing canonical `.lake` link was used read only. No update,
build, dependency clone/fetch, or other `.lake` mutation was performed.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0647` | 0 | rank 693, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English names, and literal statement | 0 | only the underspecified secondary metadata, accepted intake, and adjacent theorem records were found |
| `rg` inspection of pinned `Mathlib/ModelTheory/Satisfiability.lean` | 0 | located the stronger all-cardinals candidate and its exact hypotheses |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0647/IntakeProbe.lean` | 0 | candidate presence and full declaration type elaborated and printed |
| `python3 -m json.tool Stage1_Instances/THM-M-0647/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0647` | 0 | no whitespace errors |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition, select and
transcribe its exact theorem with incorporated definitions and assumptions, dispose of errata, and
independently approve the mapping. A later statement run can then encode that claim, minimize
pinned imports, serialize its elaborated expression, check all credited transports, and execute the
four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
