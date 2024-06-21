from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import inspect

import asyncio
from sqlalchemy.future import select
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    

 #Engine creation
engine_sync = create_engine('sqlite:///mydatabase2.db', echo=True)

# Creating a table
Base.metadata.create_all(engine_sync)

# Creating a session
Session = sessionmaker(bind=engine_sync)
session_sync = Session()

new_user = User(name='Ayhan')
session_sync.add(new_user)
session_sync.commit()

# Triggering events by performing database operations
DATABASE_URL = "sqlite+aiosqlite:///mydatabase2.db"
engine_async = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)
#Example-1
#function-1 for asynchronous query
async def get_record_by_id(record_id: int):
    async with AsyncSessionLocal() as session:
        
        #query = session.query(User).filter(User.id == record_id).one_or_none()
        # AttributeError: 'AsyncSession' object has no attribute 'query'
        
        try:
            data = select(User).where(User.id == record_id)
            result = await session.execute(data)
            record = result.fetchone()
            #select Usage: A more modern and declarative method.
            #Methods such as fetchone, fetchall, scalar are used to get the results.
        except Exception as e:
            print("Hata:", e)
        return record
    
#Example-2    
#function-2 for asynchronous query     
async def get_record_by_id2(record_id: int):
    async with AsyncSessionLocal() as session:      
        try:
            data2 =await session.execute(
            select(User).where(User.id == record_id))
            record2=data2.fetchone()
            
        except Exception as e:
            print("Hata:", e)
        
        return record2

    
# A main loop to use the asynchronous Function
async def main():   
    record = await get_record_by_id(1)
    if record:
            print("id-------->", record[0].id)
            print("name------>",record[0].name)       
    else:
        print("Record not found.")
        
    record2 = await get_record_by_id2(2)
    if record2:
            print("id-------->", record2[0].id)
            print("name------>",record2[0].name)       
    else:
        print("Record not found.")

asyncio.run(main())
