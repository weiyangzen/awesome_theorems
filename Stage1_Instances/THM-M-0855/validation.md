# THM-M-0855 intake validation

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4` (tree
`61214aa2a03c032134ddc4958b1df63df3430a85`). Validation date: 2026-07-13
(Asia/Shanghai).

This validates only the `S56-M-0855-INTAKE` planned dossier: manifest and execution identity,
source-selected human scope, proposition-changing connectivity and encoding boundary, source
crosswalk, open task DAG, pinned API availability, JSON and scoped invariants, and artifact hygiene.
It does not validate a canonical Lean expression, a source-definition transport, or a proof.

The automation-provided `Formalizations/Lean/.lake` symlink existed before this work and was used
read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
performed. The pre-existing symlink and new owned artifacts make this nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- Platform: Linux `7.0.0-27-generic`, `x86_64`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0855` | 0 | rank 1409, planned, score 86, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 6271,6276 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS -o /tmp/thm-m-0855-primary.pdf https://www.renyi.hu/~p_erdos/1972-02.pdf`, followed by `file`, `wc -c`, `pdfinfo`, `sha256sum`, and `pdftotext -layout` | 0 | institutional Erdos archive scan is a 3-page, 221,449-byte PDF with SHA-256 `a14dc030...492a7`; Theorem 1 on page 111 and its proof on pages 111-112 were inspected |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake identities recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and scoped status | 0 | pinned revision/tree recorded; status empty |
| bounded search for Chvatal-Erdos and vertex-connectivity declarations over repo-local and all pinned package Lean | 1 expected | no exact theorem or direct vertex `s`-connectivity API matched; `IsEdgeConnected` was found and classified as a non-substitute; not an external absence proof |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0855/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `974220c4...bf28`, empty stderr; no target theorem introduced |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0855-pycache python3 -m py_compile Stage1_Instances/THM-M-0855/check_intake.py` | 0 | scoped validator compiles without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0855/check_intake.py --worker-packet .stage1-worker-selftest.json --primary-pdf /tmp/thm-m-0855-primary.pdf` | 0 | target, authority, source and pin hashes, H1/M4/R4 boundary, null formal target, exact inventory, receipt, packet, primary digest, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0855/check_intake.py` | 0 | public replay mode passes without scheduler packet or temporary source scan |
| prohibited-declaration scan over the owned Lean probe | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped final-newline/trailing-whitespace checks plus per-new-file no-index checks and `git diff --check` | 0 | no whitespace diagnostics |

The two summarized hygiene rows used these literal commands (the `rg` no-match exit `1` and each
no-index new-file exit `1` are expected):

```bash
rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0855
python3 -c $'from pathlib import Path\npaths = [p for p in Path("Stage1_Instances/THM-M-0855").iterdir() if p.is_file()] + [Path(".stage1-worker-selftest.json")]\nfor path in paths:\n    data = path.read_bytes()\n    assert data.endswith(b"\\n"), path\n    assert b"\\r" not in data and b"\\x00" not in data, path\n    assert all(not line.endswith((b" ", b"\\t")) for line in data.splitlines()), path\nprint(f"scoped byte check: ok ({len(paths)} files)")'
for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0855/*; do
  git diff --no-index --check /dev/null "$f" >/tmp/thm-m-0855-diffcheck 2>&1
  test "$?" -le 1 || { cat /tmp/thm-m-0855-diffcheck; exit 1; }
done
git diff --check -- Stage1_Instances/THM-M-0855 .stage1-worker-selftest.json
```

The primary-source download is dated discovery evidence, not a hermetic release recipe. Its digest,
size, pages, locator, and inspected boundary are recorded so a later source-admission phase can
reacquire or archive it and independently review the incorporated definitions and corrections.

## Known boundary

The paper pinpoints the exact theorem family and proof, but it does not locally define
`s`-connected. The incorporated Dirac/Menger convention and parameter domain, preservation,
corrections and errata, complete assumption mapping, and independent `H0` review remain open. So do
the canonical Lean target and fingerprints, checked connectivity/independence/Hamiltonicity
transports, statement mutations, exhaustive anchor and provenance audit, obligation registry,
typed graphs, proof and composition, readable reconstruction, trust closure, hermetic replay,
deterministic bundle, and independent verification. These gates prevent audit and theorem
completion but do not invalidate a truthful self-tested `planned` intake.
