# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9908-9913` supplies exactly the title `鞍结分岔`, attribution to
many mathematicians, the 20th century, the gloss `平衡点消失的分岔`, importance `high`, and status
`已验证`. Git history places this uncited record in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no bibliography, theorem/page locator,
definitions, binders, hypotheses, conclusion, proof route, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:36966-36991` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate statements,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, DOI `10.1090/gsm/140`, was inspected as an
authoritative modern discovery source. The author page is
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/index.html`; it links the inspected preliminary
text at `https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf` and current errata at
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/errata.pdf`. Section 6.5, printed page 200,
equation (6.33), gives

```text
x' = mu + x^2.
```

It says this system has one stable and one unstable fixed point for `mu < 0`, that they collide at
`mu = 0`, and that they vanish for `mu > 0`; it names this a saddle-node bifurcation. The following
paragraph observes that the implicit-function theorem makes `f(x0, mu0) = 0` and
`partial f / partial x (x0, mu0) = 0` necessary for a local change in the number of fixed points.

This passage is explicitly among "prototypical examples." It does not state a general scalar or
finite-dimensional saddle-node theorem, generic sufficient hypotheses, a normal-form equivalence,
or an exact local uniqueness theorem. The catalog neither cites this text nor says that its target
is only equation (6.33). The passage therefore discriminates possible scope but is not adopted as
the canonical claim and receives no H0 credit. The author-hosted preliminary-edition PDF was
inspected outside the repository; it had 4,133,331 bytes and SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`.
The reproducible discovery command `pdftotext -f 211 -l 211 -layout <temporary-source-pdf> -`
followed by selecting lines 1-21 produced a 1,553-byte tight passage with SHA-256
`8c2019a0410b2edefb2a2242736e4c77480916b3941865f7c45261713578fd8d`.
The current author-linked errata PDF had SHA-256
`3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`; a bounded search found no
entry naming page 200, equation (6.33), saddle-node, or bifurcation. That no-match is not a complete
errata admission or review. No remote source is admitted as an immutable accepted evidence packet,
and no complete assumption/proof/errata mapping or independent review is claimed.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `鞍结分岔` | scalar fold, general vector-field saddle-node, or fixed-point fold for maps | parameterized functions, derivatives, ODE/flow, or map fixed points | theorem family recognized; root not selected |
| equilibrium | zero of a vector field versus fixed point of a time/map operator | `IsIntegralCurve`, a source-defined zero predicate, `Function.IsFixedPt` | representation open |
| `disappear` | two/one/zero local root count across a signed parameter, perhaps with stability | local sets, neighborhood quantifiers, root cardinality, derivative signs | direction, locality, multiplicity, and stability open |
| generic fold | nonzero parameter direction and quadratic term, simple zero eigenvalue in higher dimension | Fréchet derivatives, finite-dimensional linear maps, implicit-function/reduction infrastructure | all nondegeneracy assumptions absent |
| equation (6.33) | one elementary normal-form example | real arithmetic and derivative APIs | inspected candidate only; not a general theorem |
| `已验证` | untrusted inventory field | no declaration or proof body | no H or M credit |

## Formal crosswalk boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks generic ODE integral-curve, flow, fixed-point, derivative, and implicit-function APIs.
A bounded lexical search over repo-local Lean and pinned mathlib found no declaration named as a
saddle-node or fold bifurcation theorem. This is not the downstream exhaustive formal-anchor audit
and does not establish absence from external Lean projects.

The statement phase must select and lawfully preserve one exact source proposition; map its edition,
locator, incorporated definitions, ordered assumptions, conclusion, proof boundary, and errata;
explain why it is the catalog target rather than a nearby variant; and obtain independent source
review. Only then may it freeze a canonical Lean expression, minimal imports, checked alternate-form
transports, expression/environment fingerprints, and statement mutations.
