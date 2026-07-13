# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and non-substitution
boundaries, the open task DAG, scoped intake invariants, and a narrow pinned Lean discovery probe.
It does not validate a canonical Ceva proposition or proof because neither is frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

The Prince arXiv version-1 PDF was downloaded to temporary storage only for source inspection and
hashing. It was not added as a dependency or accepted source evidence. The recorded structured
replay recipes use only repository and already pinned inputs and deny network access.

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
- Pinned algebraic Ceva module SHA-256:
  `d9a18a91b377fcf6f2b98e21ccedda58e19e57fa4364462f4fc445cbc2777d03`.
- Pinned normed Ceva module SHA-256:
  `55bd01f7a8de8e4993aa7cec03b4c61a09624f0582d72ab98eefa4d3fd851f6e`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0200` | exit 0; rank 1532, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before editing | exit 0; only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 1443,1448 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -s https://arxiv.org/pdf/2406.08378v1 -o /tmp/ceva_birational_v1.pdf` | exit 0; 282,131-byte PDF SHA-256 `e4448220b1b79f8b9f52bdd3384d5a1bb19603d1b84896d8fe8642deb06f8fae` |
| `pdfinfo /tmp/ceva_birational_v1.pdf` | exit 0; valid 16-page PDF |
| `pdftotext -layout /tmp/ceva_birational_v1.pdf /tmp/ceva_birational_v1.txt` | exit 0; text extraction succeeded |
| `rg -n -C 12 -e 'Ceva.s theorem' -e 'Ceva theorem' -e 'if and only if' -e concurrent /tmp/ceva_birational_v1.txt` | exit 0; Theorem 1 iff, signed-side-line extension, and determinant proof identified on PDF pages 1-3; source lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty status |
| `rg -n -i -C 3 -e '\bceva\b' -e cevian -e 'directed ratio' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 0; direct metric, algebraic, and generalized forward candidates located; output SHA-256 `62fe7d8d5c5dde04f971fa59163f7e60364a2a302d5a767ce5d9e167feda0390` |
| `rg -n -i -e '\bconverse\b' -e '\biff\b' -e 'if and only if' Formalizations/Lean/.lake/packages/mathlib/Mathlib/LinearAlgebra/AffineSpace/Ceva.lean Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Normed/Affine/Ceva.lean` | exit 1 as expected; no converse or iff in the inspected Ceva modules |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0200/IntakeProbe.lean)` | exit 0; six direct pinned APIs elaborated; four representative bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; complete stdout SHA-256 `8f6a5cf8f07cbdf476aaf775d7efc85607331448c4900996ed0aa94cad547e6a`; no target theorem declared |
| `python3 -m json.tool Stage1_Instances/THM-M-0200/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0200/task-dag.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0200/intake-receipt.json` | exit 0 |
| `python3 -m json.tool .stage1-worker-selftest.json` | exit 0 |
| `python3 -c 'import ast; ast.parse(open("Stage1_Instances/THM-M-0200/check_intake.py", encoding="utf-8").read())'` | exit 0; scoped validator syntax is valid without generating files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0200/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, H1/M3/R4 null-target boundary, source and pin hashes, artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0200/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| `rg -n -i -e '\bsorry\b' -e '\badmit\b' -e '\bsorryAx\b' -e '\baxiom\b' -e '\bconstant\b' -e '\bopaque\b' -e '\bunsafe\b' Stage1_Instances/THM-M-0200 --glob '*.lean'` | exit 1 as expected; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0200 .stage1-worker-selftest.json` | exit 0; no tracked whitespace diagnostics; the scoped invariant checker separately validated final newlines and trailing whitespace in every untracked owned file and the worker packet |

## Known open gates

An accepted immutable source edition and exact proposition, historical genealogy review,
definition/assumption/conclusion/proof-boundary/translation/errata mapping, independent source
review, direction, ratio order and sign, side-segment versus sideline convention, ambient domain and
dimension, triangle and endpoint nondegeneracy, concurrency encoding, binders, and every boundary
case remain open. So do exact target elaboration and mutations, exhaustive anchor/provenance/trust
audits, discovery and obligation freezes, typed graphs, proof and composition, readable
reconstruction, hermetic replay, deterministic evidence bundle, independent verification, master
acceptance, audit completion, and theorem completion. These gates do not invalidate a truthful
self-tested `planned` intake.
