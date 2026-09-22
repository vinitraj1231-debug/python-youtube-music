# Cloudflare Workers Deploy Guide (हिंदी / Hinglish)

Is project (`python-youtube-music`) ko **Cloudflare Workers** par Python runtime ke dwara deploy karne aur API use karne ki poori jankari niche di gayi hai.

---

## ⚠️ "No URLs enabled" ya "workers.dev Disabled" Fix Kaise Karein?

Agar Cloudflare Dashboard par **"No URLs enabled"** ya **"workers.dev Disabled"** dikh raha hai, toh iska matlab hai ki worker ka public subdomain URL enable nahi hai. Isko 2 tarike se fix kar sakte hain:

### Method 1: Wrangler Se Fix Karein (Recommended)
`wrangler.json` me `"workers_dev": true` Add kar diya gaya hai. Ab aap bas apne terminal me redeploy karein:
```bash
npx wrangler deploy
```
Deploy hone ke baad Cloudflare automatically aapka URL enable kar dega (jaise `https://python-youtube-music.<your-subdomain>.workers.dev`).

### Method 2: Cloudflare Dashboard Se Fix Karein
1. [Cloudflare Dashboard](https://dash.cloudflare.com) me login karein.
2. **Workers & Pages** -> **python-youtube-music** par jayein.
3. **Domains and routes** section me jayein.
4. `workers.dev` ke paas **Enable** ya **Edit** button par click karke enable kar dein.

---

## 📋 Prerequisites (Zaroori Cheezein)

1. **Node.js** (v18 ya usse naya) aapke system par install hona chahiye.
2. **Cloudflare Account** (Free account bhi chalega).

---

## 🛠 Project Structure

Cloudflare par deploy karne ke liye ye files tayyar hain:
- `wrangler.json` - Cloudflare Worker configuration file (`"workers_dev": true` configured).
- `src/index.py` - Python Worker entrypoint jo YouTube Music API routes ko expose karta hai.
- `src/requirements.txt` / `requirements.txt` - Required Python dependencies (`requests`).

---

## 🚀 Step-by-Step Deployment Guide

### 1. Wrangler CLI Install Karein
Apne terminal par Wrangler install karein (agar pehle se nahi hai):
```bash
npm install -g wrangler
```

### 2. Cloudflare Account me Login Karein
Terminal se Cloudflare me login karein:
```bash
npx wrangler login
```
*Aapke browser me page khulega, waha se login allow karein.*

### 3. Local Development / Test Karein
Deploy karne se pehle local environment me test karne ke liye run karein:
```bash
npx wrangler dev
```
Ye aapko ek local URL dega (eg. `http://localhost:8787`). Aap browser ya Postman me endpoints test kar sakte hain.

### 4. Cloudflare Workers Par Deploy Karein
Jab sab test ho jaye, tab deploy karne ke liye ye command chalayein:
```bash
npx wrangler deploy
```

Deploy hone ke baad aapko aapka live Worker URL mil jayega (eg. `https://python-youtube-music.<your-subdomain>.workers.dev`).

---

## 📖 API Usage Guide (API Kaise Use Karein)

Base URL: `https://python-youtube-music.<your-subdomain>.workers.dev`

---

### 📡 Available API Endpoints

| Endpoint | Method | Query Parameter | Description / Kaam |
| --- | --- | --- | --- |
| `/` | `GET` | - | API status aur sabhi endpoints ki list |
| `/search` | `GET` | `?q=query` | General search (songs, albums, artists, playlists, videos) |
| `/search_songs` | `GET` | `?q=query` | Fast song search |
| `/search_albums` | `GET` | `?q=query` | Albums search |
| `/search_artists` | `GET` | `?q=query` | Artists search |
| `/search_playlists` | `GET` | `?q=query` | Playlists search |
| `/suggestions` | `GET` | `?q=query` | Search auto-suggestions |
| `/song` | `GET` | `?id=song_id` | Song details aur recommendations retrieve karein |
| `/album` | `GET` | `?id=album_id` | Album details aur tracklist retrieve karein |
| `/artist` | `GET` | `?id=artist_id` | Artist details, top songs, albums retrieve karein |
| `/playlist` | `GET` | `?id=playlist_id` | Playlist details aur tracks retrieve karein |
| `/home` | `GET` | - | YouTube Music Home feed shelves retrieve karein |
| `/hotlist` | `GET` | - | Trending / Hotlist songs retrieve karein |

---

### 💡 API Usage Examples

Suppose aapka worker URL `https://python-youtube-music.vinitraj1231.workers.dev` hai:

#### 1. Songs Search Karein
`GET https://python-youtube-music.vinitraj1231.workers.dev/search_songs?q=Arijit+Singh`

#### 2. Specific Song Info Retrieve Karein (using Video/Song ID)
`GET https://python-youtube-music.vinitraj1231.workers.dev/song?id=pPt_FZ9m2bM`

#### 3. Artist Details Retrieve Karein (using Artist ID)
`GET https://python-youtube-music.vinitraj1231.workers.dev/artist?id=UC8Yu1_yfN5qPh601Y4btsYw`

#### 4. Album Details Retrieve Karein
`GET https://python-youtube-music.vinitraj1231.workers.dev/album?id=MPREb_ctJ5HEJw8pg`

#### 5. Search Suggestions Get Karein
`GET https://python-youtube-music.vinitraj1231.workers.dev/suggestions?q=arijit`

#### 6. Trending Songs (Hotlist)
`GET https://python-youtube-music.vinitraj1231.workers.dev/hotlist`

---

### 💻 Code Integration Examples

#### Python Example:
```python
import requests

BASE_URL = "https://python-youtube-music.<your-subdomain>.workers.dev"

# Search songs
response = requests.get(f"{BASE_URL}/search_songs", params={"q": "Arijit Singh"})
songs = response.json()
print(songs)
```

#### JavaScript / Fetch Example:
```javascript
const BASE_URL = "https://python-youtube-music.<your-subdomain>.workers.dev";

// Search songs
fetch(`${BASE_URL}/search_songs?q=Arijit+Singh`)
  .then(res => res.json())
  .then(data => console.log(data));
```

#### cURL Example:
```bash
curl "https://python-youtube-music.<your-subdomain>.workers.dev/search_songs?q=Arijit+Singh"
```
