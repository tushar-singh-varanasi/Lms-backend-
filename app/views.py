# views.py

from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import( UserRegistration ,Userloginserilaizer,UserprofileSerilizer,
                         BookSerializer,TransactionSerializer,UserRegistrationSerializer,
                         )
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser,Book,Transaction
from django.http import Http404
from .permission import IsLibrarianOrReadOnly




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class  LibrarianRegistrationView(APIView):
     def post(self,request,format=None):
        Serilizer=UserRegistration(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        user=Serilizer.save()
        print('okay.......')
        Librarian_group,create= Group.objects.get_or_create(name='Librarian')
        Librarian_group.user_set.add(user)
        token=get_tokens_for_user(user)
        # print(token)
        return Response({'token':token,'msg':'Registration Successfuly'},
        status=status.HTTP_201_CREATED)
   
        
class  MemberRegistrationView(APIView):
    def post(self,request,format=None):
        Serilizer=UserRegistration(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        user=Serilizer.save()
        Librarian_group,create= Group.objects.get_or_create(name='Member')
        Librarian_group.user_set.add(user)

        token=get_tokens_for_user(user)
        # print(token)
        return Response({'token':token,'msg':'Registration Successfuly'},
        status=status.HTTP_201_CREATED)
    
class MemberregistrationbyLibrarian(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        members = CustomUser.objects.filter(groups__name='Member')
        serializer = UserRegistrationSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            librarian_group, created = Group.objects.get_or_create(name='Member')
            librarian_group.user_set.add(user)
            return Response({'msg': 'Registration Successful', 'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class memberGetdeleteupdate(APIView):
    permission_classes=[IsAuthenticated]
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = UserRegistrationSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = UserRegistrationSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# here member

   

class UserLogin(APIView):
    def post(self,request,format=None):
        Serilizer=Userloginserilaizer(data=request.data)
        Serilizer.is_valid(raise_exception=True)
        username=Serilizer.data.get('username')
        password=Serilizer.data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_error':['Email or password not match']}},status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        # Get the user's token
        user_token = request.auth

        if user_token:
            # Delete the token
            user_token.delete()

            # Optional: Blacklist the token on the server side

            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)        
        

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if request.user.groups.filter(name='Librarian').exists():
            serializer = UserprofileSerilizer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BookGETAndPost(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        book=Book.objects.all()
        serializer=BookSerializer(book,many=True)
        data=serializer.data
        return Response(data)
    
    def post(self,request,format=None):
        serializer=BookSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED) 

class BookGetdeleteupdate(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        student=self.get_object(pk)
        serializer=BookSerializer(student)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        student=self.get_object(pk)
        serializer=BookSerializer(student,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=serializer.data
        return Response(data)
    
    def delete(self, request, pk, format=None):
        student=self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class BookListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
        
# BorrowBookAPIView
class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id, status='AVAILABLE')
        user = request.user
        transaction = Transaction(book=book, user=user)
        transaction.save()
        book.status = 'BORROWED'
        book.save()
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# ReturnBookAPIView
class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserprofileSerilizer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    

class UserProfileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            user.delete()
            return Response({"detail": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   