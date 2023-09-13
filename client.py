import grpc
from instagram_user_pb2 import InstagramUserQuery
from instagram_user_pb2_grpc import InstagramUserStub
from colorama import Fore, init

# Initialize Colorama
init(autoreset=True)

def get_instagram_profile_info(username):
    channel = grpc.insecure_channel("localhost:50051")
    client = InstagramUserStub(channel)

    request = InstagramUserQuery(query=username)
    try:
        response = client.InstagramUserData(request)
        if response.username:
            # Format and style the extracted information
            print(Fore.BLUE + f"Username: {response.username}")
            print(Fore.GREEN + f"Followers: {response.followers}")
            print(Fore.GREEN + f"Following: {response.following}")
            print(Fore.YELLOW + f"Biography: {response.bio}")
            print(Fore.CYAN + f"Category: The account falls under the '{response.business_category}' category.")
            print(Fore.CYAN + f"Verified: {'Yes' if response.is_verified else 'No'}")
            # You can format and style the profile picture URL here if needed
            print(Fore.MAGENTA + f"Content: The account has posted {response.video_count} videos.")
            print(Fore.MAGENTA + f"Engagement: Most recent video has {response.most_recent_video_views} views and {response.most_recent_video_likes} likes.")
            print(Fore.RED + f"Transparency Label: {response.transparency_label}")
            print(Fore.RED + f"Business Information: {response.business_contact_info}")

            print(Fore.RESET + "Recent Posts:")
            for post in response.recent_posts:
                print(Fore.RESET + f"Post URL: {post.post_url}")
                print(Fore.RESET + f"Caption: {post.caption}")
                print()

        else:
            print("Profile not found.")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")


if __name__ == "__main__":
    username = "alnassr"
    get_instagram_profile_info(username)