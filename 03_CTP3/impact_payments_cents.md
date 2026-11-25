# Impact note — Payments team plans to switch `amount` from euros to cents

1. **What changes:** `payments.amount` would move from euros to cents (×100) — every value stays a valid number, but the unit is wrong.
2. **What breaks (lineage `source:payments+`):** `stg_payments.amount` → `fct_orders` (gross / refunded / net revenue ×100) → the **Sales dashboard** (opened daily by the CEO) and the **Finance monthly revenue report** (board & investors); and `dim_customers.lifetime_net_revenue_eur` → the **churn-prediction model** (corrupted features).
3. **Owners to warn before shipping:** Sara Martin (Sales dashboard + `fct_orders`), Paul Girard (Finance report), Karim Benali (Steward + churn model).
4. **Test to add:** a unit/range test on `amount` (EUR, 2 decimals, per-value 0.01–2000 and a mean/median range — the CTP 2 "smart" checks), plus the unit documented in the data dictionary and the data contract.
5. **Who approves:** the data owner of payments/revenue, Paul Girard (Head of Finance), signs off on the change **and its migration** in a pull request before it ships.
