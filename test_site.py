import functools,http.server,threading,os,pathlib,json,time
from playwright.sync_api import sync_playwright,expect
root=pathlib.Path(__file__).parent
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=os.environ.get('TEST_URL',f'http://127.0.0.1:{server.server_port}/')
timings=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 errors=[]
 for width in [390,1200]:
  context=b.new_context(viewport={'width':width,'height':900})
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url)
  assert page.title()=='Parcel Arrival — Track your parcel'
  assert page.locator('input').count()==1
  assert page.locator('#result').is_hidden()
  page.locator('input').fill('YSL-AU-20261117-48291')
  page.evaluate("window.submitTime=0; window.revealTime=0;document.querySelector('form').addEventListener('submit',()=>window.submitTime=performance.now());new MutationObserver(()=>{if(!document.querySelector('#result').hidden)window.revealTime=performance.now()}).observe(document.querySelector('#result'),{attributes:true,attributeFilter:['hidden']})")
  page.locator('button').click()
  assert page.locator('#loading').is_visible()
  assert page.locator('#result').is_hidden()
  assert page.locator('button').is_disabled()
  page.screenshot(path=str(root/f'check-loading-{width}.png'),full_page=True)
  expect(page.locator('#result')).to_be_visible(timeout=4000)
  elapsed=page.evaluate('revealTime-submitTime');assert 1450<=elapsed<3000,elapsed;timings.append(round(elapsed))
  assert page.locator('#loading').is_hidden()
  assert page.locator('button').is_enabled()
  assert page.locator('.confirmation h2').inner_text()=='Your order is on the way!'
  assert page.locator('.thanks').inner_text()=='Thank you for your order.'
  page.locator('#photo').evaluate('(img)=>img.decode()')
  assert page.locator('#photo').evaluate('(img)=>img.naturalWidth>0')
  assert page.locator('.eta').inner_text()=='Monday, 23 November 2026'
  assert page.locator('.number').inner_text()=='YSL-AU-20261117-48291'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(root/f'check-{width}.png'),full_page=True)
  page.locator('input').fill('UNKNOWN');assert page.locator('#result').is_hidden()
  page.locator('button').click();expect(page.locator('#message')).to_contain_text('not found',timeout=4000)
  page.locator('input').fill('ysl-au-20261117-48291');page.locator('button').click()
  expect(page.locator('#message')).to_contain_text('not found',timeout=4000);assert page.locator('#result').is_hidden()
  page.locator('input').fill('YSL-AU-20261117-48291');page.locator('button').click()
  page.locator('input').fill('changed-during-loading');page.wait_for_timeout(1700)
  assert page.locator('#result').is_hidden() and page.locator('#loading').is_hidden()
  assert page.locator('button').is_enabled()
  context.close()
 assert not errors,errors
 b.close()
server.shutdown()
print(json.dumps({'url':url,'delay_ms':timings,'passed':['mobile and desktop','loading indicator and disabled button','1.5 second delay','sender confirmation copy','photo and ETA','unknown ID','literal ID preservation','cancel stale result on input change','no overflow or JS errors']}))
