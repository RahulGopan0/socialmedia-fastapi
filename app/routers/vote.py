from fastapi import APIRouter, status, Depends, HTTPException
from .. import  main, oauth2

router = APIRouter(prefix="/vote", tags=['Vote']) 

@router.get("/{id}", status_code=status.HTTP_201_CREATED)
def vote(id: int, current_user: str = Depends(oauth2.current_user)): 
    count: int = 0
    main.cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    temp = main.cursor.fetchone()
    if temp != None:
        while True:
            try:
                main.cursor.execute("""INSERT INTO votes (post_id, user_id) VALUES (%s, %s) RETURNING *""", 
                                    (id, current_user.id))
                post_vote = main.cursor.fetchone()
                main.conn.commit()
                count = count + 1
                print(count)
                break
            except:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted")   
        main.cursor.execute("""SELECT total_votes FROM posts WHERE id = %s""", (id,))
        total_votes = main.cursor.fetchone()
        total_votes = total_votes["total_votes"]
        new_total = total_votes + count
        main.cursor.execute("""UPDATE posts SET total_votes = %s WHERE id = %s RETURNING *""", 
                            (new_total, id,))
        updated_post = main.cursor.fetchone()
        main.conn.commit()
        return updated_post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID {id} not found')