# Exact-statement gate: blocked

Item: `S56-M-0781-STATEMENT`  
Theorem: `THM-M-0781`  
Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
Its complete mathematical wording is `CH和AC独立于ZF` ("CH and AC are independent of ZF"),
with the label "Cohen's theorem", Paul Cohen, and 1963. It supplies no primary-source edition,
theorem/page, incorporated definitions, hypotheses, metatheory, or meaning of independence. Stage0
explicitly leaves the exact definitions, prerequisites, proof process, axioms, and machine artifact
open. Its `已验证` field is untrusted metadata under rev-5.6.

The wording bundles at least four materially distinct directions: positive and negative
independence directions for CH, and positive and negative directions for AC. It does not determine:

- whether each direction is a syntactic relative-consistency implication, a model-existence
  implication, an unprovability result under soundness/consistency assumptions, or a construction;
- the recursively presented object theory and proof calculus used for `ZF`;
- exact object-language formulas for CH and AC and the theory-extension operation;
- whether the CH base is literally ZF or the commonly stated ZFC, and how the positive
  constructibility direction is sourced and attributed;
- the metatheory, universes, consistency/satisfiability bridge, and non-vacuity assumptions;
- which failure or equivalent form of choice the AC component asserts.

These choices change the proposition, its binders, hypotheses, and conclusion. Selecting any one
of them would invent missing mathematics or substitute a narrower theorem. In particular, taking
four arbitrary `Prop` parameters and defining independence propositionally would erase the
required object-theory content, while assuming satisfiability of the desired extensions would make
the target circular. Consequently no canonical expression can be fingerprinted, no minimal import
can be justified, and removed-hypothesis, changed-domain, binder-scope, or boundary mutations would
have no source-frozen reference against which to be checked. The statement gate therefore fails at
exact human-claim identity, before proof or candidate credit may be considered.

## Pinned Lean boundary

The pre-existing `IntakeProbe.lean` was re-elaborated only to distinguish an available pinned Lean
environment from a missing mathematical statement. Its direct imports expose first-order theories
and satisfiability, cardinal continuum/aleph objects, and the `ZFSet` API. They do not encode the
source-selected ZF, CH, or AC sentences or state any of the four independence directions.
`ZFSet.choice` derives choice in mathlib's Lean-level ZFC model and cannot witness independence of
choice from an encoded object theory. The probe is therefore infrastructure evidence only and is
not a canonical target.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` symlink and artifacts
were used read-only. No Lake update/build, dependency clone/fetch, or other dependency mutation was
run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0781` | 0 | rank 786, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for `THM-M-0781`, `科恩定理`, and `CH和AC独立于ZF` | 0 | found only the short metadata claim and open Stage0 fields; no exact source-selected proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8acc...1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0781/IntakeProbe.lean` | 0 | seven logic/set-theory infrastructure declarations elaborated; no canonical theorem asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0781 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in the target Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-0781/instance.json` | 0 | intake instance JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0781/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and status boundary

An accountable source review must preserve and hash immutable primary-source editions, identify
exact passages for all four directions (including the positive directions and their attribution),
dispose of errata, and freeze the object theory, CH/AC formulas, consistency or model semantics,
metatheoretic assumptions, universes, ordered binders, hypotheses, conclusion, and degenerate
cases. A later statement run can then encode that same claim, minimize pinned imports, serialize
and hash its elaborated expression, add checked transports, and execute the four required mutation
classes.

The first failed gate is exact source-statement identity. This node remains open at `M4`; the root
remains `[H3, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned
statement phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted and no downstream or theorem-completion credit is
claimed.
