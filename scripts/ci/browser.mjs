import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { chromium } from 'playwright'
const base = process.env.CI_BASE_URL
for (const route of ['/', '/index.html', '/README.md', '/up', '/deployment.json']) {
  const response = await fetch(base + route)
  assert.equal(response.status, 200, route)
  const body = await response.text()
  if (route === '/' || route === '/index.html') assert.equal(body, await readFile('index.html', 'utf8'))
  if (route === '/README.md') assert.equal(body, await readFile('README.md', 'utf8'))
  if (route === '/up') assert.equal(body.trim(), 'ok')
  if (route === '/deployment.json') assert.equal(JSON.parse(body).application, 'paper-grid')
}
assert.equal((await fetch(base + '/missing-ci-route')).status, 404)
const browser = await chromium.launch()
try {
  const page = await browser.newPage({ acceptDownloads: true })
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort())
  await page.goto(base, {waitUntil: 'networkidle'})
  assert.ok(await page.locator('#paper-wrap svg circle').count() > 0, 'dot grid renders')
  await page.locator('#gridType').selectOption('blank')
  assert.equal(await page.locator('#paper-wrap svg circle').count(), 0, 'blank grid removes dots')
  await page.locator('#gridType').selectOption('dots')
  assert.ok(await page.locator('#paper-wrap svg circle').count() > 0)
  const downloadPromise = page.waitForEvent('download')
  await page.locator('#downloadBtn').click()
  const download = await downloadPromise
  const svg = await readFile(await download.path(), 'utf8')
  assert.match(svg, /<svg/)
  assert.match(svg, /<circle/)
  assert.deepEqual(errors, [])
  console.log('PASS: image routes, exact source bytes, grid switching and SVG download')
} finally { await browser.close() }

// Temporary controlled gate probe: application bytes are unchanged; production must stay put.
assert.fail('Intentional CI gate verification: this test-only commit must never deploy')
