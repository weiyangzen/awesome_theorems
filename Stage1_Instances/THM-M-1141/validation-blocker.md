# THM-M-1141 validation blocker

Item: `S56-M-1141-VALIDATION`

Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`

Validation time: `2026-07-14T00:33:48+08:00`

## Verdict

`blocked`; the assigned validation phase is not self-tested, no validation receipt is emitted, and
no proof, audit-completion, or theorem-completion credit is claimed.

The first failed gate is exact source-statement identity. The dossier selects Axler, Bourdon, and
Ramey, *Harmonic Function Theory*, second edition, Theorem 3.6. The authors' PDF has the recorded
SHA-256 `4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1`.
Its standing convention on printed page 1 (PDF page 9) says that throughout the book `n` is a fixed
positive integer greater than 1. Theorem 3.6 on printed page 48 (PDF page 55) does not override
that convention.

In contrast, `Statement.lean` quantifies every `n : Nat`, and `scope-map.md` explicitly selects an
arbitrary dimension and says dimension zero is retained because the source does not exclude it.
Thus the frozen Lean proposition includes dimensions 0 and 1 without source support or a checked
extension theorem. Compilation of that proposition cannot establish fidelity to the selected
claim. Under rev-5.6 sections 2, 5.1, 10.8, and 14, the weaker status wins.

Correcting the target is not an edit this validation worker may silently make: the registry is
hashed against `Statement.lean`, and the obligation tree, typed graphs, proof artifacts, and recipes
all depend on it. The statement-owning lane must either add the inherited `2 <= n` hypothesis or
prove an explicit checked transport covering dimensions 0 and 1, then refreeze and revalidate the
downstream artifacts.

## Additional failed gates

Even after source identity is repaired, the exact root is not kernel-closed. `Proof.lean` proves
positivity bookkeeping and abstract finite-chain propagation, then checks only the conditional
map `UniformValueComparison -> HarnackInequality`. It does not prove the local analytic Harnack
estimate, compact cover, connected-domain chain, or uniform comparison package. The root remains
`M3`, `audit_complete=false`, and `theorem_complete=false`.

Structured proof provenance is also stale: `task-dag.json` still marks the proof phase open;
`validation-specs.json` and `typed-graphs.json` still mark the positivity and propagation nodes
open; no `proof-receipt.json` or normalized-expression statement record exists. The accepted
foundation policy and complete transitive declaration/TCB provenance are absent.

Release-grade hermetic and independent validation cannot pass in this worker clone. Its pinned
Lean artifacts come from the shared warm `.lake` symlink, not a clean empty-cache offline replay.
There is no complete restorable TCB/SBOM/license archive, second signed attestation from an
independently provisioned clean runner, or independently implemented minimal verifier. Repeating a
check in this workspace would not be independent evidence.

## Commands and exact results

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1141` | 0 | rank 346; planned; L0/rework-required; theorem incomplete |
| `curl --fail --location --silent --show-error https://www.axler.net/HFT.pdf --output /tmp/m1141-source-audit.QBU5zZ/HFT.pdf` | 0 | authors' PDF downloaded only to temporary audit storage; no owned or dependency file changed |
| `sha256sum /tmp/m1141-source-audit.QBU5zZ/HFT.pdf` | 0 | `4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1` |
| `pdftotext -f 9 -l 9 -layout /tmp/m1141-source-audit.QBU5zZ/HFT.pdf -` | 0 | printed page 1 states `n` is a fixed positive integer greater than 1 |
| `pdftotext -f 55 -l 55 -layout /tmp/m1141-source-audit.QBU5zZ/HFT.pdf -` | 0 | printed page 48 contains Theorem 3.6 and no dimension override |
| `python3 -B Stage1_Instances/THM-M-1141/check_obligation_tree.py` | 0 | 11 obligations and 67 typed edges pass; root remains open `M3` |
| `python3 -B Stage1_Instances/THM-M-1141/check_proof.py` | 0 | positivity and finite-chain propagation bodies pass; analytic uniform comparison remains open |
| staged `lake env` Lean replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` in a fresh temporary directory, with trust level zero and fixed locale/timezone | 0 | all modules elaborate; printed axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound` |
| initial absolute-path temporary Lean replay from the repository root | 1 | Lean correctly rejected a source outside its root; rerunning from inside the temporary directory passed |
| `sha256sum Stage1_Instances/THM-M-1141/Statement.lean Stage1_Instances/THM-M-1141/obligation-registry.json Stage1_Instances/THM-M-1141/Proof.lean` | 0 | `07b602...a22`, `70a9e0...b3a`, `595c28...47d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; dependency source is clean |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |

## Retry condition

Resume validation only after the statement phase corrects or justifies the dimensional scope and
all statement-dependent artifacts are freshly regenerated. The proof lane must then close the
analytic root packages, after which validation still requires accepted trust/provenance evidence,
cold offline replay, and distinct independent verification.

Because the assigned validation gate failed, `.stage1-worker-selftest.json` is intentionally absent.
