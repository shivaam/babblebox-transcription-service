import requests

# Replace 'your_api_list_url' with the URL to list all entries
api_url_chat = "https://babblebox-app.shivamrastogi.com/api/ChatMessage/"

list_url = api_url_chat
headers = {
    "Authorization": f"Token 380915803ba47517c0e0dc21add9c814f85e9dd4"
}
# Send a GET request to retrieve the list of entry URLs
response = requests.get(list_url, headers=headers)
if response.status_code == 200:
    entry_urls = response.json()  # Assuming the response is in JSON format
    print(entry_urls)
    for entry_url in entry_urls:
        print(entry_url)
        # Send a DELETE request for each entry URL
        delete_response = requests.delete(list_url + entry_url.get("id"), headers=headers)
        if delete_response.status_code == 204:
            print(f"Deleted: {entry_url}")
        else:
            print(f"Failed to delete: {entry_url} (Status code: {delete_response.status_code})")
else:
    print(f"Failed to retrieve the list of entry URLs (Status code: {response.status_code})")