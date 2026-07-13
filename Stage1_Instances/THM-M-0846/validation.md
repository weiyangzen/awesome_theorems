# THM-M-0846 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, primary-source lead, and discovery-only pinned Lean API probe. It does not validate an exact
Lovasz-Szegedy proposition, graphon encoding, homomorphism-density convergence statement, proof,
accepted receipt, audit completion, or theorem completion.

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

Immutable arXiv `math/0408173v2` and mutable Crossref DOI metadata were observed through bounded
HTTP requests. Their SHA-256 values were, respectively,
`cf354b99ece5ee47499de2846e2ac0e562de66f1d9f6f04f5e23946167089a03` and
`d8f88157f236a0ce84e26d9f5213b251b55b764824e3a8cc399ddec32e7443ab`. The primary text was
inspected only to identify distinct candidate roots and definitions. It was not vendored or
accepted as H0, and published-version/correction comparison plus independent review remain open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0846` | 0 | rank 1401, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6208,6213 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded download and text inspection of arXiv `math/0408173v2` | 0 | Sections 2.2 and 2.5, Theorem 2.2, and Corollary 2.6 located; distinct candidate roots recorded; primary-source discovery only |
| bounded Crossref query for DOI `10.1016/j.jctb.2006.05.002` | 0 | matching 2006 JCTB publication metadata identified; mutable bibliographic metadata only |
| bounded word-boundary search for graphon, graph limit, dense graph sequence, homomorphism density, reflection positivity, and cut distance/norm over repo-local and pinned Lean | 1 expected | no exact-topic match; bounded search is not a global absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0846/IntakeProbe.lean` | 0 | nine adjacent pinned APIs elaborated; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced; exact output SHA-256 `92621eb3bf4eecd56561137090f301abfc498dd335afeb91128c0c4e9513ef91` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0846-pycache python3 -m py_compile Stage1_Instances/THM-M-0846/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0846/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H1/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structure and whitespace results were recorded after receipt and worker-packet creation.

## Known failures and boundary

Master acceptance is pending. Exact primary-source root selection, published-version and errata
comparison, incorporated-definition/premise/conclusion/proof-boundary mapping, neighbor-target
reconciliation, and independent source review remain open. So do the canonical Lean target,
minimal imports, expression and environment fingerprints, checked transports, statement mutations,
exhaustive anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
