# THM-M-0822 anchor-audit validation

Item: `S56-M-0822-ANCHOR_AUDIT`

Base revision: `a1c9974d7fb28cd680e6494b968544bf801a93a2`

Base tree: `1fa287bc821355aca2ca9e3ce107830a3eb58e64`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Finset.erdos_ko_rado` proves exactly the universal upper-bound conjunct of the frozen target. Its
conclusion does not assert sharpness or attainment, regardless of the docstring's prose sentence
that the bound is sharp. The statement dossier already owns a checked constructive theorem,
`erdosKoRadoStar_attains`, for the attaining conjunct.

`AnchorAudit.lean` checks the terminal type, its principal Kruskal-Katona dependencies, and an
audit-local wrapper for the upper-bound component. The checker also creates a temporary combined
Lean module from the frozen `Statement.lean`, imports the proof-bearing pinned module, and declares
`canonicalTarget_of_pinnedCandidate` directly at `ErdosKoRadoMaximumTarget`. It joins only the
existing star theorem and `Finset.erdos_ko_rado`. Thus the exact maximum-value target is checked,
not a broadened original-paper theorem, an upper bound substituted for a maximum, or an equality
classification.

The pinned terminal body is present in `KruskalKatona.lean`: it splits the `r = 0` case, uses
complements and iterated-shadow disjointness, invokes `kruskal_katona_lovasz_form`, and finishes
with a binomial recurrence and a sized-family cardinality bound. It was introduced by immutable
commit `174e4bd31d28b82604fc68a45c04fbc15140c394`, which is an ancestor of the pin. Machine axiom
reports for the terminal, upper-bound wrapper, and exact combined route are exactly `propext`,
`Classical.choice`, and `Quot.sound`. Parser-aware elaboration and source inspection found no
placeholder, bodyless declaration, unsafe/opaque body, oracle, external code, or generated
certificate in the checked route. Full transitive trust and TCB closure remains downstream.

The bounded external inventory contains two ordinary-set upper-bound candidates. Atlas revision
`34ffed396...fb50` merely wraps the same pinned mathlib terminal and adds no attainment. FormalBook
revision `701731c...bdc` has a credible independent Katona cyclic-permutation/double-counting body,
but it also proves only the upper bound, uses Lean `v4.27.0-rc1` and older mathlib, is absent from
the local dependency closure, and was not built here. A q-analog project at `5b1e47d...679` proves
a different subspace proposition and its named `q_ekr` body is `sorry`, so it is `M5` and receives
no credit. Sourcegraph found only mathlib, Atlas, and FormalBook for the exact identifier query;
GitHub code search and grep.app were unavailable, so discovery saturation is not claimed.

This is an `M0-W`-shaped route, not a legal current `M0-W` status. Rev-5.6 requires release-grade
content-addressed `E1` for that label. This node-local packet is below `E1`; the candidate and
accepted vectors therefore remain `[H1, M3, R4]`. No receipt or scheduler state is accepted, and
neither `AUDIT-Z` nor theorem completion is claimed.

## Commands and exact outcomes

Commands ran from the repository root unless another working directory is stated. The canonical
`.lake` symlink was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation ran.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, all 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0822` | 0 | rank 1380; planned; L0/rework-required; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree matched and dependency worktree was clean |
| repo-local and pinned-package `rg` queries recorded in `anchor-audit.json` | 0/1 as appropriate | one pinned EKR terminal, no independent repo-local root body, and no second pinned-package candidate |
| pinned mathlib `git log`, `git show`, object/blob, source-block, ancestry, license, and manifest checks | 0 | immutable terminal body and introduction provenance matched the ledger |
| Sourcegraph queries recorded in the ledger | 0 | exact identifier query returned four matches in mathlib, Atlas, and FormalBook; response hashes and bounded-query limits recorded |
| anonymous GitHub repository/code and grep.app queries recorded in the ledger | 0 / HTTP 403 / checkpoint | repository leads, access failures, and response hashes recorded without false negative credit |
| immutable raw/codeload inspection of Atlas, FormalBook, and the q-analog project | 0 | declarations, source hashes, pins, licenses, route scope, gaps, and integration feasibility classified |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0822/AnchorAudit.lean)` | 0 | terminal/support types, upper-bound wrapper, explicit target, and two axiom reports checked; stdout SHA-256 `7ba98b09...4e97` |
| checker-generated temporary combined Lean module | 0 | exact frozen target closed from the target-owned star and pinned terminal; output SHA-256 `5f6c08da...7f81` |
| `python3 -B Stage1_Instances/THM-M-0822/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, authority, pins, bodies, inventory, provenance, trust boundary, receipt, packet, and narrow Lean replay passed |
| `python3 -B Stage1_Instances/THM-M-0822/check_anchor_audit.py` | 0 | packet-independent replay passed |
| `python3 -m json.tool` over all new JSON files and Python `ast.parse` over the checker | 0 | structured artifacts parsed without writing bytecode |
| comment-aware prohibited-construct scan over `AnchorAudit.lean` and the pinned EKR terminal block | 1 (expected no match) | no prohibited construct found |
| `git diff --check -- Stage1_Instances/THM-M-0822 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Known failures

- The statement prerequisite and this anchor-audit node remain provisional pending
  dependency-ordered master acceptance.
- Public discovery is bounded; GitHub code search and grep.app access failed, and no saturation
  claim is made.
- Release-grade content-addressed transitive declaration/provenance/trust, compiled-artifact,
  executable, and TCB closure is open, so current evidence is below `E1` and accepted `M0-W`.
- Obligation architecture, proof-phase adoption and composition, primary-source `H0`, readable
  `R0`, hermetic replay, independent verification, deterministic release evidence, `AUDIT-Z`, and
  theorem completion remain downstream.

This completes only the assigned bounded anchor-inventory and candidate-check work pending master
acceptance. It changes no accepted theorem state.
