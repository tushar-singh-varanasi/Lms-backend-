from django.urls import path
from .views import (LibrarianRegistrationView ,MemberRegistrationView,UserLogin,LogoutView,UserProfileAPIView,BookGETAndPost,BookGetdeleteupdate,
memberGetdeleteupdate,MemberregistrationbyLibrarian,BorrowBookAPIView,ReturnBookAPIView,BookListAPIView ,CurrentUserView,UserProfileDeleteView                   )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-librarian/', LibrarianRegistrationView.as_view(), name='user-registration'),
    path('register-member/',  MemberRegistrationView.as_view(), name='member-registration'),
    path('login/',  UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/',  UserProfileAPIView.as_view(), name='profile'),
    path('profile/',  UserProfileAPIView.as_view(), name='profile'),
    path('books/', BookGETAndPost.as_view(), name='book-list'),
    path('books/<int:pk>/', BookGetdeleteupdate.as_view(), name='book-detail'),
    path("meber-registration-by-librarian/", MemberregistrationbyLibrarian.as_view(), name="member-registration-by-librarian"),
    path("meber-update-delete/<int:pk>/", memberGetdeleteupdate.as_view(), name="meber-update"),
    path('books-member/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:book_id>/borrow/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('transactions/<int:transaction_id>/return/', ReturnBookAPIView.as_view(), name='return-book'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='delete-user-profile'),







]