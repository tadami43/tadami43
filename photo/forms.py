from django.forms import ModelForm
from .models import PhotoPost

class PhotoPostForm(ModelForm):
    '''ModelFormのサブクラス
    '''
    class Meta:
        '''Model Formのインナークラス
        
        Attributes:
            model: モデルのクラス
            field: フォームで使用するモデルのフィールドを指定
        '''
        model = PhotoPost
        fields = ['category', 'title', 'comment', 'image1', 'image2']