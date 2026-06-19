from db.connection import get_conn


class MemoryService:

    def create_session(self, session_id: str):

        conn = get_conn()
        cur = conn.cursor()

        try:

            cur.execute("""
                INSERT INTO chat_sessions (
                    session_id
                )
                VALUES (%s)
                ON CONFLICT (session_id)
                DO NOTHING
            """, (session_id,))

            conn.commit()

        finally:
            cur.close()
            conn.close()

    def session_exists(self, session_id: str) -> bool:

        conn = get_conn()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT 1
                FROM chat_sessions
                WHERE session_id = %s
                LIMIT 1
            """, (session_id,))

            return cur.fetchone() is not None

        finally:
            cur.close()
            conn.close()

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        conn = get_conn()
        cur = conn.cursor()

        try:

            if not self.session_exists(session_id):
                self.create_session(session_id)

            cur.execute("""
                INSERT INTO chat_messages
                (
                    session_id,
                    role,
                    message,
                    content
                )
                VALUES (%s, %s, %s,%s)
            """, (
                session_id,
                role,
                content,
                content
            ))
            conn.commit()

        finally:
            cur.close()
            conn.close()

    def get_recent_history(
        self,
        session_id: str,
        limit: int = 10
    ):

        conn = get_conn()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT
                    role,
                    content
                FROM chat_messages
                WHERE session_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (
                session_id,
                limit
            ))

            rows = cur.fetchall()

            return rows[::-1]

        finally:
            cur.close()
            conn.close()

    def get_history_text(
        self,
        session_id: str,
        limit: int = 10
    ) -> str:

        history = self.get_recent_history(
            session_id,
            limit
        )

        history_text = ""

        for role, content in history:

            history_text += (
                f"{role.upper()}: "
                f"{content}\n"
            )

        return history_text

    def delete_session(
        self,
        session_id: str
    ):

        conn = get_conn()
        cur = conn.cursor()

        try:

            cur.execute("""
                DELETE FROM chat_sessions
                WHERE session_id = %s
            """, (session_id,))

            conn.commit()

        finally:
            cur.close()
            conn.close()

    def get_session_count(self):

        conn = get_conn()
        cur = conn.cursor()

        try:

            cur.execute("""
                SELECT COUNT(*)
                FROM chat_sessions
            """)

            return cur.fetchone()[0]

        finally:
            cur.close()
            conn.close()