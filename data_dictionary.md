# Data Dictionary

File: `data/sample_posts_clean.csv` (a 30-row sample of the full cleaned table `local_data/clean/posts_clean.csv`). One row is one original post by one of NOAA's accounts. Reposts and replies are not included.

| Field | Type | Meaning |
|---|---|---|
| `uri` | string | The post's unique address on Bluesky (AT URI). Used to remove duplicates. |
| `handle` | string | The account that posted: `nws.noaa.gov`, `climate.noaa.gov` or `noaacomms.noaa.gov`. |
| `created_at` | string | When the post was made, in UTC (ISO 8601). Set by the author's app, so it can differ slightly from when Bluesky saw it. |
| `created_local` | string | Same time converted to US Eastern time. |
| `month` | string | Month of `created_local`, as `YYYY-MM`. |
| `weekday` | string | Day of the week of `created_local`. |
| `hour` | integer | Hour of the day (0 to 23) of `created_local`. |
| `text` | string | The text of the post. |
| `text_length` | integer | Number of characters in `text`. |
| `embed_type` | string | What the post carries: `images`, `video`, `external` (a link card), `record` (a quoted post), `recordWithMedia`, or `none`. |
| `has_media` | boolean | True if `embed_type` is `images` or `video`. |
| `likes` | integer | Likes the post had when collected. |
| `reposts` | integer | Reposts the post had when collected. |
| `replies` | integer | Replies the post had when collected. |
| `quotes` | integer | Quote posts the post had when collected. |

Counts (`likes`, `reposts`, `replies`, `quotes`) are a snapshot from the collection date, so newer posts have had less time to collect them. Missing counts were set to 0.
