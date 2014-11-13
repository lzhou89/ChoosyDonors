import model
import csv
# from datetime import datetime

def load_projects(session):

    with open('opendata_projects.csv', 'rb') as csvfile:
        all_projects = csv.reader(csvfile, delimiter = ",")
        for line in all_projects:
            p = model.Project()
            p.id = line[0]
            p.teacher_id = line[1]
            p.school_id = line[2]
            p.grade_level = line[27]
            p.resource_type = line[25]
            p.total_price = float(line[32])
            p.students_reached = int(line[34])
            p.percent_funded = float(line[35])/float(line[32])
            p.num_donors = int(line[36])
            # if line[37] != "f" or line[38] != "f":
            #     p.matching = True
            p.funding_status = line[39] #should I determine based on percent funded?
            if line[43]:
                p.date_expiration = catetime.strptime(line[43], "%Y-%m-%d")
            # session.add(p)
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
            t = model.Teacher()
            t.id = line[1]
            t.school_id = line[2]
            # if line[19] != "f":
            #     t.tfa = True
            # if line[20] != "f":
            #     t.ny_teach = True 
            # session.add(t)
            s = model.School()
            s.id = line[2]
            s.nces_id = int(line[3])
            s.latitude = float(line[4])
            s.longitude = float(line[5])
            s.city = line[6]
            s.state = line[7]
            s.zip = line[8]
            s.metro = line[9]
            s.district = line[10]
            s.county = line[11]
            boolean_fields = {12: "s.school_charter", 
                           13: "s.school_magnet",
                           14: "s.school_year_round",
                           15: "s.school_nlns",
                           16: "s.school_kipp",
                           17: "s.school_charter_ready_promise",
                           19: "t.tfa",
                           20: "t.ny_teach",
                           37: "p.matching",
                           38: "p.matching"}
            for key, value in boolean_fields.iteritems():
                if line[key] == "t":
                    value = True
                elif line[key] == "f":
                    value = False
            # if line[12] != "f":
            #     s.school_charter = true
            # if line[13] != "f":
            #     s.school_magnet = true
            # if line[14] != "f":
            #     s.school_year_round = true
            # if line[15] != "f":
            #     s.school_nlns = true
            # if line[16] != "f":
            #     s.school_kipp = true
            # if line[17] != "f":
            #     s.school_charter_ready_promise = true
            s.dc_pov = line[26]
            
            session.add(p)
            session.add(t)
            session.add(s)
    
def load_essays(session):
    with open('opendata_essays.csv', 'rb') as csvfile:
        all_essays = csv.reader(csvfile, delimiter = ",")
        for line in all_essays:
            e = model.Essay()
            e.project_id = line[0]
            e.short_description = line[3]
            e.fulfillment_trailer = line[4]
            e.synopsis = line[5]
            e.title = line[2]
            session.add(e)

def load_donations(session):
    with open('opendata_donations.csv', 'rb') as csvfile:
        all_donations = csv.reader(csvfile, delimiter = ",")
        for line in all_donations:
            d1 = model.Donor()
            d1.id = line[2]
            d1.city = line[4]
            d1.state = line[5]
            d1.zip = line[6]
            d2 = model.Donation()
            d2.id = line[0]
            d2.project_id = line[1]
            d2.donor_id = line[2]
            d2.donation_to_project = float(line[9])
            d2.donation_optional_support = float(line[10])
            d2.donation_total = float(line[11])
            d2.dollar_amount = line[12]
            boolean_fields = {7: "d1.is_teacher",
                              13: "d2.donation_included_optional_support",
                              15: "d2.used_acct_credit",
                              16: "d2.used_campaign_gift_card",
                              17: "d2.used_web_purchased_gift_card",
                              18: "d2.payment_was_promo_matched",
                              19: "d2.via_giving_page",
                              20: "d2.for_honoree"}
            for key, value in boolean_fields.iteritems():
                if line[key] == "t":
                    value = True
                elif line[key] == "f":
                    value = False
            session.add(d1)
            session.add(d2)
            
def load_poverty_levels(session):
    with open('pov_levels.csv', 'rb') as csvfile:
        all_pov_levels = sv.reader(csvfile, delimiter = ",")
        for line in all_pov_levels:
            query = session.query(model.School).filter_by(zip = line[0]).all()
            for school in query:
                school.pov_level = float(line[1])
                #session action?



# def load_movies(session):
#     # use u.item
#     with open('seed_data/u.item', 'rb') as csvfile:
#         all_movies = csv.reader(csvfile, delimiter = "|")
#         for line in all_movies:
#             u = model.Movie()
#             u.id = int(line[0])
#             u.name = line[1].decode("latin-1")
#             if line[2]:
#                 u.released_at = datetime.strptime(line[2], "%d-%b-%Y")
#             u.imdb_url = line[4].decode("latin-1")
#             session.add(u)


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_projects(session)

    session.commit()



if __name__ == "__main__":
    s= model.connect()
    main(s)

