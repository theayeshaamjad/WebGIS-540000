from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from districts.models import District
from .models import Facility


class FacilitySerializer(GeoFeatureModelSerializer):
    district = serializers.SerializerMethodField()
    class Meta:
        model = Facility
        geo_field = "geom"
        fields = ["id", "name", "kind", "added", "district"]
        read_only_fields = ["added"]

    def get_district(self, obj):
        district = District.objects.filter(geom__contains=obj.geom).first()
        return district.name if district else None

    def validate_geom(self, value):
        if not District.objects.filter(geom__contains=value).exists():
            raise serializers.ValidationError(
                "This point is not inside any district of Pakistan."
            )
        return value
