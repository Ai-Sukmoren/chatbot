from langchain_community.tools import YouTubeSearchTool
from IPython.display import Image, display
import re
import ast

def youtube(prompt):
    youtube = YouTubeSearchTool()
    result = youtube.run(prompt)
    # Convert the string representation of the list back into a Python list
    result_list = ast.literal_eval(result)

    # Extract the first link
    first_link = result_list[0]
    
    # Example YouTube video URL
    video_url = first_link

    # Extract video ID from the URL
    video_id = re.search(r'(?<=v=)[^&#]+', video_url).group()

    # Construct the thumbnail URL
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/0.jpg'

    # Display the thumbnail
    pic = display(Image(url=thumbnail_url))
    
    return f'{first_link}{pic}'

youtube('A song name always by daniel ceasar')