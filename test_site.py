import functools,http.server,threading,os,pathlib,json
from playwright.sync_api import sync_playwright
root=pathlib.Path(__file__).parent
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=os.environ.get('TEST_URL',f'http://127.0.0.1:{server.server_port}/')
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 errors=[]
 for width in [390,1200]:
  context=b.new_context(viewport={'width':width,'height':850})
  page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url)
  assert page.title()=='Track My Parcel'
  assert page.locator('input').count()==1
  assert page.locator('#result').is_hidden()
  page.locator('input').fill('YSL-AU-20261117-48291');page.locator('button').click()
  assert page.locator('#result').is_visible()
  page.locator('#photo').evaluate('(img)=>img.decode()')
  assert page.locator('#photo').evaluate('(img)=>img.naturalWidth>0')
  assert page.locator('.eta').inner_text()=='Monday, 23 November 2026'
  assert page.locator('.number').inner_text()=='YSL-AU-20261117-48291'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(root/f'check-{width}.png'),full_page=True)
  page.locator('input').fill('UNKNOWN');assert page.locator('#result').is_hidden()
  page.locator('button').click();assert 'not found' in page.locator('#message').inner_text()
  page.locator('input').fill('ysl-au-20261117-48291');page.locator('button').click();assert page.locator('#result').is_hidden()
  context.close()
 assert not errors,errors
 b.close()
server.shutdown()
print(json.dumps({'url':url,'passed':['desktop and mobile','one input, clean initial state','exact number lookup','photo decoded','correct ETA','no overflow','unknown number','literal ID preservation','no JS errors']}))
