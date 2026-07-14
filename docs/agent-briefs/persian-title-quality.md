# Task brief: Persian title & terminology quality

Read `docs/agent-briefs/_shared-context.md` first. Your slice of
`CHART_REGISTRY.csv` rows is given in your launch prompt. You review `title_fa`
and `category_fa` for every row in your slice.

## Naming doctrine (owner's canonical example)

Persian titles must be **natural Persian phrases**, not translated-label-plus-
category constructions.

- WRONG: «کره و روغن حیوانی - مصرف سرانه مواد غذایی»
- RIGHT: «سرانه مصرف کره و روغن حیوانی»
- RIGHT: «سرانه مصرف شیر»

Rules:

1. Natural izafe word order. Lead with the measure concept (سرانه مصرف، نرخ تورم،
   ارزش صادرات، تولید...), then the subject.
2. NO dash-separated suffixes, NO em/en dashes anywhere. If a qualifier is needed,
   use «،» or parentheses: «تورم قیمت مصرف‌کننده (درصد سالانه)».
3. **Wikipedia-fa terminology** for every economic term. Use the established
   fa.wikipedia.org article titles: تولید ناخالص داخلی، تورم، نقدینگی،
   تراز پرداخت‌ها، بدهی خارجی، سرمایه‌گذاری مستقیم خارجی، نرخ بیکاری،
   ارزش افزوده، حساب جاری، ذخایر ارزی... When genuinely unsure of the standard
   Persian term, do ONE targeted WebSearch (`site:fa.wikipedia.org <term>`); batch
   your uncertain terms and look them up together, don't search per-row.
4. Orthography: Persian ی and ک (never Arabic ي/ك). Correct ZWNJ (نیم‌فاصله):
   می‌شود، نرخ‌ها، بین‌المللی، مصرف‌کننده. No tatweel.
5. Unit phrases consistent across the whole slice:
   - "% of GDP" → «درصد از تولید ناخالص داخلی»
   - "annual %" → «درصد سالانه»
   - "current US$" → «دلار جاری آمریکا»
   - "constant US$" → «دلار ثابت آمریکا» (تعدیل‌شده با تورم)
   - "per capita" → «سرانه…» (leading, per the doctrine above)
6. Country names: use standard Persian exonyms (ایالات متحده، عربستان سعودی، ترکیه،
   کره جنوبی...). Flag any English country name left inside a Persian title.
7. `category_fa` must be a consistent, natural Persian category name; identical
   English categories must map to identical Persian ones (note inconsistencies).
8. Numbers inside titles stay as digits; do not convert digits, that's a
   frontend concern.

## Output shard

`data/processed/quality_audit/translation_rows_<START>_<END>.csv` with columns:

```
chart_id,fa_verdict,proposed_title_fa,proposed_category_fa,reason
```

- `fa_verdict` ∈ `keep | retitle | needs_review`
- `proposed_title_fa` / `proposed_category_fa`: only when changing.
- `reason`: terse; for retitles cite which rule (e.g. "word order", "terminology:
  نقدینگی", "ZWNJ", "dash suffix").

Every row of your slice appears exactly once. Append incrementally. Log progress
per _shared-context.md rule 5.
