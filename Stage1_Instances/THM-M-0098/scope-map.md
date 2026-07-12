# Scope map

## Frozen catalog boundary

- Target ID: `THM-M-0098`; execution rank: `899`; baseline: `L0 / rework_required`.
- Catalog title: `朗兰兹纲领基本引理` ("Langlands program fundamental lemma").
- Catalog attribution and date: Robert Langlands, 1979.
- Literal catalog statement: `自守表示与伽罗瓦表示的对应` ("a correspondence between
  automorphic representations and Galois representations").
- The manifest value `已验证` is untrusted metadata and supplies no human or machine proof credit.

These facts are frozen as source provenance, not as a canonical mathematical proposition.

## Unresolved reading A: Fundamental Lemma

The title can point to the Langlands-Shelstad endoscopic Fundamental Lemma. A source-exact version
would have to decide at least:

- group versus Lie-algebra formulation and the characteristic/residue-characteristic regime;
- the nonarchimedean local field, reductive group, endoscopic datum, and integral model;
- matching regular semisimple elements or stable conjugacy classes;
- Haar and quotient-measure normalizations, transfer factors, and unit test functions;
- the precise stable-orbital-integral equality and any transfer between formulations.

None of those objects occurs in the literal catalog statement. The separate target `THM-M-0434`
and legacy module `S1_M_083.lean` are discovery aids only and confer no scope or state on this ID.

## Unresolved reading B: Langlands reciprocity

The literal statement can point to a Langlands correspondence or reciprocity program. A
source-exact version would have to decide at least:

- local versus global setting; number field, function field, or local field;
- `GL_n`, another reductive group, or an L-group formulation;
- the precise categories of automorphic representations and Galois/Weil parameters;
- coefficient fields, topology, continuity, semisimplicity, algebraicity/geometricity, and
  ramification conditions;
- directionality (bijection, one-way construction, compatible system, or functorial relation);
- local-global compatibility and Frobenius/Hecke, L-factor, epsilon-factor, and normalization laws.

The separate target `THM-M-0430` and legacy module `S1_M_058.lean` are discovery aids only. General
Langlands reciprocity is also a program containing conjectural cases, so the word "correspondence"
cannot be promoted to a proved universal theorem.

## Required statement decision

The statement phase must obtain an immutable primary source and independently reconcile the title,
attribution, 1979 date, and literal gloss. It must either select one binder-complete theorem that
all four metadata fields identify, or record a source-correction decision through the repository's
master process. Only then may it freeze domains, universes, ordered binders, hypotheses, conclusion,
boundary cases, imports, and an elaborated-expression fingerprint.

## Explicit exclusions

- Do not combine an orbital-integral conclusion with automorphic/Galois domains into a hybrid claim.
- Do not silently choose the Fundamental Lemma merely from the title or reciprocity merely from the
  gloss.
- Do not copy the canonical claim, artifacts, receipts, or accepted state of `THM-M-0430` or
  `THM-M-0434`.
- Do not substitute rank-one class field theory, a `GL_2` modularity theorem, a special endoscopic
  group, or another proved special case for an unidentified general root.
- Do not encode the desired correspondence or orbital-integral equality as unconstrained structure
  data or a hypothesis and then count an accessor or implication wrapper as the theorem.
- Do not treat nearby mathlib APIs or the catalog status `已验证` as statement or proof evidence.

No degenerate-case policy is frozen because the theorem family itself is unresolved.
