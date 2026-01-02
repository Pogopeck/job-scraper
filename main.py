import os
import asyncio
import pandas as pd
from dotenv import load_dotenv

from scrape_naukri import scrape_naukri_jobs
from filter_jobs import matches_keywords
from score_relevance import score_job

load_dotenv()

async def main():
    print("🔍 Scraping Naukri jobs...")
    jobs = await scrape_naukri_jobs(max_pages=2)

    print(f"📥 Found {len(jobs)} Bengaluru jobs. Filtering...")
    filtered = [j for j in jobs if matches_keywords(j)]

    print(f"🎯 {len(filtered)} jobs match keyword criteria. Scoring relevance...")
    for job in filtered:
        job["relevance_score"] = score_job(job)
        await asyncio.sleep(1)  # Avoid rate limits

    # Sort by score
    filtered.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Save to CSV
    df = pd.DataFrame(filtered)
    filename = "bengaluru_genai_devops_jobs.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved top jobs to {filename}")

    # Optional: Print top 3
    for i, job in enumerate(filtered[:3], 1):
        print(f"\n{i}. [{job['relevance_score']}/10] {job['title']} @ {job['company']}")
        print(f"   {job['link']}")

if __name__ == "__main__":
    asyncio.run(main())
