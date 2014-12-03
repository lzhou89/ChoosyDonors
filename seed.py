import model
import csv
import string
import sys
from datetime import datetime

csv.field_size_limit(sys.maxsize)

def tf_to_bool(val):
    if val == "f":
        return False
    if val == "t":
        return True
    return None

def load_projects(session):
    teachers = []
    schools = []

    with open('opendata_projects.csv', 'rb') as csvfile:
        all_projects = csv.reader(csvfile, delimiter = ",")
        next(all_projects)
        for line in all_projects:
            p = model.Project()
            p.id = line[0]
            p.teacher_id = line[1]
            p.school_id = line[2]
            p.grade_level = line[27]
            p.resource_type = line[25]
            p.total_price = float(line[32])
            if line[34]:
                p.students_reached = int(line[34])
            if line[32] and line[35] and float(line[32]) != 0:
                p.percent_funded = float(line[35])/float(line[32])
            p.matching = tf_to_bool(line[37]) or tf_to_bool(line[38])
            if line[43]:
                p.date_expiration = datetime.strptime(line[43], "%Y-%m-%d")
            if line[21]:
                ps = model.ProjSub()
                ps.project_id = line[0]
                ps.subject = line[21]
                ps.focus_area = line[22]
                ps.primary = True
                session.add(ps)
            if line[23]:
                ps2 = model.ProjSub()
                ps2.project_id = line[0]
                ps2.subject = line[23]
                ps2.focus_area = line[24]
                ps2.primary = False
                session.add(ps2)
            if line[1] not in teachers:
                t = model.Teacher()
                t.id = line[1]
                t.school_id = line[2]
                t.tfa = tf_to_bool(line[19])
                t.ny_teach = tf_to_bool(line[20])
                session.add(t)
                teachers.append(line[1])
            if line[2] not in schools:
                s = model.School()
                s.id = line[2]
                s.nces_id = line[3]
                s.latitude = float(line[4])
                s.longitude = float(line[5])
                s.city = line[6]
                s.state = line[7]
                s.zip_code = line[8]
                s.metro = line[9]
                s.district = line[10]
                s.county = line[11]
                # s.school_charter = (line[12] == "t") another way to do tf_to_bool
                s.school_charter = tf_to_bool(line[12])
                s.school_magnet = tf_to_bool(line[13])
                s.school_year_round = tf_to_bool(line[14])
                s.school_nlns = tf_to_bool(line[15])
                s.school_kipp = tf_to_bool(line[16])
                s.school_charter_ready_promise = tf_to_bool(line[17])
                s.dc_pov = line[26]
                session.add(s)
                schools.append(line[2])
            session.add(p)
        session.commit()
    
def load_essays(session):
    with open('opendata_essays.csv', 'rb') as csvfile:
        all_essays = csv.reader(csvfile, delimiter = ",")
        next(all_essays)
        for line in all_essays:
            query = session.query(model.Project).get(line[0])
            if query:
                query.short_description = line[3].decode("utf-8")
                query.fulfillment_trailer = line[4].decode("utf-8")
                query.synopsis = line[5].decode("utf-8")
                query.title = line[2].decode("utf-8")
        session.commit()

def load_donations(session):
    donors = []
    with open('opendata_donations.csv', 'rb') as csvfile:
        all_donations = csv.reader(csvfile, delimiter = ",")
        next(all_donations)
        for line in all_donations:
            if line[2] not in donors:
                d1 = model.Donor()
                d1.id = line[2]
                d1.city = line[4]
                d1.state = line[5]
                d1.zip_code = line[6]
                d1.is_teacher = tf_to_bool(line[7])
                donors.append(line[2])
            d2 = model.Donation()
            d2.id = line[0]
            d2.project_id = line[1]
            d2.donor_id = line[2]
            d2.donation_to_project = float(line[9])
            d2.donation_optional_support = float(line[10])
            d2.used_acct_credit = tf_to_bool(line[15])
            d2.used_campaign_gift_card = tf_to_bool(line[16])
            d2.used_web_purchased_gift_card = tf_to_bool(line[17])
            d2.payment_was_promo_matched = tf_to_bool(line[18])
            d2.via_giving_page = tf_to_bool(line[19])
            d2.for_honoree = tf_to_bool(line[20])
            session.add(d1)
            session.add(d2)
            print "ok"
        session.commit()
            
def load_poverty_levels(session):
    with open('pov_levels.csv', 'rb') as csvfile:
        all_pov_levels = csv.reader(csvfile, delimiter = ",")
        for line in all_pov_levels:
            query = session.query(model.School).filter_by(zip_code=line[0]).all()
            poverty_level = float(line[1])
            for school in query:
                school.pov_level = poverty_level
        session.commit()

def load_clusters(session):
    with open('k_clusters.csv', 'rb') as csvfile:
        all_clusters = csv.reader(csvfile, delimiter=",")
        for line in all_clusters:
            c = model.Cluster()
            c.cluster_num = line[0]
            c.project_id = line[1]
            session.add(c)
        session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_projects(session)
    # load_essays(session)
    # load_donations(session)
    # load_poverty_levels(session)
    load_clusters(session)



if __name__ == "__main__":
    s= model.session
    main(s)

