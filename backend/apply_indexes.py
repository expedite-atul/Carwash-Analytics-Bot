from sqlmodel import Session, text
from app.db import engine

def apply_indexes():
    print("Applying Indexes...")
    with Session(engine) as session:
        # ChatSession: user_id
        session.exec(text("CREATE INDEX IF NOT EXISTS ix_chatsession_user_id ON chatsession (user_id);"))
        
        # ChatMessage: session_id
        session.exec(text("CREATE INDEX IF NOT EXISTS ix_chatmessage_session_id ON chatmessage (session_id);"))
        
        # ChatMessage: created_at (for sorting)
        session.exec(text("CREATE INDEX IF NOT EXISTS ix_chatmessage_created_at ON chatmessage (created_at);"))
        
        session.commit()
        print("Indexes applied successfully!")

if __name__ == "__main__":
    apply_indexes()
