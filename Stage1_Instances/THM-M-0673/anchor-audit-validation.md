# THM-M-0673 anchor-audit validation

Item: `S56-M-0673-ANCHOR_AUDIT`

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Base tree: `635319193989301e577a430446e682952c51c538`

Cutoff: `2026-07-15T16:30:00+08:00`

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact theorem
`FirstOrder.Language.Ultraproduct.sentence_realize`. The audit wrapper preserves all four universe
parameters and universally introduces the frozen index, factor family, ultrafilter, language,
factor structure/nonemptiness instances, and sentence before invoking that declaration. Lean
elaborates the wrapper at `--trust=0`; the terminal theorem, formula bridge, bounded-formula body,
and wrapper are machine-reported sorry-free and depend exactly on `propext`, `Classical.choice`, and
`Quot.sound`.

The sentence body at lines 152-158 specializes `realize_formula_cast`, whose terminal substantive
route is the structural induction in `boundedFormula_realize_cast` at lines 94-144. The quantified
case uses `Classical.epsilon`. Lean's environment traversal covered 5,075 declarations in 190
modules and found no bodyless nonaxiom or unsafe declaration. This is strong nonrelease candidate
evidence, but it is not the release-grade executable, supply-chain, and TCB closure required for an
accepted `E1` receipt.

The bounded external search also found `LO.FirstOrder.models_Uprod` in
`FormalizedFormalLogic/Foundation` at immutable commit `c28942b...`. It is not the frozen theorem:
Foundation uses equality-free custom syntax, an unquotiented dependent-function carrier, one shared
universe for the language/index/factors, and an extra `Nonempty I` instance. Its source is visibly
placeholder-free at the inspected boundary, but the project is absent from the local dependency
closure, uses another mathlib pin, and was not built or transitively trust-audited here. Its direct
file has no prohibited source marker. A temporary immutable-archive scan found six `sorry` strings
inside a block-commented example and two active unsafe pretty-printing declarations in the imported
`FirstOrder/Basic` tree; no active placeholder was located, but actual axiom/unsafe reachability from
`models_Uprod` was not kernel-audited and therefore fails closed. It is classified `M5` for
statement, integration, and unresolved trust mismatch, not proof credit. Public exact-name search
otherwise found current mathlib, historical mathlib3 lineage, generated name data, and downstream
consumers rather than an independent exact Lean 4 body.

The exact pinned route is therefore a provisional `M0-W` candidate with nonrelease `E2` checking.
The accepted root remains `[H1, M3, R4]` pending downstream proof/composition/trust and master gates.
Neither `AUDIT-Z` nor theorem completion is claimed.

## Commands and results

All local Lean checks used the existing automation-provided `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch/install, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure, skill contract, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0673` | 0 | rank 717; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and clean-status checks for all manifest packages | 0 | mathlib revision `8a1783...ea95`, tree `bdc39a...5c2b`; all 11 materialized packages matched their manifest pins and were clean |
| scoped `rg` over repository-local and all 9,042 materialized-package Lean files | 0 | exact body only in pinned mathlib; other local hits were same-body consumers or target probes; result SHA-256 `ea08be86...b4eb` |
| bounded Sourcegraph exact-name and Foundation queries | 0 | current mathlib, historical mathlib3, generated consumers, and the mismatched Foundation theorem classified; response hashes and parsed counts are in `anchor-audit.json` |
| anonymous GitHub repository searches | 0 | two exact-topic queries returned complete zero results; code search returned HTTP 403 and receives no negative-evidence credit |
| grep.app exact-name queries | 0 | HTTP 429 security checkpoint; access limitation only |
| immutable raw inspection of `Foundation@c28942b...` source, toolchain, manifest, lakefile, and license | 0 | source SHA-256 `dd0b42...d631a6`; Lean 4.29.0; mathlib `1a37cd...`; Apache-2.0; semantic mismatch and source-scan boundary recorded without installing/building it |
| `lake env lean ../../Stage1_Instances/THM-M-0673/Statement.lean` and `python3 ../../Stage1_Instances/THM-M-0673/check_statement.py` from `Formalizations/Lean` | 0 | statement prerequisite re-elaborated; canonical expression fingerprint and mutations remained valid |
| `LC_ALL=C LANG=C NO_COLOR=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0673/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact wrapper elaborated; four sorry-free reports; axioms `[propext, Classical.choice, Quot.sound]`; 5,075-declaration/190-module closure; no bodyless nonaxiom or unsafe declaration; output SHA-256 `66040609...1134` |
| same Lean command without `--trust=0` | 0 | byte-identical output to the trust-zero run |
| `python3 -B Stage1_Instances/THM-M-0673/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | authority, statement, pins, hashes, bodies, machine closure, six-candidate inventory, receipt, packet, and offline Lean replay agreed |
| `python3 -m json.tool` on all audit JSON and the worker packet | 0 | all structured artifacts parsed |
| `git diff --check -- Stage1_Instances/THM-M-0673 .stage1-worker-selftest.json` plus direct untracked-file checks | 0 | no whitespace diagnostics |

## Search boundary

The inventory has six classified candidate groups, but exhaustive discovery is not claimed. Public
indexes may omit private or unindexed repositories, GitHub code search was rate-limited, and
grep.app was blocked by a security checkpoint. Those failures are recorded as limitations rather
than no-match evidence. No external project was cloned, fetched, installed, built, or added to the
dependency closure.

## Status boundary

This is self-tested worker evidence pending dependency-ordered master acceptance. The obligation
registry, proof-phase wrapper/composition, release-grade provenance and TCB closure, source `H0`,
readable `R0`, hermetic replay, independent verification, deterministic evidence bundle,
`AUDIT-Z`, release, and theorem completion remain open.
