from app import app, db, User, Post, Comment, ChatMessage

def run_tests():
    with app.app_context():
        db.drop_all()
        db.create_all()
        client = app.test_client()

        # create user
        client.post('/register', data={'username':'poster','password':'p'})

        # create post
        rv = client.post('/post/new', data={'title':'Hello','body':'First post body'}, follow_redirects=True)
        assert b'Hello' in rv.data

        # comment on post
        post = Post.query.first()
        assert post is not None
        rv = client.post(f'/post/{post.id}', data={'body':'Nice post'}, follow_redirects=True)
        assert b'Nice post' in rv.data

        # send chat message
        rv = client.post('/chat/send', json={'message':'hi everyone'})
        assert rv.status_code == 200
        msgs = ChatMessage.query.all()
        print('chat messages:', len(msgs))

if __name__ == '__main__':
    run_tests()
