# Statement gate blocker

Item: `S56-M-0454-STATEMENT`

Theorem: `THM-M-0454`

Verdict: blocked; no exact canonical Lean 4 target is claimed.

## First failed gate

The repository source supplies only the label "Shafarevich-Tate group" and the gloss
"the Tate-Shafarevich group of an elliptic curve." This names a mathematical object, but states no
proposition. It does not select a global field, an elliptic curve or abelian variety, a definition
of the group, or any property to prove. In particular, it does not choose among the kernel of
global-to-local cohomology maps, a torsor classification, a duality statement, a finiteness claim,
or a computation for a specified curve. These are inequivalent targets. Selecting one would invent
missing mathematics or substitute a different theorem.

The repository search found no source-frozen proposition for this ID. It found only the same
metadata wording in `Docs/researches/math_theorems.md` and generated projections. The pinned mathlib
tree contains no declaration mentioning Shafarevich-Tate or Tate-Shafarevich. Two nearby legacy
Stage1 modules mention Tate-Shafarevich finiteness only as an explicitly abstract `Prop` field or
as search vocabulary for other theorem families; neither is a definition or theorem about the
group, and neither is assigned to this target.

Consequently there is no truthful proposition to elaborate. Ordered binders, hypotheses,
conclusion, domain and universe choices, degenerate cases, checked alternate transports,
expression fingerprint, minimal import set, and meaningful statement mutations cannot be frozen.
The instance remains at `M4`. No theorem declaration, axiom, placeholder, proxy predicate, or
broadened target was introduced.

## Environment fingerprint

- Repository base revision: `e0e1658c48365b041b302468a8238be1e1f30f20`.
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
`Formalizations/Lean`. The existing `.lake` symlink points at the canonical pinned artifacts and
was read only. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0454` | 0 | Rank 303, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'Shafarevich.?Tate\|Tate.?Shafarevich\|沙法列维奇.?泰特\|Tate-Shafarevich\|Sha group' Docs Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean' --glob '*.md' --glob '*.json'` | 0 | Found the underspecified source wording, generated projections, and unrelated abstract mentions; no proposition or mathlib declaration for this target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

There is no applicable `lake env lean <target>.lean` command: no exact expression exists and no
legacy module belongs to this target. Compiling a fabricated definition or an unrelated abstract
field would not validate the assigned statement gate.

## Retry condition

Resume only after an immutable primary source or authoritative scope amendment supplies a precise
proposition, fixes the global-field and curve/abelian-variety domains, gives ordered assumptions and
the conclusion, and identifies an edition plus theorem/page and errata disposition. A later run can
then build the source-to-Lean crosswalk, elaborate the exact proposition with minimal pinned
imports, fingerprint it, check alternate encodings, and mutation-test hypotheses, domains, binder
scope, and boundary cases.

Until then, statement acceptance and theorem completion are false. Because this assigned phase is
not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
