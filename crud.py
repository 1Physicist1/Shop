import asyncio
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, name: str) -> User:
    user = User(name=name)
    session.add(user)
    await session.commit()
    print("user", user)
    return user

async def get_user_by_name(session:AsyncSession, name: str) -> User|None:
    stmt = select(User).where(User.name == name)
   # result: Result = await session.execute(stmt)
    #user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)
    print("found user", name, user)
    return user

async def create_user_profile(session: AsyncSession,
                              user_id: int,
                              first_name:str | None = None,
                              last_name:str | None = None,) -> Profile:
    profile = Profile(user_id=user_id,
                      first_name=first_name,
                      last_name=last_name,)
    session.add(profile)
    await session.commit()
    return profile

async def show_users_with_profiles(session:AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    #result: Result = await session.execute(stmt)
    #users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)

async def create_post(session:AsyncSession,user_id: int, *posts_titles: str) -> list[Post]:
    posts = [Post(title=title, user_id=user_id)
             for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts

async def get_users_with_posts(session:AsyncSession):
    #stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(
        #joinedload(User.posts)
        selectinload(User.posts),
    ).order_by(User.id)
    #users = await session.scalars(stmt)
    ##result: Result = await session.execute(stmt)
    #users = result.unique().scalars()
    ##users = result.scalars()
    users = await session.scalars(stmt)

    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)

async def get_users_with_posts_and_profiles(session:AsyncSession):
    stmt = select(User).options(
        joinedload(User.profile),
        selectinload(User.posts),
    ).order_by(User.id)

    users = await session.scalars(stmt)

    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)

async def get_posts_with_author(session:AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)

async def get_profiles_and_users_with_posts(session:AsyncSession):
    stmt = (
        select(Profile)
        .order_by(Profile.id)
        .options(
            joinedload(Profile.user).selectinload(User.posts)
        )
        .order_by(Profile.id)

    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.id, profile.user)
        print(profile.user.posts)

async def main():
    async with db_helper.session_factory() as session:
        #await create_user(session=session, name="Piter")
       # await create_user(session=session, name="Lui")
        #await create_user(session=session, name="Mary")
       # user_piter= await get_user_by_name(session=session, name= "Piter")
       # user_lui = await get_user_by_name(session=session, name= "Lui")
       # await create_user_profile(session=session,user_id=user_piter.id, first_name="Piter")
       # await create_user_profile(session=session, user_id=us er_lui.id, first_name="Piter", last_name="Black")
        #await show_users_with_profiles(session)
       # await create_post(session, user_lui.id, "SQLA 2.0", "SQLA 3/0")
        #await create_post(session, user_piter.id, "Football", "Computer games")
     #await get_users_with_posts(session)
       #await get_posts_with_author(session)
        #await get_users_with_posts_and_profiles(session)
        await get_profiles_and_users_with_posts(session)


if __name__ == '__main__':
    asyncio.run(main())