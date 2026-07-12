# THM-M-0747 exact-statement gate: blocked

- Item: `S56-M-0747-STATEMENT`
- Base revision: `5c38e670073bc890a78e61556f36d2c6b35d257d` (tree
  `95a189ecdfe548d9cff4faaebc111079babceb92`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully completed from the authoritative repository record. The record says only `单纯集的存在性`
(existence of simple sets), attributes it to Emil Post in 1944, and supplies no definition,
bibliography, result locator, ordered binders, hypotheses, exact conclusion, proof boundary,
correction history, or independent review. Stage0 explicitly leaves the precise definitions and
premises open, and rev-5.6 treats the catalog's `已验证` label as untrusted metadata.

The intake correctly disambiguates the computability-theory notion from a simplicial set and
identifies Post's paper *Recursively enumerable sets of positive integers and their decision
problems*, *Bulletin of the American Mathematical Society* 50(5), 284-316 (1944), DOI
`10.1090/S0002-9904-1944-08111-1`. It does not, however, contain an inspected immutable copy or a
pinpoint definition and existence-result passage. Its secondary Stanford Encyclopedia lead
supports the modern convention that a simple set is computably enumerable with an infinite
complement containing no infinite computably enumerable subset. That E5 lead does not establish
the exact Post statement, conventions, assumptions, or proof boundary.

The missing choices change the proposition rather than merely its notation:

- whether the carrier is Post's positive integers or `Nat`, and the checked transport between them;
- whether a set, predicate, enumeration, partial-function domain, or another exact c.e. model is
  canonical;
- whether immunity includes infinitude in its definition or is paired with a separate infinitude
  conjunct;
- whether the conclusion uses no infinite c.e. subset or the every-infinite-c.e.-set-meets-`A`
  form, and which directions of that transport are required;
- the ordered quantifiers, predicate extensionality and decidability context, foundation profile,
  and empty, finite, complement, and indexing boundary cases; and
- the exact source definition, existence-result locator, assumptions, corrections, errata, and
  independently approved source-to-statement crosswalk.

Selecting those fields from the secondary modern definition would silently choose a convention.
Replacing the target by the weaker existence of a noncomputable c.e. set, or by an invented
`Simple` structure whose fields assume the desired witness, would substitute or assume the
theorem. Consequently there is no canonical expression on which to certify minimal imports,
serialize an elaborated-expression fingerprint, compile checked alternate transports, or run the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.
Those tests are undefined, not passed. The root remains `[H1, M4, R4]`.

The current execution DAG projects the intake dependency as provisional `[_]`, but its worker
receipt declares `accepted: false` and contains no accepted receipt ID. Section 10.2 permits this
dependency-ordered attempt; eventual statement acceptance still requires master-accepted intake
evidence. The first substantive blocker remains the absent source-frozen proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using only
`Mathlib.Computability.Halting`. It checks `REPred`, `ComputablePred`, set infinitude and
complementation, and a prospective predicate intersection form. The probe states no canonical
target or theorem, and the intake explicitly labels its expression noncanonical. Its import is
therefore only a narrow substrate import, not a certified minimal import for the unidentified
target.

A bounded name search over pinned mathlib, the shared Lean source, and repository Stage1 Lean files
found no named simple-set or immune-set declaration outside this target's probe. This is feasibility
evidence only, not the downstream immutable anchor audit or a global absence claim. The scoped Lean
scan found no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe
declaration in the owned source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0747` | 0 | rank 1030; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, manifest, catalog, Stage0 record, and complete intake dossier | 0 | the repository identifies simple-set existence but supplies no source-complete proposition; intake deliberately leaves the canonical statement, binders, imports, and fingerprints null |
| `git blame -L 5507,5512 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0747/IntakeProbe.lean` | 0 | eight adjacent APIs plus the prospective noncanonical expression elaborated; output 834 bytes, 11 lines, SHA-256 `1ae85fdbca2e36ea57c6690851c121a45a4482ad0f87b83ecb6f0a111d40accb` |
| bounded simple-set and immune-set declaration search in pinned mathlib and repository Lean | 0 | only this target's two explanatory probe lines matched; no named target declaration was located outside the probe; this is not an exhaustive anchor audit |
| `rg -n --glob '*.lean'` prohibited-construct scan over `Stage1_Instances/THM-M-0747` | 1 | expected no-match exit; no prohibited Lean declaration or escape hatch found |
| `python3 -B Stage1_Instances/THM-M-0747/check_intake.py` | 1 | historical intake-only checker expects the pre-integration intake state `[ ]`; current authority projects intake `[_]`; this phase did not rewrite historical evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0747/statement-blocker.json` and scoped blocker assertions | 0 | structured blocker syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake validator is phase-local historical evidence: it freezes the original authority state
and exact nine-file intake inventory. Integration subsequently projected the intake as `[_]`, and
adding these statement-phase artifacts also expands the target directory. This attempt records the
known phase-evolution failure rather than changing the intake checker, receipt, task DAG, generated
blueprint, or authoritative execution DAG to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or approved authoritative edition, pinpoint the exact
simple-set definition and existence result with all incorporated assumptions and proof boundaries,
audit corrections and errata, and independently approve the source-to-statement mapping. That
selection must freeze the positive-integer/`Nat` transport, object and c.e. encoding, immune-set
convention, ordered binders, exact conclusion, foundations, alternate transports, and all boundary
cases.

A fresh statement run can then encode precisely that claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes. Until then this node remains `[ ]`; `audit_complete`
and `theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
