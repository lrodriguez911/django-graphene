import graphene
from graphene_django import DjangoObjectType
from books.models import Book, Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "price", "author")
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "id")

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    books = graphene.List(BookType)
    author = graphene.String(AuthorType)

    def resolve_books(self, info):
        return Book.objects.all()

    def resolve_author(self, info):
        return Author.objects.all()
    
    """ def resolve_hello(self, info):
        return f'{self}' """

schema = graphene.Schema(query=Query)