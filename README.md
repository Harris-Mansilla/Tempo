# Stride
## Your next clear step.

A personal, local-first execution planner for Harris's four-course Berkeley Fall 2026 semester. It is a working app, not a static mockup. No package installation or API key is required.


## License and use

**Tempo is public-source, proprietary software — not open source.**

Copyright © 2026 Harris Mansilla. All rights reserved. The source is published so the project can be inspected and discussed; public visibility is **not** permission to reuse, redistribute, modify, host, sublicense, sell, or commercially exploit the software. See [`LICENSE`](LICENSE) for the full notice. For licensing or permission, contact the copyright holder through GitHub.

## Open it

**Easiest:** open `Stride.html` in a desktop browser. Keep the file in a stable location and use the same browser. The entire portable app is in that one file; it does not load scripts, fonts, or libraries from a CDN.

A file preview inside a chat or phone's file viewer may not execute JavaScript. Use an actual browser. For normal phone access, host the included web app on an HTTPS site, then open that URL. Connecting the suggested deployment service is a separate step; this delivery has not been deployed.

**Source version:** open `index.html`, with `styles.css`, `data.js`, `app.js`, and `icon.svg` alongside it. Alternatively, with Python 3 installed, run:

```sh
python serve.py
```

That starts a local-only server on `http://127.0.0.1:8000` and opens your browser. Ctrl+C stops it. It is not a public deployment or a background monitoring service.

## Start with these three things

1. Open **Sources & checks**. Enter your exact EE66 discussion days/time, then the actual dates on which your Friday 3-6 PM lab meets. A reserved Friday block is not proof that a lab meets every week.
2. Open **Work queue** and reconcile any work you have completed since the initial snapshot. Update each large task's remaining-time estimate. Those estimates are starting values, not predictions about your ability.
3. Return to **Today**, choose the time and energy you have, and start one focus block. Finish by recording the next concrete step. You do not have to finish the whole assignment.

## The five views

| View | What it does |
| --- | --- |
| Today | Uses Berkeley time, deadlines, availability, energy, recorded commitments, and your stop time to suggest a next task. Offers a bounded day plan and a next-step explanation. |
| Your week | Separates fixed meetings, movable study, and unconfirmed reserved slots. Includes exams, explicit quiz dates, and transition warnings. Switch to Agenda on a phone. |
| Work queue | Separates available work, unreleased work, items needing a check, and completed work. Search, filter by course, edit, snooze, and track individual steps. |
| Courses | Your four active courses, meeting summaries, current work, and source links. EE64 is excluded. |
| Sources & checks | Keeps unresolved details visible, records your verification notes, and handles calendar imports, backups, and new-task capture. |

### Completed is not submitted

For a homework or project, use **Ready to submit** when the work itself is finished. Only use **Submitted** after uploading through the actual course service. Stride never submits work, records real attendance, emails staff, or changes enrollment. All status buttons change only this local planner.

### Flexible is not compulsory

CS61B's Monday/Wednesday/Friday 2-3 PM blocks are movable self-study defaults. They are not treated as extra attendance requirements. EE66 Friday 3-6 PM is your chosen reservation; its exact lab dates remain visibly unconfirmed until you enter them. Missing discussion details are not silently replaced by guessed times.

### Released is not scheduled to release

A future calendar row does not mean you can work on an assignment. Unreleased items stay out of the active queue, even after an expected release date passes; that transition creates a verification need, not a fake release. You can change the release state after checking the real source.

### Math reading

The app creates preparation tasks before recorded Math53 Tuesday/Thursday lectures. It does not invent the assigned textbook sections. Confirm and enter the sections for each lecture, then record completion. Holidays are excluded from the initial term calendar.

### Focus mode

Choose 25, 50, or 90 minutes, or let the app shorten a block to fit your next meeting or bedtime. Pause, resume, minimize, and log a session. Time spent does not automatically mark an assignment complete. Session notes preserve where to restart. The timer is calculated from timestamps, but it does not provide a reliable closed-app alarm or a push notification.

