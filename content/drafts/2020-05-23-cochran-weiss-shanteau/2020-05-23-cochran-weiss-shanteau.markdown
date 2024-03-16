---
title: 'Expertise as latent variable: the Cochran-Weiss-Shanteau index'
author: Michael Chow
date: '2020-05-23'
slug: cochran-weiss-shanteau
categories: []
tags: []
draft: yes
show: false
---

I've been doing some reading on skill acquisition and expert performance recently, and found an interesting set of articles that ask two questions:

* How can we measure expertise when there is no "gold standard" for performance?
* How do domains differ in their overall levels of professional competence?

To clarify what they mean by professional competence, they mention that weather forecasters tend to be highly accurate in their next-day forecasts (accurate 82% of the time), while clinical psychologists are fairly inaccurate at predicting patient violence (39% of the time). 

In these two cases, they are describing performance where the outcomes are known, so we can assess the quality of their judgments. This is the "gold standard" case. However, oftentimes we have judgments (or other performances) without known outcomes. In this case, they argue that we can use measures of reliability (or internal consistency) to identify areas with lower professional competence.

This post is made up of two sections:

* A quick review of reliability, and the measure they use for it.
* Showing this measure is a special case of (confirmatory) factor analysis.

Finally, I'll show other places in psychology and neuroscience that use their same calculations and rationale.

## Measures of competence and their limitations

(TODO: split table in two, with their reliability measures as separate table)

![](/006-expert-limits.png)

## Two necessary conditions: within- and between- "expert" reliability

, who are rating ice-skating performances.
They have a rulebook--and presumably they follow it--but **suppose we don't want to check whether they followed the rulebook, only whether they didn't.** In this case, we can check without knowing what the rules are.

### Consistency: within-"expert" reliability

Suppose judges were asked to rate many clips, and clips were repeated in order to collect multiple ratings from each judge.
A perfectly reliable judge would give the same clip the same ratings.
This does not mean that their ratings correspond to the rulebook, only that they are internally consistent: within a judge the same stimulus gets the same rating.

Below is a diagram of internal consistency in this situation.


### Concensus: between-"expert" reliability

On the other hand, suppose we took the ratings from the previous section, and compared them across judges.

This is shown in the correlation matrix below.

### Trouble on the horizon

One challenge with this perspective is that these two measures aren't really separated from one another. Under reasonable models, lower within-expert reliability implies low between-expert reliability. Another way of saying this is that consistency puts an upper bound on consensus. (This goes back to Spearman's (1904) point on measurement error).

In the following section I will discuss how by treating an expert's "self-consensus" as 1 (when thought of as a correlation), these measures take on a more satisfying interpretation:

* consistency: do they give the same thing the same judgements?
* consensus: can these two judges be thought of as one?

In this sense, we can re-evaluate two of their claims:

* clinical psychologists (consistency = .44; consensus = .40) - low consensus, due to low consistency.
* polygraphers (consistency = .91; consensus = .33) - low consensus, and **not** because of consistency.


## Modelling consistency and consensus

Latent factor model of two experts

Latent factor model of three experts


## Summary

This opens up an interesting area: low consistency with high consensus.



Thomas, R. P., & Lawrence, A. (2018). Assessment of Expert Performance Compared Across Professional Domains. Journal of Applied Research in Memory and Cognition, 7(2), 167–176. https://doi.org/10.1016/j.jarmac.2018.03.009


Shanteau, J., Weiss, D. J., Thomas, R. P., & Pounds, J. C. (2002). Performance-based assessment of expertise: How to decide if someone is an expert or not. European Journal of Operational Research, 136(2), 253–263. https://doi.org/10.1016/S0377-2217(01)00113-8
