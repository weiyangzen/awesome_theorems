# Intake validation

Base revision: `bd80ad137c187dda02bcfcb2529360ef6d9b53eb` (tree
`65fb1d54476897700b46e671380377bdd27c4e0b`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, catalog and ambiguity freeze,
source-statement and non-substitution boundaries, open task DAG, structured intake invariants, and
a narrow pinned Lean interface probe. It does not validate a canonical Bertrand proposition or
proof because the source domain, positivity premise, and endpoint convention are not frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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
- Pinned `Mathlib/NumberTheory/Bertrand.lean` SHA-256:
  `ca1588962a2c598e0f089bda6ab9fa108e89c3ee479c76bab4914f754508eb26`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0481` | exit 0; rank 1362, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 3532,3537 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/NumberTheory/Bertrand.lean'` | exit 0; pinned revision, tree, and Bertrand source blob recorded in `instance.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Bertrand.lean` | exit 0; hashes recorded above |
| bounded repository and pinned-mathlib Bertrand search | exit 0; located the exact positive half-closed candidate, alias, large-number branch, source architecture, and modern bibliography leads; no repo-local target artifact existed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0481/IntakeProbe.lean)` | exit 0; five adjacent declarations elaborated and the candidate interface plus `n=0`/`n=1` boundary checks kernel-checked; stdout SHA-256 `5011e3aaf4fc58958951774d35f933643348108e6559b87322bc0a71f936f5f5` |
| `python3 -m json.tool` on all JSON artifacts | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0481-pycache python3 -m py_compile Stage1_Instances/THM-M-0481/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0481/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authoritative identity, null target, H1/M3/R4 boundary, source and dependency pins, provisional receipt and worker packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An approved immutable primary or authoritative source and exact proposition, domain and positivity
premise, strict/inclusive endpoint choice, `n=0` and `n=1` treatment, translation and errata audit,
and independent source review remain open. So do the canonical Lean expression and environment
fingerprints, minimal imports, checked transports, statement mutations, exhaustive anchor and
terminal-body audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust and provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
