# Statement gate blocker

Item: `S56-M-0435-STATEMENT`  
Theorem: `THM-M-0435`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the topic "Shimura curves" and the gloss "modular curves
over quaternion algebras." It supplies no immutable primary-source theorem/page, base field,
quaternion algebra or archimedean ramification condition, order, level, moduli problem, model, or
conclusion. These omissions do not merely leave notation open: they fail to select among materially
different theorems about complex arithmetic quotients, algebraicity and canonical models,
representability, smoothness/properness, and uniformization. Selecting one would invent missing
mathematics and violate the exact-statement gate.

The intake's Shimura 1967 citation is explicitly a discovery-level candidate without a theorem or
page pinpoint. It therefore cannot determine the ordered binders, hypotheses, conclusion,
degenerate cases, or normalization required by rev-5.6 section 5.1. In particular, there is no
source-faithful expression to elaborate, fingerprint, transport, or subject to removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. Minimal imports also cannot be established
before the expression and its concrete object model are known.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_084.lean` does elaborate, but it does not repair
the source defect. Its `StatementShape` takes the decisive moduli predicate as an arbitrary
parameter; its `TargetStatementShape` similarly takes an arbitrary target predicate after locally
packaging order, level, and ramification data. Consequently these shapes can encode unrelated
predicates and are not an exact statement of a Shimura theorem. The module itself says that its
arithmetic moduli problem and representability theorem remain parameters. Its broad import list is
discovery infrastructure, not evidence for a minimal import closure.

No theorem declaration, proxy predicate, `sorry`, axiom, placeholder, broadened claim, or
substituted special case was introduced. Machine state remains `M4`, and neither statement
acceptance nor theorem completion is claimed.

## Environment fingerprint

- Repository base revision: `2937fce0ffb6c5ab95f3435ee8f4366fe8f85b6f`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `1c3ce78fe131b2bc5657075e59c22eead0f62972f279426aea4f8ec41f92f37f`.

## Validation evidence

Commands ran in this worker clone using only the existing canonical pinned `.lake` artifacts. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_084.lean` | 0 | Historical discovery module elaborated and printed its checked API and statement-shape types; it contains no exact terminal target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_084.lean` | 0 | Hashes match the environment fingerprint above |
| `rg -n -i 'Shimura[ _-]?Curve\|quaternionic.*Shimura\|Shimura.*quaternion' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching declaration or source reference in pinned mathlib; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0435` | 0 | Rank 84, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

The pre-existing untracked `Formalizations/Lean/.lake` symlink points to the canonical pinned Lake
artifacts and was not created or modified by this task. This dirty worker state is not release
evidence.

## Retry condition

The authoritative lane must provide an immutable primary-source edition and exact theorem/page,
including all referenced definitions, the base field and quaternion algebra assumptions,
ramification/splitting data, order and level, selected analytic or algebraic model, and the complete
conclusion. A later statement run can then encode that claim with concrete pinned APIs, determine
its minimal imports, fingerprint the elaborated expression, check any alternate encoding by Lean
transport, and run meaningful mutations.

Until those conditions are met, the statement phase is not genuinely self-tested to its completion
gate. Therefore no `.stage1-worker-selftest.json` is emitted.
