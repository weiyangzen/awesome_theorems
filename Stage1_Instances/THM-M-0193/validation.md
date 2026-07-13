# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean discovery probe.
It does not validate a canonical Pythagorean proposition or proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

The Casey/Euclid files were downloaded to `/tmp` only for source inspection and hashing. They were
not added as dependencies or accepted source evidence. The recorded structured replay recipes use
only repository and already pinned inputs and deny network access.

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
- Pinned right-angle module SHA-256:
  `821f1d55c3d3bdc7e9d28b178a90d2706e3f5380ca950bdc91507d6f685a3e38`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0193` | exit 0; rank 1222, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1394,1399 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| two bounded `curl --http1.1 -L --fail --max-time 60` requests for Gutenberg ebook `21076` PDF and TeX | exit 0; 1,860,807-byte PDF SHA-256 `fa77c91ea6b1e31fe09dea4d9a4310e7f8345dba5be0563603f62e7742ffce5c`; 628,744-byte TeX SHA-256 `7cf5f99d98b81e395ccbd90f519ed653d27c5688878a5743b0293d78bc151647` |
| `rg`/`sed` on the downloaded TeX and `pdftotext`/`awk` on the PDF | exit 0; Proposition XLVII statement at TeX lines 3795-3796 and PDF page 53; printed pages 42-43; source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty status |
| bounded `rg` and source inspection for Pythagorean, right-angle, squared-distance, norm, and inner-product declarations | exit 0; direct affine iff and vector/inner-product candidates found; integer-triple and unrelated results kept outside the root |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0193/IntakeProbe.lean)` | exit 0; six direct or adjacent pinned APIs elaborated; the two inspected iff declarations reported only `propext`, `Classical.choice`, and `Quot.sound`; complete stdout SHA-256 `4a10c782d686b5c81a4dfc43132ef324dae8429805709fb000d4921e80cf47da`; no target theorem declared |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `python3 -c` AST parse of `check_intake.py` | exit 0; scoped validator syntax is valid without generating files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0193/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, H1/M3/R4 null-target boundary, source and pin hashes, artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0193/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` loop plus scoped `git diff --check` | exit 0 for whitespace validation; no trailing-space diagnostics |

## Known open gates

An accepted immutable source edition and exact proposition, historical attribution review,
definition/assumption/conclusion/proof-boundary/translation/errata mapping, independent source
review, ambient affine domain and dimension, point ordering, nondegeneracy, square representation,
equality orientation, forward-versus-iff scope, and every boundary case remain open. So do exact
target elaboration and mutations, exhaustive anchor/provenance/trust audits, discovery and
obligation freezes, typed graphs, proof and composition, readable reconstruction, hermetic replay,
deterministic evidence bundle, independent verification, master acceptance, audit completion, and
theorem completion. These gates do not invalidate a truthful self-tested `planned` intake.
