from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    '''サインアップページのビュー
    
    '''
    # forms.pyで定義したフォームのクラス
    form_class = CustomUserCreationForm
    # レンダリングするテンプレート
    template_name = "signup.html"
    # サインアップ完了のリダイレクト先のURLパターン
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド

        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録を行う
        
        paramaters:
            form(django.forms.From):
            form_classに格納されているCustomUserCreationFormオブジェクト
        Return:
            HttpsResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り値を返すことで、
                success_urlで設定されているURLにリダイレクトさせる
        '''
        # formオブジェクトのフィールド値をデータベースに保存
        user = form.save()
        self.object = user
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpsResponseRedirect)
        return super().form_valid(form)
    
class SignUpSuccessView(TemplateView):
    '''サインアップ完了ページのビュー
        
    '''
    # レンダリングするテンプレート
    template_name = "signup_success.html"
