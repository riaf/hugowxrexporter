# HugoWXRExporter

## Overview
HugoWXRExporter is a tool for converting content created with Hugo static site generator to WordPress Extended RSS (WXR) format. This facilitates the easy migration of content from Hugo to WordPress.

## Features
- Recursively reads Hugo markdown files
- Parses metadata and content, converting them into WordPress WXR format
- Utilizes Docker to eliminate environment dependencies

## Environment Variables
You can customize the behavior of the script using the following environment variables:
- `HUGO_WXR_CREATOR`: Set the creator name for the WXR file. Default is 'admin'.
- `HUGO_WXR_GUID`: Set the base URL for GUID. The unique part of GUID will be appended to this base URL. Default is 'http://example.com/'.

## Usage

### Prerequisites
Docker must be installed to use this tool.

### Running the Tool
Pull the public Docker image and execute the Docker container, specifying the path to your Hugo `content` directory and optionally setting environment variables.

```bash
docker pull ghcr.io/riaf/HugoWXRExporter:latest
docker run -v /path/to/hugo/content:/app/content -e HUGO_WXR_CREATOR="YourName" -e HUGO_WXR_GUID="http://yourwebsite.com/" ghcr.io/riaf/HugoWXRExporter:latest /app/content
```

Replace `/path/to/hugo/content` with the actual path to your Hugo content directory. Adjust the environment variables as needed.

## License

This project is made available under the Apache License 2.0.
