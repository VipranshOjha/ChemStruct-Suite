import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QOpenGLWidget, QAction, QFileDialog, QDialog, QVBoxLayout,
                             QComboBox, QDialogButtonBox)
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Atom color and size dictionaries
ATOM_COLORS = {
    'H': (1.0, 1.0, 1.0), 'He': (0.85, 1.0, 1.0), 'Li': (0.8, 0.5, 1.0),
    'Be': (0.76, 1.0, 0.0), 'B': (1.0, 0.7, 0.7), 'C': (0.5, 0.5, 0.5),
    'N': (0.0, 0.0, 1.0), 'O': (1.0, 0.0, 0.0), 'F': (0.7, 1.0, 1.0),
    'Ne': (0.7, 0.89, 0.96), 'Na': (0.67, 0.36, 0.95), 'Mg': (0.54, 1.0, 0.0),
    'Al': (0.75, 0.65, 0.65), 'Si': (0.94, 0.78, 0.62), 'P': (1.0, 0.5, 0.0),
    'S': (1.0, 1.0, 0.18), 'Cl': (0.12, 0.94, 0.12), 'Ar': (0.5, 0.82, 0.89),
    'K': (0.56, 0.25, 0.83), 'Ca': (0.24, 1.0, 0.0), 'Sc': (0.9, 0.9, 0.9),
    'Ti': (0.75, 0.76, 0.78), 'V': (0.65, 0.65, 0.67), 'Cr': (0.54, 0.6, 0.78),
    'Mn': (0.61, 0.48, 0.78), 'Fe': (0.88, 0.4, 0.2), 'Co': (0.94, 0.56, 0.63),
    'Ni': (0.31, 0.82, 0.31), 'Cu': (0.78, 0.5, 0.2), 'Zn': (0.49, 0.5, 0.69),
    'Ga': (0.76, 0.56, 0.56), 'Ge': (0.4, 0.56, 0.56), 'As': (0.74, 0.5, 0.89),
    'Se': (1.0, 0.63, 0.0), 'Br': (0.65, 0.16, 0.16), 'Kr': (0.36, 0.72, 0.82),
    'Rb': (0.44, 0.18, 0.69), 'Sr': (0.0, 1.0, 0.0), 'Y': (0.58, 1.0, 1.0),
    'Zr': (0.58, 0.88, 0.88), 'Nb': (0.45, 0.76, 0.79), 'Mo': (0.33, 0.71, 0.71),
    'Tc': (0.23, 0.62, 0.62), 'Ru': (0.14, 0.56, 0.56), 'Rh': (0.04, 0.49, 0.55),
    'Pd': (0.0, 0.41, 0.52), 'Ag': (0.75, 0.75, 0.75), 'Cd': (1.0, 0.85, 0.56),
    'In': (0.65, 0.46, 0.45), 'Sn': (0.4, 0.5, 0.5), 'Sb': (0.62, 0.39, 0.71),
    'Te': (0.83, 0.48, 0.0), 'I': (0.58, 0.0, 0.58), 'Xe': (0.26, 0.62, 0.69),
    'Cs': (0.34, 0.09, 0.56), 'Ba': (0.0, 0.79, 0.0), 'La': (0.44, 0.83, 1.0),
    'Ce': (1.0, 1.0, 0.78), 'Pr': (0.85, 1.0, 0.78), 'Nd': (0.78, 1.0, 0.78),
    'Pm': (0.64, 1.0, 0.78), 'Sm': (0.56, 1.0, 0.78), 'Eu': (0.38, 1.0, 0.78),
    'Gd': (0.27, 1.0, 0.78), 'Tb': (0.19, 1.0, 0.78), 'Dy': (0.12, 1.0, 0.78),
    'Ho': (0.0, 1.0, 0.61), 'Er': (0.0, 0.9, 0.46), 'Tm': (0.0, 0.83, 0.32),
    'Yb': (0.0, 0.75, 0.22), 'Lu': (0.0, 0.67, 0.14), 'Hf': (0.3, 0.76, 1.0),
    'Ta': (0.3, 0.65, 1.0), 'W': (0.13, 0.58, 0.84), 'Re': (0.15, 0.49, 0.67),
    'Os': (0.15, 0.4, 0.59), 'Ir': (0.09, 0.33, 0.53), 'Pt': (0.82, 0.82, 0.88),
    'Au': (1.0, 0.82, 0.14), 'Hg': (0.72, 0.72, 0.82), 'Tl': (0.65, 0.33, 0.3),
    'Pb': (0.34, 0.35, 0.38), 'Bi': (0.62, 0.31, 0.71), 'Po': (0.67, 0.36, 0.0),
    'At': (0.46, 0.31, 0.27), 'Rn': (0.26, 0.51, 0.59), 'Fr': (0.26, 0.0, 0.4),
    'Ra': (0.0, 0.49, 0.0), 'Ac': (0.44, 0.67, 0.98), 'Th': (0.0, 0.73, 1.0),
    'Pa': (0.0, 0.63, 1.0), 'U': (0.0, 0.56, 1.0), 'Np': (0.0, 0.5, 1.0),
    'Pu': (0.0, 0.42, 1.0), 'Am': (0.33, 0.36, 0.95), 'Cm': (0.47, 0.36, 0.89),
    'Bk': (0.54, 0.3, 0.89), 'Cf': (0.63, 0.21, 0.83), 'Es': (0.7, 0.12, 0.83),
    'Fm': (0.7, 0.12, 0.73), 'Md': (0.7, 0.05, 0.65), 'No': (0.74, 0.05, 0.53),
    'Lr': (0.78, 0.0, 0.4), 'Rf': (0.8, 0.0, 0.35), 'Db': (0.82, 0.0, 0.31),
    'Sg': (0.85, 0.0, 0.27), 'Bh': (0.88, 0.0, 0.22), 'Hs': (0.9, 0.0, 0.18),
    'Mt': (0.92, 0.0, 0.15), 'Ds': (0.94, 0.0, 0.12), 'Rg': (0.96, 0.0, 0.08),
    'Cn': (0.98, 0.0, 0.05), 'Nh': (1.0, 0.0, 0.0), 'Fl': (0.85, 0.85, 0.85),
    'Mc': (0.75, 0.75, 0.75), 'Lv': (0.65, 0.65, 0.65), 'Ts': (0.55, 0.55, 0.55),
    'Og': (0.45, 0.45, 0.45)
}

