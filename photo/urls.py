from django.urls import path
from . import views

# URLパターンを逆引きできるように名前を付ける
app_name = 'photo'

# URLパターンを登録変数
urlpatterns = [
    # photoアプリへのアクセスは viewsモジュールのIndexViewを実行
    path('', views.IndexView.as_view(), name='index'),

    # 写真投稿ページへのアクセスは viewsモジュールのCreatePhotoViewを実行
    path('post/', views.CreatePhotoView.as_view(), name='post'),

    #　投稿完了ページへのアクセスは viewsモジュールのPostSuccessViewを実行
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
]