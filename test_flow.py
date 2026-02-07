from app import app, db, User, Result
import json

def run_flow():
    with app.app_context():
        # ensure clean DB for test run
        db.drop_all()
        db.create_all()

        client = app.test_client()

        # Register
        rv = client.post('/register', data={'username':'testuser','password':'pass123'}, follow_redirects=True)
        assert rv.status_code == 200

        # Login (should already be logged in after register, but test login anyway)
        rv = client.post('/login', data={'username':'testuser','password':'pass123'}, follow_redirects=True)
        assert b'TAKE QUIZ' in rv.data or rv.status_code == 200

        # Take quiz (POST)
        quiz_data = {
            'zip':'15201',
            'budget':'$',
            'types': [],
            'prefs': []
        }
        rv = client.post('/quiz', data=quiz_data, follow_redirects=True)
        assert rv.status_code == 200

        # After quiz, results endpoint should save a Result for the user
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        results = Result.query.filter_by(user_id=user.id).all()
        print('Saved results count for testuser:', len(results))
        for r in results:
            print(' -', r.timestamp, 'zip=', r.user_zip)

if __name__ == '__main__':
    run_flow()
