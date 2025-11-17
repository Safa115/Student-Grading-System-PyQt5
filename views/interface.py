import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, 
                             QGraphicsDropShadowEffect, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QDialog, QDialogButtonBox, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
import qtawesome as qta 

# --- Matplotlib Imports ---
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# --- Backend Imports (Uncomment when ready to use real DB) ---
# from models.student import Student
# from models.instructor import Instructor

# =======================================================
# 1. Custom Card for Top Stats (KPIs)
# =======================================================
class KPICard(QFrame):
    def __init__(self, title, value, icon_name):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        
        self.default_style = """
            background-color: white;
            border-radius: 15px;
            border: 1px solid #e0e0e0;
        """
        self.hover_style = """
            background-color: white;
            border-radius: 15px;
            border: 2px solid rgb(192, 192, 255); 
        """
        self.setStyleSheet(self.default_style)

        layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color="#c0c0ff").pixmap(QSize(45, 45)))
        
        text_layout = QVBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #7f8c8d; font-size: 14px; font-weight: 500; border: none;")
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet("color: #2b2b2b; font-size: 26px; font-weight: bold; border: none;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(value_lbl)
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        self.setLayout(layout)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(192, 192, 255, 0)) 
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        self.shadow.setColor(QColor(192, 192, 255, 150)) 
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        self.shadow.setColor(QColor(192, 192, 255, 0))
        super().leaveEvent(event)

# =======================================================
# 2. Custom Card for Charts (Wrapper)
# =======================================================
class ChartCard(QFrame):
    def __init__(self, canvas_widget, title):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        
        self.default_style = """
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """
        self.hover_style = """
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid rgb(192, 192, 255);
            }
        """
        self.setStyleSheet(self.default_style)

        layout = QVBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #2b2b2b; font-size: 18px; font-weight: bold; border: none; padding-bottom: 10px;")
        title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_lbl)
        layout.addWidget(canvas_widget)
        self.setLayout(layout)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(192, 192, 255, 0)) 
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        self.shadow.setColor(QColor(192, 192, 255, 150)) 
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        self.shadow.setColor(QColor(192, 192, 255, 0))
        super().leaveEvent(event)

# =======================================================
# 3. Matplotlib Canvas Helper
# =======================================================
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.patch.set_facecolor('#ffffff')
        super(MplCanvas, self).__init__(fig)

