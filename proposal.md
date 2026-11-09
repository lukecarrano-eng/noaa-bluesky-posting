# Proposal

**Title:** How Do NOAA's Bluesky Accounts Differ in What and When They Post?

**Research question:** How do NOAA's three .gov accounts on Bluesky (nws.noaa.gov, climate.noaa.gov, noaacomms.noaa.gov) differ in posting frequency, posting times, and use of images and video, and how do those choices relate to how often their posts get reposted?

**Why it matters:** Federal agencies use social media to reach the public, especially during severe weather. Looking at how different parts of one agency use the same platform shows how they approach their audiences differently.

**Data:** Public posts from the three accounts, collected from Bluesky's public API (public.api.bsky.app). The API needs no key. I only collect the accounts' own posts, not reposts or replies, so no private person's content is in the data. The handles are .gov domains and the accounts are verified by Bluesky, which is how I know they belong to NOAA. NOAA's main account is not included because its `noaa.gov` handle does not currently resolve in the API.

**Methods:** Collect each account's posts with a User-Agent that identifies me and pauses between requests. Clean the raw JSON into one table. Compare posts per month, posts by weekday and hour (in Eastern time), the share of posts with an image or video, and median reposts for each account.

**Limitations:** Bluesky is only one platform, and only some agencies are on it. Reposts and likes depend a lot on what is going on in the weather that week, so the comparison describes behavior but can't show what causes a post to spread. The API doesn't give impressions, so I can't say who saw a post.

**Feedback revisions:** None yet.
