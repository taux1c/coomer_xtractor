
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class SavedUrl(Base):
    __tablename__ = "saved_urls"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    url = Column(Text, unique=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"<SavedUrl(url={self.url})>"

    def __str__(self):
        return f"{self.url}"

    def save(self, profile):
        engine = create_engine(profile.db_string)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        with Session() as session:
            session.add(self)
            session.commit()
        engine.dispose()

async def add_to_database(urls, profile):
    try:
        for url in urls:
            saved_url = SavedUrl(url)
            saved_url.save(profile)
    except Exception as e:
        print(f"Encountered {e} while trying to add {urls} to the database.")
        return False

def not_in_database(urls, profile):
    not_in_database = []
    engine = create_engine(profile.db_string)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        for url in urls:
            result = session.query(SavedUrl).filter(SavedUrl.url == url).first()
            if result is None:
                not_in_database.append(url)
    engine.dispose()
    return not_in_database
