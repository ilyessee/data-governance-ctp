# Part 1 — Get READY (setup self-test)

The course self-test `python check_setup.py` passes with every line **OK** and the final green **READY**.

## How to reproduce

```bash
# 1. Start Docker Desktop (wait for "Engine running")
# 2. Start the ShopFast database
cd ~/Documents/datagov/shopfast-kit
docker compose up -d        # wait until 'healthy'
# 3. Start OpenRefine (opens http://127.0.0.1:3333)
# 4. Activate the virtual environment and run the self-test
source .venv/bin/activate
python check_setup.py
```

## Result

See [`check_setup_READY.txt`](check_setup_READY.txt) for the full output, and add your terminal **screenshot** as `screenshot.png` in this folder.

- Python 3.12 virtual environment ✓
- All course packages + spaCy model `en_core_web_sm` ✓
- Docker running + ShopFast database healthy (1241 customers) ✓
- OpenRefine on http://127.0.0.1:3333 ✓
