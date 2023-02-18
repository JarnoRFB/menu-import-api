"""Script to export the ReDoc documentation page into a standalone HTML file."""
import json
import pathlib
from api import app


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>VisioLab Menu Import API</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://uploads-ssl.webflow.com/610e8d4e5e20c21539aec950/612686a1377160481ec27630_Favicon.png">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
    </style>
    <style data-styled="" data-styled-version="4.4.1"></style>
</head>
<body>
    <div id="redoc-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"> </script>
    <script>
        const spec = %s;
        Redoc.init(spec, {}, document.getElementById("redoc-container"));
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    path = pathlib.Path("docs")
    path.mkdir(parents=True, exist_ok=True)
    (path / "index.html").write_text(HTML_TEMPLATE % json.dumps(app.openapi()))
