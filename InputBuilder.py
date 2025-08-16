from tkinter import *
from tkinter import ttk
import textwrap
from ttkthemes import ThemedStyle
from tkinter import filedialog

class GamessGenerator:
    def __init__(self, root):
        self.root = root
        # Define row_counter as an instance variable
        self.row_counter = 0

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate a reasonable window size based on the screen size
        window_width = int(screen_width * 0.8)  # Adjust the factor as needed
        window_height = int(screen_height * 0.8)

        # Set the window size
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Allow the window to be resizable in both directions
        self.root.resizable(True, True)

        self.root.title("Gamess Input Generator")

        # Apply the materialistic theme
        style = ThemedStyle(self.root)
        style.set_theme("arc")

        # Configure the style to match the theme
        button_bg_color = style.lookup("TButton", "background")
        style.configure("TLabel", background=button_bg_color, font=("APTOS", 12), foreground="black")
        style.configure("TCombobox", background=button_bg_color, font=("APTOS", 12), foreground="black")
        style.configure("TButton", background=button_bg_color, font=("APTOS", 12), foreground="black")
        style.configure("TText", background=button_bg_color, font=("APTOS", 12), foreground="black")
        self.root.configure(background=button_bg_color)  # Set the window background

        # Default optimization information
        self.optInfo = {
            'guess': 'HUCKEL',
            'runtyp': 'Optimize',
            'scfmeth': 'RHF',
            'lvl': 'MPLEVL=2',
            'charge': '0',
            'spin': '1',
            'memory': '10',
            'memddi': '1',
            'basis': 'cc-pVDZ',
            'geom': ' ',    
        }

        # Define the Gamess input file template
        self.gamess_template = textwrap.dedent('''
             $CONTRL SCFTYP={scfmeth} {lvl} RUNTYP={runtyp} ICHARG={charge}
             COORD=UNIQUE MULT={spin} MAXIT=200 ISPHER=1 $END
             $SYSTEM MWORDS={memory} MEMDDI ={memddi} $END
             $SCF DIRSCF=.TRUE. $END $CPHF CPHF=AO $END
             $STATPT NSTEP=100 HSSEND=.T. $END
             $BASIS  GBASIS={basis} $END
             $GUESS  GUESS={guess} $END
             $DATA
            optg and freq
            C1
            {geom}
            $END
        ''')

        # Create GUI elements
        self.create_widgets()

    def load_xyz_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XYZ Files", "*.xyz")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.geom_var.set(content)

    def create_widgets(self):
        # Dictionary of options for each parameter
        options_dict = {
            'guess': ['HUCKEL', 'HCore'],
            'runtyp': ['Energy', 'Hessian', 'Optimisation'],
            'scfmeth': ['RHF', 'UHF', 'ROHF', 'GVB', 'MCSCF'],
            'lvl': ['MPLEVL=2', 'DFT'],
            'charge': ['0', '1', '2', '3', '4', '5'],
            'spin': ['1', '2'],
            'memory': ['10', '20', '30'],
            'memddi': ['1', '2', '3'],
            'basis': ['cc-pVDZ', 'cc-pVTZ', 'cc-pVQZ'],
            'geom': ['']
        }

        column_counter = 0

        # Create and place labels and comboboxes
        for param, param_options in options_dict.items():
            label = ttk.Label(self.root, text=f"Choose {param.capitalize()}:")
            label.grid(row=self.row_counter, column=column_counter * 2, sticky=W, pady=2, padx=(5, 2))
            var = StringVar()
            var.set(param_options[0])
            drop = ttk.Combobox(self.root, textvariable=var, values=param_options, state='readonly', width=15)
            drop.grid(row=self.row_counter, column=column_counter * 2 + 1, sticky=E+W, pady=2, padx=(2, 5))
            setattr(self, f"{param}_var", var)

            column_counter += 1

            # Move to the next row after every three parameters
            if column_counter == 3:
                column_counter = 0
                self.row_counter += 1

        # Move to the next row
        self.row_counter += 1

        # Button to load .xyz file
        load_button = ttk.Button(self.root, text="Load .xyz File", command=self.load_xyz_file)
        load_button.grid(row=self.row_counter, column=0, columnspan=6, sticky=N+E+S+W, pady=5, padx=10)

        # Move to the next row after the button
        self.row_counter += 1

        # Label for the preview title
        preview_title = ttk.Label(self.root, text="Preview", font=("APTOS", 16, "bold"))
        preview_title.grid(row=self.row_counter, column=0, columnspan=6, sticky=N, pady=10)

        # Move to the next row after the title
        self.row_counter += 1

        # Text widget to display generated code
        self.preview = Text(self.root, height=15, width=100, wrap=WORD, font=("APTOS", 12), foreground="black")
        self.preview.grid(row=self.row_counter, column=0, columnspan=6, sticky=N+E+S+W, pady=5, padx=10)

        # Move to the next row after the text widget
        self.row_counter += 1

        # Button to generate Gamess input
        generate_button = ttk.Button(self.root, text="Generate Gamess Input", command=self.generate_gamess_input)
        generate_button.grid(row=self.row_counter, column=0, columnspan=6, sticky=N+E+S+W, pady=10, padx=10)

        # Configure row and column weights
        for i in range(self.row_counter + 1):
            self.root.rowconfigure(i, weight=1)
        for i in range(6):
            self.root.columnconfigure(i, weight=1)

    def generate_gamess_input(self):
        parameters = {param: getattr(self, f"{param}_var").get() for param in self.optInfo}
        parameters['geom'] = getattr(self, 'geom_var').get()
        parameters['pre'] = '$SCF DIRSCF=.TRUE. $END $CPHF CPHF=AO $END'
        parameters['post'] = ''
        gamess_input = self.gamess_template.format(**parameters)

        # Clear previous content
        self.preview.delete(1.0, END)
        # Insert the generated code into the preview
        self.preview.insert(1.0, gamess_input)

        # Save the Gamess input to a text file
        with open('gamess_input.txt', 'w') as file:
            file.write(gamess_input)

if __name__ == "__main__":
    root = Tk()
    app = GamessGenerator(root)
    root.resizable(False,False)  # Allow the window to be resizable in both directions
    root.mainloop()