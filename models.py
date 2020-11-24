from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BdtRequestLog(db.Model):
    __tablename__ = "RequestLog"
    id = db.Column(db.Integer, primary_key=True)
    request_headers = db.Column(db.String, unique=False, nullable=False)
    request_xml = db.Column(db.String, unique=False, nullable=False)
    response_xml = db.Column(db.String, unique=False, nullable=False)
    request_datetime = db.Column(db.String, unique = False, nullable = False)
    bdt_id = db.Column(db.String, unique = False, nullable = True)

    def __repr__(self):
        return f'<Request made at {repr(self.request_datetime)}>'

class BdtLog(db.Model):
    __tablename__ = 'BDTLog'
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.String, unique = False, nullable = False)
    bdt_id = db.Column(db.String, unique = True, nullable = False)
    data = db.Column(db.String, unique = False, nullable = False)

