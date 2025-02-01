from app.extensions import db
from app.services.thread_generator_service import ThreadGenerator

def run():
    db.create_all()
    thread_generator = ThreadGenerator()
    thread_id = thread_generator.create_thread()
    
    from app.models.thread import Thread
    new_thread = Thread(thread=thread_id, type="openai_assistant")
    db.session.add(new_thread)
    db.session.commit()

    print("Migration 01 completed successfully.")
    
