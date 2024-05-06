from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
# Add validators to the Author and Post models such that:

#     Post title is sufficiently clickbait-y and must contain one of the following:
#         "Won't Believe"
#         "Secret"
#         "Top"
#         "Guess"

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=True)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, address):
        authors = []
        for author in Author.query.all():
            authors.append(author.name)
        if not address:
            raise ValueError("Name must be filled out.")
        elif address in authors:
            raise ValueError("Name must be unique.")

        return address
    
    @validates('phone_number')
    def vaidate_number(self, key, address):
        print(address)
        if not int(address):
                raise ValueError("Number must contain only digits")
        if not len(address) == 10:
            raise ValueError("Number not 10 digits")
        return address

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, address):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        clickbait_count = 0
        if not address:
            raise ValueError("Post must have a title.")
        for word in clickbait_words:
            if word in address:
                clickbait_count = clickbait_count + 1
        if clickbait_count == 0:
            raise ValueError("Title not clickbait-y enough.")
        return address
    
    
    @validates('content')
    def validate_length(self, key, address):
        if len(address) != 250:
            if len(address) < 250:
                raise ValueError("Post too short.")
        return address
    
    @validates('summary')
    def validates_summary(self, key, address):
        if len(address) > 250:
            raise ValueError("Post too long.")
        return address

    @validates('category')
    def validates_category(self, key, address):
        print(address)
        categories = ["Fiction", "Non-Fiction"]
        if address not in categories:
            raise ValueError("Category must be Fiction or Non-Fiction")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