# =======================================================
# 4. Smart Dialog (Handles Add & Edit)
# =======================================================
class AddStudentDialog(QDialog):
    """
    A smart dialog that handles both Adding and Editing students.
    If `student_data` is provided, it pre-fills the fields (Edit Mode).
    """
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        
        # Set mode based on data presence
        if student_data:
            self.setWindowTitle("Edit Student")
            title_text = "Update Student Details"
            btn_text = "Update"
        else:
            self.setWindowTitle("Add New Student")
            title_text = "Enter Student Details"
            btn_text = "Save Student"
            
        self.setFixedSize(400, 280) 
        
        # Dialog Stylesheet
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-size: 14px; color: #2b2b2b; font-weight: bold; }
            QLineEdit {
                border: 1px solid #ccc; border-radius: 5px;
                padding: 5px 10px; font-size: 14px; background-color: #f9f9f9;
                min-height: 30px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(192, 192, 255); background-color: white;
            }
            QPushButton { padding: 8px 20px; font-size: 14px; border-radius: 5px; min-height: 35px; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet("font-size: 20px; color: rgb(192, 192, 255); margin-bottom: 10px; font-weight: bold;")
        layout.addWidget(title_lbl)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name (e.g. Ahmed Mohamed)")
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        # Pre-fill data if editing
        if student_data:
            self.name_input.setText(student_data['name'])
            self.email_input.setText(student_data['email'])

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        self.button_box.button(QDialogButtonBox.Save).setText(btn_text)
        self.button_box.button(QDialogButtonBox.Save).setCursor(Qt.PointingHandCursor)
        self.button_box.button(QDialogButtonBox.Save).setStyleSheet("""
            background-color: rgb(192, 192, 255); color: #2b2b2b; border: none; font-weight: bold;
        """)
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(Qt.PointingHandCursor)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet("""
            background-color: #f0f0f0; color: #555; border: 1px solid #ccc;
        """)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.email_input.text()


# =======================================================
# 5. Main Application Class
# =======================================================
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 1200, 800)

        # Global Stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QFrame#sidebar { background-color: #2b2b2b; border: none; }
            QFrame#header { background-color: #ffffff; border-bottom: 2px solid rgb(192, 192, 255); }
            QLabel#header_title { font-size: 22px; font-weight: bold; color: #2b2b2b; padding-left: 10px; }
            
            QPushButton {
                background-color: transparent; color: #ecf0f1; text-align: left;
                padding: 15px 20px; font-size: 16px; border: none; font-weight: 500;
                border-left: 4px solid transparent;
            }
            QPushButton:hover { background-color: #3a3a3a; }
            QPushButton:checked {
                color: rgb(192, 192, 255); border-left: 4px solid rgb(192, 192, 255);
                background-color: #333333; font-weight: bold;
            }
            
            QLineEdit {
                border: 1px solid #ccc; border-radius: 8px; padding: 8px;
                font-size: 14px; background-color: white;
            }
            QLineEdit:focus { border: 2px solid rgb(192, 192, 255); }
            
            QPushButton.action_btn {
                background-color: white; color: #2b2b2b; border: 1px solid #ccc;
                border-radius: 8px; padding: 8px 15px; font-weight: bold; text-align: center;
            }
            QPushButton.action_btn:hover { background-color: #f0f0f0; border: 1px solid #bbb; }
            
            QPushButton#add_btn {
                background-color: rgb(192, 192, 255); color: #2b2b2b; border: none;
            }
            QPushButton#add_btn:hover { background-color: #a0a0ff; }

            QTableWidget {
                background-color: white; border-radius: 10px; border: 1px solid #e0e0e0;
                gridline-color: #f0f0f0; font-size: 14px;
            }
            QHeaderView::section {
                background-color: rgb(192, 192, 255); color: #2b2b2b; padding: 10px;
                font-weight: bold; border: none;
            }
            QTableWidget::item:selected { background-color: #e6e6ff; color: black; }
        """)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_widget.setLayout(main_layout)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 30, 0, 0)
        sidebar_layout.setSpacing(10)
        self.sidebar.setLayout(sidebar_layout)

        app_title = QLabel("  Grading System")
        app_title.setStyleSheet("color: rgb(192, 192, 255); font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        sidebar_layout.addWidget(app_title)

        self.btn_dashboard = self.create_nav_btn("Dashboard", "fa5s.chart-line")
        self.btn_students = self.create_nav_btn("Students", "fa5s.user-graduate")
        self.btn_instructors = self.create_nav_btn("Instructors", "fa5s.chalkboard-teacher")
        self.btn_courses = self.create_nav_btn("Courses", "fa5s.book")
        self.btn_grades = self.create_nav_btn("Grades", "fa5s.clipboard-list")

        self.btn_dashboard.setChecked(True)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_students)
        sidebar_layout.addWidget(self.btn_instructors)
        sidebar_layout.addWidget(self.btn_courses)
        sidebar_layout.addWidget(self.btn_grades)
        sidebar_layout.addStretch()

        # --- Header & Content ---
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_container.setLayout(right_layout)

        self.header = QFrame()
        self.header.setObjectName("header")
        self.header.setFixedHeight(60)
        header_layout = QHBoxLayout()
        self.header.setLayout(header_layout)
        
        self.header_title = QLabel("Dashboard")
        self.header_title.setObjectName("header_title")
        header_layout.addWidget(self.header_title)
        header_layout.addStretch()

        self.content_area = QStackedWidget()
        
        # Page 0: Dashboard
        self.dashboard_page = QWidget()
        self.setup_dashboard_ui() 
        self.content_area.addWidget(self.dashboard_page)

        # Page 1: Students
        self.students_page = QWidget()
        self.setup_students_ui()
        self.content_area.addWidget(self.students_page)

        # Page 2: Instructors (Now Initialized)
        self.instructors_page = QWidget()
        self.setup_instructors_ui()
        self.content_area.addWidget(self.instructors_page)

        # Page 3 & 4: Placeholders
        self.create_dummy_page("Courses Management")
        self.create_dummy_page("Grades Management")

        right_layout.addWidget(self.header)
        right_layout.addWidget(self.content_area)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(right_container)

        # Button Connections
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, "Dashboard"))
        self.btn_students.clicked.connect(lambda: self.switch_page(1, "Students Management"))
        self.btn_instructors.clicked.connect(lambda: self.switch_page(2, "Instructors Management"))
        self.btn_courses.clicked.connect(lambda: self.switch_page(3, "Courses Management"))
        self.btn_grades.clicked.connect(lambda: self.switch_page(4, "Grades & GPA"))

    def switch_page(self, index, title_text):
        self.content_area.setCurrentIndex(index)
        self.header_title.setText(title_text)

    # ---------------------------
    # PAGE 0: DASHBOARD
    # ---------------------------
    def setup_dashboard_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.addWidget(KPICard("Total Students", "1,250", "fa5s.user-graduate"))
        cards_layout.addWidget(KPICard("Total Courses", "34", "fa5s.book"))
        cards_layout.addWidget(KPICard("Instructors", "18", "fa5s.chalkboard-teacher"))
        cards_layout.addWidget(KPICard("Avg GPA", "3.2", "fa5s.star"))
        layout.addLayout(cards_layout)

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        self.canvas_grades = MplCanvas(self, width=5, height=4, dpi=100)
        self.bars = self.canvas_grades.axes.bar(['A', 'B', 'C', 'D', 'F'], [15, 30, 45, 10, 5], color='#c0c0ff')
        self.canvas_grades.axes.set_facecolor('#ffffff')
        self.canvas_grades.mpl_connect("motion_notify_event", self.on_bar_hover)
        grades_card = ChartCard(self.canvas_grades, "Grades Distribution")
        
        self.canvas_courses = MplCanvas(self, width=5, height=4, dpi=100)
        labels = ['Python', 'Java', 'Math', 'Physics']
        sizes = [40, 30, 20, 10]
        colors = ['#c0c0ff', '#a0a0ff', '#8080ff', '#6060ff'] 
        self.canvas_courses.axes.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        courses_card = ChartCard(self.canvas_courses, "Enrollment Share")

        charts_layout.addWidget(grades_card)
        charts_layout.addWidget(courses_card)
        layout.addLayout(charts_layout)
        self.dashboard_page.setLayout(layout)

    def on_bar_hover(self, event):
        if event.inaxes == self.canvas_grades.axes:
            for bar in self.bars:
                if bar.contains(event)[0]:
                    bar.set_color('#8080ff')
                else:
                    bar.set_color('#c0c0ff')
            self.canvas_grades.draw_idle()

    # ---------------------------
    # PAGE 1: STUDENTS
    # ---------------------------
    def setup_students_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Search by ID or Name...")
        self.student_search.setFixedWidth(300)
        
        self.btn_add_student = QPushButton(" + Add Student")
        self.btn_add_student.setObjectName("add_btn") 
        self.btn_add_student.setProperty("class", "action_btn")
        self.btn_add_student.clicked.connect(self.open_add_student_dialog)
        
        self.btn_edit_student = QPushButton(" Edit")
        self.btn_edit_student.setIcon(qta.icon("fa5s.edit", color="#2b2b2b"))
        self.btn_edit_student.setProperty("class", "action_btn")
        self.btn_edit_student.clicked.connect(self.open_edit_student_dialog)

        self.btn_delete_student = QPushButton(" Delete")
        self.btn_delete_student.setIcon(qta.icon("fa5s.trash-alt", color="#c0392b"))
        self.btn_delete_student.setProperty("class", "action_btn")

        top_bar.addWidget(self.student_search)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add_student)
        top_bar.addWidget(self.btn_edit_student)
        top_bar.addWidget(self.btn_delete_student)
        layout.addLayout(top_bar)

        self.students_table = QTableWidget()
        self.students_table.setColumnCount(3)
        self.students_table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setAlternatingRowColors(True)
        self.students_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.students_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Load Data (Now using a helper function)
        self.load_students_table()

        layout.addWidget(self.students_table)
        self.students_page.setLayout(layout)

    def load_students_table(self):
        """ Loads dummy data (Or Real DB data if enabled) """
        self.students_table.setRowCount(0)
        # Dummy Data for now
        students = [
            (1, "Ahmed Mohamed", "ahmed@email.com"),
            (2, "Sara Ali", "sara@email.com"),
            (3, "Mona Ahmed", "mona@email.com"),
        ]
        # UNCOMMENT THIS TO USE REAL DB:
        # students = Student.get_all_students() 
        
        for row_idx, student in enumerate(students):
            self.students_table.insertRow(row_idx)
            for col_idx, data in enumerate(student):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                self.students_table.setItem(row_idx, col_idx, item)

    def open_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, email = dialog.get_data()
            print(f"User added: Name={name}, Email={email}")
            # Here: Call DB Add Function -> Then self.load_students_table()

    def open_edit_student_dialog(self):
        row = self.students_table.currentRow()
        if row == -1:
            print("Select a row first!")
            return
        
        # Get data from UI
        sid = self.students_table.item(row, 0).text()
        name = self.students_table.item(row, 1).text()
        email = self.students_table.item(row, 2).text()
        
        # Open dialog with data
        dialog = AddStudentDialog(self, student_data={'name': name, 'email': email})
        if dialog.exec_() == QDialog.Accepted:
            new_name, new_email = dialog.get_data()
            print(f"Update ID {sid}: {new_name}, {new_email}")
            # Here: Call DB Update Function -> Then self.load_students_table()

    # ---------------------------
    # PAGE 2: INSTRUCTORS
    # ---------------------------
    def setup_instructors_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search Instructor...")
        search_input.setFixedWidth(300)
        
        btn_add = QPushButton(" + Add Instructor")
        btn_add.setObjectName("add_btn")
        btn_add.setProperty("class", "action_btn")
        
        btn_edit = QPushButton(" Edit")
        btn_edit.setIcon(qta.icon("fa5s.edit", color="#2b2b2b"))
        btn_edit.setProperty("class", "action_btn")

        btn_delete = QPushButton(" Delete")
        btn_delete.setIcon(qta.icon("fa5s.trash-alt", color="#c0392b"))
        btn_delete.setProperty("class", "action_btn")

        top_bar.addWidget(search_input)
        top_bar.addStretch()
        top_bar.addWidget(btn_add)
        top_bar.addWidget(btn_edit)
        top_bar.addWidget(btn_delete)
        layout.addLayout(top_bar)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Dummy Data for Instructors
        instructors = [
            (101, "Dr. Hisham", "hisham@univ.edu"),
            (102, "Dr. Noha", "noha@univ.edu")
        ]
        table.setRowCount(len(instructors))
        for r, row_data in enumerate(instructors):
            for c, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)
        
        layout.addWidget(table)
        self.instructors_page.setLayout(layout)

    # --- Helpers ---
    def create_nav_btn(self, text, icon_name):
        btn = QPushButton(text)
        btn.setIcon(qta.icon(icon_name, color="white"))
        btn.setIconSize(QSize(20, 20))
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        return btn

    def create_dummy_page(self, text):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #aaa; font-size: 25px;")
        layout.addWidget(label)
        page.setLayout(layout)
        self.content_area.addWidget(page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())