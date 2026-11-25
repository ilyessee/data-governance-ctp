# Ex 4 — Data dictionary vs the dbt code: what is in my head but not yet in the code?

Comparing my `data_dictionary_template.csv` (15 columns) with the CSV generated from the dbt YAML (`export_dictionary.py` → `data_dictionary_from_dbt.csv`).

**The dbt code already captures:** column description, PII flag, classification (only for PII columns), model owner, domain, tier.

**Still only in the dictionary (in my head, not in the code):**
1. **Data type** (INTEGER / DATE / DECIMAL / VARCHAR) — not documented as metadata in YAML.
2. **Unit / format** (EUR with 2 decimals, YYYY-MM-DD, ISO-2 codes). Only `amount`'s unit made it into a description.
3. **Allowed values / range** — `status`, `country_code`, `loyalty_tier` became `accepted_values` tests, but numeric **ranges** (e.g. `amount` > 0 and < ~1500) are **not yet dbt tests**.
4. **Nullability**, **example value**, **source system** — not in the YAML at all.
5. **Classification of non-PII but sensitive columns**: the business treats `amount` and `total_amount_eur` as *confidential*, but the dbt YAML only classifies PII columns.

**The one line that matters most:** `amount` = **EUROS with 2 decimals — NOT cents**. It is now in the column description, but the *range test* that would enforce it (CTP 2's "smart" checks) is still missing from this dbt project — the next thing to add to close the gap.
