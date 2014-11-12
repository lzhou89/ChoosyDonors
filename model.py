from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation


engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, 
                                      autocommit = False,
                                      autoflush = False))
Base = declarative_base()
Base.query = session.query_property

### Class declarations go here

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(64), primary_key = True)
    title = Column(String(120), nullable=True)
    teacher_id = Column(String(64), nullable=False)
    school_id = Column(String(64), nullable = False)
    grade_level = Column(String(20), nullable = True)
    resource_type = Column(String(25), nullable=True)
    total_price = Column(Float, nullable=True)
    students_reached = Column(Integer, nullable=True)
    percent_funded = Column(Float, nullable=True)
    num_donors = Column(Integer, nullable=True)
    matching = Column(Boolean, nullable=True)
    funding_status = Column(String(20), nullable=True)
    fund_url = Column(String(120), nullable=True)
    proposal_url = Column(String(120), nullable=True)
    image_url = Column(String(120), nullable=True)
    thumb_image_url = Column(String(120), nullable=True)
    date_expiration = Column(DateTime, nullable=True)

class ProjSub(Base):
    __tablename__ = "project_subjects"

    id = Column(Integer, primary_key = True)
    project_id = Column(String(64), nullable=False)
    subject_id = Column(Integer, nullable=True)
    subject = Column(String, nullable=False)
    focus_area = Column(String, nullable=True)
    focus_area_id = Column(Integer, nullable=True)
    primary = Column(Boolean, nullable=True)

       
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String(64), primary_key = True)
    teacher_name = Column(String(30), nullable=True)
    school_id = Column(String(64), nullable=False)
    donations = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    tfa = Column(Boolean, nullable=True)
    ny_teach = Column(Boolean, nullable=True)
    cape = Column(Boolean, nullable=True)
    nea = Column(Boolean, nullable=True)
    us_cell = Column(Boolean, nullable=True)
    photo_url = Column(String(120), nullable=True)
    profile_url = Column(String(120), nullable=True)

class School(Base):
    __tablename__ = "schools"

    id = Column(String(64), primary_key=True)
    school_name = Column(String(30), nullable=True)
    nces_id = Column(BigInteger, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String(40), nullable=True)
    state = Column(String(2), nullable=True)
    zip = Column(String(15), nullable=True)
    metro = Column(String(20), nullable=True)
    district = Column(String(64), nullable=True)
    county = Column(String(64), nullable=True)
    school_charter = Column(Boolean, nullable=True)
    school_magnet = Column(Boolean, nullable=True)
    school_year_round = Column(Boolean, nullable=True)
    school_nlns = Column(Boolean, nullable=True)
    school_kipp = Column(Boolean, nullable=True)
    school_charter_ready_promise = Column(Boolean, nullable=True)
    dc_pov = Column(String(20), nullable=True)
    grad_rate = Column(Float, nullable=True)
    nclb
    student_teacher_ratio
    free_lunch
    test_results
    pov_level
    crime_rate
    impact_score = Column(Float, nullable=True)
    grade_levels = Column(String(64), nullable=True)
    school_url = Column(String(120), nullable=True)
    total_proposals = Column(Integer, nullable=True)

    # user = relationship("User",
    #     backref=backref("ratings", order_by=id))
    # movie = relationship("Movie",
    #     backref=backref("ratings", order_by=id))

class Supporter(Base):
    __tablename__ = "supporters"

    id = Column(Integer, primary_key = True)
    school_id = Column(String(64), nullable=False)
    donor_id = Column(String(64), nullable=False)

class Angel(Base):
    __tablename__ = "angels"

    id = Column(Integer, primary_key = True)
    school_id = Column(String(64), nullable=False)
    donor_id = Column(String(64), nullable=False)

class Essay(Base):
    __tablename__ = "essays"

    project_id = Column(String(64), primary_key = True)
    short_description = Column(Text, nullable=True)
    fulfillment_trailer = Column(Text, nullable=True)
    synopsis = Column(Text, nullable=True)
    title = Column(String(120), nullable=True)

class Donor(Base):
    id = Column(String(64), primary_key=True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)

class Portfolio(Base):
    id = Column(Integer, primary_key = True)
    donor_id = Column(String(64), nullable=False)
    project_id = Column(String(64), nullable=False)

class Cluster(Base):
    id = Column(Integer, primary_key = True)

### End class declarations


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()