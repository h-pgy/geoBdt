from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BdtLog(db.Model):
    __tablename__ = "BDTLOG"
    id = db.Column(db.Integer, primary_key=True)
    request_headers = db.Column(db.String, unique=False, nullable=False)
    request_xml = db.Column(db.String, unique=False, nullable=False)
    response_xml = db.Column(db.String, unique=False, nullable=False)
    response_json = db.Column(db.String, unique=False, nullable=False)
    parsed_response = db.Column(db.String, unique = False, nullable = False)
    request_datetime = db.Column(db.DateTime, unique = False, nullable = False)

    def __repr__(self):
        return f'<BDT created at {repr(self.request_datetime)}>'