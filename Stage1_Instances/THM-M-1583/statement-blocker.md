# Exact-statement gate: blocked

Item: `S56-M-1583-STATEMENT`

Theorem: `THM-M-1583`

Base revision: `e179b2be594419aa5fb33c3862f73491fdaf113e` (tree
`8c1da8dad4712804811f550b583129e7b73effdc`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1583-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this dependency-ordered
attempt, so pending acceptance did not prevent investigation. The intake receipt is
non-content-addressed, declares `accepted: false`, has no accepted receipt ID, and deliberately
leaves the canonical mathematical statement and Lean target null. It is also bound to an older
repository revision and older blueprint and execution-DAG bytes. Master acceptance remains
necessary before any eventual accepted statement transition.

Independently and decisively, the exact-statement gate cannot pass from the authoritative
repository record. The complete record is the title `算法信息论`, attribution to Ray Solomonoff,
Andrey Kolmogorov, and Gregory Chaitin, the period 1960s, and the gloss `信息的算法理论` (`the
algorithmic theory of information`). It gives no citation, truth-valued proposition, definitions,
object domain, machine model, encoding, ordered binders, hypotheses, conclusion, proof boundary,
correction history, or boundary cases. Stage0 explicitly leaves the precise definitions and
premises and every formal field open. The catalog's `已验证` label is untrusted metadata under
rev-5.6.

Algorithmic information theory is a field containing materially different theorem families,
including invariance for a selected description system, incompressibility counting,
uncomputability or semicomputability of a chosen complexity, coding theorems, randomness
characterizations, Solomonoff dominance or convergence, Chaitin incompleteness, and results about
a fixed machine's halting probability. These require different machines, encodings, complexity
variants, constants, probability objects, computability predicates, and conclusions. The
repository selects none of them.

Neighboring records make substitution especially unsafe. `THM-M-1582` separately owns Kolmogorov
complexity and its minimum-description gloss; `THM-M-1584` separately owns Chaitin's uncomputable
number. The computer-science catalog also has distinct Kolmogorov-complexity and
incompressibility records. Choosing a familiar theorem from any of these families, or conjoining
several results to represent the field, would invent, broaden, or substitute mathematics rather
than elaborate the exact received target.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which a minimal import
set, checked alternate transport, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are
undefined, not passed. The vector remains `[H5, M4, R4]`. No `Statement.lean`, theorem
declaration, proof body, weakened special case, broadened interface, axiom, or placeholder was
added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its two
direct imports expose partial-recursive code and evaluator interfaces together with finite
uniquely-decodable coding and Kraft-McMillan. All seven checks pass. The probe defines no source-
selected plain or prefix-free complexity, optimal universal machine, universal semimeasure,
randomness predicate, Solomonoff prior, Omega object, canonical target, checked transport, or
proof body. Its imports therefore cannot be certified minimal for an absent canonical statement.

A bounded lexical search of pinned mathlib and repository-local Lean found only the probe's own
disclaimer under the recorded exact-topic terms. It located no target declaration for algorithmic
information, Kolmogorov complexity, a universal prefix machine, Solomonoff induction, Chaitin
Omega, or Martin-Lof randomness. This is discovery-only feasibility evidence, not the downstream
immutable anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1583` | 0 | rank 1205; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `rg -n -C 6 'S56-M-1583\|THM-M-1583' Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | located the exact target, dependency, open statement node, owned path, deliverable, and gate |
| `git blame -L 11665,11670 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record is only the field metadata described above |
| exact `sha256sum` argv recorded in `statement-blocker.json` | 0 | hashes of all authority, source, intake, probe, toolchain, lock, and three relevant pinned mathlib inputs match the structured fields |
| `python3 -B Stage1_Instances/THM-M-1583/check_intake.py` | 1 | historical intake replay stops because it freezes intake authority state as `[ ]`, while integration records provisional `[_]`; its original nine-file inventory also becomes historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1583/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `eb75d536041de2a97c47c9c59db16fc101d1da563691d7e6f9a285b88f03a91a`; no canonical target or proof body |
| `rg -n -i --glob '*.lean' '(algorithmic[ _-]*information\|kolmogorov[ _-]*complex\|universal[ _-]*prefix\|solomonoff\|chaitin[ _-]*(omega\|Omega)\|martin[ _-]*l[oö]f\|prefix[ _-]*complex\|plain[ _-]*complex)' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems Stage1_Instances/THM-M-1583` | 0 | only the intake probe disclaimer matched; no target declaration was located |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1583` | 1 | expected no-match result; no prohibited declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1583/statement-blocker.json` and the exact `jq -e` invariant argv in the structured blocker | 0 | finalized JSON and blocked-state invariants passed |
| `git diff --check -- Stage1_Instances/THM-M-1583 .stage1-worker-selftest.json`, plus `git diff --no-index --check -- /dev/null` for each added blocker file | 0 for tracked scope; expected added-file exit 1 with empty output per new file | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is intentionally absent because the statement deliverable did not pass |

The historical intake checker is frozen to its original base, authority state, hashes, and
intake-only artifact inventory. This statement run records that limitation instead of rewriting
the intake checker, receipt, instance, task DAG, generated blueprint, or authoritative execution
DAG to manufacture agreement. Final JSON, scoped invariants, whitespace, and absent-self-test
checks are recorded in the structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must then correct, redirect, or split the field label; lawfully preserve and hash one immutable
primary or approved authoritative source; select and independently approve one exact proposition;
resolve ownership relative to `THM-M-1582`, `THM-M-1584`, and the separate computer-science
records; and map every incorporated definition, machine and encoding model, complexity or
probability convention, constant dependency, ordered binder, hypothesis, conclusion, proof
boundary, correction, erratum, and degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
