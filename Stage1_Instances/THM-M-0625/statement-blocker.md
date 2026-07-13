# Exact-statement gate: blocked

Item: `S56-M-0625-STATEMENT`

Theorem: `THM-M-0625`

Base revision: `fd0fab2ab7f4f514a5cc625bbce92879e718ba13` (tree
`4116d53bcf2573069e4b67205353fe3469dbe7bd`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0625-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Independently, the exact Lean 4 target cannot be
truthfully selected from the repository record without adding or deleting proposition-critical
mathematics.

The catalog supplies only `集态正规空间的可度量化` ("metrizability of collectionwise normal
spaces"). Bing's primary paper does not state that collectionwise normality alone implies
metrizability. Its directly relevant result is Theorem 10 on page 182:

> A Moore space is metrizable if it is collectionwise normal.

The same paper identifies a Moore space as a regular developable space. Thus the catalog omits the
Moore/developability hypothesis. Dropping that hypothesis broadens Theorem 10 into an unsupported
claim; Example F in the paper is collectionwise normal but not fully normal, while metric spaces
are paracompact/fully normal in the paper's setting. Substituting Theorem 14 would also be wrong:
that theorem establishes only that collectionwise normality implies ordinary normality.

Choosing Theorem 10 is plausible, but the intake deliberately does not adopt it as the canonical
root. Source identity, definition transport, correction/errata disposition, immutable
preservation, and independent source approval remain open. Proposition-changing choices also
remain for:

- the source definition of a discrete collection, including mutually exclusive closures and the
  closed union of every subcollection;
- collectionwise normality, including its indexed-family domain, open expansion, pairwise
  disjointness, covering, and no-cross-intersection clauses;
- development and Moore-space encodings, including the countable sequence of open covers and the
  point-star neighborhood refinement condition;
- Hausdorff, T1, and regularity conventions, arbitrary versus closed family members, universes,
  binder order, and index types; and
- `TopologicalSpace.MetrizableSpace X` versus existence of a compatible metric, with any checked
  transport and all empty, singleton, repetition, unused-index, and non-Hausdorff boundaries.

Rev-5.6 section 5 makes unresolved statement identity and a missing expression fingerprint hard
blockers. There is therefore no canonical target for which minimal imports, checked alternate
transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be certified. Those tests are undefined, not passed. No statement, declaration,
proof body, or debt change is proposed; the vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` imports
`Mathlib.Topology.Metrizable.Basic` and `Mathlib.Topology.Separation.Regular`. It re-elaborates
`RegularSpace`, `NormalSpace`, `normal_separation`, `Set.PairwiseDisjoint`,
`TopologicalSpace.PseudoMetrizableSpace`, and `TopologicalSpace.MetrizableSpace`. Its 595-byte
stdout has SHA-256 `5d13b384c5703a7356c7f1efa814adc0f742f68e35aec2f0cf4639f020d6c327`.

These are adjacent interfaces only. The probe defines neither collectionwise normality nor a
development or Moore space, and it declares no canonical target, source transport, or proof body.
Its imports therefore cannot be certified as minimal imports for an absent target. A bounded
exact-topic search found no Bing-metrization, collectionwise-normal, Moore-space, or screenability
declaration in repo-local Lean or pinned mathlib; this is discovery evidence, not a downstream
anchor audit or global nonexistence proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0625` | 0 | rank 1319; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 4636,4641 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S0008414X00030923 -o /tmp/thm-m-0625-bing-1951.pdf` | 0 | downloaded the Cambridge version-of-record PDF to a temporary non-owned evidence path; it was not added to the repository |
| `sha256sum /tmp/thm-m-0625-bing-1951.pdf` | 0 | SHA-256 `cbd17aac867cd231618bdc8661d37e87a22205fb20897329cce33e05a432d7e6`, matching the intake observation |
| `pdftotext -layout /tmp/thm-m-0625-bing-1951.pdf /tmp/thm-m-0625-bing-1951.txt` | 0 | extracted the temporary PDF text for bounded source reinspection |
| `rg -n 'THEOREM 10\|EXAMPLE F\|THEOREM 14\|A collection of point sets is discrete\|A space is collectionwise normal\|We call a sequence\|regular developable space' /tmp/thm-m-0625-bing-1951.txt` | 0 | pages 175-176 and 180-184 confirmed the source boundary above; this temporary reinspection remains H1 rather than accepted H0 |
| `rg -n -i '^\s*(def\|abbrev\|class\|structure\|inductive\|theorem\|lemma)\s+.*(collectionwise[ _-]*normal\|bing[ _-]*metri[sz]ation\|moore[ _-]*space\|developable\|screenab(le\|ility))' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no exact-topic declaration; adjacent API names and unrelated prose hits receive no target credit |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| pinned mathlib revision, tree, and status inspection | 0 | recorded revision/tree matched; package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0625/IntakeProbe.lean` | 0 | six adjacent API signatures elaborated; exact stdout hash recorded above; no target declared |
| `python3 -B Stage1_Instances/THM-M-0625/check_intake.py` | 1 | historical intake checker expects intake state `[ ]`; current authority records provisional `[_]`; it was not rewritten as statement evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0625` | 1 | expected no match for those prohibited declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0625/statement-blocker.json` | 0 | finalized structured blocker parsed as valid JSON |
| `jq -e '<blocked-statement invariant expression>' Stage1_Instances/THM-M-0625/statement-blocker.json` | 0 | identity, open state, null target/imports, four mutation records, unchanged vector, false completion flags, and absent self-test claim agree |
| `git diff --check -- Stage1_Instances/THM-M-0625 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0625/statement-blocker.json` and the same command for `statement-blocker.md` | 1 each | expected new-file difference status only; neither command emitted a whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because exact target elaboration did not pass |

The historical intake checker is bound to the intake-time authoritative `[ ]` state and its
original nine-file inventory. Integration has since advanced the intake cursor to `[_]`, and this
phase adds only blocker evidence. The failure is recorded rather than repaired by modifying the
historical intake receipt, checker, task DAG, generated blueprint, or authoritative execution DAG.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or approved authoritative source, adopt and
independently approve one exact proposition, and map every incorporated definition, binder,
hypothesis, conclusion, proof boundary, correction, erratum, and boundary case. In particular,
they must resolve the catalog's omitted Moore/developability hypothesis and freeze the discrete
family, collectionwise-normality, development, Moore-space, separation, metrizability, universe,
and index conventions.

A fresh statement run can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited transport,
and run all four mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement item or any
downstream item. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
