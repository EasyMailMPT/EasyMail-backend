import sqlalchemy as sqa

engine = sqa.create_engine("postgresql://user:psswd@host/database", echo=True, future=True)
with engine.connect() as conn:
    conn.execute(sqa.text("CREATE TABLE easymail (user string, emails string, user_emails string)"))
    conn.execute(sqa.text("INSERT INTO easymail (user, emails,user_emails) VALUES (:user, :emails, :user_emails)"),
                 [{'user': 'abc', 'emails': 'abc@agh.pl', 'user_emails': 'result of query'}]
                 )
    conn.commit()
    result = conn.execute(sqa.text('SELECT * from easymail'))
    print(result)

