# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and a pinned Lean candidate-interface probe. It does not validate a canonical
intermediate-value statement or proof because the received gloss does not choose a truth-valued
proposition, ordered codomain, binders, hypotheses, or conclusion.

The automation-provided `Formalizations/Lean/.lake` symlink was present before this work and was
used read-only. No `lake update`, `lake build`, dependency clone or fetch, network-triggering Lake
operation, or other `.lake` mutation was performed. This dirty worker snapshot is nonrelease
evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0634` | exit 0; rank 1327, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` (preflight) | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 4699,4704 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| exploratory metadata queries to German Wikisource and Internet Archive for Bolzano's 1817 title | curl exit 28 for both; each request timed out after 30 seconds and supplied no source evidence |
| Crossref bibliographic query for `Bernard Bolzano Rein analytischer Beweis 1817` | curl/jq exit 0; results contained modern secondary work, a 1908 record, and unrelated metadata, but no immutable 1817 primary edition or theorem locator; nothing was admitted as source evidence |
| bounded `rg` search over repo-local and pinned mathlib Lean sources | exit 0; direct continuous-image and intermediate-value candidates were located; the multiple candidate families confirm ambiguity and provide discovery evidence only |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0634/IntakeProbe.lean)` | exit 0; seven direct candidates elaborated; `IsConnected.image` and `intermediate_value_univ` reported `[propext, Classical.choice, Quot.sound]`; complete stdout SHA-256 `326ce5623e9287d05b5c1130e71cfe726f61e53335212232c762604d03ff302e` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0634/check_intake.py').read_text())"` | exit 0; scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0634/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; authorities, source and dependency pins, H1/M4/R4 planned state, null target, artifact hashes, receipt/packet, candidate interfaces, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0634/check_intake.py` | exit 0; packet-free public replay mode passed |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is permitted |
| scoped new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable primary or authoritative edition, exact proposition/page, incorporated definitions,
ordered binders, assumption and proof crosswalk, translation, corrections or errata, reconciliation
with `THM-M-0626`, and independent review remain open. So do the canonical Lean expression and
environment fingerprint, checked alternate forms, statement mutations, exhaustive anchor and
terminal-body provenance audit, discovery and obligation freezes, typed graphs, proof and
composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion.

These failures do not invalidate a truthful, self-tested `planned` intake. They do prevent every
statement, H0, M0, proof, audit-completion, and theorem-completion claim.
