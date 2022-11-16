from typing import List
from fastapi import status, HTTPException, APIRouter, Depends
from typing import Optional
from .. import schemas, main, oauth2 # .. go show that we are inside a folder in the main directory and we need to go up a directory which is from the folder to the main directory, therefore two dots


router = APIRouter(prefix="/posts", tags=['Posts']) #defining the router; giving prefix of the route helps to avoid typing route in every app decorator
                                                    #We use tags to group the posts functions; Since it is a list, we can add more than one tag if required; check /docs 

#Create Posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #To change the standard 200 status code to 201 since it is the more appropriate code when creating smth
def create_posts(post: schemas.PostCreate, current_user: str = Depends(oauth2.current_user)): #newpost stores data as pydantic model
    main.cursor.execute("""INSERT INTO posts (title, content, publish, user_id) VALUES (%s, %s, %s, %s) RETURNING *""", #In the query string, you always have to use %s placeholders, even when passing a number. All Python objects are converted by Psycopg2 in their SQL representation, so they get passed to the query as strings.
                    (post.title, post.content, post.publish, current_user.id)) #Using returning so that the user gets the data back which we then save it in new_post
    new_post = main.cursor.fetchone()
    main.conn.commit() # To save cahnges and insert it to the database like we press "save data changes" in pgadmin
    #post_dict = newpost.dict() #To convert pydantic model to a dict
    #post_dict['ID'] = randrange(0,10000000) 
    #my_posts.append(post_dict)
    return new_post


#Get Posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(limit: int = 10, skip: int = 0, search: Optional[str] = ""): #limit is the query parameter here (so is skip) which is an int with default value = 5. To use it, domain.com/posts?limit=x; Here, Optional means that we don't necessarly have to give "search" in which case, default value is ""
    search = '%%%s%%' % search #No idea how this works but use this when we want to filter using LIKE
    main.cursor.execute(""" SELECT * FROM posts WHERE title LIKE %s LIMIT %s OFFSET %s;""", (search, limit, skip)) 
    posts = main.cursor.fetchall() #The above statement only passes our SQL statement. To run it, we need to run this command; Fetchall() is used when we retrieve many rows
    return posts


#Get Specific Post
@router.get("/{id}", response_model=schemas.PostResponse) #{ID} is a path parameter. It is always returned as a string
def get_post(id: int):  #To convert the ID which is a string to int;
    main.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = main.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with ID {id} was not found!')
    return post


#Update Post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, current_user: int = Depends(oauth2.current_user)):
    main.cursor.execute("""SELECT user_id FROM posts WHERE id = %s""", (id,))
    user_id = main.cursor.fetchone()
    if user_id != None:
        user_id = user_id['user_id']
        if int(current_user.id) == user_id:
            main.cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", 
                                (post.title, post.content, id,))
            updated_post = main.cursor.fetchone()
            main.conn.commit()
        else:   
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with ID {id} does not exist')
    return updated_post


#Delete Post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: str = Depends(oauth2.current_user)):
    main.cursor.execute("""SELECT user_id FROM posts WHERE id = %s""", (id,))
    user_id = main.cursor.fetchone()
    if user_id != None:
        user_id = user_id["user_id"]
        if int(current_user.id) == user_id:
            main.cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
            deleted_post = main.cursor.fetchone()
            main.conn.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Post with ID {id} does not exist')
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT) #since we passed a 204, fastapi does not expect us to return data. Therefore we cannot return data 