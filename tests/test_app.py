import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'test-artifacts'
OUT.mkdir(exist_ok=True)
HTML=(ROOT/'Stride.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1440,'height':1050}, device_scale_factor=1, timezone_id='America/Los_Angeles')
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.evaluate("Object.defineProperty(window, 'localStorage', {value: {data:{}, getItem(k){return this.data[k]||null}, setItem(k,v){this.data[k]=v}, removeItem(k){delete this.data[k]}}})")
    page.set_content(HTML,wait_until='load')
    page.screenshot(path=str(OUT/'stride-desktop.png'),full_page=True)
    print('TITLE:',page.title())
    print('BODY:',page.locator('main').inner_text()[:1200])
    print('ERRORS:',errors)
    page.locator('.sidebar [data-view="week"]').click()
    page.screenshot(path=str(OUT/'stride-week.png'),full_page=True)
    print('WEEK ERRORS:',errors)
    # Capture future week with useful calendar content, maintaining truthful date indicator.
    page.locator('[data-action="week-next"]').click()
    page.screenshot(path=str(OUT/'stride-week-next.png'),full_page=True)
    for name in ['queue','courses','sources']:
        page.locator('.sidebar [data-view="'+name+'"]').click()
        page.screenshot(path=str(OUT/f'stride-{name}.png'),full_page=True)
    print('RENDER ERRORS:',errors)
    print('CHECKS',page.evaluate('JSON.stringify({day:Stride.nowDate(),fri:Stride.eventsOn("2026-09-11").map(x=>[x.title,x.start,x.end,x.mode]),holiday:Stride.eventsOn("2026-09-07"),warnings:Stride.semesterWarnings().slice(0,10)})'))
    # Mobile in fresh independent storage.
    mobile=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True,timezone_id='America/Los_Angeles')
    mp=mobile.new_page();mp.on('pageerror',lambda error:errors.append('MOBILE: '+str(error)))
    mp.evaluate("Object.defineProperty(window, 'localStorage', {value: {data:{}, getItem(k){return this.data[k]||null}, setItem(k,v){this.data[k]=v}, removeItem(k){delete this.data[k]}}})")
    mp.set_content(HTML,wait_until='load')
    mp.screenshot(path=str(OUT/'stride-mobile.png'),full_page=True)
    print('MOBILE WIDTH:',mp.evaluate('({scroll:document.documentElement.scrollWidth,width:innerWidth})'))
    for name in ['week','queue','sources']:
        mp.locator('.mobile-nav [data-view="'+name+'"]').click()
        print(name,mp.evaluate('({scroll:document.documentElement.scrollWidth,width:innerWidth})'))
    print('FINAL ERRORS:',errors)
    browser.close()
