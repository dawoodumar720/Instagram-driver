from concurrent import futures
import grpc
import instagram_user_pb2
import instagram_user_pb2_grpc
from app import profile_data

class InstagramUser(instagram_user_pb2_grpc.InstagramUserServicer):
    def InstagramUserData(self, request, context):
        if request is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Username not found.")
        else:
            username = request.query
            data = profile_data(username)

            if data:
                response = instagram_user_pb2.InstagramUserResponse(
                    username=data["username"],
                    followers=data["followers"],
                    following=data["following"],
                    bio=data["bio"],
                    business_category=data["business_category"],
                    is_verified=data["is_verified"],
                    video_count=data["video_count"],
                    most_recent_video_views=data["most_recent_video_views"],
                    most_recent_video_likes=data["most_recent_video_likes"],
                    transparency_label=data["transparency_label"],
                    business_contact_info=data["business_contact_info"],
                )

                for post in data["recent_posts"]:
                    response.recent_posts.add(
                        post_url=post["post_url"],
                        caption=post["caption"]
                    )

                return response
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, "Profile not found.")      

def serve():
    # create a grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    instagram_user_pb2_grpc.add_InstagramUserServicer_to_server(InstagramUser(), server)
    port = 50051
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server is Running on port: {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()