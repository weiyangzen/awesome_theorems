# THM-M-1138 validation-phase result

Item: `S56-M-1138-VALIDATION`

Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`

Validation time: `2026-07-14T03:48:00+08:00`

The node-scoped validator replayed the exact frozen statement, conditional composition, and local
strict-subharmonic perturbation proof in fresh `/tmp` module outputs. Every Lean invocation used
`lake env lean --trust=0` inside a bubblewrap network namespace with the host mounted read-only. No
new mathematical proof content was added during validation, and no separate verifier is claimed.

## Exact result

```text
python3 -I -B Stage1_Instances/THM-M-1138/check_validation.py
  exit 0
  PASS S56-M-1138-VALIDATION: network-isolated lake env lean --trust=0 fresh-output replay checked the exact statement, conditional composition, and local perturbation root; both proof declarations are sorry-free with exactly propext, Classical.choice, and Quot.sound; frozen route reconciliation, complete TCB/provenance, cold empty-cache, and independent-verification gates fail closed
```

The replay used the manifest-pinned Lean 4.29.0 and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It reused existing compiled dependencies read-only,
wrote only disposable outputs under `/tmp`, and performed no update, build, clone, fetch, or
dependency mutation.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, conditional composition, and the local proof root freshly elaborate under trust zero. |
| Placeholder/unsafe scan | pass | Both proof declarations are sorry-free; comment-aware source scans found no prohibited proof mechanism. |
| Axiom observation | provisional pass | All checked roots report exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Selected provenance | pass | Pinned mathlib revision/tree/remote/license, four source blobs and hashes, and their oleans agree. |
| Frozen architecture | fail closed | Registry v1 models the strong-maximum/local-constancy route; five bypassed nodes and foundation credit remain withheld. |
| Frozen proof recipes | fail closed | All 15 old recipes run only `check_obligation_tree.py` and expressly exclude the analytic proof. |
| Authoritative state | pending master | The graph remains root-open at `M3`; the accepted dossier vector remains `H1/M3/R3`, and the proof prerequisite has no master acceptance. |
| Hermetic release replay | fail closed | Warm shared compiled artifacts are not a cold empty-cache build or offline archive restoration; complete TCB/SBOM evidence is absent. |
| Independent verification | fail closed | No separately implemented verifier, distinct signed runner, or independent minimal verifier exists. |

This genuinely self-tests the validation implementation and therefore proposes worker state `[_]`,
while its validation verdict is `blocked`. It grants no accepted receipt, `E0`, `M0-*`, `AUDIT-Z`,
`THEOREM-Z`, release, theorem completion, or master-acceptance credit. Human-source `H0`, readable
`R0`, architecture reconciliation, complete trust/provenance, and all release gates remain open.
