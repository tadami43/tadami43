from django.shortcuts import render
# django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView
# Create your views here.

class IndexView(TemplateView):
    # トップページからのビュー
    # index.htmlをレンダリングする
    template_name = 'index.html'