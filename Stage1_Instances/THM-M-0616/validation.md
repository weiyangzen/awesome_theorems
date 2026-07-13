# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean API probe. It
does not validate a canonical continuity proposition or proof because neither is frozen. The
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
- The three inspected mathlib source hashes are recorded in `instance.json` and checked by the
  scoped validator.

## Source discovery boundary

The author-hosted August 6, 2024 version of Sidney A. Morris's *Topology Without Tears* was
inspected outside the repository. Its observed 8,926,811-byte PDF has SHA-256
`59f33c9ffc8199210ffff837ca3d18589de69ace6518cf537c8f040e1bf1fbaa`. Section 5.1, printed
pages 110-112, gives the real epsilon-delta definition, proves the local-neighborhood bridge,
proves its equivalence with open preimages, and defines topological continuity. The source was not
added to the repository or accepted as `H0`. Catalog identity, real-versus-general scope,
definition and assumption transport, corrections or errata, lawful immutable archival capture,
and independent review remain open.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0616` | exit 0; rank 1310, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; recorded base revision and tree above |
| `git blame -L 4573,4578 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl --http1.1 -L --retry 3 --max-time 120 --silent --show-error https://www.topologywithouttears.net/topbook.pdf -o /tmp/topbook.pdf` | exit 0; downloaded the author-hosted source to a temporary file outside the repository |
| `sha256sum /tmp/topbook.pdf` and `stat -c '%s' /tmp/topbook.pdf` | exit 0 each; SHA-256 `59f33c9f...fbaa`, size 8,926,811 bytes |
| `pdftotext -layout /tmp/topbook.pdf /tmp/topbook.txt` | exit 0; the front matter and Section 5.1 were then read manually, confirming the author, August 6, 2024 version, and complete pages 110-112 real-to-real proof route; discovery lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0616/IntakeProbe.lean)` | exit 0; four direct open-preimage and epsilon-delta APIs elaborated; `continuous_def` reports no axioms and three metric candidates report `propext`, `Classical.choice`, and `Quot.sound`; output SHA-256 `5beb9ba9b26b93ea6fc96c02d5eae2a226510370676ffbb6cab82b6a7c00240c` |
| `python3 -m json.tool Stage1_Instances/THM-M-0616/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0616/task-dag.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0616/intake-receipt.json` | exit 0 after finalization; valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | exit 0 after finalization; valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0616-pycache python3 -m py_compile Stage1_Instances/THM-M-0616/check_intake.py` | exit 0; scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0616/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and authoritative-DAG identity, H1/M3/R4 planned boundary, null target, source and pin hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0616` | exit 1 as expected; no prohibited declaration token matched |
| `while IFS= read -r file; do output=$(git diff --no-index --check /dev/null "$file" 2>&1); rc=$?; if [ "$rc" -gt 1 ] \|\| [ -n "$output" ]; then printf '%s\n%s\n' "$file" "$output"; status=1; fi; done < <(find Stage1_Instances/THM-M-0616 -maxdepth 1 -type f -print; printf '%s\n' .stage1-worker-selftest.json); test "${status:-0}" -eq 0` | exit 0; every new owned file and the worker packet produced only the expected clean-new-file exit 1 and no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0616 .stage1-worker-selftest.json` | exit 0; no tracked-diff whitespace diagnostics |

## Known open gates

Catalog-to-source identity; an immutable independently reviewed source passage; real versus metric
or pseudometric domains; global, pointwise, or relative continuity; open-preimage versus local-
neighborhood packaging; quantifier, inequality, topology-distance, binder, and boundary decisions;
the canonical Lean expression and fingerprints; checked transports and statement mutations;
exhaustive anchor and provenance audit; discovery and obligation freezes; typed graphs; proof and
composition; trust closure; source-faithful readable reconstruction; hermetic replay;
deterministic evidence bundle; independent verification; master acceptance; audit completion; and
theorem completion remain open. These failures do not invalidate a truthful self-tested `planned`
intake.
