# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

Validation date: `2026-07-13` (`Asia/Shanghai`). This evidence covers target membership, the
planned dossier and open task DAG, repository-source provenance, the duplicate boundary, JSON and
scoped intake invariants, a narrow pinned Lean substrate probe, bounded formal-name discovery,
prohibited-construct hygiene, and whitespace. It does not validate an exact mathematical statement
or a proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

Crossref's DOI record confirmed Shizuo Kakutani, the article title, Duke University Press, volume 8
issue 3, and the 1941 publication date. The publisher download endpoint returned a 1055-byte
`text/html` access-control response (SHA-256
`8bbf66afe98d8a5e611b2a7a995d92d5ee6c14ddca3241b31658ec07aca1ef43`), not a PDF. No failed
download was retained. Therefore no exact theorem text, definitions, proof boundary, or errata were
credited. The separate `THM-M-0320` dossier was inspected as a repo-local discovery lead only; no
cross-target evidence transferred.

## Commands and results

Commands ran from the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0639` | 0 | rank 1056; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 4734,4739 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines trace to the original repository source record |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1215/S0012-7094-41-00838-4` with scoped `jq` | 0 | author, title, publisher, volume/issue, date, DOI, and publisher locator confirmed |
| publisher download to `mktemp`, followed by `wc`, `file`, and `sha256sum`, then deletion | 0 | response was 1055-byte HTML with the recorded digest, not the primary paper |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` agree with the structured fingerprint |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0639/IntakeProbe.lean` | 0 | nine adjacent Euclidean, set, compactness, convexity, and upper-hemicontinuity APIs elaborated; no theorem target asserted |
| exact-name `rg` over pinned mathlib `Mathlib` and `Archive` for Kakutani/set-valued fixed-point terms | 1 (expected no match) | no exact Kakutani fixed-point declaration found in the bounded pinned-library search; not a global absence or anchor-audit claim |
| `python3 -m json.tool` on the three owned JSON artifacts and root worker packet | 0 | all structured artifacts parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0639-pycache python3 -m py_compile Stage1_Instances/THM-M-0639/check_intake.py` | 0 | scoped validator syntax checked without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-0639/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, manifest, planned H1/M4/R4 boundary, null formal target, artifact/packet agreement, and six open downstream tasks passed |
| `python3 Stage1_Instances/THM-M-0639/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; each new-file exit 1 was only the expected content difference |
| `git diff --check -- Stage1_Instances/THM-M-0639 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0639-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Primary-source admission and independent review,
duplicate disposition, exact target elaboration and statement mutations, anchor/discovery audit,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These failures prevent
statement, audit-completion, and theorem-completion claims, but do not invalidate the planned
intake.
