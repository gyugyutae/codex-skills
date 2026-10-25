# Bundled 2026-10 RISE example

Read the bundled original form for this particular program. These are not universal HWP rules.

- Period: 2026-10-01 (Thursday) through 2026-10-28 (Wednesday).
- Recognized window: 09:00–22:00; exclude 12:00–13:00; at most four hours per day; monthly maximum 20 hours.
- The form requires two evidence images **per activity session**, not two for the whole report.
- Individual activity content/photos must not be copied from a teammate.
- Submit the requested activity plan and result report as one HWP and one PDF. Budget form 3 is omitted when there was no spending, as explicitly directed in this case.
- User's course conflicts for this month: Monday 10:00–13:00 and 16:00–18:00; Tuesday 11:00–13:00; Wednesday 14:00–16:00; Thursday 14:00–16:00. Reconfirm for a later term.
- User confirmed about 20 hours of October work, but did not recall session dates/times. The example leaves those fields blank. Do not turn the five topic sections into five four-hour sessions without evidence.
- September text covered Play release preparation: disclosure, permissions, AAB, store assets and closed-test preparation. October focuses on refactoring and own-device/emulator behavior checks. Closed testing was registered, with no external participants as of 2026-10-25; this is not a public Play release.
- Repository `gyugyutae/cuee` contains 2026-10-03 refactoring/validation notes. Those notes report 4,660→4,177 app Kotlin lines and 1,115→631 service lines, measured against the then-current working tree, including comments/blank lines. A commit diff alone does not reproduce that baseline. No project token savings percentage was measured.
- New screenshots were captured on 2026-10-25. Actual CUEE debug APK ran on an Android 35 emulator; the counterpart was `mock-korail`, not live Korail. Two journeys reached matching results, and 109 unit tests passed. This does not establish external user testing, voice recognition quality, a full live booking, or payment success.
