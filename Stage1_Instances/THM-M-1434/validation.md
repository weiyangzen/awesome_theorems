# Intake validation

Base revision: `5ac2d33ee4b1a16fd90dca63313cd900ffc4bb50` (tree
`59b19df4105f58fc10c3e924c32320a284145b7c`).

Validation date: `2026-07-12` (`Asia/Shanghai`). This phase covers target membership, planned
dossier invariants, source-bibliography retrieval, JSON integrity, a bounded pinned-mathlib name
search, and a narrow Lean API probe. The automation-provided `Formalizations/Lean/.lake` symlink
existed before this work and was used read-only. No `lake update`, `lake build`, dependency clone or
fetch, or `.lake` mutation was run.

The official Annals page was retrieved twice from the URL recorded in `instance.json`; both byte
streams had SHA-256 `f050a74a...1fe6` and compared equal. The page confirms the article title,
author, journal, volume, issue, year, pages, DOI, MR, and zbMATH identifiers, but says "No abstract
available" and exposes no theorem or proof text. This supports a source lead only, not H0,
canonical-statement identity, or proof credit.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1434` | 0 | rank 932, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short` | 0 | only the pre-existing untracked automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| two `curl -L --fail --silent --show-error --max-time 30 https://annals.math.princeton.edu/1985/122-2/p06 -o <temporary-output>` retrievals, followed by `sha256sum` and `cmp -s` | 0 | identical HTML with SHA-256 `f050a74a...1fe6`; bibliography verified, no abstract/theorem text available |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| initial `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1434/IntakeProbe.lean)` with `#check Function.iterate` | 1 | `Function.iterate` was not a public identifier; the probe was corrected to the existing `Function.iterate_succ_apply` and rerun |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1434/IntakeProbe.lean)` | 0 | nine algebraic-rational, meromorphic, compactification, connected-component, iterate, and periodic-point APIs elaborated; no target theorem stated |
| bounded target-name search in pinned `Mathlib` Lean sources | 1 | expected no-match result for Sullivan/wandering-domain/Fatou-set/Fatou-component/Julia-set patterns; intake-only evidence, not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, and finalized `intake-receipt.json` | 0 | all structured artifacts are valid JSON |
| `python3 Stage1_Instances/THM-M-1434/check_intake.py` | 0 | `intake invariant check: ok`; identity, lifecycle, ownership, hashes, open DAG, and status boundary agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1434` | 1 | expected no-match result; no prohibited Lean declaration or proof hole |
| `git diff --check -- Stage1_Instances/THM-M-1434 .stage1-worker-selftest.json` | 0 | no tracked whitespace errors; `check_intake.py` separately checks line hygiene in every untracked target file and the root self-test manifest |
| `python3 scripts/lint_theorem_dossier.py THM-M-1434` | 1 | inapplicable legacy release validator: requires a direct root theorem directory and is hard-coded to the THM-M-0387 schema |

Known downstream failures remain deliberately open: primary paper text, pinpoint statement and
independent source review; canonical expression/environment fingerprints, checked transports, and
mutations; immutable formal anchor audit; obligation and discovery freezes; proof and composition;
trust closure; hermetic replay; deterministic evidence bundle; independent verification; and master
acceptance. They prevent audit and theorem completion but do not invalidate a truthful `planned`
intake.

The repository's `scripts/lint_theorem_dossier.py` is hard-coded to the direct-root
`THM-M-0387` release dossier and rejects a `Stage1_Instances` planned-intake path before inspecting
this schema. It is therefore recorded as an inapplicable legacy release validator, not as a passing
intake check. The target-owned `check_intake.py` is the narrow structured validator for this phase.
