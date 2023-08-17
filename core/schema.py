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
        fields = ("id", "first_name", "last_name", "books")
        

class CreateBookMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        author = graphene.ID()

    book = graphene.Field(BookType)

    def mutate(self, info, title, description, price, author):
        book = Book(title=title, description=description, price=price, author=author)
        book.save()
        return CreateBookMutation(book=book)
    
class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        author = graphene.ID()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title, description, price, author):
        book = Book.objects.get(pk=id)
        book.title = title
        book.description = description
        book.price = price
        book.author = author
        book.save()
        return UpdateBookMutation(book=book)
    
class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message="Book deleted successfully!")

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    books = graphene.List(BookType)
    book = graphene.Field(BookType, id=graphene.ID())
    authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.ID())

    def resolve_books(self, info):
        return Book.objects.all()
    
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_authors(self, info):
        return Author.objects.all()
    
    """ def resolve_hello(self, info):
        return f'{self}' """
    
class Mutation(graphene.ObjectType):
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()
    update_book = UpdateBookMutation.Field()
    create_author = graphene.Field(AuthorType, first_name=graphene.String(), last_name=graphene.String())

schema = graphene.Schema(query=Query, mutation=Mutation)