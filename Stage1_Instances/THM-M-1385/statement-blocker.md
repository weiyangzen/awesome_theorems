# THM-M-1385 exact-statement gate: blocked

- Item: `S56-M-1385-STATEMENT`
- Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b`
- Base tree: `49ae48302378d63f3c54b2a43eeca26433c6b7c5`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; the statement node remains `[ ]`

## First failed gate

The exact-source-statement gate fails before a canonical Lean expression can be created. The
repository record gives only the name "Sturm comparison theorem," Jacques Sturm, the year 1836,
and the gloss "comparison of zeros of solutions." It supplies no equation, interval, ordered
binders, coefficient assumptions, solution predicate, zero convention, endpoint rule, or exact
conclusion. Stage0 explicitly leaves the precise definitions and premises open. The catalog's
`verified` label is untrusted metadata under rev-5.6.

The integrated intake inspected Sturm's 1836 memoir and found two materially different plausible
roots. Section XII, journal pages 125-126, states a global zero-count and ordered-zero comparison
for two self-adjoint equations, with positive leading coefficients, coefficient orders, and a
left-endpoint logarithmic-flux inequality. Section XVI, pages 135-136, gives the local
consecutive-zero comparison without that endpoint-ratio premise, together with a reverse
at-most-one assertion. The catalog does not select section XII, section XVI, their conjunction, or
a normalized scalar transport.

That choice changes the proposition. So do the still-unfixed coefficient regularity, interval and
endpoint conventions, classical-solution encoding, nontriviality conditions, strict-interior
policy, zero isolation and multiplicity, equality cases, singular endpoints, and treatment of the
zero solution. Selecting a convenient textbook normal-form theorem would invent or substitute
mathematics rather than elaborate the exact received target. The execution skill therefore
requires a hard stop.

The intake dependency is provisional `[_]`, has no accepted receipt ID, and is not
master-accepted. This independently prevents acceptance of the statement node, but the first
substantive failure is the absent exact source-statement selection. Consequently the canonical
human statement, formal target, minimal imports, expression hash, and target-environment
fingerprint remain null. Checked transports and the removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined, not passed. The root vector stays
`[H1, M4, R4]`.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
three imports expose ten adjacent integral-curve, derivative, interval, equality-on-set, and
support APIs. All ten `#check` commands passed, but the probe declares no Sturm target or proof
body. Its imports cannot be certified minimal for an unidentified representation and receive no
statement, anchor, or proof credit.

A bounded search of repo-local Lean and pinned mathlib found no Sturm comparison declaration. The
only `Sturm` occurrences were an unrelated research string and no target theorem; broad
zero-comparison terms produced unrelated declarations. This is narrow feasibility evidence, not
the downstream immutable anchor audit or a proof of global absence.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was used
read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was
run.

## Commands and exact results

Commands ran from the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1385` | 0 | rank 995; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` link; base revision and tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree matched; package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1385/IntakeProbe.lean` | 0 | all ten adjacent pinned APIs elaborated; no canonical target or proof body |
| bounded `rg` searches for Sturm comparison and consecutive-zero declarations | 0 | only unrelated matches; no exact target declaration identified; discovery only |
| `python3 -B Stage1_Instances/THM-M-1385/check_intake.py` | 1 | historical intake validator expects intake authority state `[ ]`; current authoritative DAG records integrated provisional `[_]`; historical intake evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-1385/statement-blocker.json` plus scoped invariant checks | 0 | identity, base, null target, unchanged debt, false completion flags, four undefined mutations, changed paths, and absent worker self-test agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-1385` | 1 | expected no-match result; no prohibited Lean declaration |
| `git diff --check -- Stage1_Instances/THM-M-1385` plus added-file `git diff --no-index --check` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | the self-test manifest is absent because the phase did not pass |

## Retry condition and status boundary

The integration lane must first master-accept a refreshed intake dependency. Accountable source and
formal reviewers must preserve and hash a lawful immutable source edition, select and independently
approve exactly one source result and proof boundary, map every incorporated definition and
assumption, audit translation, corrections, and errata, and settle its relationship to the
neighboring Sturm separation and Sturm-Liouville targets. They must freeze the ODE form,
coefficient domains and regularity, interval and endpoint rules, solution and zero semantics,
ordered binders, conclusion, alternate transports, foundation profile, and every boundary case.

A fresh statement run can then encode that same claim, minimize its pinned imports, serialize and
hash the elaborated expression and environment, compile each credited transport, and run all four
required mutation classes.

This is a blocker record, not a statement-node receipt or completion claim. No exact statement,
proof, audit completion, theorem completion, or master acceptance is asserted. Because the
assigned phase is not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json`
is emitted.
