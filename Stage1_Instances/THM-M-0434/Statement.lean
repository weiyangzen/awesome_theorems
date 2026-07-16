import Mathlib.NumberTheory.LocalField.Basic
import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.MeasureTheory.Measure.Haar.Basic

/-!
# THM-M-0434 statement boundary probe

The repository has identified Ngo Bao Chau's Lie-algebra Fundamental Lemma proof family, but it
has not admitted one exact source proposition with its complete definition chain, normalization,
characteristic branch, and boundary cases. The pinned environment also lacks concrete endoscopy,
matching, transfer-factor, and orbital-integral definitions.

This module therefore checks only three adjacent pinned interfaces. It deliberately declares no
canonical Fundamental Lemma target, checked transport, mutation fixture, or proof.
-/

#check IsNonarchimedeanLocalField
#check AlgebraicGeometry.Scheme
#check MeasureTheory.Measure.IsHaarMeasure
