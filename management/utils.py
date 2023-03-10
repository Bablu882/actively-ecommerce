from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp))


generate_token = TokenGenerator()

###--------------------------------------------------------------------------------------

from django.utils.text import slugify
import random
import string


from django.conf import settings


SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)


def code_generator(size=5, chars=string.ascii_lowercase + string.digits):

    return ''.join(random.choice(chars) for _ in range(size))


def create_shortcode(instance):
    #new_slug = code_generator(size=size)
    #new_slug = f"{slugify(instance.name)}-{code_generator()}"
    new_slug = f"{slugify(instance.user.username , allow_unicode=True)}-{code_generator()}"
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=new_slug).exists()
    if qs_exists:
        return create_shortcode(instance)
    return new_slug
