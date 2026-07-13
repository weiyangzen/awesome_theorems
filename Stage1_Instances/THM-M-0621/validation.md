# Intake validation

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba` (tree
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Urysohn proposition
or proof because exact source admission and proposition-changing statement decisions remain open.
The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
Dirty worker evidence is nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0621` | exit 0; rank 1315, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| preflight `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 4608,4613 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| bounded repository and pinned-mathlib inspection for Urysohn, normal-space, bounded, locally compact, Tietze, and metrization boundaries | exit 0; one direct exact-topic interface and distinct related families were located; this was not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0621/IntakeProbe.lean)` | exit 0; five normality or Urysohn interfaces elaborated; candidate axiom summary `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `14e80499...b45328`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0621-pycache python3 -m py_compile Stage1_Instances/THM-M-0621/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0621/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, source and dependency hashes, unclassified-H/M3/R4 boundary, null target, exact inventory, receipt/packet agreement, pinned Lean probe, and six open downstream tasks agree |
| `python3 -B Stage1_Instances/THM-M-0621/check_intake.py` | exit 0 after finalization; integration-portable replay used base ancestry and base-blob hashes for mutable authority files without requiring the ephemeral worker packet or worker `.lake` symlink |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]' Stage1_Instances/THM-M-0621` | exit 1 as expected; no prohibited declaration token; diagnostic `#print axioms` remains permitted |
| `git diff --check -- Stage1_Instances/THM-M-0621 .stage1-worker-selftest.json` plus the scoped checker's byte-level text-hygiene assertions | exit 0; no tracked whitespace diagnostics, and no trailing whitespace, missing final newline, carriage return, or NUL in any owned artifact |

## Known open gates

An immutable exact human source, its incorporated definitions, ordered statement, assumption and
proof map, translation, corrections or errata, and independent review remain open. So do the
functional-versus-neighborhood interpretation; normal-versus-normal-T1 convention; exact binders,
disjointness, codomain, range, endpoint orientation, conclusion and boundary cases; canonical Lean
expression and environment fingerprints; checked transports and statement mutations; exhaustive
anchor and provenance audit; discovery and obligation freezes; typed graphs; proof and composition;
accepted trust closure; readable reconstruction; hermetic replay; deterministic bundle; independent
verification; master acceptance; audit completion; and theorem completion. These open gates do not
invalidate a truthful self-tested `planned` intake.
