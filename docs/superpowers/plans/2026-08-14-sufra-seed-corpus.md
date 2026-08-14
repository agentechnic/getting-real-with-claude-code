# Sufra Seed Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Sufra seed repository — a bilingual corpus of support tickets with a planted, changelog-correlated signal — plus the verification suite that proves the corpus can actually teach the workshop.

**Architecture:** A seeded, deterministic Python generator composes tickets from phrase banks in colloquial Saudi Arabic, fusha, English and code-switched mixtures. Authoring tools live outside the attendee-facing folder. A pytest suite verifies the properties the workshop depends on: the planted cluster exists and correlates to one release, the same theme appears across all three language registers, Q2's dominant theme differs from Q1's, and no real company is named anywhere.

**Tech Stack:** Python 3.11+, standard library only, `uv` for dependency management, `pytest` for the corpus suite. No build step, no frameworks — repository convention.

**Spec:** `docs/superpowers/specs/2026-08-14-repeatable-workflows-workshop-design.md`

## Global Constraints

- **Branch only.** All work happens on `workshop-v2`. Nothing in this plan reaches `main` before 2026-08-15 — the live site runs the Riyadh workshop that morning.
- **Fictional brand only.** The product is **Sufra** (سفرة). No ticket, changelog entry, or report may name a real company — not as the subject, not as a competitor, not in passing.
- **Offline.** Nothing in the corpus or its tooling may require network access at runtime.
- **Deterministic.** The generator is seeded with `CORPUS_SEED = 20260815`. Regenerating must produce a byte-identical corpus, or the answer key stops being true.
- **Python 3.11+**, standard library only for the generator. `pytest` is a dev dependency.
- **Attendee-facing folder is `sufra/`.** Authoring tools (`tools/`) and the answer key (`facilitator/`) live outside it and are never referenced from attendee material.
- **Language mix target:** ~55% Arabic, ~25% English, ~20% code-switched. Verified as a band, not an exact count.
- **Ticket volume:** 200 in `tickets-q1/`, 120 in `tickets-q2/`.

---

## File Structure

```
sufra/                          Attendee-facing seed repo
  CLAUDE.md                     Conventions + report format rule
  README.md                     What this is, how to start
  tickets-q1/ticket-0001.txt    200 tickets, one per file
  tickets-q2/ticket-0001.txt    120 tickets, second batch
  context/
    changelog.md                Releases with dates; v4.2 is the planted cause
    themes-2025-q4.md           Prior report — the house format to match

tools/                          Authoring tools; attendees never touch these
  corpus/__init__.py
  corpus/spec.py                Releases, themes, planted signal, phrase banks
  corpus/phrases_ar.py          Colloquial Saudi + fusha phrase banks
  corpus/phrases_en.py          English + code-switched phrase banks
  corpus/generate.py            Deterministic generator
  tests/test_spec.py            Spec internal consistency
  tests/test_corpus_q1.py       Planted signal, language mix, messiness
  tests/test_corpus_q2.py       Different dominant theme
  tests/test_safety.py          No real brands anywhere
  pyproject.toml                Dev deps for the tooling

sufra-co/  → moved out: now the separate repo thepandanlabs/sufra

facilitator/
  sufra-answer-key.md           The planted cluster, its release, the counts
```

`sufra/` holds only what an attendee needs. `tools/` and `facilitator/` are authoring surface.

---

### Task 1: Branch and tooling skeleton

**Files:**
- Create: `tools/pyproject.toml`
- Create: `tools/corpus/__init__.py`
- Create: `tools/corpus/spec.py`
- Test: `tools/tests/test_spec.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `CORPUS_SEED: int`, `RELEASES: list[Release]`, `THEMES: dict[str, Theme]`, `PLANTED: PlantedSignal`, and the dataclasses `Release(version: str, date: str, summary: str)`, `Theme(key: str, label_en: str, label_ar: str)`, `PlantedSignal(theme_key: str, release_version: str, count: int, window_days: int)`.

- [ ] **Step 1: Create the branch**

```bash
cd /Users/cloudranger/dev/projects/claude-code-workshop
git checkout -b workshop-v2
```

- [ ] **Step 2: Write the failing test**

Create `tools/tests/test_spec.py`:

```python
from datetime import date

from corpus import spec


def test_planted_signal_points_at_a_real_release():
    versions = {r.version for r in spec.RELEASES}
    assert spec.PLANTED.release_version in versions


def test_planted_signal_points_at_a_real_theme():
    assert spec.PLANTED.theme_key in spec.THEMES


def test_releases_are_chronological():
    dates = [date.fromisoformat(r.date) for r in spec.RELEASES]
    assert dates == sorted(dates), "releases must be listed oldest first"


def test_every_theme_has_both_labels():
    for key, theme in spec.THEMES.items():
        assert theme.label_en.strip(), f"{key} missing English label"
        assert theme.label_ar.strip(), f"{key} missing Arabic label"
```

- [ ] **Step 3: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_spec.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'corpus'`

- [ ] **Step 4: Write `tools/pyproject.toml`**

```toml
[project]
name = "sufra-corpus-tools"
version = "0.1.0"
description = "Authoring tools for the Sufra workshop corpus. Not attendee-facing."
requires-python = ">=3.11"
dependencies = []

[dependency-groups]
dev = ["pytest>=8.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- [ ] **Step 5: Write `tools/corpus/__init__.py`**

```python
"""Authoring tools for the Sufra workshop corpus.

Attendees never run anything in here. This generates and verifies the
material in sufra/.
"""
```

- [ ] **Step 6: Write `tools/corpus/spec.py`**

```python
"""The corpus's single source of truth.

The generator builds from this and the tests verify against it, so the
planted signal is defined exactly once. Changing anything here changes
what the facilitator answer key must say.
"""

from dataclasses import dataclass


CORPUS_SEED = 20260815

Q1_TICKET_COUNT = 200
Q2_TICKET_COUNT = 120


@dataclass(frozen=True)
class Release:
    version: str
    date: str  # YYYY-MM-DD
    summary: str


@dataclass(frozen=True)
class Theme:
    key: str
    label_en: str
    label_ar: str


@dataclass(frozen=True)
class PlantedSignal:
    theme_key: str
    release_version: str
    count: int
    window_days: int


# The v4.2 address picker is the cause the workshop is built around. Every
# other release is ordinary noise, present so the correlation has to be
# found rather than guessed.
RELEASES = [
    Release("4.0", "2026-01-08", "Ramadan pre-order scheduling."),
    Release("4.1", "2026-01-27", "Restaurant search ranking rebuilt."),
    Release("4.2", "2026-02-11", "New address picker with map pinning; "
                                 "replaces free-text address entry."),
    Release("4.3", "2026-03-04", "Loyalty points shown at checkout."),
    Release("4.4", "2026-03-23", "Order tracking screen refresh."),
    # Q2 territory — the payment migration is Q2's dominant cause.
    Release("4.5", "2026-04-14", "Payment provider migration."),
    Release("4.6", "2026-05-06", "Group orders."),
]

