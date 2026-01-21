import asyncio
from typing import Optional
from playwright.async_api import async_playwright


async def render_page_html(url: str, wait_selector: Optional[str] = None) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, timeout=60000)

        # Force waiting for job cards
        selector = wait_selector or "div.job-tile"
        try:
            await page.wait_for_selector(selector, timeout=60000)
        except Exception as e:
            print(f"[DEBUG] wait_for_selector failed for {selector}: {e}")

        html = await page.content()
        await browser.close()
        return html



def render_page_html_sync(url: str, wait_selector: Optional[str] = "div.job-tile") -> str:
    return asyncio.run(render_page_html(url, wait_selector))
