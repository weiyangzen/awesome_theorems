# Intake validation

Base revision: `2eea98305d46266f078a50cf0e85853bf6a5e702` (tree
`02279a8caa5f31ed8e37e35c8584a336eed9b974`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement ambiguity and non-substitution
boundaries, open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical Borel-Cantelli proposition or a target proof because neither has been
frozen. The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
run is nonrelease evidence.

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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0285` | exit 0; rank 1291, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| repository source and Stage0 inspection plus Git provenance checks | exit 0; both catalog copies contain only the uncited family gloss and Stage0 leaves the exact statement and formal boundary open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded `rg` search for Borel-Cantelli in repo-local Lean and pinned mathlib | completed; first, second, and Levy candidate families located; adjacent THM-M-1009 artifacts explicitly not credited |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0285/IntakeProbe.lean)` | exit 0; four candidate interfaces elaborated; both customary endpoints reported `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `12eaa612e82f8e85f2a0a6988e8cd87da413d7b7573ee51489714f08a686ee3e` |
| `python3 -m json.tool` on all structured owned JSON and the root worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0285-pycache python3 -m py_compile Stage1_Instances/THM-M-0285/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0285/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, null target, H1/M3/R4 boundary, pins, artifact hashes, provisional receipt, packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| scoped new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An accepted immutable source edition, exact theorem locator and proposition, first-versus-second-
versus-paired decision, domains, event measurability, independence, convergence/divergence and
limsup encodings, conclusion, boundary cases, errata audit, and independent source review remain
open. So do the canonical Lean expression and environment fingerprints, minimal imports, checked
transports, statement mutations, exhaustive formal anchor audit, discovery protocol, obligation
registry, typed graphs, proof and composition, provenance and trust closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These open gates do not invalidate a truthful self-tested
`planned` intake.