THEMES = {
    "driver_lost": Theme("driver_lost", "Driver could not find the address",
                         "الكابتن ما لقى العنوان"),
    "late": Theme("late", "Late delivery", "تأخير التوصيل"),
    "wrong_items": Theme("wrong_items", "Wrong or missing items",
                         "طلب خاطئ أو ناقص"),
    "cold_food": Theme("cold_food", "Food arrived cold", "الأكل وصل بارد"),
    "payment_failed": Theme("payment_failed", "Payment failed or double charged",
                            "مشكلة في الدفع أو خصم مزدوج"),
    "refund_delay": Theme("refund_delay", "Refund not received",
                          "تأخر استرداد المبلغ"),
    "app_crash": Theme("app_crash", "App crashes or will not open",
                       "التطبيق يطفي أو ما يفتح"),
    "rude_driver": Theme("rude_driver", "Driver conduct", "تعامل الكابتن"),
}

PLANTED = PlantedSignal(
    theme_key="driver_lost",
    release_version="4.2",
    count=23,
    window_days=21,
)
```

- [ ] **Step 7: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_spec.py -v
```

Expected: 4 passed

- [ ] **Step 8: Commit**

```bash
git add tools/
git commit -m "Add corpus spec: releases, themes, and the planted v4.2 signal"
```

---

### Task 2: Arabic phrase banks

**Files:**
- Create: `tools/corpus/phrases_ar.py`
- Test: `tools/tests/test_phrases.py`

**Interfaces:**
- Consumes: `spec.THEMES` keys.
- Produces: `COLLOQUIAL: dict[str, list[str]]` and `FUSHA: dict[str, list[str]]`, both keyed by theme key. Every theme key in `spec.THEMES` has at least four colloquial and two fusha variants.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_phrases.py`:

```python
from corpus import phrases_ar, spec


def test_every_theme_has_colloquial_variants():
    for key in spec.THEMES:
        assert len(phrases_ar.COLLOQUIAL.get(key, [])) >= 4, (
            f"{key} needs at least 4 colloquial variants so the corpus does "
            "not read as copy-paste"
        )


def test_every_theme_has_fusha_variants():
    for key in spec.THEMES:
        assert len(phrases_ar.FUSHA.get(key, [])) >= 2, f"{key} needs fusha variants"


def test_phrases_are_actually_arabic():
    arabic_range = range(0x0600, 0x0700)
    for bank in (phrases_ar.COLLOQUIAL, phrases_ar.FUSHA):
        for key, variants in bank.items():
            for text in variants:
                assert any(ord(ch) in arabic_range for ch in text), (
                    f"{key}: {text!r} contains no Arabic characters"
                )
```

- [ ] **Step 2: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_phrases.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'corpus.phrases_ar'`

- [ ] **Step 3: Write `tools/corpus/phrases_ar.py`**

Spelling is deliberately inconsistent — missing hamzas, dropped dots, elongated letters. That is how the queue actually looks, and it is what makes the clustering non-trivial.

```python
"""Arabic phrase banks.

Colloquial Saudi as people actually type it: missing hamzas, no
diacritics, occasional elongation, inconsistent spelling of the same
word. Fusha appears mostly in the longer escalation tickets.

"كابتن" is the ordinary word for a delivery driver here; "سواق" and
"سايق" both appear and both are correct usage.
"""

COLLOQUIAL = {
    "driver_lost": [
        "الكابتن ما لقى العمارة وطنش الاتصال",
        "السواق ضاع نص ساعه ويقول ما يعرف المكان",
        "السايق ما عرف العنوان مع اني حاطه بالضبط",
        "كلمني الكابتن ثلاث مرات يسال وين البيت، الموقع غلط بالتطبيق",
        "الموقع ودى الكابتن لشارع ثاني كامل",
        "المندوب ما لقى الفيلا ورجع الطلب",
    ],
    "late": [
        "الطلب تأخر ساعه كامله",
        "طلبت من الساعه ٨ ولين الحين ما وصل",
        "التوصيل تاخر كثير بدون اي سبب",
        "ساعه ونص انتظار وهذا مو اول مره",
    ],
    "wrong_items": [
        "جاني طلب ثاني مو طلبي",
        "ناقص صنفين من الطلب",
        "طلبت برجر وجاني شاورما",
        "الطلب غلط بالكامل وما احد رد علي",
    ],
    "cold_food": [
        "الاكل وصل بارد ومب صالح للاكل",
        "البرجر بارد والبطاطس ذابله",
        "وصل الطلب بارد بسبب التاخير",
        "الاكل كان بارد وما استفدت منه",
    ],
    "payment_failed": [
        "خصم مني مرتين لنفس الطلب",
        "انخصم المبلغ والطلب ملغي",
        "الدفع ما نجح بس المبلغ راح",
        "حاولت ادفع ثلاث مرات وكل مره يفشل",
        "خصمتوا مرتين ليش؟",
    ],
    "refund_delay": [
        "له اسبوع وما رجع المبلغ",
        "وعدتوني بالاسترداد وللحين ما وصل",
        "ملغي الطلب من زمان والفلوس ما رجعت",
        "متى يرجع المبلغ؟ صار لي عشر ايام انتظر",
    ],
    "app_crash": [
        "التطبيق يطفي كل ما افتحه",
        "ما يفتح عندي التطبيق بعد التحديث",
        "الشاشه تعلق عند الدفع",
        "التطبيق يسكر فجأه وانا اطلب",
    ],
    "rude_driver": [
        "الكابتن كان اسلوبه سيء",
        "المندوب رد علي بطريقه غير لائقه",
        "السواق رفض يطلع للدور وكان متضايق",
        "تعامل الكابتن ما كان مناسب ابدا",
    ],
}

FUSHA = {
    "driver_lost": [
        "أفيدكم بأن مندوب التوصيل لم يتمكن من الوصول إلى العنوان المحدد رغم "
        "دقته، وأرجو مراجعة آلية تحديد المواقع في التطبيق.",
        "تكرر عدم قدرة المندوبين على الوصول إلى عنواني خلال الفترة الأخيرة، "
        "علماً بأن ذلك لم يحدث سابقاً.",
    ],
    "late": [
        "تأخر الطلب عن الوقت المحدد بما يزيد على الساعة، وأرجو إفادتي بسبب "
        "التأخير.",
        "أود التقدم بشكوى بخصوص التأخر المتكرر في مواعيد التوصيل.",
    ],
    "wrong_items": [
        "وصلني طلب لا يخصني، وأرجو اتخاذ اللازم واسترداد المبلغ.",
        "الطلب المستلم ناقص عدداً من الأصناف المذكورة في الفاتورة.",
    ],
    "cold_food": [
        "وصل الطلب بحالة غير مناسبة للاستهلاك نتيجة التأخر في التوصيل.",
        "أفيدكم بأن الوجبة وصلت باردة، وأرجو النظر في آلية حفظ الطلبات.",
    ],
    "payment_failed": [
        "تم خصم المبلغ مرتين لنفس الطلب، وأرفق لكم رقم العملية، وأرجو "
        "إفادتي بآلية استرداد المبلغ.",
        "تمت عملية الخصم رغم فشل إتمام الطلب، وأطلب معالجة الأمر.",
    ],
    "refund_delay": [
        "مضى على طلب الاسترداد أكثر من عشرة أيام دون استلام المبلغ، وأرجو "
        "إفادتي بالمدة النظامية.",
        "لم يصلني المبلغ المسترد حتى تاريخه رغم تأكيدكم إتمام العملية.",
    ],
    "app_crash": [
        "يتعذر علي فتح التطبيق منذ التحديث الأخير، وأرجو إفادتي بالحل.",
        "يتوقف التطبيق عن الاستجابة عند مرحلة الدفع بشكل متكرر.",
    ],
    "rude_driver": [
        "أود الإفادة بأن أسلوب مندوب التوصيل لم يكن لائقاً، وأرجو اتخاذ "
        "الإجراء المناسب.",
        "تعرضت لتعامل غير مهني من أحد المندوبين وأرغب في تقديم شكوى رسمية.",
    ],
}
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_phrases.py -v
```

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add tools/corpus/phrases_ar.py tools/tests/test_phrases.py
git commit -m "Add Arabic phrase banks: colloquial Saudi and fusha"
```

---

### Task 3: English and code-switched phrase banks

**Files:**
- Create: `tools/corpus/phrases_en.py`
- Modify: `tools/tests/test_phrases.py`

**Interfaces:**
- Consumes: `spec.THEMES` keys.
- Produces: `ENGLISH: dict[str, list[str]]` and `MIXED: dict[str, list[str]]`, both keyed by theme key, each with at least three variants per theme.

- [ ] **Step 1: Write the failing test**

Append to `tools/tests/test_phrases.py`:

```python
from corpus import phrases_en


