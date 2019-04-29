import os

from gevent import monkey
from flask import Flask
from flask_graphql import GraphQLView
from graphql.execution.executors.gevent import GeventExecutor

from graphene import Schema

from schema import Query

monkey.patch_all()

view_func = GraphQLView.as_view(
    'graphql',
    schema=Schema(query=Query),
    executor=GeventExecutor(),
    graphiql=True
)

app = Flask(__name__)
app.add_url_rule('/graphql', view_func=view_func)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