## Import, export, and memory

Changes are saved in this browser's local storage, when available. That is **not** ChatGPT memory or cloud storage. Clearing site data, using private browsing, moving the HTML file, or changing browser/device may lose access to that copy of your records.

Use **Sources & checks -> Back up your workspace** regularly. The JSON file preserves the full local state. Import it to restore another browser. A visible warning appears when local storage is unavailable; in that case, export before closing.

Calendar import accepts ordinary single-event `.ics` entries and previews them before adding them. It is not a live calendar subscription. Recurring rules and unsupported timezone formats are reported rather than silently expanded. Imported data needs source verification.

Calendar export includes recorded confirmed/from-your-records meetings and deadlines. It excludes unconfirmed reservations and verify-only details. Flexible study is marked transparent. It creates a one-time `.ics` file, not an automatically updating calendar feed. Times are converted from Berkeley time to UTC, including the fall daylight-saving change.

## Data freshness and limits

The initial snapshot was assembled on **September 5, 2026**, from your explicit choices and screenshots, the current official CS61B and CS70 websites, and selected Berkeley email receipts/release notices. Earlier unverified assertions were not promoted into facts.

This app is **not connected to bCourses, Ed, Gradescope, Gmail, or CalCentral**. The tools used to prepare its initial data are not embedded in it. Opening a course link does not give the app access to that site. There is no hidden scraper, account connection, scheduled refresh, language-model API, or autonomous background agent. Hosted deployment alone does not add those features.

The planner makes next-step decisions locally. To keep those decisions useful, briefly check the real course sources and capture new work or changed requirements using Add task, Edit, or calendar import. Receipt-based status and user-reported status have separate provenance; missing receipts are not treated as proof of missing work. The app never guarantees that no hidden or newly published deadline exists.

The initial verification list includes:

- Your actual EE66 discussion placement.
- EE66 lab meeting dates and room.
- EE66 midterm dates.
- Whether the mini-vitamin reminder refers to the previously reported submission.
- CS70 HW0 feedback requirements.

Math53's carried-forward HW2 cutoff is marked for verification. Exact future readings are not prefilled from another year's course. The app checks recorded exam conflicts and tight transitions but cannot certify a complete conflict-free semester while required details remain missing.

## Optional hosting

Publish `index.html`, `styles.css`, `data.js`, `app.js`, `icon.svg`, `manifest.webmanifest`, and `sw.js` together on an HTTPS static host. The multi-file version includes an offline service worker and app manifest. Mobile installation behavior varies by browser. The portable `Stride.html` intentionally disables service-worker registration and needs no companion files.

The seeded schedule is personal context. Review `data.js` before making the source public. Use access-controlled hosting if you do not want the initial schedule accessible to other people. Neither local nor hosted mode contains a password, student ID, token, or connected mailbox. Hosting does not provide cross-device data sync; backups still matter.

## Keyboard shortcuts

- `1` through `5`: Today, Week, Queue, Courses, Checks.
- `N`: add a task.
- `/`: search work.
- `Space`: pause/resume while focus mode is open.
- `Escape`: close a dialog or minimize focus.

## Source and development

- `data.js`: initial personal data and provenance.
- `app.js`: ranking, calendar, focus, editing, persistence, and import/export logic.
- `styles.css`: responsive light/dark interface.
- `build.py`: rebuilds the portable file in the parent directory.
- `QA-results.json`: test results and environment limitations.
- `tests/`: optional Playwright test scripts; not needed to use the app.

To rebuild the portable file:

```sh
python build.py
```

Functional tests covered task creation, checklists, submission state, undo, focus logging, discussion placement, date-specific labs, release gating, imports, exports, Pacific daylight-saving conversion, exam transitions, dark mode, and JavaScript errors. Desktop and 390px mobile layouts were inspected. Test rendering used Chromium with mocked local storage because the build environment blocks local navigation; real browser disk persistence, mobile installation, and hosted offline operation were not end-to-end validated here.
