// Print an HTML file to an A4 PDF with a footer. Usage: node pdf.js in.html out.pdf "Footer text"
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const [input, output, footer = ""] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(input), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  await page.pdf({
    path: output,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="width:100%;font:7px Inter,Arial,sans-serif;color:#5d5d5a;padding:0 14mm;display:flex;justify-content:space-between">' +
      `<span>${esc(footer)}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
  });
  await browser.close();
})();