def test_every_theme_has_english_variants():
    for key in spec.THEMES:
        assert len(phrases_en.ENGLISH.get(key, [])) >= 3, f"{key} needs English variants"


def test_every_theme_has_mixed_variants():
    for key in spec.THEMES:
        assert len(phrases_en.MIXED.get(key, [])) >= 3, f"{key} needs code-switched variants"


def test_mixed_variants_contain_both_scripts():
    arabic_range = range(0x0600, 0x0700)
    for key, variants in phrases_en.MIXED.items():
        for text in variants:
            has_arabic = any(ord(ch) in arabic_range for ch in text)
            has_latin = any(ch.isascii() and ch.isalpha() for ch in text)
            assert has_arabic and has_latin, (
                f"{key}: {text!r} should mix Arabic and Latin script"
            )
```

- [ ] **Step 2: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_phrases.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'corpus.phrases_en'`

- [ ] **Step 3: Write `tools/corpus/phrases_en.py`**

```python
"""English and code-switched phrase banks.

The MIXED bank is the common real case: an Arabic sentence with English
product nouns dropped in, or the reverse. A correct analysis has to
group these with their Arabic and English equivalents.
"""

ENGLISH = {
    "driver_lost": [
        "Driver couldn't find building, called me 4 times",
        "The captain got lost and blamed the map pin",
        "Driver said the location in the app is wrong, took him 30 min",
        "He ended up in a different street entirely",
    ],
    "late": [
        "Order was over an hour late",
        "Waited 90 minutes, no update in the app",
        "Consistently late for the third time this month",
    ],
    "wrong_items": [
        "Received someone else's order",
        "Two items missing from my order",
        "Ordered chicken, got beef",
    ],
    "cold_food": [
        "Food arrived completely cold",
        "Fries were soggy and the burger was cold",
        "Cold food because of the delay",
    ],
    "payment_failed": [
        "Charged twice for the same order",
        "Payment failed but money was deducted",
        "Card declined three times then charged anyway",
    ],
    "refund_delay": [
        "Still waiting for my refund after 10 days",
        "Refund was promised last week, nothing yet",
        "Order cancelled ages ago, money never came back",
    ],
    "app_crash": [
        "App crashes every time I open it",
        "Won't open at all since the update",
        "Freezes on the payment screen",
    ],
    "rude_driver": [
        "Driver was rude on the phone",
        "Captain refused to come up to the floor",
        "Unprofessional behaviour from the delivery guy",
    ],
}

MIXED = {
    "driver_lost": [
        "الكابتن ما لقى الموقع، the pin was in a totally different place",
        "driver اتصل ثلاث مرات ما عرف العنوان",
        "الـ location في التطبيق غلط، he went to the wrong compound",
        "captain ضاع تماما وقال the map is wrong",
    ],
    "late": [
        "الطلب late بساعه كامله",
        "waited ساعه ونص وما وصل شي",
        "delivery تأخر مره وما في اي update",
    ],
    "wrong_items": [
        "جاني order غلط",
        "ناقص items من الطلب",
        "received طلب شخص ثاني",
    ],
    "cold_food": [
        "الاكل وصل cold تماما",
        "الـ fries باردة والبرجر بارد",
        "food بارد بسبب التاخير",
    ],
    "payment_failed": [
        "خصم مرتين، double charge على نفس الطلب",
        "payment failed بس المبلغ انخصم",
        "الـ card اترفضت بعدين خصمتوا",
    ],
    "refund_delay": [
        "الـ refund ما وصل من عشر ايام",
        "وعدتوني بـ refund وللحين ما شي",
        "cancelled الطلب والفلوس ما رجعت",
    ],
    "app_crash": [
        "الـ app يطفي كل ما افتحه",
        "ما يفتح بعد الـ update",
        "يعلق عند الـ payment screen",
    ],
    "rude_driver": [
        "الكابتن كان rude بالتلفون",
        "driver رفض يطلع fifth floor",
        "تعامل unprofessional من المندوب",
    ],
}
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_phrases.py -v
```

Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add tools/corpus/phrases_en.py tools/tests/test_phrases.py
git commit -m "Add English and code-switched phrase banks"
```

---

### Task 4: Context files — changelog and prior report

**Files:**
- Create: `sufra/context/changelog.md`
- Create: `sufra/context/themes-2025-q4.md`
- Test: `tools/tests/test_context.py`

**Interfaces:**
- Consumes: `spec.RELEASES`, `spec.PLANTED`.
- Produces: the two context files. `themes-2025-q4.md` is the house format every generated report must match — it is the spec without being called one.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_context.py`:

```python
from pathlib import Path

from corpus import spec

SUFRA = Path(__file__).resolve().parents[2] / "sufra"
CHANGELOG = SUFRA / "context" / "changelog.md"
PRIOR = SUFRA / "context" / "themes-2025-q4.md"


def test_changelog_lists_every_release():
    text = CHANGELOG.read_text(encoding="utf-8")
    for release in spec.RELEASES:
        assert release.version in text, f"changelog missing v{release.version}"
        assert release.date in text, f"changelog missing date for v{release.version}"


def test_changelog_does_not_flag_the_planted_release():
    """The correlation must be discoverable, not announced."""
    text = CHANGELOG.read_text(encoding="utf-8").lower()
    for giveaway in ("caused", "regression", "incident", "known issue", "spike"):
        assert giveaway not in text, (
            f"changelog says {giveaway!r} — that hands the answer to the room"
        )


def test_prior_report_has_the_house_format_sections():
    text = PRIOR.read_text(encoding="utf-8")
    for heading in ("## Summary", "## Themes", "## Recommendations"):
        assert heading in text, f"prior report missing {heading}"


def test_prior_report_quantifies_each_theme():
    text = PRIOR.read_text(encoding="utf-8")
    assert "tickets" in text.lower()
    assert "%" in text, "themes should carry a share, so the new report copies that"
```

- [ ] **Step 2: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_context.py -v
```

Expected: FAIL — `FileNotFoundError` on `changelog.md`

- [ ] **Step 3: Write `sufra/context/changelog.md`**

Every entry reads as routine. Nothing hints that 4.2 caused anything.

```markdown
# Sufra — Release Notes

Customer-facing release notes for the Sufra app. Newest last.

## v4.0 — 2026-01-08
Ramadan pre-order scheduling. Customers can place orders in advance for a
chosen delivery time.

## v4.1 — 2026-01-27
Restaurant search ranking rebuilt. Results now weight distance and
preparation time more heavily.

