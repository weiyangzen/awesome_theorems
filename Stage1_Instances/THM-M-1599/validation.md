# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-statement and non-substitution boundaries, open
task DAG, structured intake invariants, and a narrow pinned Lean substrate probe. It does not
validate a canonical elliptic-curve cryptography proposition or proof because neither has been
selected. The automation-provided canonical `.lake` symlink was pre-existing and used read-only;
no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty
worker run is nonrelease evidence.

## Source and environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Miller publisher PDF: 417038 bytes, 10 pages, SHA-256
  `3fa85ac65d21677d27d5f3a7643faf24e66ceb1308ef1aff3eb0143be6257f69`.
- Koblitz publisher PDF: 856117 bytes, 7 pages, SHA-256
  `dab961d15831889cf1b58d9f30772bc2482f33735e6f7cb84203232d3b8fd5a4`.
- Miller and Koblitz Crossref response SHA-256 values:
  `25d509b33abdd4ba90f6585e9c8da4c42d7a43301b42916c7d77ac5184b9e26b` and
  `ff1da20deee6a58be7182b850b4b3d931cdcc1ec35ba4787c29c9f05b2ef25ae`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1599` | exit 0; rank 1219, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 11777,11782 -- Docs/researches/math_theorems.md` | exit 0; base identities above; all six uncited catalog lines originate at `bcf3f9fa...` |
| publisher PDF and Crossref inspection for Miller DOI `10.1007/3-540-39799-X_31` and Koblitz DOI `10.1090/S0025-5718-1987-0866109-5` | exit 0 for retrieved artifacts; confirmed plural cryptosystem/source-family scope, distinct mathematical and algorithmic claims, and security-assumption or heuristic boundaries; no catalog-selected proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above and clean package source |
| bounded target-topic `rg` over pinned mathlib and repo-local Lean | completed; only an irrelevant English word occurrence matched, with no elliptic-curve cryptosystem, ECDH, ECDSA, ECIES, ElGamal, encryption, or discrete-logarithm declaration; discovery only |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1599/IntakeProbe.lean` | exit 0; five generic curve/point APIs elaborated; the imported group instance reported `propext`, `Classical.choice`, and `Quot.sound`; exact output hash is bound in the provisional receipt |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1599-pycache python3 -m py_compile Stage1_Instances/THM-M-1599/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-1599/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; authority identity, source/dependency pins, null target, H5/M4/R4 boundary, artifact hashes, provisional packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1599/check_intake.py` | exit 0; public replay mode passed without the root worker packet |
| prohibited-construct scan over `IntakeProbe.lean` | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

An immutable exact source proposition, selected scheme and claim class, complete mathematical,
algorithmic and security model, definitions, ordered binders, assumptions, conclusion, proof
boundary, corrections/errata, and independent source/scope review remain open. So do the canonical
Lean expression and environment fingerprints, checked transports, statement mutations, exhaustive
formal anchor audit, discovery protocol, obligation registry, typed graphs, proof and composition,
trust and provenance closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion. These open
gates do not invalidate a truthful self-tested `planned` intake.
