from rest_framework.exceptions import ValidationError


VALID_URL = "https://www.youtube.com"

class LessonValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field_val = value.get('video_url')
        if field_val is not None and VALID_URL not in field_val:
            raise ValidationError('YouTube video only')


