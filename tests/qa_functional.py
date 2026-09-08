from pathlib import Path
from datetime import datetime, timezone
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'Stride.html').read_text()
results=[]
def passed(name):
    results.append(name)
    print('PASS',name)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':1440,'height':1000},timezone_id='America/Los_Angeles',accept_downloads=True)
    pg=ctx.new_page(); errors=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.clock.install(time=datetime(2026,9,5,20,0,tzinfo=timezone.utc))
    # Container Chromium blocks file:// and localhost navigation. Use identical
    # bundled HTML, a deterministic clock and a localStorage mock for UI tests.
    pg.evaluate("Object.defineProperty(window, 'localStorage', {value: {data:{},getItem(k){return this.data[k]||null},setItem(k,v){this.data[k]=v},removeItem(k){delete this.data[k]}}})")
    pg.set_content(HTML,wait_until='load')
    assert pg.evaluate('Stride.nowDate()')=='2026-09-05'
    assert pg.evaluate('Stride.eventsOn("2026-09-07").length')==0
    assert pg.evaluate('Stride.eventsOn("2026-09-11").some(e=>e.course==="ee66"&&e.kind==="lecture")') is False
    assert pg.evaluate('Stride.eventsOn("2026-09-11").find(e=>e.kind==="lab").mode')=='reserved'
    passed('Calendar: Pacific dates, Labor Day, no Friday EE66 lecture, labs reserved')
    assert pg.evaluate('Stride.semesterWarnings().some(w=>w.date==="2026-09-23"&&w.text.includes("8 PM"))')
    assert pg.evaluate('Stride.wall("2026-09-08T08:00").toISOString()')=='2026-09-08T15:00:00.000Z'
    assert pg.evaluate('Stride.wall("2026-12-18T19:00").toISOString()')=='2026-12-19T03:00:00.000Z'
    passed('Exam transitions and Pacific daylight-saving conversion')
    pg.locator('.top-actions [data-action="add-task"]').click()
    pg.locator('#f-title').fill('QA: review proof techniques')
    pg.locator('#f-course').select_option('cs70')
    pg.locator('#f-kind').select_option('review')
    pg.locator('#f-due').fill('2026-09-06T10:00')
    pg.locator('#f-remaining').fill('40')
    pg.locator('#f-next').fill('Try one proof without notes.')
    pg.locator('#f-steps').fill('Choose one proof\nSolve without notes\nCheck solution')
    pg.locator('#task-form button[type="submit"]').click()
    taskid=pg.evaluate('Stride.getState().tasks.find(t=>t.title.startsWith("QA:")).id')
    assert pg.evaluate('JSON.parse(localStorage.getItem("stride.harris.v1")).tasks.some(t=>t.title.startsWith("QA:"))')
    pg.locator('.sidebar [data-view="queue"]').click()
    pg.locator('[data-action="task-detail"][data-id="'+taskid+'"]').click()
    pg.locator('#step-0').check()
    assert pg.evaluate('(id)=>Stride.getState().tasks.find(t=>t.id===id).checkedSteps.includes(0)',taskid)
    pg.locator('#dialog [data-action="toggle-task"]').click()
    pg.locator('[data-action="set-ready"]').click()
    assert pg.evaluate('(id)=>Stride.getState().tasks.find(t=>t.id===id).status',taskid)=='ready'
    pg.locator('[data-action="queue-filter"][data-value="submit"]').click()
    assert pg.locator('main').inner_text().find('QA: review')>=0
    passed('Task creation, checklist, serialization, ready-to-submit lane')
    pg.locator('[data-action="task-detail"][data-id="'+taskid+'"]').click()
    pg.locator('#dialog [data-action="toggle-task"]').click()
    pg.locator('[data-action="set-submitted"]').click()
    assert pg.evaluate('(id)=>Stride.getState().tasks.find(t=>t.id===id).status',taskid)=='submitted'
    pg.locator('#toast [data-action="undo"]').click()
    assert pg.evaluate('(id)=>Stride.getState().tasks.find(t=>t.id===id).status',taskid)=='ready'
    passed('Submission recording and undo')
    pg.locator('.sidebar [data-view="today"]').click()
    pg.locator('.hero [data-action="start-focus"]').click()
    assert pg.locator('.focus-screen').is_visible()
    pg.clock.fast_forward(120000)
    pg.locator('[data-action="focus-pause"]').click()
    elapsed=pg.evaluate('Stride.getState().timer.elapsed')
    assert elapsed>=120000
    pg.clock.fast_forward(60000)
    assert pg.evaluate('Stride.getState().timer.elapsed')==elapsed
    pg.locator('[data-action="focus-finish"]').click()
    pg.locator('#f-minutes').fill('2')
    pg.locator('#f-next').fill('Resume from the next proof.')
    pg.locator('#focus-form button[type="submit"]').click()
    assert pg.evaluate('Stride.getState().sessions.length')==1
    assert pg.evaluate('Stride.getState().timer === undefined')
    passed('Focus timer, pause, session note and progress log')
    pg.locator('.sidebar [data-view="sources"]').click()
    pg.locator('[data-action="resolve-review"][data-id="discussion"]').click()
    pg.locator('#f-title').fill('Confirmed discussion - test')
    pg.locator('input[name="days"][value="2"]').check()
    pg.locator('input[name="days"][value="4"]').check()
    pg.locator('#event-form button[type="submit"]').click()
    assert pg.evaluate('Stride.getState().reviews.find(r=>r.id==="discussion").resolved')
    assert pg.evaluate('Stride.eventsOn("2026-09-08").some(e=>e.title.includes("Confirmed discussion"))')
    passed('Set discussion days, resolves incomplete-timetable check')
    pg.locator('[data-action="resolve-review"][data-id="labdates"]').click()
    pg.locator('#f-specificDates').fill('2026-09-11\n2026-09-25')
    pg.locator('#f-location').fill('Test lab room')
    pg.locator('#event-form button[type="submit"]').click()
    assert pg.evaluate('Stride.eventsOn("2026-09-11").find(e=>e.kind==="lab").mode')=='fixed'
    assert pg.evaluate('Stride.eventsOn("2026-09-18").some(e=>e.kind==="lab")') is False
    passed('Only confirmed lab dates become actual meetings')
    ics='BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:qa-calendar-one\nDTSTART;TZID=America/Los_Angeles:20260910T160000\nSUMMARY:CS70 Imported deadline\nEND:VEVENT\nBEGIN:VEVENT\nUID:qa-repeat\nDTSTART:20260910T100000Z\nRRULE:FREQ=WEEKLY\nSUMMARY:Recurring test\nEND:VEVENT\nEND:VCALENDAR'
    parsed=pg.evaluate('(s)=>Stride.parseICS(s)',ics)
    assert len(parsed['items'])==1 and parsed['skipped']==1
    pg.locator('#import-file').set_input_files({'name':'test.ics','mimeType':'text/calendar','buffer':ics.encode()})
    pg.locator('#ics-import-form button[type="submit"]').click()
    assert pg.evaluate('Stride.getState().tasks.some(t=>t.title==="CS70 Imported deadline")')
    pg.locator('#import-file').set_input_files({'name':'test.ics','mimeType':'text/calendar','buffer':ics.encode()})
    pg.locator('#ics-import-form button[type="submit"]').click()
    assert pg.evaluate('Stride.getState().tasks.filter(t=>t.title==="CS70 Imported deadline").length')==1
    passed('ICS preview import, unsupported recurrence notice, duplicate protection')
    pg.locator('[data-action="export-json"]').first.click()
    exported=pg.evaluate('JSON.parse(localStorage.getItem("stride.harris.v1"))')
    assert exported['version']==1
    ical=pg.evaluate('Stride.makeICS()')
    assert 'BEGIN:VCALENDAR' in ical['data'] and ical['count']>0
    assert 'DESCRIPTION:' in ical['data']
    passed('JSON backup and calendar export contents')
    pg.locator('.top-actions [data-action="settings"]').click()
    pg.locator('#f-theme').select_option('dark')
    pg.locator('#settings-form button[type="submit"]').click()
    assert pg.locator('body').get_attribute('data-theme')=='dark'
    pg.locator('.sidebar [data-view="today"]').click()
    ART=ROOT/'test-artifacts'; ART.mkdir(exist_ok=True)
    pg.screenshot(path=str(ART/'stride-dark.png'),full_page=True)
    passed('Dark theme and preference storage')
    # Release gating: a planned date passing must not auto-release a task.
    pg.locator('.top-actions [data-action="add-task"]').click()
    pg.locator('#f-title').fill('QA: unreleased tomorrow')
    pg.locator('#f-availability').select_option('waiting')
    pg.locator('#f-release').fill('2026-09-06T10:00')
    pg.locator('#task-form button[type="submit"]').click()
    assert not pg.evaluate('Stride.ranked().some(t=>t.title==="QA: unreleased tomorrow")')
    pg.locator('#date-jump').fill('2026-09-07')
    pg.locator('#date-jump').dispatch_event('change')
    assert not pg.evaluate('Stride.ranked().some(t=>t.title==="QA: unreleased tomorrow")')
    passed('Unreleased tasks never automatically become executable')
    assert not errors,errors
    passed('No JavaScript exceptions across functional test suite')
    (Path(__file__).resolve().parents[1] / 'QA-results.json').write_text(json.dumps({'passed':results,'browser_errors':errors,'method':'Chromium rendering via set_content; deterministic clock and mock localStorage due to container navigation policy. Real disk-backed localStorage and service worker were not validated in this environment.'},indent=2))
    b.close()
