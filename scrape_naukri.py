import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NAUKRI_URL = "https://www.naukri.com/devops-jobs-in-bangalore"

async def scrape_naukri_jobs(max_pages=3):
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for page_num in range(1, max_pages + 1):
            url = NAUKRI_URL if page_num == 1 else f"{NAUKRI_URL}-{page_num}"
            logger.info(f"Scraping: {url}")
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("article.jobTuple", timeout=30000)

            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            job_cards = soup.select("article.jobTuple")

            for card in job_cards:
                try:
                    title_elem = card.select_one("a.title")
                    company_elem = card.select_one("a.subTitle")
                    location_elem = card.select_one("li.fleft.br2.placeHolder")
                    desc_elem = card.select_one("ul.job-description")
                    link_elem = card.select_one("a.title")

                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    location = location_elem.get_text(strip=True) if location_elem else "N/A"
                    desc = desc_elem.get_text(strip=True) if desc_elem else ""
                    link = link_elem["href"] if link_elem and link_elem.has_attr("href") else ""

                    # Only keep Bengaluru jobs (Naukri sometimes shows nearby)
                    if "bangalore" not in location.lower() and "bengaluru" not in location.lower():
                        continue

                    job = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": desc,
                        "link": link,
                        "source": "Naukri"
                    }
                    jobs.append(job)
                except Exception as e:
                    logger.error(f"Error parsing job card: {e}")
                    continue

            await asyncio.sleep(2)  # Be polite

        await browser.close()
    return jobs
