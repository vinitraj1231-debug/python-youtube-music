# Cloudflare Workers Deploy Guide (हिंदी / Hinglish)

Is project (`python-youtube-music`) ko **Cloudflare Workers** par Python runtime ke dwara deploy karne ki poori jankari niche di gayi hai.

---

## 📋 Prerequisites (Zaroori Cheezein)

1. **Node.js** (v18 ya usse naya) aapke system par install hona chahiye.
2. **Cloudflare Account** (Free account bhi chalega).

---

## 🛠 Project Structure

Cloudflare par deploy karne ke liye ye files tayyar hain:
- `wrangler.json` - Cloudflare Worker configuration file.
- `src/index.py` - Python Worker entrypoint jo YouTube Music API routes ko expose karta hai.
- `requirements.txt` - Required Python dependencies (`requests`).

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

## 📡 Available API Endpoints

Aapke Cloudflare Worker par niche diye gaye HTTP GET endpoints available honge:

| Endpoint | Query Parameter | Description |
| --- | --- | --- |
| `GET /` | - | Service status and list of endpoints |
| `GET /search` | `?q=search_query` | YouTube Music general search |
| `GET /search_songs` | `?q=song_name` | Songs search |
| `GET /search_albums` | `?q=album_name` | Albums search |
| `GET /search_artists` | `?q=artist_name` | Artists search |
| `GET /search_playlists` | `?q=playlist_name` | Playlists search |
| `GET /suggestions` | `?q=query` | Search auto-suggestions |
| `GET /song` | `?id=song_id` | Song details retrieve karein |
| `GET /album` | `?id=album_id` | Album details retrieve karein |
| `GET /artist` | `?id=artist_id` | Artist details retrieve karein |
| `GET /playlist` | `?id=playlist_id` | Playlist details retrieve karein |
| `GET /home` | - | Home feed shelves retrieve karein |
| `GET /hotlist` | - | Trending hotlist songs retrieve karein |

### Examples:
- **Search Songs:** `https://python-youtube-music.<your-subdomain>.workers.dev/search_songs?q=Arijit+Singh`
- **Get Song Info:** `https://python-youtube-music.<your-subdomain>.workers.dev/song?id=pPt_FZ9m2bM`
