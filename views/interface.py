import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, 
                             QGraphicsDropShadowEffect, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
import qtawesome as qta 

# --- Matplotlib Imports ---
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# --- Backend Imports (Your Models) ---
from models.student import Student
from models.instructor import Instructor
from models.database_manager import DatabaseManager

# =======================================================
# 1. Custom Card Helpers (UI Elements)
# =======================================================
class KPICard(QFrame):
    def __init__(self, title, value, icon_name):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(Qt.PointingHandCursor)
        self.default_style = """
            background-color: white; border-radius: 15px; border: 1px solid #e0e0e0;
        """
        self.hover_style = """
            background-color: white; border-radius: 15px; border: 2px solid rgb(192, 192, 255); 
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

class ChartCard(QFrame):
    def __init__(self, canvas_widget, title):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.default_style = """
            QFrame { background-color: white; border-radius: 15px; border: 1px solid #e0e0e0; }
        """
        self.hover_style = """
            QFrame { background-color: white; border-radius: 15px; border: 2px solid rgb(192, 192, 255); }
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

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.patch.set_facecolor('#ffffff')
        super(MplCanvas, self).__init__(fig)

# =======================================================
# 4. Dialogs (Reusable Popups)
# =======================================================
class AddStudentDialog(QDialog):
    """ Dialog for adding/editing a student """
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.is_edit_mode = bool(student_data)
        if self.is_edit_mode:
            self.setWindowTitle("Edit Student")
            title_text = "Update Student Details"
            btn_text = "Update Student"
        else:
            self.setWindowTitle("Add New Student")
            title_text = "Enter Student Details"
            btn_text = "Save Student"
            
        self.setFixedSize(420, 320) 
        
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-size: 14px; color: #2b2b2b; font-weight: bold; }
            QLineEdit {
                border: 1px solid #ccc; border-radius: 5px; padding: 5px 10px; font-size: 14px; background-color: #f9f9f9; min-height: 35px;
            }
            QLineEdit:focus { border: 2px solid rgb(192, 192, 255); background-color: white; }
            QPushButton { padding: 8px 20px; font-size: 14px; border-radius: 5px; min-height: 35px; }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet("font-size: 20px; color: rgb(192, 192, 255); margin-bottom: 10px; font-weight: bold;")
        layout.addWidget(title_lbl)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        if self.is_edit_mode:
            self.name_input.setText(student_data['name'])
            self.email_input.setText(student_data['email'])

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # --- BUTTONS SETUP: Replaced QDialogButtonBox with custom QHBoxLayout ---
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch() 
        
        self.save_button = QPushButton(btn_text)
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setStyleSheet("""
            QPushButton { 
                background-color: rgb(192, 192, 255); 
                color: #2b2b2b; 
                border: none; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 5px; 
                min-width: 150px; 
            }
            QPushButton:hover { background-color: #a0a0ff; }
        """)
        self.save_button.clicked.connect(self.accept) 

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton { 
                background-color: #f0f0f0; 
                color: #555; 
                border: 1px solid #ccc; 
                padding: 10px; 
                border-radius: 5px; 
                min-width: 150px; 
                margin-left: 10px;
            }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        self.cancel_button.clicked.connect(self.reject) 

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch() 

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def get_data(self):
        return self.name_input.text(), self.email_input.text()

class AddInstructorDialog(QDialog):
    """ Dialog for adding/editing an instructor (Copy of Student Dialog) """
    def __init__(self, parent=None, instructor_data=None):
        super().__init__(parent)
        self.is_edit_mode = bool(instructor_data)
        if self.is_edit_mode:
            self.setWindowTitle("Edit Instructor")
            title_text = "Update Instructor Details"
            btn_text = "Update Instructor"
        else:
            self.setWindowTitle("Add New Instructor")
            title_text = "Enter Instructor Details"
            btn_text = "Save Instructor"
            
        self.setFixedSize(420, 320) 
        
        self.setStyleSheet("""
            QDialog { background-color: white; }
            QLabel { font-size: 14px; color: #2b2b2b; font-weight: bold; }
            QLineEdit {
                border: 1px solid #ccc; border-radius: 5px; padding: 5px 10px; font-size: 14px; background-color: #f9f9f9; min-height: 35px;
            }
            QLineEdit:focus { border: 2px solid rgb(192, 192, 255); background-color: white; }
            QPushButton { padding: 8px 20px; font-size: 14px; border-radius: 5px; min-height: 35px; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet("font-size: 20px; color: rgb(192, 192, 255); margin-bottom: 10px; font-weight: bold;")
        layout.addWidget(title_lbl)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")

        if self.is_edit_mode:
            self.name_input.setText(instructor_data['name'])
            self.email_input.setText(instructor_data['email'])

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # --- BUTTONS SETUP: Replaced QDialogButtonBox with custom QHBoxLayout ---
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch() 
        
        self.save_button = QPushButton(btn_text)
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setStyleSheet("""
            QPushButton { 
                background-color: rgb(192, 192, 255); 
                color: #2b2b2b; 
                border: none; 
                font-weight: bold; 
                padding: 10px; 
                border-radius: 5px; 
                min-width: 150px; 
            }
            QPushButton:hover { background-color: #a0a0ff; }
        """)
        self.save_button.clicked.connect(self.accept) 

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet("""
            QPushButton { 
                background-color: #f0f0f0; 
                color: #555; 
                border: 1px solid #ccc; 
                padding: 10px; 
                border-radius: 5px; 
                min-width: 150px; 
                margin-left: 10px;
            }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        self.cancel_button.clicked.connect(self.reject) 

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch() 

        layout.addLayout(buttons_layout)
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
        self.db_manager = DatabaseManager()

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
                color: rgb(192, 192, 255); border-left: 4px solid rgb(192, 192, 255); background-color: #333333; font-weight: bold;
            }
            
            QLineEdit { border: 1px solid #ccc; border-radius: 8px; padding: 8px; font-size: 14px; background-color: white; }
            QLineEdit:focus { border: 2px solid rgb(192, 192, 255); }
            
            QPushButton.action_btn {
                background-color: white; color: #2b2b2b; border: 1px solid #ccc;
                border-radius: 8px; padding: 8px 15px; font-weight: bold; text-align: center;
            }
            QPushButton.action_btn:hover { background-color: #f0f0f0; border: 1px solid #bbb; }
            
            QPushButton#add_btn { background-color: rgb(192, 192, 255); color: #2b2b2b; border: none; }
            QPushButton#add_btn:hover { background-color: #a0a0ff; }

            QTableWidget { background-color: white; border-radius: 10px; border: 1px solid #e0e0e0; gridline-color: #f0f0f0; font-size: 14px; }
            QHeaderView::section { background-color: rgb(192, 192, 255); color: #2b2b2b; padding: 10px; font-weight: bold; border: none; }
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

        # --- Sidebar Setup ---
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

        # --- Content Area Setup ---
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
        
        # Pages Setup
        self.dashboard_page = QWidget()
        self.setup_dashboard_ui() 
        self.content_area.addWidget(self.dashboard_page)

        self.students_page = QWidget()
        self.setup_students_ui()
        self.content_area.addWidget(self.students_page)

        self.instructors_page = QWidget()
        self.setup_instructors_ui()
        self.content_area.addWidget(self.instructors_page)

        self.content_area.addWidget(self.create_dummy_page("Courses Management"))
        self.content_area.addWidget(self.create_dummy_page("Grades Management"))


        right_layout.addWidget(self.header)
        right_layout.addWidget(self.content_area)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(right_container)

        # Connections
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, "Dashboard"))
        self.btn_students.clicked.connect(lambda: self.switch_page(1, "Students Management"))
        self.btn_instructors.clicked.connect(lambda: self.switch_page(2, "Instructors Management"))
        self.btn_courses.clicked.connect(lambda: self.switch_page(3, "Courses Management"))
        self.btn_grades.clicked.connect(lambda: self.switch_page(4, "Grades & GPA"))

    def switch_page(self, index, title_text):
        self.content_area.setCurrentIndex(index)
        self.header_title.setText(title_text)
        if index == 1:
            self.load_students_table()
        if index == 2:
            self.load_instructors_table()

    # --- DASHBOARD LOGIC ---
    def setup_dashboard_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        cards_layout.addWidget(KPICard("Total Students", "0", "fa5s.user-graduate"))
        cards_layout.addWidget(KPICard("Total Courses", "0", "fa5s.book"))
        cards_layout.addWidget(KPICard("Instructors", "0", "fa5s.chalkboard-teacher"))
        cards_layout.addWidget(KPICard("Avg GPA", "0.0", "fa5s.star"))
        layout.addLayout(cards_layout)
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        self.canvas_grades = MplCanvas(self, width=5, height=4, dpi=100)
        self.bars = self.canvas_grades.axes.bar(['A', 'B', 'C', 'D', 'F'], [0, 0, 0, 0, 0], color='#c0c0ff')
        self.canvas_grades.axes.set_facecolor('#ffffff')
        self.canvas_grades.mpl_connect("motion_notify_event", self.on_bar_hover)
        grades_card = ChartCard(self.canvas_grades, "Grades Distribution")
        self.canvas_courses = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas_courses.axes.pie([1], labels=['No Data'], autopct='%1.1f%%', colors=['#e0e0e0'])
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
    # STUDENTS LOGIC (Page 1)
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
        self.btn_delete_student.clicked.connect(self.delete_selected_student)

        top_bar.addWidget(self.student_search)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add_student)
        top_bar.addWidget(self.btn_edit_student)
        top_bar.addWidget(self.btn_delete_student)
        layout.addLayout(top_bar)

        self.students_table = QTableWidget()
        self.students_table.setColumnCount(4)
        self.students_table.setHorizontalHeaderLabels(["ID", "Name", "Email", "GPA"])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setAlternatingRowColors(True)
        self.students_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.students_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.students_table)
        self.students_page.setLayout(layout)
        
    def load_students_table(self):
        """ Fetches all students from DB and populates the table """
        self.students_table.setRowCount(0)
        try:
            students = Student.get_all_students() 
            for row_idx, student_data in enumerate(students):
                self.students_table.insertRow(row_idx)
                
                # Column 0: ID, 1: Name, 2: Email, 3: GPA
                self.students_table.setItem(row_idx, 0, QTableWidgetItem(str(student_data[0])))
                self.students_table.setItem(row_idx, 1, QTableWidgetItem(str(student_data[1])))
                self.students_table.setItem(row_idx, 2, QTableWidgetItem(str(student_data[2])))
                
                gpa_val = student_data[4] if len(student_data) > 4 else 'N/A'
                self.students_table.setItem(row_idx, 3, QTableWidgetItem(str(gpa_val)))
                
                for i in range(4):
                    self.students_table.item(row_idx, i).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Error loading students: {e}")
            QMessageBox.critical(self, "DB Error", f"Failed to load students: {e}")


    def open_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, email = dialog.get_data()
            if name and email:
                try:
                    new_student = Student(name=name, email=email, student_id=None)
                    new_student.save_to_db() 
                    self.load_students_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not add student: {e}")

    def open_edit_student_dialog(self):
        row = self.students_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select a student to edit.")
            return
            
        sid = int(self.students_table.item(row, 0).text())
        name = self.students_table.item(row, 1).text()
        email = self.students_table.item(row, 2).text()
        
        dialog = AddStudentDialog(self, student_data={'name': name, 'email': email})
        if dialog.exec_() == QDialog.Accepted:
            new_name, new_email = dialog.get_data()
            if new_name and new_email:
                try:
                    # Update is handled by Student object with existing ID
                    student_to_update = Student(name=new_name, email=new_email, student_id=sid)
                    student_to_update.save_to_db() 
                    self.load_students_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not update student: {e}")

    def delete_selected_student(self):
        row = self.students_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select a student to delete.")
            return
            
        sid = int(self.students_table.item(row, 0).text())
        name = self.students_table.item(row, 1).text()
        
        confirm_box = QMessageBox(self)
        confirm_box.setWindowTitle("Confirm Delete")
        confirm_box.setText(f"Are you sure you want to delete '{name}'?")
        confirm_box.setIcon(QMessageBox.Question)
        
        # Add buttons
        yes_btn = confirm_box.addButton(QMessageBox.Yes)
        no_btn = confirm_box.addButton(QMessageBox.No)
        
        # Style the buttons
        btn_style = """
            QPushButton { 
                background-color: rgb(192, 192, 255); 
                color: #2b2b2b; 
                border: none; 
                padding: 5px 15px; 
                min-width: 60px; 
                border-radius: 5px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #a0a0ff; 
            }
        """
        yes_btn.setStyleSheet(btn_style)
        no_btn.setStyleSheet(btn_style)
        
        confirm = confirm_box.exec_()
        
        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.delete_student(sid) 
                self.load_students_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete student: {e}")

    # ---------------------------
    # INSTRUCTORS LOGIC (Page 2)
    # ---------------------------
    def setup_instructors_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        top_bar = QHBoxLayout()
        self.instructor_search = QLineEdit()
        self.instructor_search.setPlaceholderText("Search Instructor...")
        self.instructor_search.setFixedWidth(300)
        
        self.btn_add_instructor = QPushButton(" + Add Instructor")
        self.btn_add_instructor.setObjectName("add_btn")
        self.btn_add_instructor.setProperty("class", "action_btn")
        self.btn_add_instructor.clicked.connect(self.open_add_instructor_dialog)
        
        self.btn_edit_instructor = QPushButton(" Edit")
        self.btn_edit_instructor.setIcon(qta.icon("fa5s.edit", color="#2b2b2b"))
        self.btn_edit_instructor.setProperty("class", "action_btn")
        self.btn_edit_instructor.clicked.connect(self.open_edit_instructor_dialog)

        self.btn_delete_instructor = QPushButton(" Delete")
        self.btn_delete_instructor.setIcon(qta.icon("fa5s.trash-alt", color="#c0392b"))
        self.btn_delete_instructor.setProperty("class", "action_btn")
        self.btn_delete_instructor.clicked.connect(self.delete_selected_instructor)

        top_bar.addWidget(self.instructor_search)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_add_instructor)
        top_bar.addWidget(self.btn_edit_instructor)
        top_bar.addWidget(self.btn_delete_instructor)
        layout.addLayout(top_bar)

        self.instructors_table = QTableWidget()
        self.instructors_table.setColumnCount(3)
        self.instructors_table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        self.instructors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.instructors_table.verticalHeader().setVisible(False)
        self.instructors_table.setAlternatingRowColors(True)
        self.instructors_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.instructors_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        layout.addWidget(self.instructors_table)
        self.instructors_page.setLayout(layout)
        
        self.load_instructors_table()

    def load_instructors_table(self):
        """ Fetches all instructors from DB and populates the table """
        self.instructors_table.setRowCount(0)
        try:
            instructors = Instructor.get_all_instructors() 
            for row_idx, instructor_data in enumerate(instructors):
                self.instructors_table.insertRow(row_idx)
                
                # Column 0: ID, 1: Name, 2: Email
                self.instructors_table.setItem(row_idx, 0, QTableWidgetItem(str(instructor_data[0])))
                self.instructors_table.setItem(row_idx, 1, QTableWidgetItem(str(instructor_data[1])))
                self.instructors_table.setItem(row_idx, 2, QTableWidgetItem(str(instructor_data[2])))
                
                for i in range(3):
                    self.instructors_table.item(row_idx, i).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Error loading instructors: {e}")
            QMessageBox.critical(self, "DB Error", f"Failed to load instructors: {e}")

    def open_add_instructor_dialog(self):
        dialog = AddInstructorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name, email = dialog.get_data()
            if name and email:
                try:
                    new_instructor = Instructor(name=name, email=email, instructor_id=None)
                    new_instructor.save_to_db() 
                    self.load_instructors_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not add instructor: {e}")

    def open_edit_instructor_dialog(self):
        row = self.instructors_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select an instructor to edit.")
            return
            
        iid = int(self.instructors_table.item(row, 0).text())
        name = self.instructors_table.item(row, 1).text()
        email = self.instructors_table.item(row, 2).text()
        
        dialog = AddInstructorDialog(self, instructor_data={'name': name, 'email': email})
        if dialog.exec_() == QDialog.Accepted:
            new_name, new_email = dialog.get_data()
            if new_name and new_email:
                try:
                    # Update is handled by Instructor object with existing ID
                    instructor_to_update = Instructor(name=new_name, email=new_email, instructor_id=iid)
                    instructor_to_update.save_to_db()
                    self.load_instructors_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not update instructor: {e}")

    def delete_selected_instructor(self):
        row = self.instructors_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Warning", "Please select an instructor to delete.")
            return
            
        iid = int(self.instructors_table.item(row, 0).text())
        name = self.instructors_table.item(row, 1).text()
        
        # Use custom QMessageBox for styling delete buttons
        confirm_box = QMessageBox(self)
        confirm_box.setWindowTitle("Confirm Delete")
        confirm_box.setText(f"Are you sure you want to delete '{name}'?")
        confirm_box.setIcon(QMessageBox.Question)
        
        # Add buttons
        yes_btn = confirm_box.addButton(QMessageBox.Yes)
        no_btn = confirm_box.addButton(QMessageBox.No)
        
        # Style the buttons
        btn_style = """
            QPushButton { 
                background-color: rgb(192, 192, 255); 
                color: #2b2b2b; 
                border: none; 
                padding: 5px 15px; 
                min-width: 60px; 
                border-radius: 5px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #a0a0ff; 
            }
        """
        yes_btn.setStyleSheet(btn_style)
        no_btn.setStyleSheet(btn_style)
        
        confirm = confirm_box.exec_()
        
        if confirm == QMessageBox.Yes:
            try:
                Instructor.delete_instructor(iid) 
                self.load_instructors_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete instructor: {e}")

    # --- HELPERS ---
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
        return page

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())