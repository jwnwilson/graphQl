from collections import namedtuple
import json

from graphene import ObjectType
from graphene import String
from graphene import Boolean
from graphene import List
from graphene import Field
from graphene import Int
from graphene import UUID
from graphene import Float

from api import Api


API = Api()


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(json.dumps(data), object_hook=_json_object_hook)


class MarvelSummary(ObjectType):
    resourceURI = String()
    name = String()
    role = String()


class MarvelDataContainer(ObjectType):
    offset = Int()
    limit = Int()
    total = Int()
    count = Int()


class CharacterDataContainer(MarvelDataContainer):
    results = List(lambda: Character)


class ComicSummary(MarvelSummary):
    pass


class CharacterSummary(MarvelSummary):
    pass


class StorySummary(MarvelSummary):
    pass


class EventSummary(MarvelSummary):
    pass


class MarvelList(ObjectType):
    available = Int()
    returned = Int()
    collectionURI = String()


class ComicList(ObjectType):
    items = List(ComicSummary)


class StoryList(ObjectType):
    items = List(StorySummary)


class EventList(ObjectType):
    items = List(EventSummary)


class Character(ObjectType):
    id = String()
    name = String()
    description = String()
    modified = String()
    resourceURI = String()
    urls = List(String)
    thumbnail = String()
    comics = Field(ComicList)
    stories = Field(StoryList)
    events = Field(EventList)
    # series = Field(SeriesList)


class CharacterList(MarvelList):
    items = List(CharacterSummary)
    details = List(CharacterDataContainer)

    def resolve_details(self, info):
        characters = []
        if self.items:
            character_ids = [
                c.resourceURI.split('/')[-1] for c in self.items
            ]

            characters = API.character.get_batch(character_ids)
        return json2obj(characters)


class Comic(ObjectType):
    id = String()
    digitalId = String()
    title = String()
    issueNumber = Int()
    variantDescription = String()
    description = String()
    modified = String()
    characters = Field(CharacterList)
    stories = Field(StoryList)
    events = Field(EventList)


class Query(ObjectType):
    comic = Field(
        Comic,
        id=String(required=True)
    )
    comics = List(
        Comic,
    )

    def resolve_comic(self, info, id):
        return json2obj(API.comic.get(id))

    def resolve_comics(self, info):
        return json2obj(API.comic.find())
