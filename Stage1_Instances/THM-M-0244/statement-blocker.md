# Exact-statement gate: blocked

Item: `S56-M-0244-STATEMENT`

Theorem: `THM-M-0244`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0244-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. More importantly, the intake deliberately leaves the
canonical human claim and formal target null. The repository's complete claim is only
`角区域内的Phragmen-Lindelof原理` (the Phragmen-Lindelof principle in an angular region), together
with the theorem name, Ernst Lindelof attribution, 1908 date, and an untrusted `已验证` label. It
does not cite a numbered result or fix the angular domain, regularity, boundary estimate,
angle-sensitive growth condition, conclusion, ordered binders, proof boundary, corrections,
errata, or degenerate cases.

The inspected joint 1908 Phragmen-Lindelof paper contains materially distinct candidates. Part II,
no. 4 treats a centered sector with an existential subcritical growth exponent. Part II, no. 5
treats a connected domain contained in a sector with a different, critical-order little-o growth
condition. Part I contains a more general exceptional-boundary-point principle. The catalog does
not select among them, and the intake records no independent review approving one root. Choosing
no. 4, no. 5, or a modern variant would invent a proposition-changing source decision rather than
elaborate the exact received target.

Rev-5.6 section 5 makes statement ambiguity and a missing expression fingerprint hard blockers.
There is therefore no canonical target for which minimal imports, checked alternate transports,
or removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations can be
certified. Those mutations are undefined, not passed. No `Statement.lean`, axiom, placeholder,
weakened special case, or broadened theorem was introduced. The provisional vector remains
`[H1, M3, R4]`.

## Pinned Lean Boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact-topic
module `Mathlib.Analysis.Complex.PhragmenLindelof`. It exposes horizontal and vertical strip,
coordinate-quadrant, and right-half-plane principles. The existing `IntakeProbe.lean` elaborates
eight representative declarations and a bounded maximum-modulus ingredient through that one
direct import. These declarations use materially different domain and growth hypotheses, and the
module exposes no theorem parameterized by an arbitrary opening angle. A coordinate quadrant,
strip, or half-plane cannot silently replace the unresolved angular-region root.

The probe authenticates only the candidate API and pin. It does not select the source proposition,
declare a canonical target, establish an arbitrary-angle transport, certify target-import
minimality, or supply proof credit. The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0244` | 0 | rank 1254; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree are recorded above |
| `git blame -L 1759,1764 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `rg -n -i --glob '*.lean' 'Phragm[eé]n[- ]Lindel[oö]f\|PhragmenLindelof\|angular[ _-]*(region\|domain)\|sector[ _-]*(theorem\|principle)' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances/THM-M-0244` | 0 | found only the target probe and pinned Phragmen-Lindelof family, plus imports of that module; no repo-local source-selected arbitrary-angle target or checked transport |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0244/IntakeProbe.lean)` | 0 | nine candidate interfaces elaborated; stdout SHA-256 `e4ce8508ffbb8e8952809e962d2429dbe26e430c63d4e3243fc7847dfc03e839`; no canonical target declared |
| `python3 -B Stage1_Instances/THM-M-0244/check_intake.py` | 1 | historical intake checker expects the pre-integration authoritative intake state `[ ]`; current authority records `[_]`; it was not rewritten as statement evidence |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0244` | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0244/statement-blocker.json` and scoped invariant check | 0 each | structured blocker parses; item identity, null target/imports, undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| scoped `git diff --check` and no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is frozen to intake-time authority and its original nine-file
artifact inventory. Integration has since changed the authoritative intake cursor from `[ ]` to
`[_]`, and this statement attempt adds two blocker files. Its fail-closed replay is recorded rather
than repaired by changing historical intake evidence.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers
must preserve and hash one immutable primary or approved authoritative source, select and pinpoint
one exact proposition, transcribe every incorporated definition and formula, reconcile joint
attribution, translation, corrections and errata, and independently approve its source-to-Lean
crosswalk. They must fix the sector or contained-domain geometry, vertex, orientation, opening,
function carrier and regularity, finite-boundary and infinity behavior, exact growth filter and
critical exponent, maximum-bound conclusion, ordered binders, foundation profile, and every
boundary and degenerate case.

A later statement worker can then encode exactly that reviewed claim, minimize its pinned imports,
serialize and hash its elaborated expression and environment, compile every credited
strip/quadrant/sector transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
