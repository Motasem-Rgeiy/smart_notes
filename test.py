import trafilatura

# Download and extract web page content
downloaded = trafilatura.fetch_url('https://openrouter.ai/blog/announcements/openrouter-is-joining-stripe/')
result = trafilatura.extract(downloaded)
print(result)