## v4.2 — 2026-02-11
New address picker with map pinning. Replaces free-text address entry.
Saved addresses are migrated automatically.

## v4.3 — 2026-03-04
Loyalty points balance now shown at checkout.

## v4.4 — 2026-03-23
Order tracking screen refresh, with clearer driver progress.

## v4.5 — 2026-04-14
Payment provider migration. Card handling moves to the new processor.

## v4.6 — 2026-05-06
Group orders. Multiple people can add to a single basket.
```

- [ ] **Step 4: Write `sufra/context/themes-2025-q4.md`**

```markdown
# Support Themes — Q4 2025

Prepared by the support team. Covers 1 October – 31 December 2025.

## Summary

We handled 1,840 tickets in Q4, up 12% on Q3. Volume growth tracked order
growth, so ticket rate per order was roughly flat. Nothing in this quarter
points to a single systemic cause; the mix is the usual seasonal one, with
delivery timing dominating during the December peak.

## Themes

| Theme | Tickets | Share | Trend vs Q3 |
|---|---|---|---|
| Late delivery | 612 | 33% | ▲ 4pts |
| Wrong or missing items | 388 | 21% | ▬ flat |
| Food arrived cold | 295 | 16% | ▲ 2pts |
| Payment failed or double charged | 203 | 11% | ▼ 3pts |
| Refund not received | 147 | 8% | ▬ flat |
| App crashes or will not open | 111 | 6% | ▼ 1pt |
| Driver conduct | 84 | 5% | ▬ flat |

### Late delivery — 612 tickets (33%)
Concentrated in the last three weeks of December, peaking on weekends.
Riyadh and Jeddah accounted for most of the increase. Typical wording ranges
from "الطلب تأخر ساعه" through to formal escalations requesting refunds.

### Wrong or missing items — 388 tickets (21%)
Steady across the quarter. Roughly two-thirds are missing items rather than
a wholly incorrect order.

### Food arrived cold — 295 tickets (16%)
Correlates with the late delivery theme; most of these tickets also mention
a delay.

## Recommendations

1. Add restaurant-side capacity signals before the next seasonal peak.
2. Review packaging for the ten most-ordered cold-on-arrival items.
3. Reduce refund processing time; it is the theme with the worst sentiment
   even at low volume.

## Method

Tickets were read, grouped by theme, and counted. Where a ticket raised more
than one issue it was assigned to the dominant one. Counts are exact, not
sampled.
```

- [ ] **Step 5: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_context.py -v
```

Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add sufra/context/ tools/tests/test_context.py
git commit -m "Add Sufra changelog and the Q4 report that sets the house format"
```

---

### Task 5: The generator

**Files:**
- Create: `tools/corpus/generate.py`
- Test: `tools/tests/test_generate.py`

**Interfaces:**
- Consumes: `spec`, `phrases_ar`, `phrases_en`.
- Produces: `build_tickets(quarter: str) -> list[Ticket]` and `write_corpus(quarter: str, out_dir: Path) -> int`, where `Ticket` is `Ticket(number: int, date: str, channel: str, language: str, theme_key: str, subject: str, body: str)`. `quarter` is `"q1"` or `"q2"`. Returns the count written.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_generate.py`:

```python
from corpus import generate, spec


def test_q1_produces_the_expected_volume():
    tickets = generate.build_tickets("q1")
    assert len(tickets) == spec.Q1_TICKET_COUNT


def test_generation_is_deterministic():
    first = generate.build_tickets("q1")
    second = generate.build_tickets("q1")
    assert [t.body for t in first] == [t.body for t in second], (
        "the corpus must regenerate identically or the answer key goes stale"
    )


def test_q2_produces_the_expected_volume():
    assert len(generate.build_tickets("q2")) == spec.Q2_TICKET_COUNT


def test_writes_one_file_per_ticket(tmp_path):
    written = generate.write_corpus("q1", tmp_path)
    assert written == spec.Q1_TICKET_COUNT
    assert len(list(tmp_path.glob("ticket-*.txt"))) == spec.Q1_TICKET_COUNT
```

- [ ] **Step 2: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_generate.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'corpus.generate'`

- [ ] **Step 3: Write `tools/corpus/generate.py`**

```python
"""Deterministic generator for the Sufra ticket corpus.

Seeded so the corpus regenerates byte-identically. The facilitator answer
key states exact counts, so drift here silently invalidates the workshop.

Messiness is deliberate: near-empty tickets, duplicates, and inconsistent
formatting all appear, because a clean corpus would not teach anything.
"""

import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from . import phrases_ar, phrases_en, spec

CHANNELS = ["in-app", "email", "phone-callback", "whatsapp"]

# Baseline theme weights, before the planted signal is layered on.
Q1_WEIGHTS = {
    "late": 30, "wrong_items": 18, "cold_food": 14, "payment_failed": 10,
    "refund_delay": 8, "app_crash": 7, "rude_driver": 6, "driver_lost": 7,
}
# Q2 shifts hard to payment: a Skill that hardcoded Q1's answer fails here.
Q2_WEIGHTS = {
    "payment_failed": 34, "refund_delay": 20, "late": 14, "wrong_items": 10,
    "cold_food": 8, "app_crash": 6, "driver_lost": 5, "rude_driver": 3,
}

QUARTER_WINDOWS = {
    "q1": (date(2026, 1, 1), date(2026, 3, 31)),
    "q2": (date(2026, 4, 1), date(2026, 6, 30)),
}


@dataclass(frozen=True)
class Ticket:
    number: int
    date: str
    channel: str
    language: str
    theme_key: str
    subject: str
    body: str


def _pick_language(rng: random.Random) -> str:
    roll = rng.random()
    if roll < 0.55:
        return "ar"
    if roll < 0.80:
        return "en"
    return "mixed"


def _body_for(rng: random.Random, theme_key: str, language: str) -> str:
    if language == "ar":
        # Fusha shows up in the longer, more formal escalations.
        if rng.random() < 0.25:
            return rng.choice(phrases_ar.FUSHA[theme_key])
        return rng.choice(phrases_ar.COLLOQUIAL[theme_key])
    if language == "en":
        return rng.choice(phrases_en.ENGLISH[theme_key])
    return rng.choice(phrases_en.MIXED[theme_key])


def _subject_from(body: str) -> str:
    """A support tool's auto-filled subject: the customer's own first words.

    Never the theme label. The whole task is deriving the theme, and a
    canonical label in the header would hand it over.
    """
    first_line = body.strip().splitlines()[0]
    words = first_line.split()
    subject = " ".join(words[:6])
    return subject if len(subject) <= 60 else subject[:57].rstrip() + "..."


def _weighted_theme(rng: random.Random, weights: dict[str, int]) -> str:
    keys = list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys], k=1)[0]


def _planted_dates(rng: random.Random) -> list[date]:
    """Dates for the planted cluster: inside the window after the release."""
    release = next(r for r in spec.RELEASES
                   if r.version == spec.PLANTED.release_version)
    start = date.fromisoformat(release.date)
    return [start + timedelta(days=rng.randint(0, spec.PLANTED.window_days))
            for _ in range(spec.PLANTED.count)]


