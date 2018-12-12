from rest_framework import serializers
from mappings.models import Movie, Theater, Screening


# Ticket Movie Serializer
class TicketMovieSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'pk',
            'title',
            'show'
        )

    def get_show(self, movie):
        pk_list = self.context.get("show")
        if movie.pk in pk_list:
            return True
        else:
            return False


# Ticket Theater Serializer
class TicketTheaterSubLocationSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = Theater
        fields = (
            'pk',
            'sub_location',
            'show'
        )

    def get_show(self, theater):
        pk_list = self.context.get("show")
        if theater.pk in pk_list:
            return True
        else:
            return False


class TicketTheaterLocationSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=64)

    def to_representation(self, instance):
        data = super(TicketTheaterLocationSerializer, self).to_representation(instance)
        theater_by_filter = [theater for theater in Theater.objects.all()
                             if theater.location == instance["location"]]
        serializer = TicketTheaterSubLocationSerializer(
            theater_by_filter,
            many=True,
            context={"show": self.context.get("show")}
        )
        num = {"num": len(serializer.data)}
        return [data, {"theater_set": serializer.data}, num]



# Ticket Screening DateTime Serializer
class TicketScreeningTimeSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField()
    class Meta:
        model = Screening
        fields = (
            'pk',
            'times',
        )

    def get_times(self, screening):
        return screening.time.time()

class TicketScreeningDateTimeSerializer(serializers.Serializer):
    date = serializers.DateField()

    # serializer.data 대신 validated_data를 쓴다면 to_internal_value로 데이터를 조작한다.
    # def to_internal_value(self, data):
    #     return data

    # serializer.data 를 쓸 때에만 to_representation을 거쳐간다.
    def to_representation(self, instance):
        data = super(TicketScreeningDateTimeSerializer, self).to_representation(instance)
        screening_by_filter = [screen for screen in Screening.objects.all()
                               if screen.time.date() == instance["date"] and screen.pk in self.context.get("show")]
        serializer = TicketScreeningTimeSerializer(screening_by_filter, many=True)
        if serializer.data:
            show = {"show": True}
        else:
            show = {"show": False}
        return [data, {"time_set": serializer.data}, show]

# class TicketLocationSerializer(serializers.ModelSerializer):
#     nums = serializers.SerializerMethodField()
#     theaters = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Theater
#         fields = (
#             'location',
#             'nums',
#             'theaters'
#         )
#
#     def get_nums(self, theater):
#         count = 0
#         for pk in self.context.get("selected"):
#             if theater.location == Theater.objects.get(pk=pk).location:
#                 count += 1
#         return count
#
#     def get_theaters(self, theater):
#         theater_by_location = Theater.objects.filter(location=theater.location)
#         serializers = TicketSubLocationSerializer(
#             theater_by_location,
#             context={"selected": self.context.get("selected")},
#             many=True
#         )
#         return serializers.data