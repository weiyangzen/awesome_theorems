# THM-M-0232 intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978` (tree
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target-set consistency, the fail-closed planned dossier, repository-source and
duplicate-target boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical Rouché proposition or proof: the catalog
does not fix the contour/domain, regularity, inequality convention, zero count, multiplicity, or
relationship to `THM-M-0234`. The automation-provided canonical `.lake` symlink was pre-existing
and used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was
performed. This dirty worker run is nonrelease evidence.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean before and after
  the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0232` | 0 | rank 1244; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree match this record |
| `git blame -L 1675,1680 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| BnF SRU catalog query for *Mémoire sur la série de Lagrange* | 0 | response SHA-256 `75598e9556bed796e827abe86b554abb6fb39933caaf196ee1fe5964ec7500fc`; two Rouché records identify an 1866 Paris 31-page edition/offprint; bibliographic discovery only |
| MacTutor Eugène Rouché biography retrieval | 0 | page SHA-256 `46e92c9ca1e8ebd66a0c1abebadc6b31b25024adf59957ef0d36e154d458bfe4`; reports the 1862 volume-39 source and quotes a perturbation-form statement; secondary lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output |
| bounded case-insensitive search for Rouché/Rouche and literal argument-principle terms over repo-local Lean and pinned mathlib | 1 | expected no-match result; no source-identical target declaration under the searched terms; intake discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0232/IntakeProbe.lean)` | 0 | eight adjacent APIs elaborated; combined output SHA-256 `4a13a2dcbb18c343e2779399e9dabef98228ba2707d0755858e16aef9fd44461`; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | 0 after finalization | valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0232-pycache python3 -m py_compile Stage1_Instances/THM-M-0232/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0232/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H1/M4/R4 boundary, duplicate boundary, pins, artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check`, plus `git diff --no-index --check /dev/null <file>` for every new file | 0 for tracked-diff check; 1 expected per no-index content diff | no whitespace diagnostics; no-index exit 1 means the new file differs from `/dev/null` |

## Known open gates

An accountable source and scope decision must preserve and independently review one immutable exact
proposition and reconcile the apparently overlapping `THM-M-0234` record. The source edition and
page, definition chain, proof boundary, translation, corrections and errata; contour/domain and
orientation; analytic regularity; function roles and strict inequality; zero-count finiteness and
multiplicity; nonvanishing; quantifier order; and boundary cases remain open. So do the canonical
Lean expression and environment fingerprint, checked transports, four statement mutations,
exhaustive anchor and external-candidate audit, discovery protocol, obligation registry, typed
graphs, proof and composition, provenance and trust closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion.

These open gates do not invalidate a truthful self-tested `planned` intake. They prevent any claim
that the statement, proof, or theorem has been completed. Only the integration lane can accept the
provisional intake node.
