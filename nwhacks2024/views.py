import json
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from nwhacks2024.document_parse.document_parser import extract_table
from nwhacks2024.geooding.scrape_gmaps import get_photos_by_place_id


# Create your views here.


def load_map(request):
    context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}
    return render(request, "home.html", context)


def process_place_id(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            place_id = data.get("placeId")

            image_urls = []
            while len(image_urls) == 0:
                # Use Selenium to gather menu images
                image_urls = get_photos_by_place_id(place_id)
                print(image_urls)

            # Store image URLs in session
            request.session["image_urls"] = image_urls

            return JsonResponse({"redirect_url": "/menu_gallery/"})
        except Exception as e:
            # Log the exception for debugging
            print(f"Error: {e}")
            # Return a JSON response with the error message
            return JsonResponse({"error": str(e)}, status=500)


def menu_gallery(request):
    # Retrieve image URLs from session
    image_urls = request.session.get("image_urls", [])

    # Clear the session data
    if "image_urls" in request.session:
        del request.session["image_urls"]

    return render(request, "image_gallery.html", {"image_urls": image_urls})


@require_http_methods(["POST"])
def process_image(request):
    # Parse the request body to get the data
    data = json.loads(request.body)
    image_url = data.get("imageUrl")
    print(image_url)
    table = None
    count = 0
    while True:
        try:
            count = count + 1
            if count > 5:
                break
            print(count)
            table = extract_table(image_url)
            break
        except:
            if table is not None and table.dataframe is not None:
                break
            continue

    if table is not None and table.dataframe is not None:
        # df = join_tables(tables)
        # file_path = "table.csv"
        # df = pd.read_csv(file_path)
        df = table.dataframe
        print(df)
        # Convert the DataFrame to HTML
        df_html = df.to_html()

        request.session["df_html"] = df_html

        return JsonResponse({"redirect_url": "/menu_filter/"})
    else:
        return JsonResponse({"error": "Unable to process the image or no data found."})


from openai import OpenAI


def menu_filter(request):
    # Handle form submission

    # Retrieve image URLs from session
    df_html = request.session.get("df_html", [])
    assistant_reply = ""
    if request.method == "POST":
        search_term = request.POST.get("search", "")
        try:
            OPENAI_API_KEY = os.environ["OPENAI_API_KEY_NWHACKS2024"]
        except:
            OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY_NWHACKS2024")

        # Apply the patch to the OpenAI client to support response_model
        # Also use MD_JSON mode since the vision model does not support any special structured output mode
        client = OpenAI(api_key=OPENAI_API_KEY)
        openai_response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            max_tokens=1800,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Based on the table, answer the question below: """
                            + search_term,
                        },
                        {"type": "text", "text": df_html},
                    ],
                },
            ],
        )
        assistant_reply = openai_response.choices[0].message.content
        # openai_response = openai_response["choices"][0]["message"]["content"][0][
        #     "content"
        # ]

    # # Clear the session data
    # if "df_html" in request.session:
    #     del request.session["df_html"]

    return render(
        request,
        "menu_filter.html",
        {"df_html": df_html, "search_response": assistant_reply},
    )
