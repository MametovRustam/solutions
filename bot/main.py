import asyncio
import random
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    url = Column(String)

TOKEN = "7643621620:AAE_4V78zesCLPve7gMi7kZd7VVOE8i_13k"
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_message = (
        "Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете :)\n\n"
        "- Чтобы я запомнил статью, мне достаточно передать ссылку на неё. К примеру, http://example.com\n"
        "- Чтобы получить случайную статью, достаточно передать мне команду /getarticle. Но помни! "
        "Отдавая статью тебе на прочтение, она больше не хранится в моей базе. Так что тебе нужно её изучить."
    )
    await message.answer(welcome_message)

@router.message(Command("getarticle"))
async def get_random_article(message: types.Message):
    session = Session()
    try:
        user_id = message.from_user.id
        articles = session.query(Article).filter(Article.user_id == user_id).all()
        if not articles:
            await message.answer("Вы пока не сохранили ни одной статьи. Если нашли что-то стоящее, я жду!")
            return

        random_article = random.choice(articles)
        await message.answer(f"Вы хотели прочитать: {random_article.url}\nСамое время это сделать!")
        session.delete(random_article)
        session.commit()

    except Exception as e:
        await message.answer("Произошла ошибка при получении статьи.")
        print(f"Ошибка: {e}")
    finally:
        session.close()

@router.message()
async def save_article(message: types.Message):
    if message.text.startswith(('http://', 'https://')):
        session = Session()
        try:
            user_id = message.from_user.id
            existing = session.query(Article).filter(Article.url == message.text, Article.user_id == user_id).first()
            if existing:
                await message.answer("Упс, вы уже это сохраняли.")
                return

            article = Article(url=message.text, user_id=user_id)
            session.add(article)
            session.commit()
            await message.answer("Сохранил, спасибо!")

        except IntegrityError:
            await message.answer("Упс, вы уже это сохраняли.")
            session.rollback()
        except Exception as e:
            await message.answer("Произошла ошибка при сохранении статьи.")
            session.rollback()
            print(f"Ошибка: {e}")
        finally:
            session.close()
    else:
        await message.answer("Это не ссылка :(\n- Чтобы я запомнил статью, мне достаточно передать ссылку на неё. К примеру, http://example.com")

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
