"""CTP 2 - Exercise 1: profile customers.csv with pandas and build the quality scorecard.
Run from the 02_CTP2 folder:  python profile_customers.py

Idea: each quality rule = one measurable question. We count the "failing rows",
then score = 100 * (1 - failing / total). Severity answers: does it break
MONEY, the LAW, or only a CHART? "Who fixes it" follows the RACI:
  - Owner      -> must be fixed at the SOURCE (signup form / app validation)
  - Steward    -> owns the de-duplication / merge policy
  - Custodian  -> standardises it in the TRANSFORM (pipeline), e.g. casing, dates, leading zeros
"""
import re
import csv
import pandas as pd

KIT = "../../shopfast-kit/data/"          # repo/02_CTP2 -> repo -> datagov -> shopfast-kit
df = pd.read_csv(KIT + "customers.csv", dtype=str)   # dtype=str: keep raw text (e.g. 01300 keeps its leading 0)
n = len(df)
TODAY = pd.Timestamp("2026-11-25")

print("Rows:", n)
print("\nEmpty values per column:\n", df.isna().sum())
print("\nDuplicated customer_id rows:", df["customer_id"].duplicated(keep=False).sum())

# ---------- small helpers ----------
def blank(s):                       # True where a cell is missing OR empty after trimming
    return s.isna() | (s.astype(str).str.strip() == "")

def nonblank(col):                  # the series, trimmed, only where it is not blank
    s = df[col]
    return s[~blank(s)].astype(str).str.strip()

EMAIL_RE  = r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$"
DATE_RE   = r"^\d{4}-\d{2}-\d{2}$"
POSTAL_RE = r"^\d{5}$"
ALLOWED_TIER = {"bronze", "silver", "gold", "platinum"}
ISO2 = {"FR", "DE", "ES", "BE"}
# map every spelling of a country to its ISO-2 code (for the postal-code rule)
COUNTRY_MAP = {"fr": "FR", "fra": "FR", "france": "FR",
               "de": "DE", "deu": "DE", "germany": "DE", "allemagne": "DE",
               "es": "ES", "espagne": "ES", "spain": "ES",
               "be": "BE", "bel": "BE", "belgique": "BE", "belgium": "BE"}

# ---------- TODO 1 (Uniqueness): same person registered twice = duplicate normalised email ----------
email_norm = df["email"].astype(str).str.strip().str.lower()
dup_email = (~blank(df["email"])) & email_norm.duplicated(keep=False)

# ---------- TODO 2 (Validity): emails that do not look like an email ----------
bad_email = (~blank(df["email"])) & (~df["email"].astype(str).str.strip().str.match(EMAIL_RE))

# ---------- TODO 3 (Consistency): country not written as a clean ISO-2 code ----------
country_trim = df["country"].astype(str).str.strip()
bad_country = (~blank(df["country"])) & (~country_trim.isin(ISO2))
print("\nCountry spellings:\n", country_trim[~blank(df['country'])].value_counts())

# ---------- TODO 4 (Consistency): signup_date not in YYYY-MM-DD ----------
bad_signup_fmt = (~blank(df["signup_date"])) & (~df["signup_date"].astype(str).str.strip().str.match(DATE_RE))

# ---------- TODO 5 (Validity): loyalty_tier outside the allowed set (case-insensitive) ----------
bad_tier = (~blank(df["loyalty_tier"])) & (~df["loyalty_tier"].astype(str).str.strip().str.lower().isin(ALLOWED_TIER))

# ---------- TODO 6 (Accuracy): birth dates in the future or before 1906 ----------
birth = pd.to_datetime(df["birth_date"].astype(str).str.strip(), format="%Y-%m-%d", errors="coerce")
bad_birth = birth.notna() & ((birth > (TODAY - pd.DateOffset(years=18))) | (birth < pd.Timestamp("1906-01-01")))

# ---------- TODO 7 (Validity): French postal codes that are not 5 digits ----------
iso_country = country_trim.str.lower().map(COUNTRY_MAP)           # normalised country
is_fr = iso_country == "FR"
bad_postal_fr = is_fr & (~df["postal_code"].astype(str).str.strip().str.match(POSTAL_RE))

# ---------- extra completeness + a timeliness proxy ----------
empty_email   = blank(df["email"])
empty_country = blank(df["country"])
dup_id        = df["customer_id"].duplicated(keep=False)
future_signup = pd.to_datetime(df["signup_date"].astype(str).str.strip(), format="%Y-%m-%d", errors="coerce") > TODAY

# ---------- the scorecard: (dimension, rule, column, how, failing_mask, severity, who) ----------
RULES = [
 ("Completeness","email is filled","email","blank(email)", empty_email,"Medium","Owner (fix signup form)"),
 ("Completeness","country is filled","country","blank(country)", empty_country,"Medium","Owner (fix signup form)"),
 ("Uniqueness","customer_id is unique","customer_id","duplicated(customer_id)", dup_id,"High","Steward (merge policy)"),
 ("Uniqueness","one account per person","email","duplicate lower-cased email", dup_email,"High","Steward (merge policy)"),
 ("Validity","email looks like an email","email","regex "+EMAIL_RE, bad_email,"Medium","Owner (form validation)"),
 ("Validity","loyalty_tier in bronze/silver/gold/platinum","loyalty_tier","lower() not in set", bad_tier,"Low","Custodian (normalise in transform)"),
 ("Validity","French postal code has 5 digits","postal_code","FR rows not matching ^\\d{5}$", bad_postal_fr,"Medium","Custodian (pad leading 0 in transform)"),
 ("Consistency","country is an ISO-2 code","country","value not in {FR,DE,ES,BE}", bad_country,"Medium","Custodian (standardise in transform)"),
 ("Consistency","signup_date is YYYY-MM-DD","signup_date","not matching ^\\d{4}-\\d{2}-\\d{2}$", bad_signup_fmt,"Low","Custodian (parse in transform)"),
 ("Accuracy","birth_date is plausible (1906..today-18y)","birth_date","parsed date out of range", bad_birth,"Medium","Owner (validate at entry)"),
 ("Timeliness","signup_date is not in the future","signup_date","parsed date > today", future_signup,"Medium","Owner (source validation)"),
]

out = "quality_scorecard.csv"
header = ["dimension","rule_in_plain_words","column","how_you_measured_it","failing_rows",
          "total_rows","score_pct","severity_high_medium_low","who_should_fix_owner_steward_custodian"]
print("\n%-13s %-42s %8s %7s" % ("DIMENSION","RULE","FAILING","SCORE%"))
with open(out,"w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(header)
    for dim, rule, col, how, mask, sev, who in RULES:
        fail = int(mask.sum()); score = round(100*(1-fail/n), 1)
        w.writerow([dim, rule, col, how, fail, n, score, sev, who])
        print("%-13s %-42s %8d %6.1f" % (dim, rule[:42], fail, score))
print("\nScorecard written to", out, "(", len(RULES), "rules over", len({r[0] for r in RULES}), "dimensions )")
