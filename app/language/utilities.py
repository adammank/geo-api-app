from .serializers import LanguageSerializer


def get_or_create_languages(languages: "iterable"):

    if not languages:
        return

    language_names = []

    for language in languages:
        serializer = LanguageSerializer(data={"name": language})
        serializer.is_valid(raise_exception=True)
        language_names.append(serializer.save().name)

    return language_names
