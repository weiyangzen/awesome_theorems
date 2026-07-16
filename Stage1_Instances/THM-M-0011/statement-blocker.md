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

No canonical Lean target, proxy predicate, theorem declaration, proof escape, broadened conjunction,
or substituted module theorem was introduced. The new `Statement.lean` is explicitly a substrate
probe rather than a canonical formula. The intake machine grade remains `M4`, and statement
acceptance and theorem completion remain false.

## Current rev-5.6 statement packet

At repository base `1cc6aa61bb055a5c032297ee457905c849af7608`, the v2 theorem node has rank
`320`, layer `0`, dependency context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, and no direct or
transitive hard parents, reuse hints, or shared groups. The required parent inspection order was
therefore the empty sequence; `dependency-reuse-ledger.json` records that audit against graph
SHA-256 `e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` without an
independence claim or transferred provider credit.

`Statement.lean` now elaborates one read-only, single-import vocabulary probe for
`Mathlib.Algebra.Category.ModuleCat.Descent`. It checks extension of scalars, preservation of finite
limits under flatness, reflection of isomorphisms under faithful flatness, and comonadicity. The
probe intentionally defines no target and supplies no exact-statement credit. `statement.json`
records null canonical fields, all four unexecuted mutation classes, the pinned environment, and the
positive-gate failure. `check_statement.py` emits the required structured negative semantic result.

The HEAD statement acceptance contract explicitly says a negative finding cannot satisfy the
deliverable. Therefore `S02-EXACT-TARGET` fails, the phase predicate is false, and the validator
must report `phase_accepted=false` even though the blocker packet and Lean probe self-test
successfully.

## Environment fingerprint

- Repository base revision for the current packet: `1cc6aa61bb055a5c032297ee457905c849af7608`.
- Validation date: 2026-07-17 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Direct probe import SHA-256:
  `dac6c87bd1a670bb875089061f357d2026118e9408ada42d6ad6070bc831d477`.
- Legacy discovery module SHA-256:
  `64de9ae48c5f0b6902fea34f1f24a445f3a17deb4d8617738e813510c74f7b7a`.

## Validation evidence

Commands ran in this worker clone. Lean used the existing canonical pinned `.lake` link; no Lake
update/build, dependency clone/fetch, or `.lake` mutation was performed. The earlier table below is
retained as historical intake evidence; the current statement receipt and worker packet bind the
2026-07-17 command set and results.

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
