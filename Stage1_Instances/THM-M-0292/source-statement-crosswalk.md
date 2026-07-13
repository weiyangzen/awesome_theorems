# Source-statement crosswalk

## Repository source

The catalog record at `Docs/researches/math_theorems.md:2097-2102` contains exactly:

| Catalog field | Literal value | Intake interpretation |
|---|---|---|
| name | `迪尼定理` | recognizable Dini theorem family |
| attribution | `Ulisse Dini` | historical metadata, not a proof citation |
| time | `1878` | matches the primary-book lead below |
| statement | `单调函数列的一致收敛` | uniform convergence of a monotone function sequence; not binder-complete |
| importance | `中` | scheduling metadata only |
| formal status | `已验证` | explicitly untrusted; grants no source or machine credit |

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no citation, compact domain,
continuity assumption, convergence premise, monotonicity direction, formula, definition, ordered
binder, proof boundary, correction record, reviewer, or formal artifact.
`Docs/Stage0_Blueprint.md:8062-8087` repeats the gloss while explicitly leaving precise definitions
and premises, proof history, dependencies, alternate forms, axioms, machine status, and artifact
links open. It is planning metadata, not an independent source.

## Clause crosswalk

| Catalog component | Candidate mathematical component | Prospective Lean surface | Intake state |
|---|---|---|---|
| function sequence | `F : ℕ → α → ℝ` | unbundled functions or `ℕ → C(α, ℝ)` | index, domain, values, and bundling open |
| monotone | pointwise monotone in the sequence index | `Monotone F` or `∀ x ∈ s, Monotone (F · x)` | direction and meaning open |
| pointwise limit | `F n x → f x` for every domain point | `∀ x ∈ s, Tendsto (F · x) atTop (𝓝 (f x))` | omitted by catalog; expected but not admitted |
| continuity | every `F n` and limit `f` are continuous | `Continuous` / `ContinuousOn` | omitted by catalog; expected but not admitted |
| compact domain | closed interval, compact space, or compact set | `[CompactSpace α]` / `IsCompact s` | omitted by catalog; choice open |
| uniform convergence | one index works for all points | `TendstoUniformly` / `TendstoUniformlyOn` | conclusion family identified; encoding open |
| `已验证` | inventory-screening label | accepted source and kernel receipts would be required | no credit |

The missing hypotheses materially affect truth. They cannot be inferred into the canonical root
merely because they are standard or already available in mathlib.

## Primary-work lead

The 1878 attribution matches Ulisse Dini, *Fondamenti per la teorica delle funzioni di variabili
reali*, Pisa, Tipografia T. Nistri e C., 1878, VIII + 407 pages. The Bavarian State Library IIIF
manifest at `https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11374230/manifest`
(observed SHA-256 `59352baea3cda1039d6c97837268a2c88b36102a2d8f7238db884b6834389be5`)
records the author, title, Pisa/Nistri publication, year, language, extent, identifiers, and an
enumeration of 430 page-image canvases under URN `urn:nbn:de:bvb:12-bsb11374230-9`.

The scan was located but the exact original Dini theorem, incorporated definitions, page span,
proof boundary, correction or errata status, and translation were not identified or independently
reviewed during intake. The book-to-theorem relationship is unverified. The secondary naming and
bibliographic Dini lead jointly support only a provisional family-level `H1`, not the pinpoint `E4`
evidence and independent review required for `H0`.

## Secondary formulation

The Encyclopedia of Mathematics entry "Dini theorem," permanent revision `32779`
(`https://encyclopediaofmath.org/index.php?title=Dini_theorem&oldid=32779`), states that if
continuous nonnegative functions `u_n` on `[a,b]` have a continuous sum, then the series
`∑ u_n` converges uniformly; it notes a generalization to an arbitrary compactum. This is an
inspected secondary `E5` source, adapted from an original entry by L. D. Kudryavtsev, not
proof-source evidence. The observed API payload had SHA-256
`706d060dada3be39e47308589c7cc9b8b0b7e4f1eb07a7f3ef62d81f11f936f7`.

The series statement is related to an increasing sequence by taking partial sums. A checked and
source-reviewed crosswalk must still account for nonnegative increments, the initial term and
indexing, continuity of partial sums and the sum, and equivalence between uniform convergence of a
series and uniform convergence of its partial-sum sequence. It is not credited as an alternate
encoding at intake.

## Pinned Lean candidates

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/Topology/UniformSpace/Dini.lean` documents the classical real compact-set theorem and
generalizes its codomain. The closest compact-set declarations are:

- `Monotone.tendstoUniformlyOn_of_forall_tendsto`: compact `s`; every `F i` continuous on `s`;
  pointwise increasing sequence; continuous limit; pointwise convergence; uniform convergence on
  `s`.
- `Antitone.tendstoUniformlyOn_of_forall_tendsto`: the corresponding decreasing-sequence theorem.

The module also exposes `Monotone.tendstoUniformly_of_forall_tendsto` and
`Antitone.tendstoUniformly_of_forall_tendsto` for compact spaces, locally uniform forms without a
compactness premise, and bundled `ContinuousMap` compact-open convergence forms. Its ambient index
is any preorder and its codomain is a normed ordered lattice group, so selecting a declaration is a
scope decision rather than a name match.

`IntakeProbe.lean` imports only this exact-topic module, checks the principal interfaces, and checks
the classical `ℕ`/`ℝ` compact-set specializations. This supports provisional `M3` discovery:
kernel-visible theorem declaration interfaces exist, but `THM-M-0292` still has no source-selected
canonical expression, checked transport, accepted wrapper, or accepted receipt. The bounded inspection is
not the downstream anchor, terminal-provenance, axiom, or trust audit.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable primary or authoritative
edition, identify the exact theorem and definition chain, map every domain, binder, continuity and
convergence premise, monotonicity condition, conclusion, proof transition, and boundary case, audit
translations and corrections, and approve the crosswalk independently. Only then may the statement
phase select minimal imports, freeze an exact Lean expression, compile checked transports, serialize
expression and environment fingerprints, and execute all required mutations.
