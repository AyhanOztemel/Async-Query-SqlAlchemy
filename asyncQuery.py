from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
import asyncio
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

#Engine creation
engine_sync = create_engine('sqlite:///mydatabase.db', echo=True)

# Creating a table
Base.metadata.create_all(engine_sync)

# Creating a session
Session = sessionmaker(bind=engine_sync)
session_sync = Session()

# Database operations
new_user = User(name='Ayhan')
session_sync.add(new_user)
session_sync.commit()

DATABASE_URL = "sqlite+aiosqlite:///mydatabase.db"
engine_async = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)

#asynchronous query
async def get_record_by_id(record_id: int, delay: int = 0):
    await asyncio.sleep(delay)  # Delay simulation
    async with AsyncSessionLocal() as session:
        try:
            data = select(User).where(User.id == record_id)
            result = await session.execute(data)
            record = result.fetchone()
        except Exception as e:
            print("Hata:", e)
            record = None
        return record

async def main():
    # Let's add different delay times to different queries
    tasks = [
        get_record_by_id(10, 23),  # 23 seconds delay
        get_record_by_id(14, 12),  # 12 seconds delay
        get_record_by_id(15, 5),  # 5 seconds delay
        get_record_by_id(13, 4)   # 4 seconds delay
    ]

     #Let's get the results as the tasks are completed(enumerate->asynchronous)
    for i, task in enumerate(asyncio.as_completed(tasks), start=1):
        record = await task
        if record:
            print(f"record{i}---->id-------->", record[0].id)
            print(f"record{i}---->name------>", record[0].name)
        else:
            print(f"Record{i} not found.")

asyncio.run(main())
