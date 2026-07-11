# Statement gate blocker

Item: `S56-M-0011-STATEMENT`  
Theorem: `THM-M-0011`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the title "flat descent theorem" and the phrase "descent
theory under flat base change." It does not identify the objects being descended, the category or
site, faithful-flatness or covering hypotheses, effectiveness, or an exact conclusion. In
particular, it does not select among effective faithfully flat descent for modules, fpqc descent of
quasi-coherent sheaves, descent of scheme-morphism properties, and flat base-change results. These
have materially different binders, hypotheses, and conclusions. Selecting one would narrow or
substitute the source wording rather than elaborate its exact theorem.

The intake crosswalk names SGA 1, Expose VIII only as candidate genealogy. It has no inspected
edition hash, theorem or proposition number, pages, premise crosswalk, or errata audit, so it cannot
authorize a canonical claim. This is the statement-identity hard stop required by rev-5.6 sections
0.1 and 5: the ordered binders, exact hypotheses and conclusion, degenerate cases, normalized
expression hash, checked transports, and meaningful statement mutations cannot be frozen before
the intended source theorem is identified.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_104.StatementShape` does not repair the ambiguity. Its own documentation
defines it as a module-category boundary, not the terminal source theorem. It packages three
mathlib consequences of a faithfully flat commutative-ring homomorphism: reflection of
isomorphisms, preservation of finite limits by extension of scalars, and comonadicity. Treating that
conjunction as the exact root would silently choose modules and faithful flatness and omit the
other plausible meanings of the source phrase. Its successful elaboration below is therefore
discovery evidence only, with no exact-statement or proof credit.

No canonical Lean file, proxy predicate, theorem declaration, proof escape, broadened conjunction,
or substituted module theorem was introduced. The intake machine grade remains `M4`, and statement
acceptance and theorem completion remain false.

## Environment fingerprint

- Repository base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `64de9ae48c5f0b6902fea34f1f24a445f3a17deb4d8617738e813510c74f7b7a`.

## Validation evidence

Commands ran in this worker clone. Lean used the existing canonical pinned `.lake` link; no Lake
update/build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0011` | 0 | rank 104, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_104.lean` | 0 | legacy module-category boundary and neighboring audit declarations elaborated; this does not establish source identity |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_104.lean` | 0 | hashes match the environment fingerprint above |

## Retry condition

Provide an immutable primary-source edition and pinpoint theorem/proposition and pages that select
the intended descent result, including all referenced definitions, assumptions, and errata. The
next statement run can then freeze its objects, base-change direction, topology or faithful-flatness
conditions, effectiveness and conclusion; encode it with minimal pinned imports; check any
relationship to the legacy module candidate; and mutation-test hypotheses, domain, binder scope,
and degenerate nonfaithful or noneffective cases.

Until that information exists, the assigned phase cannot be genuinely self-tested to its
completion gate. Consequently no `.stage1-worker-selftest.json` is emitted.
