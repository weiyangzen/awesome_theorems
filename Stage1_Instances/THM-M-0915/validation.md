# THM-M-0915 intake validation

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`; base tree:
`6434a20532ae7c523ad293e67a6228ab384bfb8a`. Validation date: 2026-07-13
(Asia/Shanghai). This is nonrelease worker evidence.

This validation covers target membership, the planned dossier and open task DAG, literal repository
provenance, source-family discrimination, a narrow pinned Lean API probe, JSON and scoped
invariants, prohibited-construct hygiene, and whitespace. It does not validate a canonical
generating-function proposition or proof because the catalog method gloss does not identify one.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e` on Linux `7.0.0-27-generic` x86_64.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after the
  probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

All six catalog lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the record contains no bibliography. A bounded
repository search found formal-power-series and specialized generating-function APIs, not a
target-specific theorem or source statement.

Wilf's *generatingfunctionology*, second edition, was inspected transiently from the author's
University of Pennsylvania site. The 231-page, 1,247,451-byte PDF had SHA-256
`aeecec4df4fbb81b5a3824492ed816c290af44fccb0b1307f7f42f26e5b008ef`. Its contents and printed
pages 30-33 distinguish ordinary, exponential, analytic, and Dirichlet generating functions and
give formal coefficientwise equality and Cauchy multiplication. This confirms that the gloss is a
subject family, but it neither selects a catalog root nor supplies an accepted statement/proof
crosswalk. No external source file was added, and no H0 credit is claimed.

## Commands and results

Commands ran at repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0915` | 0 | rank 1457; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6693,6698 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at the repository source-record commit |
| temporary Wilf PDF inspection with `curl`, `pdfinfo`, `pdftotext`, and `sha256sum` | 0 | subject-family distinctions, printed-page boundary, size, page count, and digest recorded; no source admitted |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions shown above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` search in repo-local Lean and pinned mathlib | 0 | generic power-series, partition, Catalan, and unrelated probability-MGF occurrences found; no source-selected target-specific root |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0915/IntakeProbe.lean)` | 0 | six generic APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; stdout 875 bytes, SHA-256 `a9d295e1e96aa83acb92b945c89fedf80421bfb402b294bad84cd7228d07a089`; stderr empty |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0915-pycache python3 -m py_compile Stage1_Instances/THM-M-0915/check_intake.py` | 0 | scoped validator compiled without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0915/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null canonical target, H5/M4/R4 boundary, source and dependency pins, hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0915/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | expected no match | no `sorry`, `admit`, `sorryAx`, bodyless declaration, opaque declaration, or unsafe declaration |
| per-file `git diff --no-index --check /dev/null` and `git diff --check` | 0 aggregate | no whitespace diagnostics for any new artifact |

## Known open gates

An immutable exact source proposition, generating-function kind, coefficient carrier, sequence or
class, formal or analytic semantics, operation or recurrence, ordered binders, hypotheses,
conclusion, algebraic and convergence cases, pinpoint proof and errata crosswalk, and independent
source approval remain open. So do the canonical Lean target and minimal imports,
expression/environment fingerprints, checked transports, statement mutations, exhaustive anchor
audit, discovery protocol, obligation registry, typed graphs, proof and composition,
source/provenance/trust closure, readable reconstruction, hermetic replay, deterministic bundle,
independent verification, master acceptance, audit completion, and theorem completion.

These failures block ordinary statement and theorem execution but do not invalidate a truthful
self-tested planned intake. The `H5` classification applies only to the unstable catalog method
gloss, not to established generating-function mathematics.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0915-INTAKE` only. It supports a planned
dossier and a concrete statement blocker, not an accepted node receipt. No canonical statement,
H0 source closure, proof, audit completion, theorem completion, or master acceptance is claimed.