def build_tickets(quarter: str) -> list[Ticket]:
    rng = random.Random(f"{spec.CORPUS_SEED}-{quarter}")
    weights = Q1_WEIGHTS if quarter == "q1" else Q2_WEIGHTS
    total = spec.Q1_TICKET_COUNT if quarter == "q1" else spec.Q2_TICKET_COUNT
    window_start, window_end = QUARTER_WINDOWS[quarter]
    span = (window_end - window_start).days

    plan: list[tuple[date, str]] = []

    if quarter == "q1":
        for when in _planted_dates(rng):
            plan.append((when, spec.PLANTED.theme_key))

    while len(plan) < total:
        when = window_start + timedelta(days=rng.randint(0, span))
        plan.append((when, _weighted_theme(rng, weights)))

    plan.sort(key=lambda pair: pair[0])

    tickets = []
    for index, (when, theme_key) in enumerate(plan, start=1):
        language = _pick_language(rng)
        body = _body_for(rng, theme_key, language)

        # Messiness. Roughly 1 in 12 tickets is near-empty, and 1 in 20 is a
        # verbatim resend of the previous one, because real queues contain both.
        if rng.random() < 0.08:
            body = body.split("،")[0].split(",")[0][:28]
        elif rng.random() < 0.05 and tickets:
            body = tickets[-1].body

        # The subject is derived from what the customer wrote, the way a
        # support tool auto-fills it. It must NEVER be the canonical theme
        # label — that would turn clustering into "group by subject" and
        # delete the exercise.
        subject = _subject_from(body)

        tickets.append(Ticket(
            number=index,
            date=when.isoformat(),
            channel=rng.choice(CHANNELS),
            language=language,
            theme_key=theme_key,
            subject=subject,
            body=body,
        ))
    return tickets


def render(ticket: Ticket) -> str:
    """One ticket as a support-tool export. Header fields, then free text.

    The theme is NOT written into the file — deriving it is the exercise.
    """
    return (
        f"Ticket: SUF-{ticket.number:05d}\n"
        f"Date: {ticket.date}\n"
        f"Channel: {ticket.channel}\n"
        f"Subject: {ticket.subject}\n"
        f"\n"
        f"{ticket.body}\n"
    )


def write_corpus(quarter: str, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    tickets = build_tickets(quarter)
    for ticket in tickets:
        path = out_dir / f"ticket-{ticket.number:04d}.txt"
        path.write_text(render(ticket), encoding="utf-8")
    return len(tickets)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2] / "sufra"
    for quarter, folder in (("q1", "tickets-q1"), ("q2", "tickets-q2")):
        count = write_corpus(quarter, root / folder)
        print(f"wrote {count} tickets to {folder}")
```

- [ ] **Step 4: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_generate.py -v
```

Expected: 4 passed

- [ ] **Step 5: Generate the corpus**

```bash
cd tools && uv run python -m corpus.generate
```

Expected: `wrote 200 tickets to tickets-q1` and `wrote 120 tickets to tickets-q2`

- [ ] **Step 6: Commit**

```bash
git add tools/corpus/generate.py tools/tests/test_generate.py sufra/tickets-q1/ sufra/tickets-q2/
git commit -m "Generate the Sufra ticket corpus, 200 in Q1 and 120 in Q2"
```

---

### Task 6: Corpus property verification

**Files:**
- Create: `tools/tests/test_corpus_q1.py`
- Create: `tools/tests/test_corpus_q2.py`
- Create: `tools/tests/test_safety.py`

**Interfaces:**
- Consumes: `generate.build_tickets`, `spec`.
- Produces: nothing importable. This is the facilitator's pre-flight gate — every property the workshop depends on is asserted here.

- [ ] **Step 1: Write the failing tests for Q1**

Create `tools/tests/test_corpus_q1.py`:

```python
from collections import Counter
from datetime import date, timedelta

from corpus import generate, spec

TICKETS = generate.build_tickets("q1")


def test_planted_cluster_exists_in_the_window_after_the_release():
    release = next(r for r in spec.RELEASES
                   if r.version == spec.PLANTED.release_version)
    start = date.fromisoformat(release.date)
    end = start + timedelta(days=spec.PLANTED.window_days)

    in_window = [
        t for t in TICKETS
        if t.theme_key == spec.PLANTED.theme_key
        and start <= date.fromisoformat(t.date) <= end
    ]
    assert len(in_window) >= spec.PLANTED.count, (
        f"expected at least {spec.PLANTED.count} planted tickets after "
        f"v{release.version}, found {len(in_window)} — the workshop's "
        "central discovery does not exist"
    )


def test_planted_theme_is_rare_before_the_release():
    release = next(r for r in spec.RELEASES
                   if r.version == spec.PLANTED.release_version)
    start = date.fromisoformat(release.date)
    before = [t for t in TICKETS
              if t.theme_key == spec.PLANTED.theme_key
              and date.fromisoformat(t.date) < start]
    after = [t for t in TICKETS
             if t.theme_key == spec.PLANTED.theme_key
             and date.fromisoformat(t.date) >= start]
    assert len(after) > 2 * len(before), (
        "the spike must be visible against the baseline, otherwise there is "
        f"nothing to notice ({len(before)} before, {len(after)} after)"
    )


def test_language_mix_is_in_band():
    counts = Counter(t.language for t in TICKETS)
    total = len(TICKETS)
    assert 0.45 <= counts["ar"] / total <= 0.65, counts
    assert 0.15 <= counts["en"] / total <= 0.35, counts
    assert 0.10 <= counts["mixed"] / total <= 0.30, counts


def test_the_planted_theme_appears_in_all_three_registers():
    languages = {t.language for t in TICKETS
                 if t.theme_key == spec.PLANTED.theme_key}
    assert languages == {"ar", "en", "mixed"}, (
        "the cluster must span all three registers, or grouping it is trivial"
    )


def test_corpus_contains_near_empty_tickets():
    stubs = [t for t in TICKETS if len(t.body) <= 30]
    assert stubs, "a real queue contains useless one-liners; this one does not"


def test_corpus_contains_duplicates():
    bodies = Counter(t.body for t in TICKETS)
    assert any(count > 1 for count in bodies.values()), "no duplicate tickets"


def test_theme_is_never_written_into_the_ticket():
    """Neither the theme key nor its canonical label may appear in a file.

    If it did, clustering would collapse into "group by the Subject line"
    and the exercise would be gone.
    """
    labels = {t.label_en for t in spec.THEMES.values()} | \
             {t.label_ar for t in spec.THEMES.values()}
    for ticket in TICKETS:
        rendered = generate.render(ticket)
        assert ticket.theme_key not in rendered, (
            f"SUF-{ticket.number:05d} leaks the theme key"
        )
        for label in labels:
            assert label not in rendered, (
                f"SUF-{ticket.number:05d} leaks the canonical label {label!r} — "
                "deriving the theme is the task"
            )


def test_subjects_are_not_all_identical_within_a_theme():
    """Varied subjects, or the header still gives the grouping away."""
    planted = [t for t in TICKETS if t.theme_key == spec.PLANTED.theme_key]
    assert len({t.subject for t in planted}) >= 4, (
        "the planted cluster's subjects are too uniform to be realistic"
    )
```

- [ ] **Step 2: Run it to make sure it fails or passes honestly**

```bash
cd tools && uv run pytest tests/test_corpus_q1.py -v
```

Expected: all pass. If `test_the_planted_theme_appears_in_all_three_registers` or the language-band test fails, adjust `Q1_WEIGHTS` or the planted count in `spec.py` and regenerate — do **not** weaken the test.

- [ ] **Step 3: Write the Q2 tests**

Create `tools/tests/test_corpus_q2.py`:

