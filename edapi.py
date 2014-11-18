import model
from edcom_key import KEY
    
def get_ncesids(session):
    nces_ids=[]
    query = session.query(model.School).all()
    for school in query:
        nces_ids.append(school.nces_id)
    return nces_ids

def create_url(ids):
    f = open('day_1.txt', 'a')
    in1 = 0
    in2 = 120
    for i in range(100):
        f.write("\n"+str(i)+"\n")
        seg_ids = ids[in1:in2]
        x = 0
        for i in range(120):
            write_to_file = "&methods["+str(x)+"][f]=schoolSearch&methods["+\
            str(x)+"][nces_id]="+seg_ids[i]+"&methods["+str(x)+"][key]="+\
            KEY+"&methods["+str(x)+"][sn]=sf&methods["+str(x)+"][fid]=F"+str(x+1)
            f.write(write_to_file)
            x += 1
            write_to_file = "&methods["+str(x)+"][f]=getStudentStats&methods["+\
            str(x)+"][nces_id]="+seg_ids[i]+"&methods["+str(x)+"][key]="+\
            KEY+"&methods["+str(x)+"][sn]=sf&methods["+str(x)+"][fid]=F"+str(x+1)
            f.write(write_to_file)
            x += 1
        in1 += 120
        in2 += 120
    f.close()

def main(session):
    nces_ids = get_ncesids(session)
    day_1 = nces_ids[:4000]
    day_2 = nces_ids[4000:8000]
    day_3 = nces_ids[8000:12000]
    day_4 = nces_ids[12000:16000]
    day_5 = nces_ids[16000:20000]
    day_6 = nces_ids[20000:24000]
    day_7 = nces_ids[24000:28000]
    day_8 = nces_ids[28000:20000] #come back
    day_9 = nces_ids[16000:20000]
    day_10 = nces_ids[16000:20000]
    day_11 = nces_ids[16000:20000]
    day_12 = nces_ids[16000:20000]
    day_13 = nces_ids[16000:20000]
    day_14 = nces_ids[16000:20000]
    day_15 = nces_ids[16000:20000]
    create_url(day_1)

if __name__ == "__main__":
    s= model.session
    main(s)

