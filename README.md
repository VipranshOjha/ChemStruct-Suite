Here’s your updated `README.md` for **ChemStruct Suite**:

---

# 🧪 ChemStruct Suite

**ChemStruct Suite** is an integrated toolkit for computational chemistry, combining a **GAMESS input file builder** with an interactive **3D molecular visualizer**.
Easily configure quantum chemistry simulations, load molecular structures, and explore them in rich, real-time 3D.

---

## ✨ Features

### **1️⃣ GAMESS Input Builder (`InputBuilder.py`)**

* **Material-inspired Tkinter UI** with theme support via `ttkthemes`.
* Dropdown menus for quickly selecting:

  * SCF methods (RHF, UHF, ROHF, GVB, MCSCF)
  * Basis sets (cc-pVDZ, cc-pVTZ, cc-pVQZ)
  * RUNTYP (Energy, Hessian, Optimization)
  * Memory settings, charge, spin multiplicity, etc.
* **.xyz file loader** for importing molecular geometries.
* Live **preview panel** for generated GAMESS input.
* **One-click export** to `gamess_input.txt`.

---

### **2️⃣ Molecular Visualizer (`MolecularVisualizer.py`)**

* **3D rendering** of molecules using OpenGL with realistic atom colors and sizes.
* **PDB file support** for loading molecular structures.
* **Interactive atom placement** – Click in the 3D space to add atoms.
* Scroll to **zoom in/out**.
* Atom selection via dropdown menu (supports full periodic table).

---

## 📂 Project Structure

```
ChemStructSuite/
│── InputBuilder1.0.py           # GAMESS Input Builder GUI
│── MolecularVisualizer.py       # 3D Molecular Visualizer with PyQt5 + OpenGL
│── InputBuilder1.0.spec         # Build config for creating executables
```

---

## 🚀 Installation

### 1️⃣ Install Dependencies

Make sure you have Python 3.x and install the required libraries:

```bash
pip install tkinter ttkthemes pyqt5 PyOpenGL numpy
```

> Note: `tkinter` may already be included with your Python installation.

---

## 🖥 Usage

### **Run the Input Builder**

```bash
python InputBuilder1.0.py
```

* Fill in desired GAMESS parameters.
* Load `.xyz` geometry if needed.
* Click **"Generate GAMESS Input"** to preview and save the file.

### **Run the Molecular Visualizer**

```bash
python MolecularVisualizer.py
```

* Use **File → Open** to load a `.pdb` structure.
* Select an atom type from **Atom → Select Atom**.
* Left-click in the viewer to add atoms.
* Scroll to zoom in/out.

---

## 🔮 Future Improvements

* Add **bond rendering** between atoms in the visualizer.
* Support **drag-and-drop** for file loading.
* Enable **saving modified molecules** back to `.pdb` format.
* Add **GAMESS job submission** integration.

---

## 📜 License

This project is open-source and free to use for **learning** and **research purposes**.

---