```python
from collections import Counter

from corpus import generate

Q1 = generate.build_tickets("q1")
Q2 = generate.build_tickets("q2")


def _dominant(tickets):
    return Counter(t.theme_key for t in tickets).most_common(1)[0][0]


def test_q2_dominant_theme_differs_from_q1():
    assert _dominant(Q2) != _dominant(Q1), (
        "if both quarters share a dominant theme, a Skill that hardcoded "
        "Q1's finding would pass the cold run and prove nothing"
    )


def test_q2_is_dominated_by_payment_problems():
    assert _dominant(Q2) == "payment_failed"


def test_q2_has_no_planted_driver_spike():
    counts = Counter(t.theme_key for t in Q2)
    assert counts["driver_lost"] < counts["payment_failed"] / 3, (
        "Q2 must not repeat Q1's signal"
    )
```

- [ ] **Step 4: Write the safety tests**

Create `tools/tests/test_safety.py`:

```python
"""No real company may appear anywhere in the corpus.

Two hundred fabricated complaints attached to a real business is
defamatory content, and this repository is public.
"""

from pathlib import Path

import pytest

REAL_BRANDS = [
    "hungerstation", "hunger station", "jahez", "جاهز", "ninja", "نينجا",
    "careem", "كريم", "uber", "أوبر", "talabat", "طلبات", "deliveroo",
    "mrsool", "مرسول", "noon", "نون", "chefz", "الشيف",
]

SUFRA = Path(__file__).resolve().parents[2] / "sufra"


def _all_text_files():
    return sorted(SUFRA.rglob("*.txt")) + sorted(SUFRA.rglob("*.md"))


@pytest.mark.parametrize("brand", REAL_BRANDS)
def test_no_real_brand_appears_in_the_corpus(brand):
    for path in _all_text_files():
        text = path.read_text(encoding="utf-8").lower()
        assert brand not in text, f"{path.name} names a real company: {brand!r}"


def test_the_corpus_actually_has_files_to_check():
    assert len(_all_text_files()) > 300, "safety scan found almost nothing to scan"
```

- [ ] **Step 5: Run the whole suite**

```bash
cd tools && uv run pytest -v
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add tools/tests/
git commit -m "Verify the corpus: planted signal, language mix, Q2 divergence, no real brands"
```

---

### Task 7: Attendee-facing seed files and the answer key

**Files:**
- Create: `sufra/CLAUDE.md`
- Create: `sufra/README.md`
- Create: `facilitator/sufra-answer-key.md`
- Test: `tools/tests/test_seed_files.py`

**Interfaces:**
- Consumes: `spec.PLANTED`, `spec.RELEASES`.
- Produces: the seed's conventions file and the facilitator answer key. Nothing later imports these; they are read by Claude and by the facilitator respectively.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_seed_files.py`:

```python
from pathlib import Path

from corpus import spec

ROOT = Path(__file__).resolve().parents[2]
SUFRA = ROOT / "sufra"
KEY = ROOT / "facilitator" / "sufra-answer-key.md"


def test_claude_md_states_the_report_format_rule():
    text = (SUFRA / "CLAUDE.md").read_text(encoding="utf-8")
    assert "themes-2025-q4.md" in text, (
        "CLAUDE.md must point at the prior report; it is the house format"
    )


def test_claude_md_does_not_leak_the_answer():
    text = (SUFRA / "CLAUDE.md").read_text(encoding="utf-8").lower()
    assert "4.2" not in text
    assert "address picker" not in text


def test_readme_does_not_leak_the_answer():
    text = (SUFRA / "README.md").read_text(encoding="utf-8").lower()
    assert "4.2" not in text
    assert "address picker" not in text


def test_answer_key_names_the_release_and_the_count():
    text = KEY.read_text(encoding="utf-8")
    assert spec.PLANTED.release_version in text
    assert str(spec.PLANTED.count) in text


def test_answer_key_is_not_inside_the_attendee_folder():
    assert not (SUFRA / "expected").exists(), (
        "the answer key must not ship inside the folder attendees open"
    )
```

- [ ] **Step 2: Run it to make sure it fails**

```bash
cd tools && uv run pytest tests/test_seed_files.py -v
```

Expected: FAIL — `FileNotFoundError` on `CLAUDE.md`

- [ ] **Step 3: Write `sufra/CLAUDE.md`**

```markdown
# CLAUDE.md — Sufra support analysis

## What this is

A quarter of customer support tickets for Sufra, a food delivery app, plus
the product changelog and last quarter's themes report. The job is to work
out what this quarter's themes are and write them up.

## The material

- `tickets-q1/` — one ticket per file. Header fields, then whatever the
  customer actually wrote.
- `tickets-q2/` — a later batch. Leave it alone unless asked.
- `context/changelog.md` — what shipped, and when.
- `context/themes-2025-q4.md` — last quarter's report.

## Language

Tickets arrive in Arabic, English, and a mix of both. The Arabic is mostly
colloquial Saudi as people type it — inconsistent spelling, missing hamzas,
no diacritics — with fusha in the longer formal complaints.

The same complaint appears in all three registers. Group by what the
customer means, never by the language they wrote it in.

## Report format

Match `context/themes-2025-q4.md` exactly: a `## Summary`, a `## Themes`
table with ticket counts and share percentages, a short prose section per
significant theme, and `## Recommendations`. Same headings, same order.

## Conventions

- Counts must be exact. Count tickets; do not estimate or sample.
- A ticket raising several issues is assigned to its dominant one, as last
  quarter's method section describes.
- Quote real ticket text when it illustrates a theme, in its original
  language. Do not translate quotes into English.
- Do not modify anything under `tickets-q1/` or `tickets-q2/`.

## What to ask me about, never assume

- Any theme that is not in last quarter's report — say why it is new.
- Anything that looks like a cause rather than a symptom.
```

- [ ] **Step 4: Write `sufra/README.md`**

```markdown
# Sufra — support ticket analysis

The working folder for the workshop.

## What's here

```
tickets-q1/    200 support tickets, one per file
tickets-q2/    120 more, from the following quarter
context/       the product changelog and last quarter's report
CLAUDE.md      conventions, and the report format to match
```

## Start

```bash
cd sufra
claude
```

Then ask for what you want. Read `CLAUDE.md` first if you want to know what
Claude already knows.

## A note on the tickets

They are messy on purpose. Some are one useless line. Some are duplicates.
They arrive in Arabic, English, and both at once. That is what a real
support queue looks like, and handling it is the point.
```

- [ ] **Step 5: Write `facilitator/sufra-answer-key.md`**

```markdown
# Sufra corpus — facilitator answer key

**Do not show this page to attendees.** It is the answer to the question
that makes the session land.

## The planted signal

`tickets-q1/` contains **23 tickets** about drivers being unable to find the
customer's address, clustered in the **21 days after v4.2 shipped on
2026-02-11**. v4.2 replaced free-text address entry with a map pin.

The correlation is the discovery. Individually the tickets read as ordinary
complaints — a lost driver is unremarkable. Only reading them against
`context/changelog.md` shows that a release caused them.

Baseline for the same theme before v4.2 is low; the test suite asserts the
spike is at least 3× the prior rate, so it is visible without being obvious.

## What a good report does

- Names driver-address problems as a distinct theme rather than folding them
  into "late delivery".
- States the count.
- Connects the cluster to v4.2 **by date**, and says so in the
  recommendations.
- Groups Arabic, English and code-switched tickets describing the same
  problem into one theme.

## What a weak report does

- Reports "delivery issues" as one large generic theme.
- Gives no counts, or estimates them.
- Never opens `context/changelog.md`.
- Treats Arabic and English tickets as separate themes.

