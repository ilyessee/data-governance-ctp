# CTP 2 — Which governance guard was missing at ShopFast?

**The missing guard was a *data contract* on the `amount` column** — nobody had written down, and made an **owner** accountable for, the rule *"amount is in euros, roughly 0–2000 €, with decimals"*; so when the payment team switched euros to cents the values stayed schema-valid, the naive tests passed silently, and only a contract-backed **range / distribution test** would have caught the ×100 error.

*In short: owner + contract + test — and the root one that was absent is the **data contract** (the agreed meaning and range of the field), without which no test could exist.*
