{% docs gross_revenue %}
**Gross revenue (EUR)** — total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs net_revenue %}
**Net revenue (EUR)** — gross revenue minus refunds, **excluding VAT** (divided by 1.20); shipping fees are kept in.
Formula: `(gross_revenue_eur - refunded_eur) / 1.20`. Example: 120 € paid, no refund → 100 €.
Owner: Paul Girard (Head of Finance) · Steward: Karim Benali · Status: approved (2026-11-25).
Note: Sales commissions use a separate measure (gross − refunds, VAT **included**) — that is not this term.
{% enddocs %}

{% docs active_customer %}
**Active customer** — an account with at least one **non-cancelled** order in the **last 12 months**.
Example: last non-cancelled order 8 months ago → active; 14 months ago → not.
Owner: Paul Girard (Head of Finance) · Steward: Karim Benali · Status: approved (2026-11-25).
Note: company standard is 12 months; Sales' 6-month view is a separate term, "recently active customer".
{% enddocs %}

{% docs churned_customer %}
**Churned customer** — a customer who was active before but has **no non-cancelled order in the last 12 months** (the complement of "active customer").
Owner: Paul Girard (Head of Finance) · Steward: Karim Benali · Status: approved (2026-11-25).
{% enddocs %}

{% docs customer %}
**Customer** — a unique account registered in ShopFast (one row per `customer_id` in `dim_customers`). One person may hold several accounts, so "customer" means the account, not the person.
Owner: Sara Martin (Head of Sales) · Steward: Karim Benali · Status: approved (2026-11-25).
{% enddocs %}

{% docs order %}
**Order** — a single purchase transaction placed by a customer (one row per `order_id` in `fct_orders`). A cancelled order is still an order (`status = 'cancelled'`) but is excluded from the active-customer rule.
Owner: Sara Martin (Head of Sales) · Steward: Karim Benali · Status: approved (2026-11-25).
{% enddocs %}
