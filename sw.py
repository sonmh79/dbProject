import sys
import pymysql
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from secretkey import *

login_form_class = uic.loadUiType("login.ui")[0]
main_form_class = uic.loadUiType("main.ui")[0]

class MainClass(QMainWindow, main_form_class):
    def __init__(self,id) :
        super().__init__()
        self.setupUi(self)
        self.id = id
        self.dbConn = pymysql.connect(
            user=USERID, passwd=PASSWD, host='127.0.0.1', db='sw', charset='utf8')
        self.cursor = self.dbConn.cursor(pymysql.cursors.DictCursor)
        self.cur_semester = "21-2"
        self.mainSQL = """
                SELECT s.id, s.name, s.department, e.score as `attendance(%s)`, h.score as `homework(%s)`, t.midterm as `midterm(%s)`, t.finals as `finals(%s)`, a.grade
                FROM attend as a, student as s, class as c, attendance as e, homework as h, test as t
                WHERE s.id = a.studentid and a.classid = c.classid and a.semester = c.semester and a.classid = %s and a.semester = %s and e.id = a.aid and h.id = a.hid and t.id = a.tid and c.pid = %s
                """

        # Set Combo Box
        self.my_class = self.executeSQL(f"SELECT classid, semester, subject FROM class WHERE pid = {id}")
        for d in self.my_class:
            if d["semester"] == self.cur_semester:
                self.cmb_class.addItem(d["subject"]) # 콤보 박스에 강의 추가
        self.cur_className = self.cmb_class.itemText(0) # 콤보 박스의 첫번째가 기본값
        for d in self.my_class:
            if d["subject"] == self.cur_className:
                self.cur_classID = d["classid"]

        # Set Host Name
        host = self.executeSQL(f"select name from professor where id = {self.id}")[0]["name"]
        self.lbl_hostname.setText(f"{host}님 안녕하세요")


        # Signals
        self.btn_update.clicked.connect(self.updateValue)
        self.cmb_class.currentIndexChanged.connect(self.updateClass)
        self.btn_search.clicked.connect(self.searchByName)
        self.input_searchByName.returnPressed.connect(self.searchByName)
        self.btn_resetInput.clicked.connect(self.initTable)
        self.btn_forceInsert.clicked.connect(self.fInsert)
        self.btn_forceDelete.clicked.connect(self.fDelete)
        self.btn_calcScore.clicked.connect(self.calcScore)
        self.btn_saveExcel.clicked.connect(self.saveExcel)
        self.btn_resetGrade.clicked.connect(self.resetGrade)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sortByColumn)

        # Initialize
        self.initTable()

    def sortByColumn(self):

        """ Sort Column by Clicking Header """

        self.tableWidget.setSortingEnabled(True)

    def resetGrade(self):

        """ Reset Grade to NA """

        self.executeSQL("UPDATE attend SET grade = %s WHERE classid = %s",
                        ("na", self.cur_classID))
        self.dbConn.commit()
        self.initTable()

    def saveExcel(self):

        """ Save Table to Excel File """

        try:
            self.result.to_excel(f"{self.cur_semester}학기 {self.cur_className} 수강생 명단.xlsx",index=False)
            self.informationMessage("저장에 성공하였습니다.")

        except:
            self.warningMessage("저장에 실패하였습니다.")

    def calcScore(self):

        """ Calculate Total Score """

        self.initTable()

        if int(self.input_pA.text()) + int(self.input_pH.text()) + int(self.input_pM.text()) + int(self.input_pF.text()) != 100:
            self.warningMessage("비율의 합이 100이 아닙니다 !")

        apLimit,a0Limit,bpLimit,b0Limit,cpLimit,c0Limit,dpLimit,d0Limit = float(self.input_apMin.text()),float(self.input_a0Min.text()),float(self.input_bpMin.text()),float(self.input_b0Min.text()),float(self.input_cpMin.text()),float(self.input_c0Min.text()),float(self.input_dpMin.text()),float(self.input_d0Min.text())
        cnt_ap,cnt_a0,cnt_bp,cnt_b0,cnt_cp,cnt_c0,cnt_dp,cnt_d0=0,0,0,0,0,0,0,0
        for i in range(len(self.result)):
            id = self.result.iloc[i,:]["id"]
            name = self.result.iloc[i,:]["name"]
            dept = self.result.iloc[i,:]["department"]
            score_a = float(self.result.iloc[i,:]["attendance"+"("+self.input_pA.text()+")"])
            score_h = float(self.result.iloc[i,:]["homework"+"("+self.input_pH.text()+")"])
            score_m = float(self.result.iloc[i,:]["midterm"+"("+self.input_pM.text()+")"])
            score_f = float(self.result.iloc[i,:]["finals"+"("+self.input_pF.text()+")"])

            total_score = score_a + score_h + score_m * (int(self.input_pM.text())/100) + score_f * (int(self.input_pF.text())/100)

            finalGrade = "F"
            if total_score >= apLimit:
                cnt_ap += 1
                finalGrade = "A+"
            elif total_score >= a0Limit:
                cnt_a0 += 1
                finalGrade = "A0"
            elif total_score >= bpLimit:
                cnt_bp += 1
                finalGrade = "B+"
            elif total_score >= b0Limit:
                cnt_b0 += 1
                finalGrade = "B0"
            elif total_score >= cpLimit:
                cnt_cp += 1
                finalGrade = "C+"
            elif total_score >= c0Limit:
                cnt_c0 += 1
                finalGrade = "C0"
            elif total_score >= dpLimit:
                cnt_dp += 1
                finalGrade = "D+"
            elif total_score >= d0Limit:
                cnt_d0 += 1
                finalGrade = "D0"

            self.executeSQL("UPDATE attend SET grade = %s WHERE studentid = %s and classid = %s",(finalGrade,id,self.cur_classID))
        cnt_sum = cnt_ap+cnt_a0+cnt_bp+cnt_b0+cnt_cp+cnt_c0+cnt_dp+cnt_d0
        self.lbl_ap.setText(str(round((cnt_ap/cnt_sum)*100,1))+"%")
        self.lbl_a0.setText(str(round((cnt_a0/cnt_sum)*100,1))+"%")
        self.lbl_bp.setText(str(round((cnt_bp/cnt_sum)*100,1))+"%")
        self.lbl_b0.setText(str(round((cnt_b0/cnt_sum)*100,1))+"%")
        self.lbl_cp.setText(str(round((cnt_cp/cnt_sum)*100,1))+"%")
        self.lbl_c0.setText(str(round((cnt_c0/cnt_sum)*100,1))+"%")
        self.lbl_dp.setText(str(round((cnt_dp/cnt_sum)*100,1))+"%")
        self.lbl_d0.setText(str(round((cnt_d0/cnt_sum)*100,1))+"%")

        self.initTable()

    def informationMessage(self,text):

        """ Information Message """

        QMessageBox.information(self, "", text, QMessageBox.Yes)

    def warningMessage(self,text):

        """ Warning Message """

        QMessageBox.warning(self, "", text, QMessageBox.Yes)

    def fInsert(self):

        """ Insert Student by Force """

        id, name, dept = self.input_id.text(), self.input_name.text(), self.input_dept.text()
        student_info = self.executeSQL("SELECT * FROM student WHERE id = %s and name = %s and department = %s",(id,name,dept))
        if student_info == (): # 1. 학생 존재 여부 확인
            self.warningMessage("조건에 맞는 학생이 없습니다!")
        else:
            result = self.executeSQL("SELECT * FROM attend WHERE classid = %s and semester = %s and studentid = %s",(self.cur_classID,self.cur_semester,id))
            if result != (): # 2. 이미 수업을 듣고 있는지 확인
                self.warningMessage("이미 존재하는 학생입니다!")
            else:
                result = self.executeSQL("SELECT * FROM attendance")
                new_id = len(result) + 1
                self.executeSQL("INSERT INTO attendance VALUES (%s,%s)",(str(new_id),'10'))
                self.executeSQL("INSERT INTO homework VALUES (%s,%s)",(str(new_id),'10'))
                self.executeSQL("INSERT INTO test VALUES (%s,%s,%s)",(str(new_id),'0','0'))
                self.executeSQL("INSERT INTO attend VALUES (%s,%s,%s,%s,%s,%s,%s)",(self.cur_classID,self.cur_semester,id,new_id,new_id,new_id,"na"))
                self.dbConn.commit()
                self.initTable()
                self.informationMessage(f"{id} {name} {dept} 강제 입력 성공 !")
                self.input_id.clear(), self.input_name.clear(), self.input_dept.clear()

    def fDelete(self):

        """ Delete Student by Force """

        id, name, dept = self.input_id.text(), self.input_name.text(), self.input_dept.text()
        result = self.executeSQL("SELECT * FROM attend WHERE classid = %s and semester = %s and studentid = %s",(self.cur_classID, self.cur_semester,id))
        self.executeSQL("DELETE FROM attend WHERE aid = %s",(str(result[0]["aid"])))
        self.dbConn.commit()
        self.initTable()
        self.informationMessage(f"{id} {name} {dept} 강제 삭제 성공 !")
        self.input_id.clear(), self.input_name.clear(), self.input_dept.clear()

    def searchByName(self):

        """ Search Database by Name """

        name = self.input_searchByName.text()
        sql = self.mainSQL + " and s.name = %s"
        data = [int(self.input_pA.text()),int(self.input_pH.text()),int(self.input_pM.text()),int(self.input_pF.text()),self.cur_classID, self.cur_semester,self.id] + [name]
        result = self.executeSQL(sql,data)
        # Dataframe to Table
        table = self.tableWidget
        self.result = pd.DataFrame(result)
        result = self.result
        table.setColumnCount(len(result.columns))
        table.setRowCount(len(result))
        table.cellClicked.connect(self.set_label)
        table.setHorizontalHeaderLabels(result.columns)  # 컬럼 헤더 입력

        for i in range(len(result)):
            for j in range(len(result.columns)):
                table.setItem(i, j, QTableWidgetItem(str(result.iloc[i, j])))

        self.initInfo()

    def initInfo(self):

        """ Initialize Information """

        self.lbl_tStudents.setText(f"총 {len(self.result)}명")

    def updateClass(self):

        """ Update Main Table to Changed Class """

        combobox = self.cmb_class
        self.cur_className = combobox.currentText()
        self.initTable()
        self.initInfo()

    def executeSQL(self,sql,data=()):

        """ Return Result from Executing SQL"""

        self.cursor.execute(sql,data)
        return self.cursor.fetchall()

    def initTable(self):

        """ Initialize Main Table from Database """

        for d in self.my_class:
            if d["subject"] == self.cur_className:
                self.cur_classID = d["classid"]

        data = [int(self.input_pA.text()), int(self.input_pH.text()), int(self.input_pM.text()),
                int(self.input_pF.text()), self.cur_classID, self.cur_semester,self.id]
        result = self.executeSQL(self.mainSQL,data)

        # Dataframe to Table
        table = self.tableWidget
        self.result = pd.DataFrame(result)
        result = self.result
        table.setColumnCount(len(result.columns))
        table.setRowCount(len(result))
        table.cellClicked.connect(self.set_label)
        table.setHorizontalHeaderLabels(result.columns)  # 컬럼 헤더 입력

        for i in range(len(result)):
            for j in range(len(result.columns)):
                table.setItem(i, j, QTableWidgetItem(str(result.iloc[i, j])))

        self.initInfo()
        self.input_searchByName.clear()

    def resetResultLayout(self):

        """ Clear All Widgets in Result Layout """

        for i in reversed(range(self.resultLayout.count())):
            self.resultLayout.itemAt(i).widget().setParent(None)

    def updateValue(self):

        """ Update Database """

        # Save Changed Values
        layout = self.resultLayout
        self.update_values = []
        for i in range(1,layout.count(),2):
            self.update_values.append(layout.itemAt(i).widget().text())

        try:
            for i in range(3, len(self.result.columns)):
                if self.clicked_values[i] != self.update_values[i]:
                    if i == 3:
                        sql = "UPDATE attendance SET score = %s WHERE id = (SELECT aid FROM attend WHERE studentid = %s and classid = %s and semester = %s)"
                        data = (self.update_values[i], self.update_values[0],self.cur_classID,self.cur_semester)
                        self.executeSQL(sql, data)

                    if i == 4:
                        sql = "UPDATE homework SET score = %s WHERE id = (SELECT hid FROM attend WHERE studentid = %s and classid = %s and semester = %s)"
                        data = (self.update_values[i], self.update_values[0],self.cur_classID,self.cur_semester)
                        self.executeSQL(sql, data)

                    if i == 5:
                        sql = "UPDATE test SET midterm = %s WHERE id = (SELECT tid FROM attend WHERE studentid = %s and classid = %s and semester = %s)"
                        data = (self.update_values[i], self.update_values[0],self.cur_classID,self.cur_semester)
                        self.executeSQL(sql, data)

                    if i == 6:
                        sql = "UPDATE test SET finals = %s WHERE id = (SELECT tid FROM attend WHERE studentid = %s and classid = %s and semester = %s)"
                        data = (self.update_values[i], self.update_values[0],self.cur_classID,self.cur_semester)
                        self.executeSQL(sql, data)

                    if i == 7:
                        sql = "UPDATE attend SET grade = %s WHERE studentid = %s and classid = %s and semester = %s"
                        data = (self.update_values[i], self.update_values[0],self.cur_classID,self.cur_semester)
                        self.executeSQL(sql, data)
            self.dbConn.commit()
            self.initTable()
            self.resetResultLayout()
            self.informationMessage("저장되었습니다.")

        except:
            self.warningMessage("저장에 실패하였습니다.")

    def set_label(self, row, column):

        """ Set Clicked Row for Update Value """

        self.resetResultLayout() # Clear Widgets in Layout
        self.clicked_values = []
        layout = self.resultLayout

        for i,c in enumerate(self.result.columns):
            item = self.tableWidget.item(row, i)
            value = item.text()
            self.clicked_values.append(value)
            l = QLabel(f"{c}: ")
            e = QLineEdit()
            e.setText(value)
            layout.addWidget(l)
            layout.addWidget(e)
            if i == 0 or i == 1 or i == 2:
                e.setReadOnly(True)


class LoginClass(QMainWindow, login_form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.btn_login.clicked.connect(self.login)
        dbConn = pymysql.connect(
            user=USERID, passwd=PASSWD, host='127.0.0.1', db='sw', charset='utf8')
        cursor = dbConn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from professor"
        cursor.execute(sql)
        self.result = cursor.fetchall()


    def login(self):
        id = int(self.input_id.text())
        pw = int(self.input_pw.text())

        for r in self.result:
            if r["id"] == id and r["pw"] == pw:
                QMessageBox.information(self,"Information",f"{r['name']}님 안녕하세요!",QMessageBox.Yes)
                QCoreApplication.exit(r["id"]) # 교수 ID 반환
                break
        QMessageBox.warning(self, "Information", "Please Check again", QMessageBox.Yes)

if __name__ == "__main__" :
    flag = False
    app = QApplication(sys.argv)
    myWindow = LoginClass()
    myWindow.show()
    pro_id = app.exec_()
    if pro_id != 0:
        flag = True
    if flag:
        app1 = QApplication(sys.argv)
        myWindow = MainClass(pro_id)
        myWindow.show()
        app1.exec_()