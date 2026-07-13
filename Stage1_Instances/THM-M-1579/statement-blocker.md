# Exact-statement gate: blocked

Item: `S56-M-1579-STATEMENT`

Theorem: `THM-M-1579`

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1579-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits dependency-ordered
preparation from that predecessor, so the pending acceptance did not prevent this investigation.
The intake receipt is non-content-addressed, declares `accepted: false`, has no accepted receipt
ID, and deliberately leaves the canonical mathematical statement and Lean target null. Master
acceptance remains necessary before any eventual accepted statement transition.

Independently, the exact-statement gate cannot pass from the authoritative repository record. It
supplies only the title `信道容量` (`channel capacity`), Claude Shannon, the year 1948, and the
gloss `信道的最大传输速率` (`the maximum transmission rate of a channel`). It supplies no citation,
channel class, capacity definition, logarithm base or time normalization, ordered binders,
hypotheses, conclusion, proof boundary, correction history, or boundary cases. Stage0 explicitly
leaves the precise definitions and premises open, and the catalog's `已验证` label is untrusted
under rev-5.6.

The inspected primary-source family exposes materially different roots rather than selecting one.
Shannon's 1948 paper contains a noiseless-channel asymptotic definition, a finite-state
determinant/largest-root formula, a noisy discrete maximum-information-rate definition, Theorem
12's operational reliable-message limit, and a continuous bandlimited-channel definition. A
modern finite-alphabet memoryless-channel capacity formula or capacity-achieving-input theorem is
another narrower possibility. Some candidates are definitions and some are propositions; their
domains, normalization, assumptions, optimizer and limit semantics, and boundary behavior are not
interchangeable.

Selecting a familiar finite-DMC formula, promoting a definition to a theorem, choosing Shannon's
Theorem 12, or substituting the neighboring entropy or coding targets would invent, narrow, or
replace missing mathematics rather than elaborate the exact received target. The intake therefore
classifies the catalog claim as not one stable proposition at `[H5, M4, R4]`.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical expression for which a minimal import set,
checked alternate transport, or the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutations are undefined,
not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, weakened special case, or
broadened interface was added.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates in the pinned environment. Its six
direct imports expose ten adjacent probability-mass, stochastic-kernel, binary-entropy,
Kullback-Leibler, uniquely-decodable-code, and Hamming interfaces. All checks pass. The probe
defines no Shannon information rate, mutual information, channel capacity, operational-capacity
theorem, capacity-achieving input, canonical target, checked transport, or proof body. Its imports
therefore cannot be certified minimal for an absent canonical statement.

A bounded lexical search found no matching target declaration in pinned mathlib. The sole
repository-local Lean hit is a metadata string naming the external project
`abenenson/channel-capacity` at commit `a212a605d3ec5a23034e0c40f51b2b92d594efa5`; that string is
not a declaration or proof artifact. This is discovery-only feasibility evidence, not the
downstream immutable anchor audit or a global absence claim.

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
| `python3 scripts/stage1_target.py show THM-M-1579` | 0 | rank 1202; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `rg -n -C 8 'S56-M-1579-(INTAKE\|STATEMENT)\|THM-M-1579' Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Execution_DAG_rev-5.6.json Docs/Stage0_Blueprint.md Docs/researches/math_theorems.md Docs/researches/cs_theorems.md`; `jq . Stage1_Instances/THM-M-1579/{instance.json,task-dag.json,intake-receipt.json}`; scoped reads of the remaining intake files | 0 | confirmed the sparse maximum-rate gloss, inequivalent source candidates, explicit null canonical target, and unresolved proposition choices |
| `sha256sum Docs/Stage1_{Targets_rev-5.6.json,Blueprint_rev-5.6.md,Execution_DAG_rev-5.6.json} skills/execute-stage1-rev56/SKILL.md Docs/{Blueprint_Guidelines.md,Stage0_Blueprint.md} Docs/researches/{math_theorems.md,cs_theorems.md} Stage1_Instances/THM-M-1579/{README.md,instance.json,intake-receipt.json,scope-map.md,source-statement-crosswalk.md,task-dag.json,IntakeProbe.lean,check_intake.py,validation.md} Formalizations/Lean/{lean-toolchain,lake-manifest.json}` and `sha256sum` on the seven named pinned mathlib source files | 0 | exact current hashes are recorded in `statement-blocker.json`; historical intake authority hashes were not rewritten |
| `python3 -B Stage1_Instances/THM-M-1579/check_intake.py` | 1 | historical intake replay stops because it freezes the intake authority state as `[ ]`, while integration records provisional `[_]`; its original nine-file inventory is also historical after this phase |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1579/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `771e7e299be77968df4ad109582be2c9a1a023e4a931c01cfac9493b26c894fe`; no canonical target or proof body |
| `rg -n -i --glob '*.lean' 'channel[ _-]*(capacity\|coding)\|noisy[ _-]*channel\|mutual[ _-]*information\|Shannon[ _-]*(channel\|coding)' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | the sole hit was the external-project metadata string; no target declaration was located |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1579` | 1 | expected no-match result; no prohibited declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-1579/statement-blocker.json` | 0 | the finalized structured blocker parsed as valid JSON |
| scoped statement-blocker invariant assertions | 0 | identity, open blocked state, null target and imports, unchanged H5/M4/R4 vector, four undefined mutations, false completion flags, exact two-file change scope, and absent self-test agree |
| `git diff --check -- Stage1_Instances/THM-M-1579` plus per-added-file `git diff --no-index --check /dev/null <file>` | 0 for the scoped check; expected new-file status 1 with empty output for each no-index check | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to its original authority state and intake-only artifact
inventory. This statement run records that limitation instead of rewriting the intake checker,
receipt, instance, task DAG, generated blueprint, or authoritative execution DAG to manufacture
agreement.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash one lawful immutable primary or authoritative source edition, decide whether the
noun entry is theorem-eligible, select or correct one truth-valued proposition, and independently
approve a crosswalk of every incorporated definition, ordered binder, hypothesis, conclusion,
proof boundary, correction, erratum, and degenerate case. They must resolve noiseless definition
versus finite-state Theorem 1 versus noisy discrete definition versus operational Theorem 12 versus
continuous capacity versus a modern finite-DMC result, along with channel class, normalization,
optimizer, error, and limit conventions.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
