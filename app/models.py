from django.core.validators import RegexValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from users.models import User


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # タイトル（手動入力）
    title = models.CharField(
        verbose_name='タイトル',
        blank=True,
        null=True,
        max_length=100,
        default='',
    )

    # 画像ファイル
    image = models.ImageField(
        upload_to='images/',
        verbose_name='画像',
        blank=True,
        null=True,
    )

    # サムネイル（画像ファイルから自動生成）
    image_thumbnail = ImageSpecField(source='image',
                                     autoconvert=True,
                                     processors=[ResizeToFill(400, 300)],
                                     format='JPEG',
                                     options={'quality': 60})

    # 撮影時間（Exifより取得）
    shooting_time = models.DateTimeField(
        verbose_name='撮影時間',
        blank=True,
        null=True,
    )

    # 撮影時間（Exifより取得）
    geo_location = models.CharField(
        verbose_name='経度緯度',
        blank=True,
        null=True,
        max_length=100,
        default='',
        validators=[RegexValidator(
            regex=r'-?([0-8]?[0-9]|90)\.[0-9]{1,6},\s?-?((1?[0-7]?|[0-9]?)[0-9]|180)\.[0-9]{1,6}$',
            message='緯度：-90.000000 ~ 90.000000 / 経度: -180.000000 ~ 180.000000（小数点以下６桁以内）を指定します。'
                    '緯度と統計はカンマ「,」で区切ります。例：35.658581,139.745433',
        )]
    )

    # 撮影場所 経度緯度を元にMapAPIから取得
    location = models.CharField(
        verbose_name='撮影場所',
        blank=True,
        null=True,
        max_length=100,
        default='',
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return '%06d' % self.id

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '画像データ'
        verbose_name_plural = '画像データ'
