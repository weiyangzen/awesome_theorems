# Statement gate blocker

Item: `S56-M-0458-STATEMENT`

Theorem: `THM-M-0458`

Verdict: blocked; no exact canonical Lean 4 target is claimed.

## First failed gate

The repository source supplies only the label "Arakelov-Zhang inequality", the gloss "height
inequality for arithmetic surfaces", the year 1992, and an untrusted `已验证` status. These data do
not identify a unique proposition. In particular, they do not select between a successive-minima
and height inequality, an arithmetic intersection positivity inequality, or a specialization to
arithmetic surfaces of another Zhang height theorem. Those alternatives have different objects,
hypotheses, constants, normalizations, and conclusions.

The repository search found no more precise source statement for this ID. The intake identifies
Zhang's 1995 paper *Positive line bundles on arithmetic varieties* only as a discovery lead; it
does not fix a theorem/page or establish that the repository's 1992 label refers to a result in
that paper. Selecting a formula from that lead would invent the missing source identity rather
than elaborate the exact repository target. The pinned mathlib source has no matching Arakelov
arithmetic-surface, arithmetic-intersection, Hermitian-line-bundle, or successive-minima API from
which a source-faithful target could be assembled.

Consequently there is no truthful proposition whose ordered binders, hypotheses, conclusion,
domains, universes, boundary cases, and normalization conventions can be frozen and elaborated.
There can therefore be no normalized expression hash, minimal-import claim, checked alternate
transport, or meaningful removed-hypothesis/domain/binder-scope/boundary mutation suite. Under
rev-5.6 sections 2 and 5, statement ambiguity is a hard blocker. The machine state remains `M4`.
No `sorry`, axiom, placeholder predicate, abstract proxy, broadened theorem, or substituted
real-number inequality was introduced.

## Environment fingerprint

- Repository base revision: `4338dcf8983e2bea1e56fc115e89473934aa350f`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone, except commands explicitly changing into
`Formalizations/Lean`. The existing `.lake` symlink points to the canonical pinned artifacts and
was read only. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0458` | 0 | Rank 306, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'Arakelov.?Zhang\|Zhang.?Arakelov\|阿拉克洛夫.?张寿武\|arithmetic surface.{0,80}height\|height.{0,80}arithmetic surface' Docs Formalizations/Lean/AwesomeTheorems --glob '*.lean' --glob '*.md' --glob '*.json'` | 0 | Found only the underspecified metadata and its generated projections; no exact proposition or Lean target |
| `rg -n -i 'Arakelov\|arithmetic (surface\|intersection\|variet)\|Hermitian line bundle\|successive minima' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching pinned mathlib source; exit 1 means no matches |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

There is no applicable `lake env lean <target>.lean` command: neither an exact expression nor a
legacy module for this target exists. Elaborating a fabricated interface or an unrelated generic
inequality would not validate the assigned statement gate.

## Retry condition

Resume only after an immutable primary source or authoritative scope amendment identifies the
intended theorem by edition and theorem/page and fixes its exact formula, arithmetic-surface
conventions, ordered quantifiers, positivity and regularity hypotheses, metric and height
normalizations, constants, conclusion, degenerate cases, and errata disposition. Pinned Lean APIs
for each referenced arithmetic-geometric object are then required. A later statement run can
crosswalk that source, elaborate and fingerprint the exact expression with minimal imports, check
alternate encodings, and run the required mutations.

Until then, statement acceptance and theorem completion are false. Because the assigned phase is
not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
