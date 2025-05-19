
# 🧪 Test Coverage Summary

| File                             | Statements | Missed | Coverage | Lines Missing       |
|----------------------------------|:----------:|:------:|:--------:|--------------------|
| app/__init__.py                  |    13      |   0    | 100%     |                    |
| app/routes/__init__.py           |     0      |   0    | 100%     |                    |
| app/routes/audio_routes.py       |    64      |   4    | 94%      | 156-166            |
| app/routes/json_routes.py        |    57      |   1    | 98%      | 39                 |
| app/routes/meeting_routes.py     |    34      |   0    | 100%     |                    |
| app/services/__init__.py         |     0      |   0    | 100%     |                    |
| app/services/audio_processor.py  |   109      |   8    | 93%      | 137, 140, 170, 172-175, 180 |
| app/services/calendar_api.py     |    50      |   0    | 100%     |                    |
| app/services/calendar_integration.py | 26    |   0    | 100%     |                    |
| app/services/nlp_analysis.py     |    70      |   2    | 97%      | 60, 148            |
| app/utils/__init__.py            |     0      |   0    | 100%     |                    |
| app/utils/entity_utils.py        |    85      |   2    | 98%      | 197-198            |
| app/utils/logger.py              |    16      |   0    | 100%     |                    |
| app/utils/logging_utils.py       |    46      |   0    | 100%     |                    |
| app/utils/nextcloud_utils.py     |    32      |   0    | 100%     |                    |
| **TOTAL**                        |   602      |  17    | 97%      |                    |

---

## Highlights

- **All major modules >93% covered**; core logic is well-protected by tests.
- **100% coverage** for most utility, routing, and service modules.
- **Minor gaps** in:
  - `audio_routes.py` (lines 156–166)
  - `audio_processor.py` (lines 137, 140, 170, 172–175, 180)
  - `nlp_analysis.py` (lines 60, 148)
  - `entity_utils.py` (lines 197–198)
  - `json_routes.py` (line 39)
- **Easy targets** for 100%: a handful of specific lines remain to be tested.

---

## How to use this

- Paste into your README, a `docs/coverage.md`, or your wiki.
- Optionally, annotate which lines are “hard to test” or “not relevant for unit tests” (like error paths or very rare edge cases).

## Example action item for contributors

> “Want to help? Write tests to cover the following lines:  
> - `audio_routes.py`: lines 156–166  
> - `audio_processor.py`: lines 137, 140, 170, 172–175, 180  
> - etc.”
