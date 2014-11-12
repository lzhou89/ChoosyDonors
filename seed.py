import model
import csv
# from datetime import datetime

def load_projects(session):
    # use u.user

    with open('opendata_projects.csv', 'rb') as csvfile:
        all_projects = csv.reader(csvfile, delimiter = ",")
        for line in all_projects:
            p = model.Project()
            p.id = line[0]
            p.teacher_id = line[1]
            p.school_id = line[2]
            p.grade_level = line[27]
            p.resource_type = line[25]
            p.total_price = line[32]
            p.students_reached = line[34]
            p.percent_funded = float(line[35])/float(line[32])
            p.num_donors = line[36]
            if line[37] != "f" or line[38] != "f":
                p.matching = true
            p.funding_status = line[39]
            p.date_expiration = line[43]
            session.add(p)
            if line[21]:
                ps = model.ProjSub()
                ps.project_id = line[0]
                ps.subject = line[21]
                ps.focus_area = line[22]
                ps.primary = true
                session.add(ps)
            if line[23]:
                ps2 = model.ProjSub()
                ps2.project_id = line[0]
                ps2.subject = line[23]
                ps2.focus_area = line[24]
                session.add(ps2)
            t = model.Teacher()
            t.id = line[1]
            t.school_id = line[2]
            if line[19] != "f":
                t.tfa = true
            if line[20] != "f":
                t.ny_teach = true
            session.add(t)
            s = model.School()
            s.id = line[2]
            s.nces_id = line[3]
            s.latitude = line[4]
            s.longitude = line[5]
            s.city = line[6]
            s.state = line[7]
            s.zip = line[8]
            s.metro = line[9]
            s.district = line[10]
            s.county = line[11]
            if line[12] != "f":
                s.school_charter = true
            if line[13] != "f":
                s.school_magnet = true
            if line[14] != "f":
                s.school_year_round = true
            if line[15] != "f":
                s.school_nlns = true
            if line[16] != "f":
                s.school_kipp = true
            if line[17] != "f":
                s.school_charter_ready_promise = true
            s.dc_pov = line[26]
            session.add(s)
    

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        all_movies = csv.reader(csvfile, delimiter = "|")
        for line in all_movies:
            u = model.Movie()
            u.id = int(line[0])
            u.name = line[1].decode("latin-1")
            if line[2]:
                u.released_at = datetime.strptime(line[2], "%d-%b-%Y")
            u.imdb_url = line[4].decode("latin-1")
            session.add(u)

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as csvfile:
        all_ratings = csv.reader(csvfile, delimiter= "\t")
        for line in all_ratings:
            u = model.Rating()
            u.user_id = int(line[0])
            u.movie_id = int(line[1])
            u.rating = int(line[2])
            session.add(u)


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)
    session.commit()



if __name__ == "__main__":
    s= model.connect()
    main(s)

# DB = None
# CONN = None

# def connect_to_db():
#     global DB, CONN
#     CONN = sqlite3.connect("Skills3.db")
#     DB = CONN.cursor()

# def make_new_customer():
#     data = open('customers.csv')
#     data.readline()
#     for line in data:
#         customer = line.rstrip().split(',')
#         (customer_id, first, last, email, telephone,called) = customer
#         customer_id = int(customer_id)

#         query = """INSERT INTO Customers VALUES (?, ?, ?, ?, ?, ?)"""
#         DB.execute(query, (customer_id, first, last, email, telephone,called))

#     return

# def make_new_order():
#     data = open('orders.csv')
#     data.readline()
#     for line in data:
#         line = line.decode("utf-8")
#         order = line.rstrip().split(',')
#         (order_id, order_date, status, customer_id, email, address,
#          city, state, postalcode, num_watermelons, num_othermelons,
#           subtotal, tax, order_total) = order
#         order_id = int(order_id)
#         customer_id = int(customer_id)
#         num_watermelons = int(num_watermelons)
#         num_othermelons = int(num_othermelons)
#         subtotal = float(subtotal)
#         tax = float(tax)
#         order_total = float(order_total)
#         query = """INSERT INTO Orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
#         DB.execute(query, (order_id, order_date, status, customer_id, 
#             email, address, city, state, postalcode, num_watermelons, 
#             num_othermelons, subtotal, tax, order_total))
#     return


# def main():
#     connect_to_db()
#     make_new_customer()
#     make_new_order()
#     CONN.commit()



#     CONN.close()
