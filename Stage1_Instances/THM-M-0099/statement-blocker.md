# Exact-statement gate: blocked

Item: `S56-M-0099-STATEMENT`

Theorem: `THM-M-0099`

Base revision: `b4e1220a37cc10a96534cfd411e3b29523d7fd81` (tree
`a67dd08a83c396119f4762e0ff109cd0df43ee60`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0099-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is explicitly unaccepted and
non-content-addressed, has no accepted receipt ID, and requires independent source,
duplicate-resolution, formal, and integration review before dependent statement work. It
deliberately leaves the canonical mathematical statement and Lean target null.

Independently, the repository record does not identify one exact proposition. It supplies only the
title "Ngo Bao Chau theorem," the year 2008, and the gloss "proof of the Fundamental Lemma." A
second target, `THM-M-0434`, has the same author, year, and gloss. No accepted decision says whether
the records are aliases, a catalog collision, or intentionally different roots. Borrowing the
neighbor's legacy statement-shape artifact would violate target ownership and would not solve the
source ambiguity.

The inspected primary-source lead is Ngo's arXiv `0801.0446v3`, *Le lemme fondamental pour les
algebres de Lie*. Its introductory Theorem 1 and detailed Theorem 1.11.1 give related formulations
of the Lie-algebra Fundamental Lemma. The detailed formula is

```text
O_a^kappa(1_{g_v}, dt_v) = q^(r^G_{H,v}(a_H)) SO_{a_H}(1_{h_v}, dt_v).
```

The source's section 1.11.3 relates this to the discriminant-normalized introductory equation.
However, the definitions and hypotheses preceding Theorem 1.11.1, the normalization bridge, the
equal-characteristic proof and Waldspurger unequal-characteristic transfer boundary, the
nonintegral zero case, and the exact choice between the two formulations have not been transcribed,
preserved, and independently approved for this target.

Those choices change the proposition rather than merely its notation. They include the complete
discrete valuation ring and local field, reductive group scheme and Weyl-order restriction,
pointed endoscopic datum, matching regular semisimple classes, regular centralizers, Haar-measure
transport, kappa and stable orbital integrals, discriminants, transfer factors, characteristic
branch, ordered binders, and degenerate cases. Encoding abstract predicates or arbitrary integral
functions would substitute a broad statement shape for Ngo's theorem; assuming their comparison
would assume the desired result.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a missing elaborated
expression fingerprint hard blockers. There is consequently no canonical expression for which
minimal imports, fixed context, checked transports, or removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations can be certified. Those mutation tests are
undefined, not passed. The root remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborated under the pinned environment. It checks three
adjacent APIs: nonarchimedean local fields, schemes, and Haar measures. They are possible substrate
only. The probe declares no canonical target, checked transport, or proof body, so its imports
cannot be certified minimal for the absent target.

A bounded pinned-mathlib search found only unrelated uses of "fundamental lemma" in homotopical
algebra and the Selberg sieve. An exact-topic search found no endoscopy, transfer-factor,
orbital-integral, stable-conjugacy, hyperspecial, or parahoric API. The repo-local
`S1_M_083.lean` file belongs to `THM-M-0434`, describes itself as a statement-shape boundary, and
uses abstract fields and functions rather than a source-faithful object model or proof. It is not
imported or credited here. These searches are bounded discovery evidence, not an exhaustive anchor
audit or proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink exposed the canonical pinned artifacts and was used read-only.
No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0099` | 0 | rank 1115; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided untracked `.lake` symlink existed; base identifiers appear above |
| `git blame -L 726,731 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0099/IntakeProbe.lean` | 0 | three adjacent APIs elaborated; stdout SHA-256 `6301409cbcad14585946ce70a8fdee223e07d8322d672e5090ba652b0391136f`; no target or proof body declared |
| bounded exact-topic `rg` in pinned mathlib | 0/1 | two unrelated "fundamental lemma" matches; exact endoscopy/orbital-integral terms had the expected no-match exit 1; bounded discovery only |
| `python3 -B Stage1_Instances/THM-M-0099/check_intake.py` | 1 | historical intake replay stops at its assertion that authoritative intake state is `[ ]`; integration now records provisional `[_]`; this known stale-intake failure is not statement evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0099/statement-blocker.json` plus a scoped Python invariant check | 0 | JSON parsed; item and target identity, blocked `[ ]` state, null statement surfaces, four undefined mutation classes, unchanged debt, empty evidence lists, false completion flags, and absent self-test agreed |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe)\b' Stage1_Instances/THM-M-0099` | 1 | expected no-match result; no forbidden Lean declaration or proof placeholder found |
| `git diff --check -- Stage1_Instances/THM-M-0099` and `git diff --no-index --check /dev/null <new-file>` for each blocker artifact | 0 / 1 | tracked check had no diagnostics; each no-index check returned only the expected new-file difference status and no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The finalized JSON blocker was parsed and scoped invariants checked for item identity, null target,
null imports and fingerprints, unchanged debt, four undefined mutation classes, false completion
flags, and the no-self-test boundary. A prohibited declaration scan over the owned Lean probe found
no forbidden declaration or proof placeholder. New-file and scoped whitespace checks passed.

## Retry Condition And Status Boundary

The intake dependency must be independently reviewed and master-accepted. Accountable reviewers
must resolve ownership with `THM-M-0434`, lawfully preserve and hash one immutable source edition,
select one exact source proposition, and independently approve every incorporated definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, erratum, characteristic
branch, normalization, and boundary case.

A later statement run can then encode exactly that approved source model, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. No `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, accepted state, statement fingerprint, or proof credit is claimed.
