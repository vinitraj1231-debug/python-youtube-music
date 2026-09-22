import json
import os
import sys
from urllib.parse import parse_qs, urlparse

# Patch requests/urllib3 in Pyodide/Emscripten environment if pyodide_http is available
try:
    import pyodide_http
    pyodide_http.patch_all()
except Exception:
    pass

# Ensure current directory (src/) is in sys.path so 'ytm' can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from js import Headers, Response
import ytm

api = ytm.YouTubeMusic()


def make_response(data, status=200):
    headers = Headers.new()
    headers.set("Content-Type", "application/json; charset=utf-8")
    headers.set("Access-Control-Allow-Origin", "*")
    headers.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    headers.set("Access-Control-Allow-Headers", "Content-Type")

    body = json.dumps(data, ensure_ascii=False, default=str)
    return Response.new(body, status=status, headers=headers)


async def on_fetch(request, env):
    method = request.method

    if method == "OPTIONS":
        return make_response({}, status=200)

    parsed_url = urlparse(request.url)
    path = parsed_url.path.rstrip("/")
    if not path:
        path = "/"
    params = parse_qs(parsed_url.query)

    try:
        if path in ("/", "/api"):
            return make_response({
                "status": "online",
                "service": "YouTube Music Cloudflare Worker API",
                "version": getattr(ytm, "__version__", "0.1.0"),
                "endpoints": {
                    "GET /search?q=<query>": "Search YouTube Music",
                    "GET /search_songs?q=<query>": "Search songs",
                    "GET /search_albums?q=<query>": "Search albums",
                    "GET /search_artists?q=<query>": "Search artists",
                    "GET /search_playlists?q=<query>": "Search playlists",
                    "GET /suggestions?q=<query>": "Get search suggestions",
                    "GET /song?id=<id>": "Get song details",
                    "GET /album?id=<id>": "Get album details",
                    "GET /artist?id=<id>": "Get artist details",
                    "GET /playlist?id=<id>": "Get playlist details",
                    "GET /home": "Get home shelf feed",
                    "GET /hotlist": "Get trending hotlist"
                }
            })

        q = params.get("q", [""])[0]
        item_id = params.get("id", [""])[0]

        if path == "/search":
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search(q))

        elif path == "/search_songs":
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search_songs(q))

        elif path == "/search_albums":
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search_albums(q))

        elif path == "/search_artists":
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search_artists(q))

        elif path == "/search_playlists":
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search_playlists(q))

        elif path in ("/search_suggestions", "/suggestions"):
            if not q:
                return make_response({"error": "Missing 'q' query parameter"}, status=400)
            return make_response(api.search_suggestions(q))

        elif path == "/song":
            if not item_id:
                return make_response({"error": "Missing 'id' query parameter"}, status=400)
            return make_response(api.song(item_id))

        elif path == "/album":
            if not item_id:
                return make_response({"error": "Missing 'id' query parameter"}, status=400)
            return make_response(api.album(item_id))

        elif path == "/artist":
            if not item_id:
                return make_response({"error": "Missing 'id' query parameter"}, status=400)
            return make_response(api.artist(item_id))

        elif path == "/playlist":
            if not item_id:
                return make_response({"error": "Missing 'id' query parameter"}, status=400)
            return make_response(api.playlist(item_id))

        elif path == "/home":
            return make_response(api.home())

        elif path == "/hotlist":
            return make_response(api.hotlist())

        else:
            return make_response({"error": f"Endpoint '{path}' not found"}, status=404)

    except Exception as err:
        return make_response({"error": str(err)}, status=500)
