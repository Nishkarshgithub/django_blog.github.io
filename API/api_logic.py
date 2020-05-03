from .models import User, Author, Blog, Comments
from rest_framework.response import Response
from datetime import datetime
from django.contrib.auth import authenticate, logout
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Constant Import
from .constant import STATUS, DETAIL, FAILURE, SUCCESS, BLOGDATA, FALSE_VALUE, TRUE_VALUE, COMMENTDATA

# Serializers Import
from .serializers import BlogSerializer, CommentsSerializer

# UTILS Import
from .utils import USER_LOGIN, BLOG_CREATE


class Loginview(APIView):
    '''
        This API provides user to authenticate and returns the related user data if it exists.
        x-www-form-urlencoded data using postman

        GET REQUEST

        Key    		value
        username  	xxxxxxx
        password	xxxxxxx

        {
            "username" : "nishkarsh_gupta",
            "password" : "Mn456fgvjik" 
        }

        API Response

        {
            "status": "success",
            "detail": "USER LOGGED IN",
            "data": {
                "token": "1e6ca3c363b91ebcd27f5641e2cfcccff0a20cbe",
                "user_data": {
                    "name": "Nishkarsh Gupta",
                    "createTime": "2020-05-03T10:05:51+05:30",
                    "Is_active": true
                }
            }
        }

    '''
    def get(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({ STATUS: FAILURE, DETAIL: "USER LOGIN FAILED"}, status.HTTP_204_NO_CONTENT)
        user = authenticate(username=username, password=password)
        # if authentication fails
        if not user: return Response({ STATUS: FAILURE, DETAIL: "USER LOGIN FAILED"}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return USER_LOGIN(user, request)


class UserLogout(APIView):
    '''
        This API ends the user login session.
    
        GET REQUEST
        
        headers = { "Authorization" : 'Token 1e6ca3c363b91ebcd27f5641e2cfcccff0a20cbe' }

        API Response

        {
            "status": "success",
            "detail": "USER LOGGED OUT"
        }
        
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response({ STATUS: SUCCESS, DETAIL: "USER LOGGED OUT"}, status.HTTP_200_OK)


class BLOG(viewsets.ViewSet):
    '''
        This API use Rest Framework built-in viewset functions

        GET REQUEST

        headers = { "Authorization" : 'Token 1e6ca3c363b91ebcd27f5641e2cfcccff0a20cbe' }
        
        CREATE

        {
            "title": "Babur Mughal Emperor",
            "content": "Babur, born Zahīr ud-Dīn Muhammad, was the founder and first Emperor of the Mughal dynasty in the Indian subcontinent. He was descendant of both Timur and Genghis Khan through his father and mother respectively.",
            "publish": true
        }


        REMOVE 

        {
            "blog_Id": 2
        }


        COMMENT

        {
            "blog_Id": 3,
            "comment": "Amazing write-up!"
        }


        API RESPONSE

        CREATE RESPONSE

        {
            "status": "success",
            "detail": "BLOG CREATED SUCCESSFULLY!"
        }

        LIST RESPONSE

        {
            "status": "success",
            "detail": "BLOG LISTED SUCCESSFULLY!",
            "blog_data": [
                {
                    "Id": 2,
                    "created_at": "2020-05-03T12:55:02.805356+05:30",
                    "title": "Machine learning Field of study",
                    "content": "Machine learning is the study of computer algorithms that improve automatically through experience. It is seen as a subset of artificial intelligence.",
                    "is_publised": true,
                    "is_active": true,
                    "created_by": 1
                }
                {
                    "Id": 1,
                    "created_at": "2020-05-03T10:09:50+05:30",
                    "title": "Skint Dad",
                    "content": "So when I talk about coming at a niche from a different angle, this example is exactly what I mean. Skint Dad is a site that helps young / new dads save money and be more frugal in their day to day living. There’s also a section on their that shows guys how to make a little more cash on top of their monthly day job wage, which is vital in some cases just to keep your head above water.  A lot of new dads have the added stress of not having their wives’ or girlfriends’ wage coming in each month, due to the temporary career change in being a full time mum of a baby. So having some content around how they can make a few extra “Ps” in their wallet each month, can ease the burden somewhat.",
                    "is_publised": true,
                    "is_active": true,
                    "created_by": 1,
                    "comments": [
                        {
                            "Id": 1,
                            "created_at": "2020-05-03T10:12:14+05:30",
                            "content": "Well Said!",
                            "created_by": 2,
                            "created_for": 1
                        }
                    ]
                }
            ]
        }

        REMOVE RESPONSE

        {
            "status": "success",
            "detail": "BLOG REMOVED SUCCESSFULLY!"
        }

        COMMENT RESPONSE

        {
            "status": "success",
            "detail": "COMMENT SUCCESS"
        }

    '''
    permission_classes = (IsAuthenticated,)

    # LIST FUNCTION

    def list(self, request):
        try:
            SERIALIZED_DATA = []
            USER = Author.objects.get(user__id=request.user.id)
            queryset = Blog.objects.filter( created_by = USER, is_active = TRUE_VALUE ).order_by('-created_at').all()
            for query in queryset:
                SERIALIZED_QUERY = BlogSerializer(query).data
                commentsqueryset = Comments.objects.filter(created_for__Id = query.Id)
                if commentsqueryset: SERIALIZED_QUERY['comments'] = CommentsSerializer(commentsqueryset, context = {}, many=True).data
                SERIALIZED_DATA.append(SERIALIZED_QUERY)
        except (ValueError, KeyError, SyntaxError):
            return Response({ STATUS: SUCCESS, DETAIL: "Author do not publish any blogs."}, status.HTTP_200_OK)
        return Response({ STATUS: SUCCESS, DETAIL: "BLOG LISTED SUCCESSFULLY!", BLOGDATA: SERIALIZED_DATA }, status.HTTP_200_OK)


    # CREATE FUNCTION

    def create(self, request):
        try:
            title = request.data['title']
            content = request.data['content']
            publish = request.data['publish']
            print(title, content, publish)
        except ValueError:
            return Response({ STATUS: FAILURE, DETAIL: "BLOG DATA FIELD MISSING."}, status.HTTP_204_NO_CONTENT)
        USER = Author.objects.get(user__id=request.user.id)
        return BLOG_CREATE(request, USER, title, content, publish)


    # DELETE FUNCTION

    def destroy(self, request, pk=None):
        try:
            BLOG_ID = request.data['blog_Id']
        except KeyError:
            return Response({ STATUS: FAILURE, DETAIL: "BLOG ID MISSING."}, status.HTTP_204_NO_CONTENT)
        USER = Author.objects.get(user__id=request.user.id)
        # Check if the USER has the right to delete the blog or not
        try: 
            BLOGDATA =  Blog.objects.get(Id = BLOG_ID, created_by = USER)
            BLOGDATA.is_active = False
            BLOGDATA.save()
        except (Blog.DoesNotExist, ValueError, SyntaxError, KeyError):
            return Response({ STATUS: FAILURE, DETAIL: "BLOG OWNERSHIP NOT MATCH."}, status.HTTP_200_OK)
        return Response({ STATUS: SUCCESS, DETAIL: "BLOG REMOVED SUCCESSFULLY!" }, status.HTTP_200_OK)


    # COMMENT FUNCTION

    def comment(self, request):
        try:
            BLOG_ID = request.data['blog_Id']
            COMMENT = request.data['comment']
        except KeyError:
            return Response({ STATUS: FAILURE, DETAIL: "BLOG ID MISSING."}, status.HTTP_204_NO_CONTENT)
        USER = Author.objects.get(user__id=request.user.id)
        try:
            BLOG = Blog.objects.get(Id = BLOG_ID)
            Comments.objects.create( created_by = USER, created_for = BLOG, created_at = datetime.now(), content = COMMENT)
        except (ValueError, SyntaxError, KeyError):
            return Response({ STATUS: FAILURE, DETAIL: "BLOG DOES NOT EXIST."}, status.HTTP_200_OK)
        return Response({ STATUS: SUCCESS, DETAIL: "COMMENT SUCCESS" }, status.HTTP_200_OK)