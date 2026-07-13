# Statement-phase blocker

Item: `S56-M-0260-STATEMENT`

Theorem: `THM-M-0260`

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702`

## Verdict

The exact-statement gate is blocked. The repository record gives only the title "Yoccoz theorem",
the year 1988, and the gloss `Siegel盘的线性化` ("linearization of Siegel disks"). It contains no
formula, primary-source locator, incorporated definitions, ordered binders, hypotheses, conclusion,
proof boundary, corrections, or independent review. The provisional intake consequently and
correctly leaves the canonical human claim and Lean target null.

The gloss does not select one proposition. Plausible readings include Brjuno sufficiency for every
holomorphic germ, Yoccoz's non-Brjuno converse for a normalized quadratic polynomial, an iff for a
quadratic family, or a geometric or boundary theorem about an existing Siegel disk. These choices
change the domain, quantifiers, arithmetic predicate, conjugacy model, normalization, and
conclusion. Selecting a familiar variant would therefore invent or substitute mathematics rather
than elaborate the received target. The separately scheduled `THM-M-1432` repeats the same gloss
and supplies neither a scope decision nor evidence for this item.

The Societe Mathematique de France and Numdam records identified during intake are bibliographic
discovery leads only. They point to Yoccoz's 1995 Asterisque volume and distinguish a prior
Brjuno-condition sufficiency result from Yoccoz's quadratic converse. They do not select the
catalog's 1988 root, provide a definition-complete theorem crosswalk, settle corrections or errata,
or carry independent approval.

`IntakeProbe.lean` was re-elaborated against the existing pinned environment. It checks eight
generic analytic, unit-disc, and semiconjugacy interfaces, but defines no Brjuno condition, Siegel
disk, canonical target, transport, or proof body. A bounded exact-topic search of repository-local
Lean and pinned mathlib found no Yoccoz, Brjuno/Bruno, Siegel-disk, Cremer, or holomorphic-dynamical
linearization declaration under the searched terms. This is narrow statement-feasibility evidence,
not a downstream anchor audit or a global absence claim. The probe's imports cannot be certified
minimal for a target that has not been selected.

## Commands and results

Commands ran in this worker clone on `2026-07-13` (`Asia/Shanghai`). Lean used the
automation-provided canonical pinned `.lake` artifacts read-only. No update, build, clone, fetch,
or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0260` | 0 | rank 1268, planned, L0/rework-required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision `2eea9830...e702`; tree `02279a8c...b974` |
| `python3 -B Stage1_Instances/THM-M-0260/check_intake.py` | 1 | historical intake replay rejects current integrated `HEAD`; its checker is intentionally frozen to intake base `c6fd6dad...978` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at commit `98dc76e3...d40`; Lake `5.0.0-src+98dc76e` |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a31...c2b`, clean package worktree |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0260/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `67228c6c...e9c9`, empty stderr; no target theorem |
| bounded exact-topic `rg` over repository-local and pinned-mathlib Lean sources | 1 | expected no-match exit with empty output; no source-identical target found under the searched terms |
| scoped prohibited-declaration scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| finalized JSON parse and scoped blocker invariants | 0 | item identity, open blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped whitespace and file-integrity checks | 0 | both blocker artifacts have LF endings, final newline, no NUL, no trailing whitespace, and no diff-check diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the assigned statement phase did not pass |

## Retry condition

First revalidate and master-accept the intake dependency. Then preserve and hash one lawful immutable
primary or approved authoritative source and independently approve the exact root. That decision
must reconcile the 1988 provenance and `THM-M-1432`, and freeze the germ or quadratic model,
rotation-number and Brjuno conventions, analytic-conjugacy direction and normalization, every
ordered binder and hypothesis, the exact conclusion and proof boundary, corrections and errata,
alternate encodings, foundation and computation profiles, and all degenerate cases. A fresh
statement worker may then encode only that claim, minimize pinned imports, serialize and hash the
elaborated expression and environment, compile every credited transport, and run the removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

The root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. `H5`
classifies the received catalog wording as not yet a stable proposition; it does not refute any
properly stated Yoccoz theorem. This blocker is not a statement-node receipt or completion claim, so
no `.stage1-worker-selftest.json` is emitted.
