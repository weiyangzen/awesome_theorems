# Statement validation record

Item: `S56-M-0276-STATEMENT`

Base revision: `902d9ce008e88a35a2307c85355560a230cc33c2` (tree
`dfc20d8141f18f6b09a03e818acfff408e836714`).

## Frozen target

`Stage1Instances.THM_M_0276.BanachOpenMappingTarget` is a closed conjunction of the ordinary
same-field Banach open mapping theorem over `Real` and over `Complex`. In each conjunct it
quantifies over independent-universe normed additive commutative groups `E` and `F`, normed-space
and complete-space instances on both, and a bundled continuous linear map `f`. Its only
mathematical antecedent is `Function.Surjective f`; its conclusion is `IsOpenMap f`.

The immutable Rotem/Tzorani notes select this scope through the standing real-or-complex scalar
convention, their definitions of Banach space and open map, and Theorem 2.2.11. The checked
`Iff.rfl` transport expands `IsOpenMap` to the source wording that `f '' U` is open whenever `U` is
open. This statement selection does not repair or credit the following printed proof, whose Baire
cover repeats the unit ball where radius-`n` balls are required. Human status therefore remains
`H2` pending a correction, independent review, catalog identity, and primary-history audit.

## Commands and results

Commands ran in this isolated worker clone on 2026-07-13. Lean used the existing canonical pinned
`.lake` artifacts read-only. No update, build, clone, fetch, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0276` | 0 | rank 1282; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| `python3 -B Stage1_Instances/THM-M-0276/check_intake.py` | 1 | known historical replay boundary: the intake checker expects authoritative intake state `[ ]`, while integration now records `[_]`; it was not rewritten or cited as statement evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...6740`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib revision/tree/status inspection | 0 | revision `8a178386...eea95`, tree `bdc39a31...e5c2b`; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0276/IntakeProbe.lean` | 0 | six exact-topic interfaces elaborated; three axiom reports contained `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `d84aba7f...04774` |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0276/Statement.lean` | 0 | exact target, expanded-open-map `Iff`, five expected mutation type rejections, and explicit root expression elaborated; stdout SHA-256 `073326d6...82aae` |
| delete the sole direct import in a temporary file and run pinned Lean | 1 | expected failure beginning with unknown `NormedAddCommGroup`; one-import necessity confirmed |
| `python3 -B Stage1_Instances/THM-M-0276/check_statement.py` | 0 | expression/source/output hashes, import deletion, six pairwise-distinct expressions, structured artifacts, authoritative item, toolchain, and dependency pins agree |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`/`opaque`, or `unsafe` declaration |
| exact JSON parse command, `validate_statement_artifacts.py`, and scoped `git diff --check` | 0 | records agree; the artifact validator checked text hygiene for every owned file and root packet; no whitespace diagnostic occurred |

## Mutation and import boundary

The removed-hypothesis mutation drops surjectivity. The domain mutation drops the entire complex
conjunct. The binder mutation asks only for the existence of one operator rather than proving the
claim for every operator. The completeness mutation removes completeness of the domain. The final
boundary mutation adds injectivity by replacing surjectivity with bijectivity, improperly excluding
noninjective quotient-type maps. Lean rejects every mutation as a term of the root, and the
validator separately compares all fully explicit expressions.

`Mathlib.Analysis.Complex.Basic` is the only direct import. It supplies the concrete real and
complex normed-field instances plus all statement vocabulary. The proof-bearing
`Mathlib.Analysis.Normed.Operator.Banach` module is not imported, and no theorem from it is invoked.

## Status boundary

This is statement-only self-test evidence pending master acceptance. The vector remains
`[H2, M3, R4]`. No open-mapping proof, accepted state, H0, M0, R0, anchor audit, obligation tree,
audit completion, theorem completion, release evidence, or master acceptance is claimed.
