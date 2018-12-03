import re

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Q

User = get_user_model()


# Create your models here.
# Movie - Screening - Theater를 연결한다.
# Screening은 Movie와 Theater의 intermediate개체


# Dynamic Path for Meadia File upload_to
def main_directory_path(instance, filename):
    directory = instance.title
    return f'{directory}/{filename}'


def still_cut_directory_path(instance, filename):
    directory = instance.movie.title
    return f'{directory}/{filename}'


# 영화(Movie) 객체 모델
class Movie(models.Model):

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '영화'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 타이틀
    title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    # 감독
    director = models.CharField(max_length=30, blank=True, null=True)

    # 출연배우(cast) 관련 수정 가능 사항
    # 만약 배우를 새로운 object로 만들어 해당 배우 정보 및 출연작 정보를
    # 나타내도록 구현하고자 한다면 cast = models.ManyToManyField로 만들어야한다.

    # List(Array) object를 저장할 수 있는 modelfield는 없는 것으로 보인다
    # 이 경우 두 가지의 방법을 생각할 수 있다
    # 1) 'obj1, obj2, ... ' 의 charfield로 받은 후, 이후 사용시 split() method로
    # list도 추후에 환원한다.
    # 2) PostgreSQL을 사용하는 경우, 이들 library에서 ArrayField를 import하는 방법이 있다.

    # 출연 배우
    cast = models.CharField(max_length=128, blank=True, null=True)
    # 러닝타임
    duration_min = models.IntegerField(blank=True, null=True)
    # 개봉일
    opening_date = models.DateField(blank=True, null=True)
    # 영화 장르
    genre = models.CharField(max_length=32, blank=True, null=True)
    # 영화 줄거리
    description = models.TextField(max_length=512, blank=True, null=True)
    # 트레일러
    trailer = models.URLField(default='', blank=True, null=True)
    # 예매율
    reservation_score = models.FloatField(default=0, blank=True, null=True)
    # 상영 여부
    # timezone.now() 와 비교하여 전체 instance 일괄 업데이트
    # admin.action 버튼 생성
    now_show = models.BooleanField(default=False, blank=True, null=True)
    # 영화 메인 포스터
    main_img = models.ImageField(upload_to=main_directory_path, blank=True, null=True)
    # 예매 내역 저장
    # reservation_history = JSONField(blank=True, null=True)


# 스틸컷
# ArrayField 작동 불가
# Stillcut ForeignKey 모델을 생성하도록 한다.
class Stillcut(models.Model):
    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = '스틸컷'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    movie = models.ForeignKey(Movie, related_name='stillcuts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=still_cut_directory_path)


# 영화관(Theater) 객체 모델
class Theater(models.Model):
    def __str__(self):
        return self.sub_location

    class Meta:
        verbose_name = '극장'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 지역 대분류(광역시/도 단위 카테고리 ex) 서울 / 충청남도)
    location = models.CharField(max_length=10)
    # 지역 소분류 = 영화관 이름( ex)강남점, 신촌점)
    sub_location = models.CharField(max_length=15)
    # 세부 주소정보 : 텍스트 주소 or 경도/위도 사용
    address = models.CharField(max_length=50)

    # 상영중인 영화(Movie 목록)
    # 이후 immediate를 through로 설정히가나
    # related_name, related_query_name을 아래에 설정해야 한다.
    current_movies = models.ManyToManyField(
        Movie,
        through='Screening',
        related_name='theaters',
        related_query_name='theater',
    )


# 상영관(Auditorium) 객체 모델
class Auditorium(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '상영관'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 상영관 이름( ex) A관, 2관 .... )
    name = models.CharField(max_length=10)
    # 좌석수
    seats_no = models.IntegerField(default=0)
    # 소속 영화관
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)


# 상영(Screening) 객체 모델
class Screening(models.Model):
    def __str__(self):
        return self.auditorium

    class Meta:
        verbose_name = '상영'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 상영 영화
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, )
    # 상영 영화관(theater)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, )
    # 상영관(auditorium)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)


# 상영시간
# screening_time ArrayField 작동 불가.
class ScreeningTime(models.Model):
    def __str__(self):
        return str(self.time)

    class Meta:
        verbose_name = '상영 시간'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name='screening_times')
    time = models.DateTimeField()


# 좌석(Seat) 객체 모델
class Seat(models.Model):
    def __str__(self):
        return f'{self.row}행 {self.number}열'

    class Meta:
        verbose_name = '좌석'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 좌석 위치(행)
    row = models.IntegerField()
    # 좌석 위치(열)
    number = models.IntegerField()
    # 배치 상영관
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    # 예매 여부
    reservation_check = models.BooleanField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Seat, self).save()
        self.auditorium.seats_no = len(Seat.objects.filter(auditorium=self.auditorium))
        self.auditorium.save()

    def delete(self, using=None, keep_parents=False):
        super(Seat, self).delete()
        self.auditorium.seats_no = len(Seat.objects.filter(auditorium=self.auditorium))
        self.auditorium.save()


# 예매(Reservation) 객체 모델
class Reservation(models.Model):
    def __str__(self):
        return f'{self.user} / {self.screening}'

    class Meta:
        verbose_name = '예약'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    # 예매 유저
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # 예매 영화
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 예매 극장
    # theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    # 예매 상영 정보(상영관)
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, blank=True, null=True)
    # 예매 상영 시간
    screening_time = models.ForeignKey(ScreeningTime, on_delete=models.CASCADE, blank=True, null=True)
    # 예매 좌석 정보
    # seat = models.ForeignKey(SelectedSeat, on_delete=models.CASCADE)
    # 결제 완료 시점(예매 시간)
    # created_at = models.DateTimeField(auto_now_add=True)
    # 취소 여부 확인
    is_active = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Reservation, self).save()
        # 예매 취소(is_active = False) 전환 시에도 아래 예매율 변동 처리를 넣을 것.
        Instance = self.screening.movie
        active_reservations = Reservation.objects.filter(is_active=True)
        Instance.reservation_score = len(active_reservations.objects.filter(movie=Instance)) / len(active_reservations)
        Instance.save()


# 선택된 좌석
class SelectedSeat(models.Model):
    def __str__(self):
        return self.seat

    class Meta:
        verbose_name = '선택 좌석'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='selected_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

# 이후 reservation_type (ex) 청소년, 일반 ...)을 추가할 수 있다.
# 이 경우는 Reservation에 reservation_type 필드를 추가하고,
# class Reservation_Type(models.Model)을 추가한다.
# Charfield + Choice_Set을 구성한다.(or CHOICE FIELD를 사용)