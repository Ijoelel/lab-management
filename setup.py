import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtWidgets import *
from src import control

class LabManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab Management Application")
        self.setGeometry(100, 100, 1000, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_user_list)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Sidebar layout
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)

        # Create Dashboard section
        dashboard = QPushButton("Dashboard")
        dashboard.clicked.connect(self.dashboard_selected)
        dashboard.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create User section
        user_label = QLabel("User")
        user_combo = QComboBox()
        user_combo.addItems(["Select Action", "Add User", "Delete User", "Edit User", "List User"])
        user_combo.currentIndexChanged.connect(self.user_action_selected)

        # Create Usage section
        usage_label = QLabel("Usage")
        usage_combo = QComboBox()
        usage_combo.addItems(["Select Action", "View Usage", "Edit Usage", "Add Usage", "Delete Usage"])
        usage_combo.currentIndexChanged.connect(self.usage_action_selected)

        # Create Equipment section
        equipment_label = QLabel("Equipment")
        equipment_combo = QComboBox()
        equipment_combo.addItems(["Select Action", "Add Equipment", "Delete Equipment", "Edit Equipment", "List Equipment"])
        equipment_combo.currentIndexChanged.connect(self.equipment_action_selected)

        # Add widgets to the sidebar layout
        sidebar_layout.addWidget(dashboard)
        sidebar_layout.addWidget(user_label)
        sidebar_layout.addWidget(user_combo)
        sidebar_layout.addWidget(usage_label)
        sidebar_layout.addWidget(usage_combo)
        sidebar_layout.addWidget(equipment_label)
        sidebar_layout.addWidget(equipment_combo)

        # Main content area with QStackedWidget
        self.pages = QStackedWidget()
        self.pages.addWidget(self.create_dashboard_page())
        self.pages.addWidget(self.create_add_user_page())
        self.pages.addWidget(self.create_delete_user_page())
        self.pages.addWidget(self.create_edit_user_page())
        self.pages.addWidget(self.create_list_user_page())
        self.pages.addWidget(self.create_view_usage_page())
        self.pages.addWidget(self.create_edit_usage_page())
        self.pages.addWidget(self.create_add_usage_page())
        self.pages.addWidget(self.create_delete_usage_page())
        self.pages.addWidget(self.create_add_equipment_page())
        self.pages.addWidget(self.create_delete_equipment_page())
        self.pages.addWidget(self.create_edit_equipment_page())
        self.pages.addWidget(self.create_list_equipment_page())

        # Add sidebar and pages to the main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(main_widget)

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        dashboard_label = QLabel("Lab Management Application\nby\nAfrizal Luthfi Eka Arnatha") 
        layout.addWidget(dashboard_label)
        return page

    # User Pages
    def create_add_user_page(self):
        page = QWidget()
        
        add_user_layout = QVBoxLayout(page)
        add_user_layout.addWidget(QLabel("Halaman Tambah User"))

        add_user_layout.addWidget(QLabel("Nama User"))
        name_input = QLineEdit()
        add_user_layout.addWidget(name_input)

        add_user_layout.addWidget(QLabel("Role"))
        role_combo = QComboBox()
        role_combo.addItems(["Admin", "User", "Technician"])
        add_user_layout.addWidget(role_combo)

        add_user_layout.addWidget(QLabel("Email"))
        email_input = QLineEdit()
        add_user_layout.addWidget(email_input)

        add_user_layout.addWidget(QLabel("Password"))
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        add_user_layout.addWidget(password_input)

        add_user_button = QPushButton("Tambah User")
        add_user_button.clicked.connect(lambda: self.show_message_dialog(control.User().add_user(name_input.text(), email_input.text(), password_input.text(), role_combo.currentText(),), "Status penambahan pengguna"))
        add_user_layout.addWidget(add_user_button)

        return page

    def create_delete_user_page(self):
        page = QWidget()

        delete_user_layout = QVBoxLayout(page)
        delete_user_layout.addWidget(QLabel("Halaman Hapus User"))

        delete_user_layout.addWidget(QLabel("Nama User"))
        name_input = QLineEdit()
        delete_user_layout.addWidget(name_input)

        delete_user_layout.addWidget(QLabel("Email"))
        email_input = QLineEdit()
        delete_user_layout.addWidget(email_input)

        delete_user_button = QPushButton("Hapus User")
        delete_user_button.clicked.connect(lambda: self.show_message_dialog(control.User().delete_user(name_input.text(), email_input.text()), "Status penghapusan pengguna"))
        delete_user_layout.addWidget(delete_user_button)

        return page

    def create_edit_user_page(self):
        page = QWidget()

        edit_user_layout = QVBoxLayout(page)
        edit_user_layout.addWidget(QLabel("Halaman Edit User"))

        edit_user_layout.addWidget(QLabel("Nama User"))
        name_input=QLineEdit()
        edit_user_layout.addWidget(name_input)

        edit_user_layout.addWidget(QLabel("Email"))
        email_input=QLineEdit()
        edit_user_layout.addWidget(email_input)

        edit_user_layout.addWidget(QLabel("Nama Baru"))
        new_name_input=QLineEdit()
        edit_user_layout.addWidget(new_name_input)

        edit_user_layout.addWidget(QLabel("Email Baru"))
        new_email_input=QLineEdit()
        edit_user_layout.addWidget(new_email_input)

        edit_user_layout.addWidget(QLabel("Role Baru"))
        role_combo = QComboBox()
        role_combo.addItems(["Admin", "User", "Technician"])
        edit_user_layout.addWidget(role_combo)

        edit_user_button = QPushButton("Update User")
        edit_user_button.clicked.connect(lambda: self.show_message_dialog(control.User().update_user(name_input.text(), email_input.text(), new_name_input.text(), new_email_input.text(), role_combo.currentText()), "Status pengeditan pengguna"))
        edit_user_layout.addWidget(edit_user_button)

        return page

    def create_list_user_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.user_table = QTableWidget()
        self.user_table.setRowCount(0)  # Start with zero rows
        self.user_table.setColumnCount(3)  # 4 columns
        self.user_table.setHorizontalHeaderLabels(["Nama", "Email", "Role"])

        # Add some sample data (You can dynamically add data here)
        users = control.User().get_all_user()

        if users:
            for user in users:
                self.add_user_data(user["nama"], user["email"], user["role"])

        # Set the size policy to expanding
        self.user_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make the table stretch to fit the width
        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.user_table)
        return page
    
    def add_user_data(self, name, email, role):
        row_position = self.user_table.rowCount()
        self.user_table.insertRow(row_position)  # Insert a new row
        self.user_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.user_table.setItem(row_position, 1, QTableWidgetItem(email))
        self.user_table.setItem(row_position, 2, QTableWidgetItem(role))

    # Usage Pages
    def create_view_usage_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.usage_table = QTableWidget()
        self.usage_table.setRowCount(0)  # Start with zero rows
        self.usage_table.setColumnCount(6)  # 4 columns
        self.usage_table.setHorizontalHeaderLabels(["Nama", "Email", "Tanggal", "Role", "Status", "Usage Information"])

        # Add some sample data (You can dynamically add data here)
        usages = control.Usage().get_all_usage()

        if usages:
            for usage in usages:
                self.add_usage_data(usage["nama"], usage["email"], usage["date"], usage["role"], usage["status"], usage["info"])

        # Set the size policy to expanding
        self.usage_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make the table stretch to fit the width
        header = self.usage_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.usage_table)
        return page

    def add_usage_data(self, name, email, date, role, status, info):
        row_position = self.usage_table.rowCount()
        self.usage_table.insertRow(row_position)  # Insert a new row
        self.usage_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.usage_table.setItem(row_position, 1, QTableWidgetItem(email))
        self.usage_table.setItem(row_position, 2, QTableWidgetItem(date))
        self.usage_table.setItem(row_position, 3, QTableWidgetItem(role))
        self.usage_table.setItem(row_position, 4, QTableWidgetItem(status))
        self.usage_table.setItem(row_position, 5, QTableWidgetItem(info))

    def create_edit_usage_page(self):
        page = QWidget()

        edit_usage_layout = QVBoxLayout(page)
        edit_usage_layout.addWidget(QLabel("Halaman Edit Penggunaan Lab"))

        edit_usage_layout.addWidget(QLabel("Nama User"))
        name_input=QLineEdit()
        edit_usage_layout.addWidget(name_input)

        edit_usage_layout.addWidget(QLabel("Tanggal"))
        date_input=QDateEdit()
        edit_usage_layout.addWidget(date_input)

        edit_usage_layout.addWidget(QLabel("Status Baru"))
        new_status_input=QLineEdit()
        edit_usage_layout.addWidget(new_status_input)

        edit_usage_layout.addWidget(QLabel("Informasi Penggunaan baru"))
        new_info_input=QLineEdit()
        edit_usage_layout.addWidget(new_info_input)

        edit_usage_button = QPushButton("Update Penggunaan Lab")
        edit_usage_button.clicked.connect(lambda: self.show_message_dialog(control.Usage().edit_usage(name_input.text(), date_input.text(), new_status_input.text(), new_info_input.text()), "Status pengeditan pengguna"))
        edit_usage_layout.addWidget(edit_usage_button)

        return page
    
    def create_add_usage_page(self):
        page = QWidget()

        add_usage_layout = QVBoxLayout(page)
        add_usage_layout.addWidget(QLabel("Halaman Tambah Penggunaan Lab"))

        add_usage_layout.addWidget(QLabel("Nama User"))
        name_input=QLineEdit()
        add_usage_layout.addWidget(name_input)

        add_usage_layout.addWidget(QLabel("Email"))
        email_input=QLineEdit()
        add_usage_layout.addWidget(email_input)

        add_usage_layout.addWidget(QLabel("Tanggal"))
        date_input=QDateEdit()
        add_usage_layout.addWidget(date_input)

        add_usage_layout.addWidget(QLabel("Role"))
        role_combo = QComboBox()
        role_combo.addItems(["Admin", "User", "Technician"])
        add_usage_layout.addWidget(role_combo)

        add_usage_layout.addWidget(QLabel("Status"))
        status_input=QLineEdit()
        add_usage_layout.addWidget(status_input)

        add_usage_layout.addWidget(QLabel("Info"))
        info_input=QLineEdit()
        add_usage_layout.addWidget(info_input)

        add_usage_button = QPushButton("Tambah Penggunaan Lab")
        add_usage_button.clicked.connect(lambda: self.show_message_dialog(control.Usage().add_usage(name_input.text(), email_input.text(), date_input.text(), role_combo.currentText(), status_input.text(), info_input.text()), "Status pengeditan penggunaan lab"))
        add_usage_layout.addWidget(add_usage_button)

        return page

    def create_delete_usage_page(self):
        page = QWidget()

        delete_usage_layout = QVBoxLayout(page)
        delete_usage_layout.addWidget(QLabel("Halaman Hapus User"))

        delete_usage_layout.addWidget(QLabel("Nama User"))
        name_input = QLineEdit()
        delete_usage_layout.addWidget(name_input)

        delete_usage_layout.addWidget(QLabel("Tanggal"))
        date_input = QDateEdit()
        delete_usage_layout.addWidget(date_input)

        delete_usage_button = QPushButton("Hapus Penggunaan Lab")
        delete_usage_button.clicked.connect(lambda: self.show_message_dialog(control.Usage().delete_usage(name_input.text(), date_input.text()), "Status penghapusan penggunaan lab"))
        delete_usage_layout.addWidget(delete_usage_button)

        return page

    # Equipment Pages
    def create_add_equipment_page(self):
        page = QWidget()

        add_equipment_layout = QVBoxLayout(page)
        add_equipment_layout.addWidget(QLabel("Halaman Tambah Equipment"))

        add_equipment_layout.addWidget(QLabel("Nama Equipment"))
        name_input=QLineEdit()
        add_equipment_layout.addWidget(name_input)

        add_equipment_layout.addWidget(QLabel("Status Equipment"))
        status_combo = QComboBox()
        status_combo.addItems(["New", "Broken"])
        add_equipment_layout.addWidget(status_combo)

        add_equipment_button = QPushButton("Tambah Equipment")
        add_equipment_button.clicked.connect(lambda: self.show_message_dialog(control.Equipment().add_equipment(name_input.text(), status_combo.currentText()), "Status penambahan equipment"))
        add_equipment_layout.addWidget(add_equipment_button)

        return page

    def create_delete_equipment_page(self):
        page = QWidget()

        delete_equipment_layout = QVBoxLayout(page)
        delete_equipment_layout.addWidget(QLabel("Halaman Hapus Equipment Lab"))

        delete_equipment_layout.addWidget(QLabel("Nama Equipment"))
        name_input = QLineEdit()
        delete_equipment_layout.addWidget(name_input)

        delete_equipment_layout.addWidget(QLabel("Status Equipment"))
        status_combo = QComboBox()
        status_combo.addItems(["New", "Broken"])
        delete_equipment_layout.addWidget(status_combo)

        delete_equipment_button = QPushButton("Hapus Equipment")
        delete_equipment_button.clicked.connect(lambda: self.show_message_dialog(control.Equipment().delete_equipment(name_input.text(), status_combo.currentText()), "Status penghapusan equipment"))
        delete_equipment_layout.addWidget(delete_equipment_button)

        return page

    def create_edit_equipment_page(self):
        page = QWidget()

        edit_equipment_layout = QVBoxLayout(page)
        edit_equipment_layout.addWidget(QLabel("Halaman Edit User"))

        edit_equipment_layout.addWidget(QLabel("Nama Equipment"))
        name_input=QLineEdit()
        edit_equipment_layout.addWidget(name_input)

        edit_equipment_layout.addWidget(QLabel("Status Equipment"))
        status_combo = QComboBox()
        status_combo.addItems(["New", "Broken"])
        edit_equipment_layout.addWidget(status_combo)
        
        edit_equipment_layout.addWidget(QLabel("Status Equipment Baru"))
        new_status_combo = QComboBox()
        new_status_combo.addItems(["New", "Broken"])
        edit_equipment_layout.addWidget(new_status_combo)

        edit_equipment_layout.addWidget(QLabel("Jumlah Barang"))
        new_qty_input=QLineEdit()
        edit_equipment_layout.addWidget(new_qty_input)

        edit_equipment_button = QPushButton("Update Equipment Data")
        edit_equipment_button.clicked.connect(lambda: self.show_message_dialog(control.Equipment().update_equipment(name_input.text(), status_combo.currentText(), new_status_combo.currentText(), int(new_qty_input.text())), "Status pengeditan pengguna"))
        edit_equipment_layout.addWidget(edit_equipment_button)

        return page
    
    def create_list_equipment_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        self.equipment_table = QTableWidget()
        self.equipment_table.setRowCount(0)  # Start with zero rows
        self.equipment_table.setColumnCount(3)  # 4 columns
        self.equipment_table.setHorizontalHeaderLabels(["Nama Equipment", "Quantity", "Status"])

        # Add some sample data (You can dynamically add data here)
        equipments = control.Equipment().get_all_equipment()

        if equipments:
            for equipment in equipments:
                self.add_equipment_data(equipment["nama_equipment"], equipment["qty"], equipment["status"])

        # Set the size policy to expanding
        self.equipment_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make the table stretch to fit the width
        header = self.equipment_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.equipment_table)
        return page
    
    def add_equipment_data(self, name, qty, status):
        row_position = self.equipment_table.rowCount()
        self.equipment_table.insertRow(row_position)  # Insert a new row
        self.equipment_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.equipment_table.setItem(row_position, 1, QTableWidgetItem(str(qty)))
        self.equipment_table.setItem(row_position, 2, QTableWidgetItem(status))

    # Action Selection Handlers
    def dashboard_selected(self):
        self.pages.setCurrentIndex(0)
    def user_action_selected(self, index):
        action_map = {1: 1, 2: 2, 3: 3, 4: 4}  # Map combo box index to page index
        self.pages.setCurrentIndex(action_map.get(index, 0))

        if index == 4:
            self.update_user_list()


    def usage_action_selected(self, index):
        action_map = {1: 5, 2: 6, 3: 7, 4: 8}
        self.pages.setCurrentIndex(action_map.get(index, 0))

        if index == 1:
            self.update_usage_list()

    def equipment_action_selected(self, index):
        action_map = {1: 9, 2: 10, 3: 11, 4: 12}
        self.pages.setCurrentIndex(action_map.get(index, 0))

        if index == 4:
            self.update_equipment_list()

    # Utility function
    def show_message_dialog(self, msg, title):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)

        if msg == 0:
            msg_box.setText("Gagal melakukan operasi")    
        elif msg == 1:
            msg_box.setText("Berhasil melakukan operasi")
        elif msg == 2:
            msg_box.setText("Nama dan Email tidak terdaftar sebagai pengguna")

        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def refresh_data(self):
        # Call this function to refresh data from the database
        self.update_user_list()
        self.update_usage_list()
        self.update_equipment_list()

    def update_user_list(self):
        # Refresh the user list from the database
        users = control.User().get_all_user()
        self.user_table.setRowCount(0)  # Clear the existing rows

        if users:
            for user in users:
                self.add_user_data(user["nama"], user["email"], user["role"])

    def update_usage_list(self):
        # Refresh the usage list from the database
        usages = control.Usage().get_all_usage()
        self.usage_table.setRowCount(0)  # Clear the existing rows

        if usages:
            for usage in usages:
                self.add_usage_data(usage["nama"], usage["email"], usage["date"], usage["role"], usage["status"], usage["info"])

    def update_equipment_list(self):
        # Refresh the equipment list from the database
        equipments = control.Equipment().get_all_equipment()
        self.equipment_table.setRowCount(0)  # Clear the existing rows

        if equipments:
            for equipment in equipments:
                self.add_equipment_data(equipment["nama_equipment"], equipment["qty"], equipment["status"])

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("src/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    window = LabManagementApp()
    window.show()

    app.exec()