## How to run the moment

Do not announce the signal. When the first reports appear, ask the room:

> *"Anything in here that looks like a cause rather than a symptom?"*

Wait. Someone will connect the dates. If nobody does after a minute, narrow
it: *"When did the driver complaints start? What happened that week?"*

Whoever finds it should say it, not you.

## Q2

`tickets-q2/` is dominated by **payment failures and refund delays**
following the v4.5 payment provider migration on 2026-04-14. This is
deliberately a different story from Q1 — a Skill that quietly hardcoded
"drivers can't find addresses" will produce a confidently wrong report on
Q2, which is exactly what the cold run is meant to expose.

## Regenerating

```bash
cd tools && uv run python -m corpus.generate
```

Seeded, so it reproduces byte-identically. If you change anything in
`tools/corpus/spec.py`, the counts on this page are no longer true — rerun
`uv run pytest` and update them.
```

- [ ] **Step 6: Run the tests to verify they pass**

```bash
cd tools && uv run pytest tests/test_seed_files.py -v
```

Expected: 5 passed

- [ ] **Step 7: Run the whole suite**

```bash
cd tools && uv run pytest -v
```

Expected: all pass.

- [ ] **Step 8: Commit**

```bash
git add sufra/CLAUDE.md sufra/README.md facilitator/ tools/tests/test_seed_files.py
git commit -m "Add Sufra seed conventions, README, and the facilitator answer key"
```

---

### Task 8: Facilitator dry run

The corpus is not done because tests pass. It is done when it teaches.

**Files:**
- Create: `facilitator/sufra-dry-run.md`
- Modify: `facilitator/sufra-answer-key.md` (record the observed result)

**Interfaces:**
- Consumes: the whole corpus.
- Produces: a written record of a real run, which phase 2's content is then written against.

- [ ] **Step 1: Run the task exactly as an attendee would**

```bash
cd sufra
claude
```

Ask for the quarter's themes report, matching the house format. Do not
coach it. Let it work.

- [ ] **Step 2: Check the output against the answer key**

Confirm the report names the driver-address theme separately, states a
count near 23, and connects it to v4.2 by date.

- [ ] **Step 3: Record what happened**

Create `facilitator/sufra-dry-run.md` documenting: the prompt used, whether
the signal was found unaided, how long it took, and anything that surprised
you. Phase 2's participant pages are written against this record, so it has
to be honest about what did not work.

- [ ] **Step 4: If the signal was NOT found unaided**

That is a corpus defect, not an attendee failing. Options, in order of
preference:

1. Sharpen `CLAUDE.md`'s "what to ask me about" line about causes.
2. Raise `PLANTED.count` in `spec.py`, regenerate, rerun the suite.
3. Narrow `PLANTED.window_days` so the cluster is tighter in time.

Do not fix it by putting the answer in the changelog — `test_changelog_does_not_flag_the_planted_release` exists to prevent exactly that.

- [ ] **Step 5: Commit**

```bash
git add facilitator/
git commit -m "Record the Sufra corpus dry run"
```

---

### Task 9: Sufra brand and product page

Immersion, on the AWS Wild Rydes / Unicorn Rentals principle: attendees who feel like Sufra's support lead notice more than attendees doing an exercise. It also gives beat 3's discovery something to look at — reading 23 complaints is analytical, reading them *after seeing the screen that caused them* is visceral.

Does not gate anything. Can run in parallel with Tasks 1–8.

**This lives in a separate repository**, published on GitHub Pages, so Sufra can grow into a real web app later and eventually take its own domain without dragging the workshop repo along. Nothing about it belongs on the `workshop-v2` branch.

**Repository:** `thepandanlabs/sufra` → `https://thepandanlabs.github.io/sufra/`

**Files (all in the new repo):**
- Create: `index.html`
- Create: `README.md`
- Create: `.nojekyll`
- Test: `tests/test_brand_page.py`

**Interfaces:**
- Consumes: the release list from `tools/corpus/spec.py` in the workshop repo — copied by hand, not imported. Two repos, no coupling.
- Produces: a public URL the workshop links to at beat 0. Nothing imports it.

**Honesty requirement, non-negotiable:** this is a public site for a company that does not exist. Both the page footer and the repo README must say plainly that Sufra is fictional and made for a workshop. It must never be possible for someone landing on it cold to think it is a real service — no signup field, no fake app-store links, no fake contact details, nothing that collects input.

**The one hard constraint: the address picker must not look broken.** It has to read as a sensible product decision, because that is the actual lesson — reasonable changes cause problems and only the data tells you. A mock that telegraphs the failure hands over the discovery, exactly like the Subject-line bug in Task 5.

- [ ] **Step 1: Create the repository**

Confirm with the user before creating anything public.

```bash
mkdir -p ~/dev/projects/sufra && cd ~/dev/projects/sufra
git init && git branch -M main
touch .nojekyll
gh repo create thepandanlabs/sufra --public --source=. \
  --description "Sufra — a fictional Riyadh food delivery app, built for a Claude Code workshop."
```

- [ ] **Step 2: Write the failing test**

Create `tests/test_brand_page.py` in the new repo:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"


def test_page_says_plainly_that_sufra_is_fictional():
    """A public site for a company that does not exist must say so."""
    html = PAGE.read_text(encoding="utf-8").lower()
    assert "fictional" in html, (
        "someone landing here cold must not be able to mistake this for a "
        "real service"
    )


def test_page_collects_nothing():
    html = PAGE.read_text(encoding="utf-8").lower()
    for element in ("<form", "<input", "<textarea", "mailto:"):
        assert element not in html, (
            f"{element} suggests a real service taking real details"
        )


def test_page_exists_and_is_self_contained():
    html = PAGE.read_text(encoding="utf-8")
    assert "<svg" in html, "logo should be inline SVG — no external assets"
    for external in ("http://", "https://", "cdn."):
        assert external not in html, (
            "the brand page must work offline like everything else"
        )


def test_page_is_bilingual():
    html = PAGE.read_text(encoding="utf-8")
    assert "سفرة" in html
    assert 'lang="ar"' in html or 'dir="rtl"' in html


def test_address_picker_is_not_described_as_broken():
    """The discovery must stay discoverable."""
    html = PAGE.read_text(encoding="utf-8").lower()
    for giveaway in ("broken", "bug", "issue", "problem", "sorry",
                     "known", "outage", "complaint"):
        assert giveaway not in html, (
            f"the product page says {giveaway!r} — that gives away beat 3"
        )


def test_page_does_not_use_the_workshop_palette():
    """Sufra is a company, not workshop chrome."""
    html = PAGE.read_text(encoding="utf-8").upper()
    assert "#D17D59" not in html, "Sufra needs its own brand, not the site's"
```

- [ ] **Step 3: Run it to make sure it fails**

```bash
cd ~/dev/projects/sufra && uv run --with pytest pytest tests/ -v
```

Expected: FAIL — `FileNotFoundError` on `index.html`

- [ ] **Step 4: Design `index.html`**

**REQUIRED SUB-SKILL: invoke `frontend-design` before writing this page.** This is the one asset in phase 1 that is judged on how it looks. It should stand up as a real company's site — the kind of thing someone would screenshot without knowing it was made for a workshop.

Design direction:

- **Bilingual by construction, not translated.** Arabic and Latin share the lockup. The RTL half is laid out as RTL, not mirrored as an afterthought. Getting this right is most of what will make a Riyadh room believe it.
- **Its own palette, deliberately far from `#D17D59`.** The reference below uses deep green and sand; take it further if something better presents itself. Warm, food-adjacent, confident. Not another orange startup.
- **Typographic confidence over decoration.** Resist geometric-pattern clichés for Gulf brands. Strong type, generous space, restraint.
- **The two phone mocks are the centrepiece** — English and Arabic side by side, both showing the address picker. That pairing is what beat 3 calls back to.
- **Self-contained.** Inline SVG, inline CSS, no external anything. Tested.
- **Motion, if any, is subtle.** A static page that feels alive beats one that performs.

