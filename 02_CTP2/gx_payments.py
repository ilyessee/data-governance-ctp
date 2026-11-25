"""CTP 2 - Exercise 4: replay the 'cents' incident.
A naive suite (not null / unique / allowed values) PASSES on payments_batch_2.csv although every amount is 100x too big.
Only value-range and distribution expectations catch it.

Lesson: VALID is not the same as ACCURATE. Every batch_2 amount is a valid number
in EUR with a known method -> the naive schema checks all pass. What is wrong is the
MEANING (euros were sent as cents, x100). Business-aware range/distribution rules catch it.
"""
import pandas as pd
import great_expectations as gx

KIT = "../../shopfast-kit/data/"   # repo/02_CTP2 -> repo -> datagov -> shopfast-kit
files = {"payments (history)": KIT + "payments.csv", "payments_batch_2 (new)": "payments_batch_2.csv"}

context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast_payments")
asset = source.add_dataframe_asset(name="payments")
batch_def = asset.add_batch_definition_whole_dataframe("whole")
E = gx.expectations

naive = [E.ExpectColumnValuesToNotBeNull(column="payment_id"), E.ExpectColumnValuesToBeUnique(column="payment_id"),
         E.ExpectColumnValuesToNotBeNull(column="amount"), E.ExpectColumnValuesToBeInSet(column="currency", value_set=["EUR"]),
         E.ExpectColumnValuesToBeInSet(column="method", value_set=["card", "paypal", "apple_pay", "bank_transfer"])]
smart = naive + [
    # 1) A single payment is between 0.01 and 2000 EUR (history max is ~1400). batch_2 goes up to 37996 -> FAIL.
    E.ExpectColumnValuesToBeBetween(column="amount", min_value=0.01, max_value=2000),
    # 2) The AVERAGE payment stays around 50-500 EUR (history mean ~236). batch_2 mean ~18900 -> FAIL.
    E.ExpectColumnMeanToBeBetween(column="amount", min_value=50, max_value=500),
    # 3) The MEDIAN payment stays around 50-400 EUR (history median ~184). batch_2 median ~18500 -> FAIL.
    E.ExpectColumnMedianToBeBetween(column="amount", min_value=50, max_value=400),
    # 4) Amounts are written in euros WITH a decimal point (49.90), never as raw cents (4990). batch_2 is 100% integers -> FAIL.
    E.ExpectColumnValuesToMatchRegex(column="amount_txt", regex=r"^\d+\.\d+$", mostly=0.99),
]

def run(name, expectations, df):
    suite = context.suites.add_or_update(gx.ExpectationSuite(name=name))
    for e in expectations: suite.add_expectation(e.copy() if hasattr(e, "copy") else e)
    suite.save()
    return batch_def.get_batch(batch_parameters={"dataframe": df}).validate(suite)

for label, path in files.items():
    df = pd.read_csv(path, dtype=str); df["amount_txt"] = df["amount"]; df["amount"] = pd.to_numeric(df["amount"])
    for suite_name, exps in [("naive_payments", naive), ("smart_payments", smart)]:
        res = run(suite_name, exps, df)
        failed = [r.expectation_config.type for r in res.results if not r.success]
        print(f"{label:<24} {suite_name:<15} success={res.success}  failed={failed}")
