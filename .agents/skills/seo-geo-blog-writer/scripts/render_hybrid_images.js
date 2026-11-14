#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

function usage() {
  console.error('Usage: node render_hybrid_images.js <composition.html> <output-directory>');
}

async function main() {
  const [, , htmlArg, outputArg] = process.argv;
  if (!htmlArg || !outputArg) {
    usage();
    process.exit(2);
  }

  const htmlPath = path.resolve(htmlArg);
  const outputDir = path.resolve(outputArg);

  if (!fs.existsSync(htmlPath)) {
    throw new Error(`Composition not found: ${htmlPath}`);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  let chromium;
  try {
    ({ chromium } = require('playwright'));
  } catch (error) {
    throw new Error('Playwright is required. Install it with: npm install playwright');
  }

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({
      viewport: { width: 1280, height: 900 },
      deviceScaleFactor: 1,
    });

    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all(
        [...document.images].map((image) =>
          image.complete
            ? Promise.resolve()
            : new Promise((resolve) => {
                image.onload = resolve;
                image.onerror = resolve;
              })
        )
      );
    });

    const artboards = page.locator('.art');
    const count = await artboards.count();
    if (!count) {
      throw new Error('No elements with class .art were found.');
    }

    for (let index = 0; index < count; index += 1) {
      const artboard = artboards.nth(index);
      const outputName =
        (await artboard.getAttribute('data-output')) ||
        `${(await artboard.getAttribute('id')) || `image-${index + 1}`}.png`;
      const box = await artboard.boundingBox();

      if (!box || Math.round(box.width) !== 1200 || Math.round(box.height) !== 675) {
        throw new Error(`${outputName} must render at 1200x675px.`);
      }

      const destination = path.join(outputDir, outputName);
      await artboard.screenshot({ path: destination });
      console.log(`${outputName}: 1200x675`);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
