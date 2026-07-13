# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers the planned dossier, scope and source-statement boundaries, open downstream task
DAG, JSON and scoped invariants, and a narrow pinned Lean candidate probe. It does not validate a
canonical Kruskal-Katona statement or proof because no exact source formulation has been selected.
The automation-provided canonical `.lake` symlink was pre-existing and used read-only. No
dependency update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker
evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source clean and used read-only.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `KruskalKatona.lean` SHA-256:
  `c6351d7ee422db9eed8f45335f4128eb3a66fe09997d12abc15eba38e9863f1c`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0966` | exit 0; rank 1500, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| bounded Crossref queries for the Kruskal chapter and Katona reprint | exit 0; bibliographic metadata captured under `/tmp`; no primary theorem text or source-proof credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0 with no output; pinned package source clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0966/IntakeProbe.lean)` | exit 0; basic, iterated, and Lovasz declarations plus four APIs elaborated; all three declarations report `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `b416f048...4da3`, stderr empty |
| `python3 -m json.tool` on all JSON artifacts and the worker packet | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0966-pycache python3 -m py_compile Stage1_Instances/THM-M-0966/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0966/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, null target, H1/M3/R4 boundary, source pins, exact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

The probe's candidate-signature and axiom output was (line wrapping normalized):

```text
Finset.kruskal_katona {n r : ℕ} {𝒜 𝒞 : Finset (Finset (Fin n))}
  (h𝒜r : Set.Sized r ↑𝒜) (h𝒞𝒜 : 𝒞.card ≤ 𝒜.card)
  (h𝒞 : Finset.Colex.IsInitSeg 𝒞 r) : 𝒞.shadow.card ≤ 𝒜.shadow.card
Finset.iterated_kk {n r k : ℕ} {𝒜 𝒞 : Finset (Finset (Fin n))}
  (h₁ : Set.Sized r ↑𝒜) (h₂ : 𝒞.card ≤ 𝒜.card)
  (h₃ : Finset.Colex.IsInitSeg 𝒞 r) :
  (Finset.shadow^[k] 𝒞).card ≤ (Finset.shadow^[k] 𝒜).card
Finset.kruskal_katona_lovasz_form {n r k i : ℕ} {𝒜 : Finset (Finset (Fin n))}
  (hir : i ≤ r) (hrk : r ≤ k) (hkn : k ≤ n)
  (h₁ : Set.Sized r ↑𝒜) (h₂ : k.choose r ≤ 𝒜.card) :
  k.choose (r - i) ≤ (Finset.shadow^[i] 𝒜).card
'Finset.kruskal_katona' depends on axioms: [propext, Classical.choice, Quot.sound]
'Finset.iterated_kk' depends on axioms: [propext, Classical.choice, Quot.sound]
'Finset.kruskal_katona_lovasz_form' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This authenticates only the pinned candidate signatures and vocabulary. It does not establish
identity with the unfrozen repository root, minimality of imports, source equivalence, accepted
proof-body provenance or trust closure, cascade representation, exact-size segment existence, or
equality characterization.

## Known open gates

The exact source proposition, complete primary source, theorem/page and premise mapping,
corrections and errata audit, and independent source review remain open. So do the canonical Lean
expression and environment fingerprints, minimal imports, checked transports and mutations,
exhaustive formal-anchor audit, discovery and obligation freezes, typed proof/provenance graphs,
proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These failures do not invalidate a truthful, self-tested `planned` intake.
