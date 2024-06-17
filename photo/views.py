from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
# django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView, ListView
# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
# method_decorator
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost
# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView
# django.views.genericからDeleteViewをインポート
from django.views.generic import DetailView
#tuiks
from django.db.models import F
 
from django.shortcuts import redirect, get_object_or_404
from .models import PhotoPost
from django.urls import reverse

 
def mypage_view(request):
    # ビューのロジックを記述する
    return render(request, 'base.html')
 
def nice_success(request, pk):
    post = get_object_or_404(PhotoPost, pk=pk)
    post.nice += 1  # niceフィールドを1増やす
    post.save()     # 保存する
    return redirect('mypage_view')  # 成功したらどこかにリダイレクトする
 
class IndexView(ListView):
    '''トップページのビュー
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # モデルBlogPostのオブジェクトにorder_by()を適用して
    # 投稿日時の降順で並べ替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 15
    

# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN＿URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー
    
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに投稿する
    
    Attributes:
        form_class: モデルとフィールドが登録されたフォームクラス
        template_name: レンダリングするテンプレート
        success_url: データベースへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPosuFormをフォームクラスとして登録
    form_class = PhotoPostForm
    #レンダリングするテンプレート
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う
        paramaters:
            form(django.forms.Form):
                form_classに格納されているphotoPostFormオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()に戻り値を返すことで、
                success_urlで設定されているURLにリダイレクトされる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit = False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    
    Attributes:
        template_name:レンダリングするテンプレート
    '''
    # index.htmlをレンダリング
    template_name = 'post_success.html'

class CategoryView(ListView):
    '''カテゴリページのビュー
    
    Attribute:
        template_name:レンダリングするテンプレート
        paginate_by:1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 15

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
            クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # categoryキーの値(Categoryテーブルのid)を取得する
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories
    
class UserView(ListView):
    '''ユーザーの投稿一覧ページのビュー
    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # ページに表示するレコードの件数
    paginate_by = 15

    def get_queryset(self):
        '''クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Return: クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        # field(フィールド名=id)で絞り込む
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list
    
class DetailView(DetailView):
    '''詳細ページのビュー

    投稿記事の詳細を表示するのでDetailViewを継承する
    Attributes:
        template_name: レンダリングするテンプレート
        model: モデルのクラス
    '''
    # post.htmlをレンダリングする
    template_name = 'detail.html'
    # ページに表示するレコードの件数
    model = PhotoPost

class MypageView(ListView):
    '''マイページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
    '''
    # mypage.htmlをレンダリングする
    template_name = 'mypage.html'
    # ページに表示するレコードの件数
    paginate_by = 15

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Return:
            クエリによって取得されたレコード
        '''
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている、
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(user = self.request.user).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return queryset
    
class PhotoDeleteView(DeleteView):
    '''レコードの削除を行うビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
        success_url: 削除完了後のリダイレクト先のURL
    '''
    # 操作の対象はPhotoPostモデル
    model = PhotoPost
    # Photo_delete.htmlをレンダリング
    template_name = 'photo_delete.html'
    # 処置完了後にマイページにリダイレクト
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
        '''レコードの削除を行う

        Parameters:
            self:PhotoDeleteViewオブジェクト
            requiest:WSGIRequest(HttpRequest)オブジェクト
            args:引数として渡される辞書(dict)
            kwargs:キーワード月の辞書(dict)
            {'pk':21}のようにレコードのidが渡される
        Returns:
            HttpResponseRedirect(success_url)を返して
            success_urlにリダイレクト
        '''
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)


class ResultView(ListView):
    template_name = 'result_list.html'
    paginate_by = 15
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            result_list = PhotoPost.objects.filter(
                title__icontains=query).order_by('-posted_at')
        else:
            result_list = PhotoPost.objects.all().order_by('-posted_at')
        return result_list
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import PhotoPost
 
def count(request, pk):
    # 指定されたPKに一致するPhotoPostオブジェクトを取得する
    post = get_object_or_404(PhotoPost, pk=pk)
   
    # セッションから、このユーザーがこの投稿にいいねをしたかどうかをチェック
    liked_posts = request.session.get('liked_posts', [])
   
    # この投稿がユーザーのいいねリストにあるかどうかをチェック
    if pk in liked_posts:
        # 既にいいねを押している場合は、いいねを取り消す
        post.nice -= 1
        liked_posts.remove(pk)
    else:
        # いいねを追加する
        post.nice += 1
        liked_posts.append(pk)
   
    # セッションにいいねした投稿のリストを保存する
    request.session['liked_posts'] = liked_posts
   
    # 投稿を保存する
    post.save()
   
    # リダイレクトする
    return redirect('http://127.0.0.1:8000/')

class AscView(ListView):
    template_name = 'asc.html'
    queryset = PhotoPost.objects.order_by('posted_at')
    paginate_by = 15

class NiceDescView(ListView):
    template_name = 'nice_desc.html'
    queryset = PhotoPost.objects.order_by('-nice')
    paginate_by = 15





def result_list(request):
    query = request.GET.get('query', '')  # クエリを取得する。なければ空文字列をデフォルトとする。

    context = {
        'query': query,
        # 他の必要なコンテキストデータを追加する
    }
    return render(request, 'result_list.html', context)
