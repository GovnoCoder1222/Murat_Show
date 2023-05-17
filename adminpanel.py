import sqlite3


class Admin_panel:

    def __init__(self, login,password):
        self.__private_login = login
        self.__private_password = password

    @property
    def private_attr(self):
        return self.__private_login, self.__private_password

    @private_attr.setter
    def private_attr(self, *private_attr):
        self.__private_attr = private_attr


    def make_table(self,day,time):
        conn = sqlite3.connect('ticketbase.db')
        curr = conn.cursor()
        count_of_day = 0
        self.day = day
        self.time = time
        count_of_time = len(self.time)

        #for i in range(0,count_of_time):
        curr.execute(f'''CREATE TABLE IF NOT EXISTS work_time_(
                                id TEXT,
                                time TEXT,
                                time_id INTEGER,
                                place INTEGER,
                                row INTEGER,
                                price INTEGER,
                                is_free_place INTEGER,
                                work_day_id INTEGER,
                                FOREIGN KEY (work_day_id) REFERENCES work_day_(id{count_of_day})
                                )''')


        for x in range(0,count_of_time):
            curr.execute(f'''INSERT INTO work_time_(time_id) VALUES (?)''',(count_of_day,))
            for i in range(1, 250+1):
                if i>0 and i<=50:
                    row = 1
                    price = 5000
                if i>= 51 and i <=100:
                    row = 2
                    price = 4500
                if i>= 101 and i <=150:
                    row = 3
                    price = 3000
                if i>= 151 and i <=200:
                    row = 4
                    price = 2500
                if i>= 201 and i <=250:
                    row = 5
                    price = 2000

                curr.execute(f''' INSERT OR IGNORE INTO work_time_ (place,row,price,time,id,is_free_place) VALUES(?,?,?,?,?,?) ''', (i,row,price,self.time[x],self.day,1))


        conn.commit()
        conn.close()