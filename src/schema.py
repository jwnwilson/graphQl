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


class Comic(ObjectType):
    id = String()
    digitalId = String()
    title = String()
    issueNumber = Int()

    def resolve_comic(self, info):
        return json2obj(API.comic.get(self.comic_id))


class Query(ObjectType):
    comics = List(
        Comic,
        comic_id=String()
    )

    def resolve_comics(self, info, comic_id):
        return json2obj(API.comic.find(comic_id=comic_id))
