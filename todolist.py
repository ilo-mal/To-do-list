# Write your code here
# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db

engine = create_engine('sqlite:///c:\\todo.db')
Base = declarative_base()


class TableTask(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class ToDoList:
    def __init__(self):
        self.my_list()

    def today_tasks(self):
        print(f'Today {datetime.today().day} {datetime.today().strftime("%b")}:')
        check_q = session.query(TableTask.task).filter(TableTask.deadline == datetime.today()).count()
        today_query = session.query(TableTask.task).filter(TableTask.deadline == datetime.today())
        if check_q:
            enu = enumerate(today_query, 1)
            for x in enu:
                print(x[0], *x[1])
            print('')
            return self.my_list()
        else:
            print('Nothing to do!\n')
            return self.my_list()

    def add_task(self):
        print('Enter task')
        task_desk = input()
        print('Enter deadline')
        task_date_raw = input()
        if task_date_raw == '':
            self.add_new = TableTask(task=task_desk)
        else:
            task_date = datetime.strptime(task_date_raw, '%Y-%m-%d')
            self.add_new = TableTask(task=task_desk, deadline=task_date)
        session.add(self.add_new)
        session.commit()
        print('The task has been added!\n')
        return self.my_list()

    def all_tasks(self):
        print('All tasks:')
        ch_q = session.query(TableTask).count()
        today_query = session.query(TableTask).order_by(TableTask.deadline)
        if ch_q != 0:
            a = 1
            for x in today_query:
                print(str(a) + '.', str(x) + '.', x.deadline.day, x.deadline.strftime("%b"))
                a += 1
            print('')
            return self.my_list()
        else:
            print('Nothing to do!\n')
            return self.my_list()

    def week_tasks(self):
        #print("Week's tasks:\n")
        week_dic = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        for z in week_dic:
            week_day = (datetime.today() + timedelta(z)).weekday()
            d_w = datetime.today() + timedelta(z)
            print(week_dic[week_day], d_w.day, f'{datetime.today().strftime("%b")}')
            ch_query = session.query(TableTask).filter(TableTask.deadline == d_w.date()).count()
            today_query = session.query(TableTask).filter(TableTask.deadline == d_w.date())
            if ch_query != 0:
                enu = enumerate(today_query, 1)
                for x in enu:
                    print(x[0], x[1])
                print('')
            else:
                print('Nothing to do!\n')
        return self.my_list()

    def my_list(self):
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
        self.choice = input('')
        while self.choice != '0':
            if self.choice == '1':
                self.today_tasks()
            elif self.choice == '2':
                self.week_tasks()
            elif self.choice == '3':
                self.all_tasks()
            elif self.choice == '4':
                self.add_task()
            elif self.choice == '0':
                print('Bye!')
                break


a = ToDoList()
