# Exact-statement gate: blocked

Item: `S56-M-0777-STATEMENT`  
Theorem: `THM-M-0777`  
Worker base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the repository source record. The
record supplies only the title "Godel's incompleteness theorem" and the gloss "a consistent formal
system containing arithmetic is incomplete." Stage0 explicitly leaves the exact definitions,
premises, formal system, logical foundation, proof route, and machine artifact open. The
`source_status_untrusted` value `已验证` is inventory metadata, not a proposition or evidence.

The gloss does not select one mathematical theorem. In particular, it does not fix:

1. the object language, proof calculus, or effective presentation of the theory;
2. whether "contains arithmetic" means extension or interpretation of a specified arithmetic base;
3. ordinary consistency, omega-consistency, 1-consistency, or soundness;
4. Godel's original 1931 formulation or a later Rosser-strengthened formulation; or
5. whether the conclusion is syntactic incompleteness, two unprovability claims for a constructed
   Godel sentence, or another related consequence.

Those choices alter the ordered binders, hypotheses, definitions, and conclusion. Selecting one
without an immutable pinpoint source and reviewed source-to-statement mapping would invent missing
mathematics or silently substitute a related theorem. Consequently there is no canonical Lean
expression to serialize or hash, no defensible minimal import for that expression, no checked
transport to alternate encodings, and no meaningful removed-hypothesis, changed-domain,
binder-scope, or boundary mutation suite. The rev-5.6 statement gate therefore fails before proof
or anchor evidence may receive credit.

## Pinned Lean boundary

The pre-existing `IntakeProbe.lean` imports `Mathlib.Logic.Godel.GodelBetaFunction` and checks
`Nat.beta`, `Nat.unbeta`, and `Nat.beta_unbeta_coe`. It was re-elaborated to distinguish an
available pinned Lean environment from a missing mathematical specification. Mathlib's module
documentation calls this coding lemma a step toward eventually including the first incompleteness
theorem; it is not an incompleteness statement and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json` SHA-256
digests are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical `.lake`
artifacts were consumed read-only; no update, build, clone, fetch, or dependency mutation was run.

## Exact validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0777` | 0 | rank 782, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `rg` over the repository source, Stage0 record, manifest, and owned intake for the theorem ID and Chinese/English claim | 0 | only the underspecified gloss, open Stage0 fields, manifest metadata, and intake analysis were found; no exact proposition |
| `rg` over pinned mathlib for first incompleteness, incompleteness theorem, omega-consistency, and Rosser | 0 | only beta-function documentation mentions the first incompleteness theorem; unrelated Church-Rosser declarations also matched `Rosser` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0777/IntakeProbe.lean)` | 0 | all three beta-function API checks elaborated; no canonical incompleteness target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0777 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom occurs in owned Lean source |
| `python3 -m json.tool Stage1_Instances/THM-M-0777/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0777/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Required unblocker and status boundary

An accountable source reviewer must archive and hash an immutable primary-source edition, identify
the exact theorem/section/page, transcribe all incorporated definitions and assumptions, resolve
translation and errata, and independently approve the crosswalk. Only then may a statement worker
encode precisely that claim, minimize its pinned imports, fingerprint the elaborated expression,
check transports, and execute all four mutation classes.

This statement node remains `[ ]`, with machine debt `M4`. The dossier remains `planned`; its root
remains `[H1, M4, R4]`, `audit_complete: false`, and `theorem_complete: false`. This is a truthful
statement-phase blocker, not completion of the statement node or any later node. Because the
assigned deliverable did not pass its gate, no `.stage1-worker-selftest.json` is emitted.
