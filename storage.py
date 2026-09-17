import json
from pathlib import Path
from datetime import datetime

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)

def save_result(candidate, result):
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in candidate)
    path = RESULTS / f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps({
        "candidate": candidate,
        "created_at": datetime.now().isoformat(),
        **result
    }, indent=2))
