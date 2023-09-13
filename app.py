import requests
import json
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def get_instagram_profile(username):
    base_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    response_cookies = requests.get(base_url)
    cookies = response_cookies.cookies

    new_cookies = {
        'csrftoken': cookies['csrftoken'],
        'ig_did': cookies['ig_did'],
        'ig_nrcb': cookies['ig_nrcb'],
        'mid': cookies['mid'],
    }

    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'dpr': '1',
        'referer': f'https://www.instagram.com/{username}/',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-full-version-list': '"Chromium";v="116.0.5845.187", "Not)A;Brand";v="24.0.0.0", "Google Chrome";v="116.0.5845.187"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'viewport-width': '1416',
        'x-asbd-id': '129477',
        'x-csrftoken': 'Yuhymwb03YmJgI02P6RY8mNoNiiQnFPU',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'username': f"{username}",
    }

    response = requests.get(
        'https://www.instagram.com/api/v1/users/web_profile_info/',
        params=params,
        cookies=new_cookies,
        headers=headers,
    )

    return response

def save_profile_data(username, response):
    if response.status_code == 200:
        data = response.json()

        # Define the filename for the JSON file
        filename = f"{username}_profile.json"

        # Write the response data to the JSON file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Profile data saved to {filename}")
    else:
        print(f"Failed to retrieve profile data. Status code: {response.status_code}")

def show_profile_data(username):
    response = get_instagram_profile(username)
    save_profile_data(username, response)

    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant profile information
        user_data = data.get("data", {}).get("user", {})
        username = user_data.get("username")
        followers = user_data.get("edge_followed_by", {}).get("count")
        following = user_data.get("edge_follow", {}).get("count")
        bio = user_data.get("biography")

        # Check if the account is verified
        is_verified = user_data["is_verified"]

        # Check if the profile picture features the club's logo (You may need to implement custom logic for this)
        profile_picture_url = user_data["profile_pic_url_hd"]

        # Extract recent posts (up to the first 5)
        recent_posts = user_data["edge_owner_to_timeline_media"]["edges"][:5]

        # Extract video count, views, and likes for the most recent video
        video_count = user_data["edge_felix_video_timeline"]["count"]
        
        if video_count > 0:
            most_recent_video = user_data["edge_felix_video_timeline"]["edges"][0]["node"]
            most_recent_video_views = most_recent_video["video_view_count"]
            most_recent_video_likes = most_recent_video["edge_liked_by"]["count"]
        else:
            most_recent_video_views = 0
            most_recent_video_likes = 0

        # Extract transparency label
        transparency_label = user_data.get("transparency_label", "Not Available")

        # Extract business information
        business_category = user_data.get("business_category_name", "Not Available")
        business_contact_info = user_data.get("business_contact_method", "Not Available")

        # Format and style the extracted information
        print(Fore.BLUE + f"Username: {username}")
        print(Fore.GREEN + f"Followers: {followers}")
        print(Fore.GREEN + f"Following: {following}")
        print(Fore.YELLOW + f"Biography: {bio}")
        print(Fore.CYAN + f"Category: The account falls under the '{business_category}' category.")
        print(Fore.CYAN + f"Verified: {'Yes' if is_verified else 'No'}")
        # You can format and style the profile picture URL here if needed
        print(Fore.MAGENTA + f"Content: The account has posted {video_count} videos.")
        print(Fore.MAGENTA + f"Engagement: Most recent video has {most_recent_video_views} views and {most_recent_video_likes} likes.")
        print(Fore.RED + f"Transparency Label: {transparency_label}")
        print(Fore.RED + f"Business Information: {business_contact_info}")

        print(Fore.RESET + "Recent Posts:")
        for post in recent_posts:
            post_node = post["node"]
            post_url = f"https://www.instagram.com/p/{post_node['shortcode']}/"
            post_caption = post_node["edge_media_to_caption"]["edges"][0]["node"]["text"]
            print(Fore.RESET + f"Post URL: {post_url}")
            print(Fore.RESET + f"Caption: {post_caption}")
            print()

    else:
        print(Fore.RED + "Unable to display profile data.")

def profile_data(username):
    response = get_instagram_profile(username)
    save_profile_data(username, response)

    if response.status_code == 200:
        data = response.json()
        profile_data = {}  # Create a dictionary to store the extracted information
        
        # Extract relevant profile information
        user_data = data.get("data", {}).get("user", {})
        profile_data["username"] = user_data.get("username")
        profile_data["followers"] = user_data.get("edge_followed_by", {}).get("count")
        profile_data["following"] = user_data.get("edge_follow", {}).get("count")
        profile_data["bio"] = user_data.get("biography")

        # Check if the account is verified
        profile_data["is_verified"] = user_data["is_verified"]

        # Check if the profile picture features the club's logo (You may need to implement custom logic for this)
        profile_data["profile_picture_url"] = user_data["profile_pic_url_hd"]

        # Extract recent posts (up to the first 5)
        recent_posts = user_data["edge_owner_to_timeline_media"]["edges"][:5]
        profile_data["recent_posts"] = []

        for post in recent_posts:
            post_node = post["node"]
            post_url = f"https://www.instagram.com/p/{post_node['shortcode']}/"
            post_caption = post_node["edge_media_to_caption"]["edges"][0]["node"]["text"]
            profile_data["recent_posts"].append({
                "post_url": post_url,
                "caption": post_caption
            })

        # Extract video count, views, and likes for the most recent video
        profile_data["video_count"] = user_data["edge_felix_video_timeline"]["count"]
        
        if profile_data["video_count"] > 0:
            most_recent_video = user_data["edge_felix_video_timeline"]["edges"][0]["node"]
            profile_data["most_recent_video_views"] = most_recent_video["video_view_count"]
            profile_data["most_recent_video_likes"] = most_recent_video["edge_liked_by"]["count"]
        else:
            profile_data["most_recent_video_views"] = 0
            profile_data["most_recent_video_likes"] = 0

        # Extract transparency label
        profile_data["transparency_label"] = user_data.get("transparency_label", "Not Available")

        # Extract business information
        profile_data["business_category"] = user_data.get("business_category_name", "Not Available")
        profile_data["business_contact_info"] = user_data.get("business_contact_method", "Not Available")

        return profile_data  # Return the extracted data as a dictionary

    else:
        return None  # Return None if unable to display profile data


if __name__ == "__main__":
    # username = "alnassr"
    username = input("Enter Usename: ")
    show_profile_data(username)