ATOM_SIZES = {
   'H': 0.1, 'He': 0.1, 'Li': 0.2, 'Be': 0.2, 'B': 0.2, 'C': 0.2, 'N': 0.2,
    'O': 0.2, 'F': 0.2, 'Ne': 0.2, 'Na': 0.3, 'Mg': 0.3, 'Al': 0.3, 'Si': 0.3,
    'P': 0.3, 'S': 0.3, 'Cl': 0.3, 'Ar': 0.3, 'K': 0.4, 'Ca': 0.4, 'Sc': 0.4,
    'Ti': 0.4, 'V': 0.4, 'Cr': 0.4, 'Mn': 0.4, 'Fe': 0.4, 'Co': 0.4, 'Ni': 0.4,
    'Cu': 0.4, 'Zn': 0.4, 'Ga': 0.4, 'Ge': 0.4, 'As': 0.4, 'Se': 0.4, 'Br': 0.4,
    'Kr': 0.4, 'Rb': 0.5, 'Sr': 0.5, 'Y': 0.5, 'Zr': 0.5, 'Nb': 0.5, 'Mo': 0.5,
    'Tc': 0.5, 'Ru': 0.5, 'Rh': 0.5, 'Pd': 0.5, 'Ag': 0.5, 'Cd': 0.5, 'In': 0.5,
    'Sn': 0.5, 'Sb': 0.5, 'Te': 0.5, 'I': 0.5, 'Xe': 0.5, 'Cs': 0.6, 'Ba': 0.6,
    'La': 0.6, 'Ce': 0.6, 'Pr': 0.6, 'Nd': 0.6, 'Pm': 0.6, 'Sm': 0.6, 'Eu': 0.6,
    'Gd': 0.6, 'Tb': 0.6, 'Dy': 0.6, 'Ho': 0.6, 'Er': 0.6, 'Tm': 0.6, 'Yb': 0.6,
    'Lu': 0.6, 'Hf': 0.6, 'Ta': 0.6, 'W': 0.6, 'Re': 0.6, 'Os': 0.6, 'Ir': 0.6,
    'Pt': 0.6, 'Au': 0.6, 'Hg': 0.6, 'Tl': 0.6, 'Pb': 0.6, 'Bi': 0.6, 'Po': 0.6,
    'At': 0.6, 'Rn': 0.6, 'Fr': 0.7, 'Ra': 0.7, 'Ac': 0.7, 'Th': 0.7, 'Pa': 0.7,
    'U': 0.7, 'Np': 0.7, 'Pu': 0.7, 'Am': 0.7, 'Cm': 0.7, 'Bk': 0.7, 'Cf': 0.7,
    'Es': 0.7, 'Fm': 0.7, 'Md': 0.7, 'No': 0.7, 'Lr': 0.7, 'Rf': 0.7, 'Db': 0.7,
    'Sg': 0.7, 'Bh': 0.7, 'Hs': 0.7, 'Mt': 0.7, 'Ds': 0.7, 'Rg': 0.7, 'Cn': 0.7,
    'Nh': 0.7, 'Fl': 0.7, 'Mc': 0.7, 'Lv': 0.7, 'Ts': 0.7, 'Og': 0.7
}

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.molecule = []
        self.zoom = -10.0
        self.atoms = []
        self.selected_atom = 'C'

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, self.width() / self.height(), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.zoom)
        self.draw_molecule()

    def draw_molecule(self):
        for atom in self.atoms:
            self.draw_atom(atom['symbol'], atom['x'], atom['y'], atom['z'])

    def draw_atom(self, atom_symbol, pos_x, pos_y, pos_z):
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        color = ATOM_COLORS.get(atom_symbol, (1.0, 1.0, 1.0))
        size = ATOM_SIZES.get(atom_symbol, 0.5)
        glColor3f(*color)
        quadric = gluNewQuadric()
        gluSphere(quadric, size, 20, 20)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def load_molecule(self, file_name: str):
        self.molecule = self.parse_pdb(file_name)
        self.update()

    def add_atom(self, symbol, pos_x, pos_y, pos_z):
        atom_data = {
            'symbol': symbol,
            'x': pos_x,
            'y': pos_y,
            'z': pos_z
        }
        self.atoms.append(atom_data)
        self.update()

    def parse_pdb(self, file_name):
        atoms = []
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    atom = {
                        'symbol': line[76:78].strip(),
                        'x': float(line[30:38].strip()),
                        'y': float(line[38:46].strip()),
                        'z': float(line[46:54].strip())
                    }
                    atoms.append(atom)
        return atoms

    def setZoom(self, zoom):
        self.zoom = zoom
        self.update()

    def convert_screen_to_3d(self, screen_x, screen_y):
        # Get the viewport, projection, and modelview matrices
        viewport = glGetIntegerv(GL_VIEWPORT)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)

        # Invert Y coordinate for OpenGL (OpenGL's origin is bottom-left, but Qt's is top-left)
        screen_y = viewport[3] - screen_y - 1

        # Read the depth value from the z-buffer at the clicked position
        z_depth = glReadPixels(screen_x, screen_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

        # Ensure depth is within the valid range
        if z_depth == 1.0:  # This means no depth info was found (clicking outside the objects)
            z_depth = 0.5  # Default to some middle depth

        # Unproject the 2D screen coordinates into 3D world coordinates
        x_3d, y_3d, z_3d = gluUnProject(screen_x, screen_y, z_depth, modelview, projection, viewport)

        return x_3d, y_3d, z_3d

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Molecule Visualizer")

        # Initialize OpenGL widget
        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)

        # Initialize selected_atom attribute
        self.selected_atom = 'C'

        # Create a combo box for atom selection
        self.atom_combobox = QComboBox(self)
        self.atom_combobox.addItems(ATOM_COLORS.keys())
        self.atom_combobox.currentIndexChanged.connect(self.on_atom_selection_changed)
        self.atom_combobox.setCurrentText(self.selected_atom)
        
        # Add the combo box to the menu
        self.init_menu()

    def init_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        atom_menu = menu_bar.addMenu("Atom")
        select_atom_action = QAction("Select Atom", self)
        select_atom_action.triggered.connect(self.open_atom_selection_dialog)
        atom_menu.addAction(select_atom_action)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDB File", "", "PDB Files (*.pdb);;All Files (*)",
                                                   options=options)
        if file_name:
            self.opengl_widget.load_molecule(file_name)

    def open_atom_selection_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Atom")

        layout = QVBoxLayout()
        layout.addWidget(self.atom_combobox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            self.selected_atom = self.atom_combobox.currentText()

    def on_atom_selection_changed(self, index):
        self.selected_atom = self.atom_combobox.currentText()
        self.opengl_widget.selected_atom = self.selected_atom

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.selected_atom:
            mouse_x = event.x()
            mouse_y = event.y()

            x_3d, y_3d, z_3d = self.opengl_widget.convert_screen_to_3d(mouse_x, mouse_y)

            self.opengl_widget.add_atom(self.selected_atom, x_3d, y_3d, z_3d)

            self.opengl_widget.update()

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        self.opengl_widget.setZoom(self.opengl_widget.zoom + angle / 120.0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    sys.exit(app.exec_())
