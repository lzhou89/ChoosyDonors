import model
from edcom_key import KEY
    
def get_ncesids(session):
    nces_ids=[]
    query = session.query(model.School).all()
    for school in query:
        nces_ids.append(school.nces_id)
    return nces_ids

def create_url(ids):
    f = open('api_reqs.txt', 'a')
    for i in range(100):
        f.write(i) #fix!!!
        for i in range(114):
            write_to_file = "&methods["+i+"][f]=schoolSearch&methods["+\
            i+"][nces_id]="+ids[i]+"&methods["+i+"][key]="+KEY+"&methods["+\
            i+"][sn]=sf&methods["+i+"][fid]=F"+str(i+1)
            f.write(write_to_file)
    f.close()

def main(session):
    nces_ids = get_ncesids(session)
    day_1 = nces_ids[:12000]
    day_2 = nces_ids[12000:24000]
    day_3 = nces_ids[24000:36000]
    day_4 = nces_ids[36000:48000]
    day_5 = nces_ids[48000:]

if __name__ == "__main__":
    s= model.session
    main(s)

