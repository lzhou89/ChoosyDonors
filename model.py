from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, BigInteger
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
    teacher_id = Column(String(64), ForeignKey('teachers.id'), nullable=False)
    school_id = Column(String(64), ForeignKey('schools.id'), nullable = False)
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

    teacher = relationship("teacher", backref=backref("projects", order_by=id))
    school = relationship("school", backref=backref("projects", order_by=id))

class ProjSub(Base):
    __tablename__ = "project_subjects"

    id = Column(Integer, primary_key = True)
    project_id = Column(String(64), ForeignKey('projects.id'), nullable=False)
    subject_id = Column(Integer, nullable=True)
    subject = Column(String, nullable=False)
    focus_area = Column(String, nullable=True)
    focus_area_id = Column(Integer, nullable=True)
    primary = Column(Boolean, nullable=True)

    project = relationship("project", backref=backref("project_subjects", order_by=id))
       
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String(64), primary_key = True)
    teacher_name = Column(String(30), nullable=True)
    school_id = Column(String(64), ForeignKey('schools.id'), nullable=False)
    donations = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    tfa = Column(Boolean, nullable=True)
    ny_teach = Column(Boolean, nullable=True)
    cape = Column(Boolean, nullable=True)
    nea = Column(Boolean, nullable=True)
    us_cell = Column(Boolean, nullable=True)
    photo_url = Column(String(120), nullable=True)
    profile_url = Column(String(120), nullable=True)

    school = relationship("school", backref=backref("teachers", order_by=id))

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
    nclb = Column(Boolean, nullable=True)
    student_teacher_ratio = Column(Integer, nullable=True)
    free_lunch = Column(Integer, nullable=True)
    test_results = Column(Integer, nullable=True)
    pov_level = Column(Float, nullable=True)
    crime_rate = Column(Float, nullable=True)
    impact_score = Column(Float, nullable=True)
    grade_levels = Column(String(64), nullable=True)
    school_url = Column(String(120), nullable=True)
    total_proposals = Column(Integer, nullable=True)

class Supporter(Base):
    __tablename__ = "supporters"

    id = Column(Integer, primary_key = True)
    school_id = Column(String(64), ForeignKey('schools.id'), nullable=False)
    donor_id = Column(String(64), ForeignKey('donors.id'), nullable=False)

    school = relationship("school", backref=backref("supporters", order_by=id))
    donor = relationship("donor", backref=backref("supporter_of", order_by=id))

class Angel(Base):
    __tablename__ = "angels"

    id = Column(Integer, primary_key = True)
    school_id = Column(String(64), ForeignKey('schools.id'), nullable=False)
    donor_id = Column(String(64), ForeignKey('donors.id'), nullable=False)

    school = relationship("school", backref=backref("angels", order_by=id))
    donor = relationship("donor", backref=backref("angel_of", order_by=id))

class Essay(Base):
    __tablename__ = "essays"

    project_id = Column(String(64), ForeignKey('projects.id'), primary_key = True)
    short_description = Column(Text, nullable=True)
    fulfillment_trailer = Column(Text, nullable=True)
    synopsis = Column(Text, nullable=True)
    title = Column(String(120), nullable=True)

    project = relationship("project", backref=backref("essay", order_by=id))

class Donor(Base):
    __tablename__ = "donors"

    id = Column(String(64), primary_key=True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(2), nullable=True)
    zip = Column(String(15), nullable=True)
    is_teacher = Column(Boolean, nullable=True)
    num_students = Column(Integer, nullable=True)
    name = Column(String(64), nullable=True)
    total_proposals = Column(Integer, nullable=True)
    donor_photo_url = Column(String(120), nullable=True)
    total_supporters = Column(Integer, nullable=True)
    num_donors_acquired = Column(Integer, nullable=True)
    donor_profile_url = Column(String(120), nullable=True)
    num_proposals_supported = Column(Integer, nullable=True)

class Donation(Base):
    __tablename__ = "donations"

    id = Column(String(64), primary_key=True)
    project_id = Column(String(64), ForeignKey('projects.id'), nullable=False)
    donor_id = Column(String(64), ForeignKey('donors.id'), nullable=False)
    donation_to_project = Column(Float, nullable=True)
    donation_optional_support = Column(Float, nullable=True)
    donation_total = Column(Float, nullable=True)
    dollar_amount = Column(String(64), nullable=True)
    donation_included_optional_support = Column(Boolean, nullable=True)
    used_acct_credit = Column(Boolean, nullable=True)
    used_campaign_gift_card = Column(Boolean, nullable=True)
    used_web_purchased_gift_card = Column(Boolean, nullable=True)
    payment_was_promo_matched = Column(Boolean, nullable=True)
    via_giving_page = Column(Boolean, nullable=True)
    for_honoree = Column(Boolean, nullable=True)

    project = relationship("project", backref=backref("donations", order_by=id))
    donor = relationship("donor", backref=backref("donations", order_by=id))

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key = True)
    donor_id = Column(String(64), ForeignKey('donors.id'), nullable=False)
    project_id = Column(String(64), ForeignKey('projects.id'), nullable=False)

    project = relationship("project", backref=backref("portfolios", order_by=id))
    donor = relationship("donor", backref=backref("portfolios", order_by=id))

class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key = True)
    cluster_num = Column(Integer, nullable=False)
    project_id = Column(String(64), ForeignKey('projects.id'), nullable=False)
    keywords = Column(Text, nullable=True)

    project = relationship("project", backref=backref("clusters", order_by=id))

### End class declarations


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()