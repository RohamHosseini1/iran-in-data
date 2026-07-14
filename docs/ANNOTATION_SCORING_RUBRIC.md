# Annotation scoring rubric

Every law/event linked to a chart carries TWO scores. They answer two different
questions and must not be collapsed into one.

## Why the vocabulary changed

These fields used to be called `relevance` and `attribution`. "Attribution" invites the
question *"can we PROVE this law moved the line?"* The honest answer is almost always
no, because we have no identification strategy and no counterfactual. So every scorer
retreated to 1 or 2, and the result was absurd: the 1951 **Oil Nationalization** scored
2 against GDP, the 1979 **Bank Nationalization Act** scored 2, the **Interest-Free
Banking Act** scored 1, while a routine 1996 annual budget law scored 4 and was the
single highest-scored law on Iran's GDP chart. The scale had stopped meaning anything.

The right question is **expected causation**: *would we EXPECT this instrument to have
moved this measure?* That is answerable from economic reasoning, and Oil Nationalization
against GDP answers it with a 5.

---

## `correlation` (1 to 5) - does this belong to THIS measure's story?

Drives whether a reader of this chart should see it at all.

| | |
|---|---|
| **5** | Central to this measure's story. A reader who does not know this law does not understand this chart. |
| **4** | Clearly part of this measure's domain and history. |
| **3** | Genuinely related to the measure, one of many such instruments. |
| **2** | Tangential. Touches the domain but a reader of this chart would not miss it. |
| **1** | Barely connected. Should not be linked at all. |

## `expected_causation` (1 to 5) - would we EXPECT it to have moved this line?

Drives whether we draw a marker on the line. It is a claim about **expected economic
effect**, NOT a claim of proven causation. Judge the instrument's *reach* and *size*
against *this specific measure*.

| | |
|---|---|
| **5** | Structurally reorganises what this measure is measuring. We would expect a visible break in the series. |
| **4** | Major instrument; we would expect a material, visible effect on this measure. |
| **3** | Real but partial or indirect effect expected; one force among several. |
| **2** | Marginal expected effect. One of many small instruments; would not expect to see it in the line. |
| **1** | Negligible, procedural or administrative. No expected effect on this measure. |

---

## The scale is RELATIVE TO THE SPECIFIC CHART

The same law scores differently against different measures. This is the single most
important rule, and getting it wrong is what broke the first pass.

- **Annual Budget Law x GDP** -> expected_causation **2**. One year's routine budget is
  a small force against a $400bn economy.
- **Annual Budget Law x Government Expenditure** -> expected_causation **5**. The budget
  law *is* the series.
- **Targeted Subsidies Reform x CPI** -> **5**. It reset administered prices nationwide;
  inflation visibly jumped.
- **Targeted Subsidies Reform x Wheat Production** -> **3**. Real effect through input
  costs, but indirect.

## Worked anchors (calibrate against these)

| Law x Measure | correlation | expected_causation | why |
|---|---|---|---|
| Oil Nationalization Act (1951) x GDP | 5 | 5 | Seized the country's dominant industry; output collapsed under the blockade. A break in the series. |
| Oil Nationalization Act (1951) x Wheat Production | 3 | 1 | Historically central to Iran, but no expected channel to wheat. |
| Bank Nationalization Act (1979) x Money Supply | 5 | 5 | The state took the entire banking system. |
| Interest-Free (Usury-Free) Banking Act (1983) x Interest Rates | 5 | 5 | It redefined the instrument the series measures. |
| Targeted Subsidies Reform Law x CPI | 5 | 5 | Nationwide administered-price reset. |
| Fourth/Fifth National Development Plan x GDP | 5 | 4 | Directed the entire investment programme of the state. |
| Direct Taxation Act (1988) x Tax Revenue | 5 | 5 | It is the law that defines the series. |
| Direct Taxation Act (1988) x GDP | 4 | 3 | Real macro effect, but one force among many. |
| Article 44 privatisation x GDP | 5 | 4 | Reassigned ownership of a large share of the economy. |
| Executive bylaw issuing 200bn rials of participation bonds x Government Debt | 2 | 1 | A single small tranche. Negligible against the aggregate. |
| Amendment renumbering annexes of a development plan x GDP | 2 | 1 | Purely procedural. |

## Hard rules

1. **Never** infer causation from the chart's shape. Score the instrument's expected
   reach, not what the line happens to do.
2. A big, famous law is NOT automatically a 5 on every chart. Check the channel to the
   specific measure (Oil Nationalization x Wheat = 1).
3. A small, boring instrument IS allowed to be a 1. Most bylaws are 1s and that is
   correct. Do not inflate to be generous.
4. If you would not expect an economist to point at the line and say "that is this law",
   expected_causation is at most 2.
5. Scores are independent. High correlation with low expected causation is a normal and
   important combination: the White Revolution against GDP is correlation 5,
   expected_causation 2. You must see it; we cannot credit the line's movement to it.