The block below is a **floor, not a target** — a working starting point that already passes the tests. Exceed it.

The one thing that must not change: nothing on the page may hint that the address picker caused a problem. It reads as a straightforward product improvement, because that is what it looked like at the time.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sufra — سفرة</title>
<style>
  :root {
    --green: #1B4332; --green-light: #2D6A4F; --sand: #E9C46A;
    --cream: #FDFBF7; --ink: #1A1A18; --muted: #6B7280;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--cream); color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
  }
  header {
    background: var(--green); color: var(--cream);
    padding: 1.25rem 2rem; display: flex; align-items: center; gap: 0.75rem;
  }
  .wordmark { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; }
  .wordmark-ar { font-size: 1.25rem; opacity: 0.75; }
  .hero { padding: 4rem 2rem; max-width: 60rem; margin: 0 auto; text-align: center; }
  .hero h1 { font-size: 2.5rem; margin: 0 0 0.75rem; letter-spacing: -0.03em; }
  .hero p { font-size: 1.15rem; color: var(--muted); margin: 0 auto; max-width: 34rem; }
  .phones {
    display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap;
    padding: 2rem; max-width: 60rem; margin: 0 auto;
  }
  .phone {
    width: 15rem; border: 1px solid #E5E0D8; border-radius: 1.5rem;
    background: #fff; padding: 1rem; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
  }
  .phone h3 { font-size: 0.8125rem; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--muted); margin: 0 0 0.75rem; }
  .map {
    height: 8rem; border-radius: 0.75rem; position: relative;
    background:
      repeating-linear-gradient(0deg, #EDF2EE 0 1px, transparent 1px 28px),
      repeating-linear-gradient(90deg, #EDF2EE 0 1px, transparent 1px 28px),
      #F6F8F6;
  }
  .pin {
    position: absolute; left: 50%; top: 46%; width: 14px; height: 14px;
    margin: -7px 0 0 -7px; border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg); background: var(--green);
  }
  .field {
    margin-top: 0.75rem; border: 1px solid #E5E0D8; border-radius: 0.5rem;
    padding: 0.5rem 0.625rem; font-size: 0.8125rem; color: var(--ink);
  }
  .field span { display: block; font-size: 0.6875rem; color: var(--muted); }
  .btn {
    margin-top: 0.75rem; background: var(--green); color: var(--cream);
    border-radius: 0.5rem; padding: 0.5rem; text-align: center;
    font-size: 0.8125rem; font-weight: 600;
  }
  .rtl { direction: rtl; text-align: right; }
  section.notes { max-width: 42rem; margin: 0 auto; padding: 2rem; }
  section.notes h2 { font-size: 1.125rem; }
  .rel { border-left: 3px solid var(--sand); padding-left: 1rem; margin: 1rem 0; }
  .rel strong { display: block; }
  .rel span { color: var(--muted); font-size: 0.875rem; }
  footer { padding: 2rem; text-align: center; color: var(--muted); font-size: 0.8125rem; }
</style>
</head>
<body>

<header>
  <svg width="32" height="32" viewBox="0 0 32 32" aria-label="Sufra">
    <circle cx="16" cy="16" r="14" fill="none" stroke="#E9C46A" stroke-width="1.5"/>
    <circle cx="16" cy="16" r="7" fill="#E9C46A"/>
  </svg>
  <span class="wordmark">sufra</span>
  <span class="wordmark-ar" lang="ar" dir="rtl">سفرة</span>
</header>

<div class="hero">
  <h1>Dinner, on its way.</h1>
  <p>Order from the restaurants near you across Riyadh, Jeddah and Dammam.
     Track it to your door.</p>
</div>

<div class="phones">
  <div class="phone">
    <h3>Set your address</h3>
    <div class="map"><div class="pin"></div></div>
    <div class="field"><span>Delivering to</span>An Narjis, Riyadh</div>
    <div class="btn">Confirm location</div>
  </div>

  <div class="phone rtl" lang="ar" dir="rtl">
    <h3>حدد موقعك</h3>
    <div class="map"><div class="pin"></div></div>
    <div class="field"><span>التوصيل إلى</span>النرجس، الرياض</div>
    <div class="btn">تأكيد الموقع</div>
  </div>
</div>

<section class="notes">
  <h2>What's new</h2>

  <div class="rel">
    <strong>Group orders</strong>
    <span>Everyone adds to one basket. Split it however you like.</span>
  </div>
  <div class="rel">
    <strong>Faster checkout</strong>
    <span>Card payments move to our new processor.</span>
  </div>
  <div class="rel">
    <strong>Pin your location</strong>
    <span>Drop a pin on the map instead of typing your address. Your saved
          addresses come across automatically.</span>
  </div>
  <div class="rel">
    <strong>Loyalty at checkout</strong>
    <span>See your points before you pay.</span>
  </div>
</section>

<footer>Sufra is a fictional company, invented for a workshop.</footer>

</body>
</html>
```

Note the "Pin your location" entry reads as an improvement, because that is what it was. Nothing on this page hints at what happened next.

- [ ] **Step 5: Run the tests to verify they pass**

```bash
cd ~/dev/projects/sufra && uv run --with pytest pytest tests/ -v
```

Expected: all passed

- [ ] **Step 6: Look at it, in both directions**

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080/sufra-co/`. Check it at desktop and phone widths, and read the Arabic half as an Arabic reader would — right to left, starting top-right.

The bar: it looks like a company's site, not a workshop asset. If it reads as a prop, the immersion is not doing its job and the page is not done. Screenshot it; if you would not post that screenshot, iterate.

- [ ] **Step 7: Write the README, commit, and publish**

`README.md` must open by saying Sufra is fictional and why it exists.

```bash
cd ~/dev/projects/sufra
git add -A
git commit -m "Sufra — fictional Riyadh food delivery app for the Claude Code workshop"
git push -u origin main
gh api -X POST repos/thepandanlabs/sufra/pages -f 'source[branch]=main' -f 'source[path]=/'
```

Then confirm `https://thepandanlabs.github.io/sufra/` renders, and that the fictional-company notice is visible without scrolling to the very bottom.

---

## Definition of done for phase 1

- `cd tools && uv run pytest -v` passes in full.
- `sufra/tickets-q1/` holds 200 files and `sufra/tickets-q2/` holds 120.
- Regenerating produces no git diff.
- A facilitator dry run found the v4.2 correlation without coaching, and that run is written down.
- No real company is named anywhere under `sufra/`.
- Task 9 is tracked separately: the Sufra site lives in `thepandanlabs/sufra`, not on this branch. Phase 1 is done without it; it is done when the page is live, self-contained, says plainly that Sufra is fictional, and does not telegraph the v4.2 discovery.
- Everything is on `workshop-v2`. Nothing is on `main`.

Phase 2 (workshop content) is written against the dry-run record, not against this plan's assumptions.
