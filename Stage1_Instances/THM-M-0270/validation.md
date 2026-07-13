# Intake validation

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Fatou proposition or
proof because source variant selection and statement freeze remain open. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only. No update, build, clone, fetch, or
other dependency mutation was performed. Dirty worker evidence is nonrelease.

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

## Source boundary

Axler's author-hosted page, dated current open-access PDF, and errata page were retrieved for
bounded inspection. Section 3A, Exercise 17, printed page 86 states and names the standard Fatou
inequality. The PDF digest is
`7a7ab07fb74f5394c3180da51875ec467a0d89627321c8b2624b6b9b9585fb4e`; the errata-page digest is
`20d3f842d10d6b4529cbdc9459f50debb2e81790deeb380ede3be0c0b6349fb8`, with no bounded-search
match for Fatou, page 86, or Exercise 17. The source is a modern mutable lead and the proof is left
as an exercise, so it receives H1 rather than H0. Crossref metadata located the matching-year 1906
Fatou paper but no exact lemma passage was inspected or credited.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0270` | exit 0; rank 1277, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1943,1948 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded retrieval and inspection of Axler's author page, current PDF, and errata page | exit 0; Section 3A Exercise 17, page 86 inspected as an H1 modern source lead; response and PDF digests recorded in `instance.json` |
| bounded Crossref inspection for DOI `10.1007/BF02418579` | exit 0; matching P. Fatou 1906 paper metadata located, but no exact Fatou-lemma passage or source crosswalk established |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0270/IntakeProbe.lean)` | exit 0; two direct named Fatou interfaces and three adjacent APIs elaborated; both candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `383e38620a29d7f4812de9da059233c9125365472b6c9ec1e769cf9b47d01008` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; the two direct declarations and adjacent uses were located; no source-identical target or proof credit was inferred; this is intake discovery, not an exhaustive anchor audit |
| `python3 -m json.tool` on the structured intake artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0270-pycache python3 -m py_compile Stage1_Instances/THM-M-0270/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0270/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, source and dependency hashes, H1/M3/R4 boundary, null target, exact artifact inventory, receipt/packet agreement, probe digest, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped per-file new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An immutable exact source result, incorporated definitions, ordered statement, assumption and proof
map, historical provenance, translation, complete correction audit, and independent source review
remain open. So do canonical Lean expression and environment fingerprints, checked transports,
statement mutations, exhaustive anchor and terminal-body provenance audit, discovery and obligation
freezes, typed graphs, proof and composition acceptance, transitive trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.
