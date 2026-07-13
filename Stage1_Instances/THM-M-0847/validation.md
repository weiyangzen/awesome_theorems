# THM-M-0847 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic source-family observations, and discovery-only pinned Lean API probe. It does
not validate an exact graphon proposition, graphon definition, convergence or cut-metric theorem,
proof, accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified. The
automation-provided canonical `.lake` link was used read-only; no update, build, clone, fetch, or
other dependency mutation was performed.

## Environment

- Repository base: `444860f481e8bbf64a3357008fd4d01a52006f08`
- Base tree: `dee24a14497f877ebd81712a99d2da08de62d7ad`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref metadata for monograph DOI `10.1090/coll/060` and five relevant chapters was observed
through bounded HTTP requests. Canonicalized response SHA-256 values were, respectively,
`1ed8486429669579f78ebbe972d8244942071926433fd90b715a26a26eeb5b47` and
`dd2dbb88ae80e5993717bcb89dc63b68bad1f277d7dc00dc0ed4e143b614be5f`. ArXiv API metadata and
the PDF for `math/0408173v2` had SHA-256 values
`587e8c041a0192d85a8c4c1af332f57773571b5b15b38661ca6ac7ca6223f8ee` and
`cf354b99ece5ee47499de2846e2ac0e562de66f1d9f6f04f5e23946167089a03`. No external source was
vendored. These are mutable, nonrelease discovery observations; they establish neither a selected
root nor H0.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0847` | 0 | rank 1402, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6215,6220 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref observations for DOI `10.1090/coll/060` and chapters 07, 08, 11, 14, and 15 | 0 | matching Lovász 2012 monograph and distinct graphon/cut-distance/convergence/space/algorithm chapters identified; metadata only |
| bounded Crossref and arXiv observations for `10.1016/j.jctb.2006.05.002` / `math/0408173v2` | 0 | Lovász-Szegedy dense-graph-limit lead inspected to distinguish neighboring `THM-M-0846`; no statement or proof transferred |
| bounded exact-topic search over repo-local Lean and all pinned packages | 1 expected | no `graphon`, graph-limit, cut-norm/distance, or homomorphism-density API matched; unrelated `Set.graphOn` was separately inspected and rejected; bounded search is not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0847/IntakeProbe.lean` | 0 | nine adjacent pinned APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced; exact output SHA-256 `aad813d0ba5c09cde0549564f093829276d205620d78787fd433a1684ab32a3b` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0847-pycache python3 -m py_compile Stage1_Instances/THM-M-0847/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0847/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The structural, Lean, JSON, scoped-checker, prohibited-construct, and whitespace commands were
rerun after final artifact serialization.

## Known failures and boundary

Master acceptance is pending. The catalog subject label still lacks a selected exact proposition.
Primary-source admission, pinpoint statement/proof/correction mapping, independent graphon review,
neighbor-target reconciliation, formal target and mutation certificate, exhaustive anchor audit,
obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
hermetic replay, deterministic bundle, and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
