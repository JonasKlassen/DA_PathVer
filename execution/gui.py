import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from antlr4 import *
from pysmt.shortcuts import Solver, Not, get_env
from DA_PathVer.contract.antlr.contractLexer import contractLexer
from DA_PathVer.contract.antlr.contractParser import contractParser
from DA_PathVer.contract.ast.contract_ast_builder import ContractASTBuilder
from DA_PathVer.execution.contract_formula_builder import ContractFormulaBuilder
from DA_PathVer.execution.program_formula_builder import ProgramFormulaBuilder, load_trace
from DA_PathVer.program.antlr.repeat_arrLexer import repeat_arrLexer
from DA_PathVer.program.antlr.repeat_arrParser import repeat_arrParser
from DA_PathVer.program.ast.program_ast_builder import ProgramASTBuilder
from DA_PathVer.execution.trace_generator import TraceGenerator

class RepeatArrVerifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Repeat-Arr Verifier")
        self.root.geometry("600x500")

        self.program_dir = tk.StringVar()
        self.trace_num = tk.StringVar(value="1")
        self.contract_num = tk.StringVar(value="1")
        self.contract_num.trace_add("write", lambda *args: self.update_contract_display())
        self.selected_solver = tk.StringVar(value="z3")
        self.program_dir.trace_add("write", lambda *args: self.on_folder_change(*args))
        self.program_dir.trace_add("write", lambda *args: self.update_contract_display())

        # History for selection lists
        self.last_populated_vars = []
        self.last_populated_trace = []

        # Caching state
        self.last_folder = None
        self.last_trace_num = None
        self.cached_executor = None
        self.cached_trace_info = None
        self.cached_domain = None
        self.cached_execution = None

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Program Folder Selection
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill='x', **padding)
        ttk.Label(folder_frame, text="Program Folder:").pack(side='left')
        ttk.Entry(folder_frame, textvariable=self.program_dir).pack(side='left', fill='x', expand=True, padx=5)
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side='left')

        # Trace NUM
        num_frame = ttk.Frame(self.root)
        num_frame.pack(fill='x', **padding)
        ttk.Label(num_frame, text="Trace:").pack(side='left')
        ttk.Spinbox(num_frame, from_=1, to=100, textvariable=self.trace_num, width=5).pack(side='left', padx=5)
        ttk.Button(num_frame, text="Create New Trace", command=self.open_create_trace_dialog).pack(side='left', padx=5)
        ttk.Button(num_frame, text="Create/Edit Contract", command=self.open_create_contract_dialog).pack(side='left', padx=5)

        # Solver Selection
        solver_frame = ttk.Frame(self.root)
        solver_frame.pack(fill='x', **padding)
        ttk.Label(solver_frame, text="Solver:").pack(side='left')
        solvers = list(get_env().factory.all_solvers().keys())
        if not solvers:
            solvers = ["z3"]
        ttk.Combobox(solver_frame, textvariable=self.selected_solver, values=solvers).pack(side='left', padx=5)

        # Buttons - Step 1
        step1_frame = ttk.Frame(self.root)
        step1_frame.pack(fill='x', **padding)
        self.process_btn = ttk.Button(step1_frame, text="Step 1: Process Program & Trace", command=self.process_program)
        self.process_btn.pack(side='left', padx=5)

        # Selection Area for Watch List
        self.selection_frame = ttk.LabelFrame(self.root, text="Step 2: Watch List Selection (Populated after processing)")
        self.selection_frame.pack(fill='both', expand=False, **padding)

        # Variables Selection
        var_sel_frame = ttk.Frame(self.selection_frame)
        var_sel_frame.pack(side='left', fill='both', expand=True, padx=5)
        ttk.Label(var_sel_frame, text="Variables:").pack(anchor='w')
        self.vars_listbox = tk.Listbox(var_sel_frame, height=5, exportselection=False)
        self.vars_listbox.pack(fill='both', expand=True)
        
        index_frame = ttk.Frame(var_sel_frame)
        index_frame.pack(fill='x')
        ttk.Label(index_frame, text="Index:").pack(side='left')
        self.var_index = tk.IntVar(value=0)
        ttk.Spinbox(index_frame, from_=0, to=1000, textvariable=self.var_index, width=5).pack(side='left', padx=5)
        
        ttk.Label(index_frame, text="To:").pack(side='left')
        self.var_index_to = tk.IntVar(value=0)
        ttk.Spinbox(index_frame, from_=0, to=1000, textvariable=self.var_index_to, width=5).pack(side='left', padx=5)

        # Trace Elements Selection
        trace_sel_frame = ttk.Frame(self.selection_frame)
        trace_sel_frame.pack(side='left', fill='both', expand=True, padx=5)
        ttk.Label(trace_sel_frame, text="Trace Elements:").pack(anchor='w')
        self.trace_elements_listbox = tk.Listbox(trace_sel_frame, height=5, exportselection=False)
        self.trace_elements_listbox.pack(fill='both', expand=True)

        # Watch List Controls
        watch_controls_frame = ttk.Frame(self.selection_frame)
        watch_controls_frame.pack(side='left', fill='y', padx=5)
        ttk.Button(watch_controls_frame, text="Add to Watch", command=self.add_to_watch).pack(fill='x', pady=2)
        ttk.Button(watch_controls_frame, text="Remove", command=self.remove_from_watch).pack(fill='x', pady=2)

        # Watch List Display
        watch_display_frame = ttk.Frame(self.selection_frame)
        watch_display_frame.pack(side='left', fill='both', expand=True, padx=5)
        ttk.Label(watch_display_frame, text="Watch List:").pack(anchor='w')
        self.watch_listbox = tk.Listbox(watch_display_frame, height=5)
        self.watch_listbox.pack(fill='both', expand=True)

        # Results Table
        results_frame = ttk.LabelFrame(self.root, text="Counter-Model Values")
        results_frame.pack(fill='both', expand=True, **padding)
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        self.results_tree = ttk.Treeview(results_frame, columns=("Variable", "Trace", "Index", "Value"), show='headings', height=5)
        self.results_tree.heading("Variable", text="Variable")
        self.results_tree.heading("Trace", text="Trace")
        self.results_tree.heading("Index", text="Index")
        self.results_tree.heading("Value", text="Value")
        self.results_tree.column("Variable", width=100)
        self.results_tree.column("Trace", width=100)
        self.results_tree.column("Index", width=50)
        self.results_tree.column("Value", width=100)
        self.results_tree.pack(fill='both', expand=True)

        # Buttons - Step 3
        step3_frame = ttk.Frame(self.root)
        step3_frame.pack(fill='x', **padding)
        ttk.Label(step3_frame, text="Contract:").pack(side='left')
        ttk.Spinbox(step3_frame, from_=1, to=100, textvariable=self.contract_num, width=5).pack(side='left', padx=5)
        self.solve_btn = ttk.Button(step3_frame, text="Step 3: Solve Contract", command=self.solve_contract)
        self.solve_btn.pack(side='left', padx=5)

        self.contract_display = ttk.Label(step3_frame, text="", foreground="blue")
        self.contract_display.pack(side='left', padx=5)

        # Output Area (Log)
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill='both', expand=True, **padding)
        ttk.Label(output_frame, text="Log:").pack(anchor='w')
        self.log_text = tk.Text(output_frame, height=15)
        self.log_text.pack(fill='both', expand=True)

        self.contract_num.trace_add("write", lambda *args: self.update_contract_display())

    def update_contract_display(self):
        folder = self.program_dir.get()
        contract_num = self.contract_num.get()
        if not folder or not contract_num:
            self.contract_display.config(text="")
            return

        contract_path = os.path.join(folder, f"contract{contract_num}.txt")
        if os.path.exists(contract_path):
            try:
                with open(contract_path, 'r') as f:
                    content = f.read().strip()
                    display_content = self.to_official_symbols(content)
                    self.contract_display.config(text=display_content)
            except:
                self.contract_display.config(text="[Error reading file]")
        else:
            self.contract_display.config(text="[Not found]")

    def browse_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.program_dir.set(directory)

    def on_folder_change(self, *args):
        # Clear watch list if folder changes
        if hasattr(self, 'watch_listbox'):
            self.watch_listbox.delete(0, tk.END)
            # Clear results too
            if hasattr(self, 'results_tree'):
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)
            self.log("Folder changed, watch list and results cleared.")

    def add_to_watch(self):
        var_idx = self.vars_listbox.curselection()
        trace_idx = self.trace_elements_listbox.curselection()
        if not var_idx or not trace_idx:
            messagebox.showwarning("Warning", "Please select both a variable and a trace element.")
            return
        
        var = self.vars_listbox.get(var_idx)
        trace = self.trace_elements_listbox.get(trace_idx)
        start_index = self.var_index.get()
        end_index = self.var_index_to.get()
        
        if end_index < start_index:
            end_index = start_index
            
        for i in range(start_index, end_index + 1):
            pair = f"{var}[{i}] @ {trace}"
            if pair not in self.watch_listbox.get(0, tk.END):
                self.watch_listbox.insert(tk.END, pair)

    def remove_from_watch(self):
        selection = self.watch_listbox.curselection()
        if selection:
            self.watch_listbox.delete(selection)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def run_execution(self):
        self.process_program()
        self.solve_contract()

    def process_program(self):
        folder = self.program_dir.get()
        if not folder:
            messagebox.showerror("Error", "Please select a program folder.")
            return

        trace_num = self.trace_num.get()

        # Always reprocess from the beginning
        self.log_text.delete('1.0', tk.END)
        self.log("--- Processing Program and Trace ---")
        
        program_path = os.path.join(folder, "program.txt")
        trace_path = os.path.join(folder, f"trace{trace_num}.txt")
        execution_path = os.path.join(folder, f"execution{trace_num}.json")
        
        # Check files for Step 1 & 2
        for p in [program_path, trace_path, execution_path]:
            if not os.path.exists(p):
                self.log(f"Error: File not found: {p}")
                messagebox.showerror("Error", f"File not found: {p}")
                return

        try:
            self.log("Step 1: Loading Execution and Program...")
            with open(execution_path, 'r') as f:
                execution = json.load(f)

            with open(program_path) as f:
                program_content = f.read()
                for const_name, const_value in execution.get('const', {}).items():
                    program_content = program_content.replace(const_name, str(const_value))
                input_stream = InputStream(program_content)

            lexer = repeat_arrLexer(input_stream)
            parser = repeat_arrParser(CommonTokenStream(lexer))
            ast = ProgramASTBuilder().visit(parser.program())

            self.log("Step 2: Building Domain...")
            executor = ProgramFormulaBuilder(ast, execution)
            trace_info = load_trace(ast, trace_path, execution['target'])
            domain = executor.build_domain(trace_info)
            
            # Populate selection lists
            self.vars_listbox.delete(0, tk.END)
            self.last_populated_vars = executor.variables
            for v in self.last_populated_vars:
                self.vars_listbox.insert(tk.END, v)
            
            self.trace_elements_listbox.delete(0, tk.END)
            trace_indices = [ti[0] for ti in trace_info]
            self.last_populated_trace = ["epsilon"] if "epsilon" not in trace_indices else []
            self.last_populated_trace += trace_indices
            for t in self.last_populated_trace:
                self.trace_elements_listbox.insert(tk.END, t)

            # Cache results
            self.last_folder = folder
            self.last_trace_num = trace_num
            self.cached_executor = executor
            self.cached_trace_info = trace_info
            self.cached_domain = domain
            self.cached_execution = execution
            
        except Exception as e:
            self.log(f"An error occurred during Step 1/2: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return

    def solve_contract(self):
        folder = self.program_dir.get()
        contract_num = self.contract_num.get()

        # Step 3, 4, 5: Contract parsing and solving (always run)
        # However, we only do this if Step 1/2 succeeded or were cached.
        if self.cached_executor is None:
            return

        contract_path = os.path.join(folder, f"contract{contract_num}.txt")
        if not os.path.exists(contract_path):
            self.log(f"Error: File not found: {contract_path}")
            messagebox.showerror("Error", f"File not found: {contract_path}")
            return

        try:
            self.log(f"--- Running Contract {contract_num} ---")
            self.log("Step 3: Parsing Contract...")
            execution = self.cached_execution
            with open(contract_path) as f:
                contract_content = f.read()
                for const_name, const_value in execution.get('const', {}).items():
                    contract_content = contract_content.replace(const_name, str(const_value))
                contract_input_stream = InputStream(contract_content)

            contract_lexer = contractLexer(contract_input_stream)
            contract_parser = contractParser(CommonTokenStream(contract_lexer))
            contract_ast = ContractASTBuilder().visit(contract_parser.contract())

            self.log("Step 4: Building Problem Formula...")
            cfb = ContractFormulaBuilder(self.cached_trace_info, self.cached_executor.idx_vars)
            problem = cfb.resolve_formula(contract_ast)

            if problem is None:
                self.log("Contract found no matching cases.")
                return

            self.log(f"Step 5: Solving with {self.selected_solver.get()}...")
            with Solver(name=self.selected_solver.get()) as solver:
                solver.add_assertion(self.cached_domain)
                solver.add_assertion(Not(problem))
                
                # Clear results table
                for item in self.results_tree.get_children():
                    self.results_tree.delete(item)

                if solver.solve():
                    self.log("RESULT: Counter model found (Contract is NOT valid)")
                    
                    # Evaluate Watch List
                    watch_items = self.watch_listbox.get(0, tk.END)
                    if watch_items:
                        model = solver.get_model()
                        from pysmt.shortcuts import Select, Int
                        for item in watch_items:
                            try:
                                # item is "var[idx] @ trace"
                                import re
                                match = re.match(r"(.+)\[(\d+)\] @ (.+)", item)
                                if match:
                                    var, idx_val, trace = match.groups()
                                    idx_val = int(idx_val)
                                    if var in self.cached_executor.idx_vars and trace in self.cached_executor.idx_vars[var]:
                                        sym = self.cached_executor.idx_vars[var][trace][0]
                                        val = model.get_value(Select(sym, Int(idx_val)))
                                        self.results_tree.insert("", tk.END, values=(var, trace, idx_val, str(val)))
                                    else:
                                        self.results_tree.insert("", tk.END, values=(var, trace, idx_val, "NOT FOUND"))
                            except Exception as ve:
                                self.log(f"Error evaluating {item}: {str(ve)}")
                else:
                    self.log("RESULT: Contract is valid")

        except Exception as e:
            self.log(f"An error occurred during Step 3/4/5: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def to_official_symbols(self, text):
        mapping = {
            "EXISTS": "∃",
            "FORALL": "∀",
            "{": "⟨",
            "}": "⟩",
            "=>": "→",
            "<=>": "↔",
            "==": "="
        }
        res = text
        # Order matters to avoid partial replacement
        for k in ["<=>", "=>", "==", "EXISTS", "FORALL", "{", "}"]:
            res = res.replace(k, mapping[k])
        return res

    def from_official_symbols(self, text):
        mapping = {
            "∃": "EXISTS",
            "∀": "FORALL",
            "⟨": "{",
            "⟩": "}",
            "→": "=>",
            "↔": "<=>"
        }
        res = text
        for k, v in mapping.items():
            res = res.replace(k, v)
        
        # Carefully replace = with == without breaking !=, <=, >=, =>, <=>
        # We can protect them temporarily
        res = res.replace("!=", "___NEQ___").replace("<=", "___LE___").replace(">=", "___GE___")
        res = res.replace("=>", "___IMP___").replace("<=>", "___EQV___")
        res = res.replace("=", "==")
        res = res.replace("___NEQ___", "!=").replace("___LE___", "<=").replace("___GE___", ">=")
        res = res.replace("___IMP___", "=>").replace("___EQV___", "<=>")
        
        return res

    def open_create_contract_dialog(self):
        folder = self.program_dir.get()
        if not folder:
            messagebox.showerror("Error", "Please select a program folder.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create/Edit Contract")
        dialog.geometry("500x400")

        padding = {'padx': 10, 'pady': 5}
        
        num_frame = ttk.Frame(dialog)
        num_frame.pack(fill='x', **padding)
        ttk.Label(num_frame, text="Contract NUM:").pack(side='left')
        contract_num_var = tk.IntVar(value=self.contract_num.get())
        ttk.Spinbox(num_frame, from_=1, to=100, textvariable=contract_num_var, width=5).pack(side='left', padx=5)

        # Editor
        editor_frame = ttk.Frame(dialog)
        editor_frame.pack(fill='both', expand=True, **padding)
        
        # Toolbar for symbols
        toolbar = ttk.Frame(editor_frame)
        toolbar.pack(fill='x')
        
        symbols = [
            ("∃", "∃"), ("∀", "∀"), ("⟨", "⟨"), ("⟩", "⟩"), 
            ("[", "["), ("]", "]"), ("<", "<"), (">", ">"), ("=", "="),
            ("→", "→"), ("↔", "↔"), ("!", "!"), ("&", "&"), ("|", "|")
        ]
        
        def insert_symbol(s):
            editor.insert(tk.INSERT, s)
            editor.focus_set()

        for label, sym in symbols:
            btn = ttk.Button(toolbar, text=label, width=3, command=lambda s=sym: insert_symbol(s))
            btn.pack(side='left', padx=2)

        editor = tk.Text(editor_frame, height=10)
        editor.pack(fill='both', expand=True, pady=5)
        
        # Load existing if available
        def load_existing(*args):
            path = os.path.join(folder, f"contract{contract_num_var.get()}.txt")
            editor.delete("1.0", tk.END)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read()
                    editor.insert("1.0", self.to_official_symbols(content))
        
        contract_num_var.trace_add("write", load_existing)
        load_existing()

        def save():
            num = contract_num_var.get()
            content = editor.get("1.0", tk.END).strip()
            internal_content = self.from_official_symbols(content)
            path = os.path.join(folder, f"contract{num}.txt")
            with open(path, 'w') as f:
                f.write(internal_content)
            self.contract_num.set(num)
            self.update_contract_display()
            dialog.destroy()

        ttk.Button(dialog, text="Save Contract", command=save).pack(pady=10)

    def open_create_trace_dialog(self):
        folder = self.program_dir.get()
        if not folder:
            messagebox.showerror("Error", "Please select a program folder.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Trace")
        dialog.geometry("400x500")

        tk.Label(dialog, text="Trace NUM:").pack(pady=5)
        trace_num_var = tk.StringVar(value="1")
        tk.Entry(dialog, textvariable=trace_num_var).pack(pady=5)

        initial_values_frame = tk.LabelFrame(dialog, text="Initial Values (from epsilon)")
        initial_values_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Container for initial value entries
        entries_container = tk.Frame(initial_values_frame)
        entries_container.pack(fill='both', expand=True)

        value_entries = {} # var -> [(index_var, value_var), ...]

        def load_params():
            # Clear previous entries
            for widget in entries_container.winfo_children():
                widget.destroy()
            value_entries.clear()

            trace_num = trace_num_var.get()
            execution_path = os.path.join(folder, f"execution{trace_num}.json")
            program_path = os.path.join(folder, "program.txt")

            if not os.path.exists(execution_path):
                # Offer to create from existing execution files
                execution_files = [f for f in os.listdir(folder) if f.startswith("execution") and f.endswith(".json")]
                if not execution_files:
                    messagebox.showerror("Error", f"Execution file not found: {execution_path}\nNo other execution files found to copy from.")
                    return
                
                # Create a simple selection dialog
                pick_dialog = tk.Toplevel(dialog)
                pick_dialog.title("Select execution file to copy")
                pick_dialog.geometry("300x200")
                
                tk.Label(pick_dialog, text=f"execution{trace_num}.json does not exist.\nSelect an existing one to copy from:").pack(pady=5)
                
                selected_file = tk.StringVar(value=execution_files[0])
                ttk.Combobox(pick_dialog, textvariable=selected_file, values=execution_files, state="readonly").pack(pady=5)
                
                def do_copy():
                    src = os.path.join(folder, selected_file.get())
                    shutil.copy(src, execution_path)
                    pick_dialog.destroy()
                    load_params() # Retry loading

                tk.Button(pick_dialog, text="Copy and Continue", command=do_copy).pack(pady=10)
                return
            if not os.path.exists(program_path):
                messagebox.showerror("Error", f"Program file not found: {program_path}")
                return

            try:
                with open(execution_path, 'r') as f:
                    execution_config = json.load(f)
                
                with open(program_path, 'r') as f:
                    program_content = f.read()
                    for const_name, const_value in execution_config.get('const', {}).items():
                        program_content = program_content.replace(const_name, str(const_value))
                
                input_stream = InputStream(program_content)
                lexer = repeat_arrLexer(input_stream)
                parser = repeat_arrParser(CommonTokenStream(lexer))
                ast = ProgramASTBuilder().visit(parser.program())

                start_func_id = execution_config.get('target', {}).get('epsilon')
                if start_func_id is None:
                    # Try to find start function from constants if it's not directly an ID
                    # or if epsilon points to a constant name
                    self.log("Warning: 'epsilon' not found in target map. Using default start function.")
                    # Fallback: maybe there is a constant that defines the start function
                    # In dice_game, 'GAME' is the entry point
                    if 'GAME' in execution_config.get('const', {}):
                        start_func_id = execution_config['const']['GAME']
                    else:
                        messagebox.showerror("Error", "'epsilon' entry not found in target map of execution.json")
                        return

                # Find the function in AST
                # The function names in AST are integers (IDs)
                func = None
                if start_func_id in ast.functions:
                    func = ast.functions[start_func_id]
                else:
                    # Maybe start_func_id is a name? But AST builder uses INTEGER().getText()
                    # Check constants
                    for k, v in execution_config.get('const', {}).items():
                        if v == start_func_id and k in ast.functions:
                            func = ast.functions[k]
                            break
                        if k == start_func_id and v in ast.functions:
                            func = ast.functions[v]
                            break
                
                if not func:
                    messagebox.showerror("Error", f"Start function {start_func_id} not found in program.")
                    return

                for param in func.params:
                    frame = tk.Frame(entries_container)
                    frame.pack(fill='x', padx=5, pady=2)
                    tk.Label(frame, text=f"{param}:", width=10, anchor='w').pack(side='left')
                    
                    idx_var = tk.IntVar(value=0)
                    tk.Entry(frame, textvariable=idx_var, width=5).pack(side='left', padx=2)
                    tk.Label(frame, text="=").pack(side='left')
                    val_var = tk.StringVar(value="0")
                    tk.Entry(frame, textvariable=val_var, width=10).pack(side='left', padx=2)
                    
                    if param not in value_entries:
                        value_entries[param] = []
                    value_entries[param].append((idx_var, val_var))

                    # Button to add more indices for the same parameter (array)
                    def add_more(p=param):
                        f = tk.Frame(entries_container)
                        # Insert after the last entry of this param
                        f.pack(fill='x', padx=5, pady=2)
                        tk.Label(f, text="", width=10).pack(side='left') # spacing
                        iv = tk.IntVar(value=len(value_entries[p]))
                        tk.Entry(f, textvariable=iv, width=5).pack(side='left', padx=2)
                        tk.Label(f, text="=").pack(side='left')
                        vv = tk.StringVar(value="0")
                        tk.Entry(f, textvariable=vv, width=10).pack(side='left', padx=2)
                        value_entries[p].append((iv, vv))

                    tk.Button(frame, text="+", command=add_more, width=2).pack(side='left', padx=2)

            except Exception as e:
                messagebox.showerror("Error", f"Error processing program: {str(e)}")
                import traceback
                print(traceback.format_exc())

        tk.Button(dialog, text="Load Parameters", command=load_params).pack(pady=5)

        def generate():
            trace_num = trace_num_var.get()
            initial_values = {}
            for param, entries in value_entries.items():
                if len(entries) == 1 and entries[0][0].get() == 0:
                    # Single value at index 0, treat as scalar if desired, 
                    # but TraceGenerator handles dicts too.
                    # Actually, if we want it to be an array in trace generator:
                    initial_values[param] = {entries[0][0].get(): int(entries[0][1].get())}
                else:
                    initial_values[param] = {e[0].get(): int(e[1].get()) for e in entries}
            
            self.generate_new_trace(folder, trace_num, initial_values)
            dialog.destroy()

        tk.Button(dialog, text="Generate Trace", command=generate).pack(pady=20)

    def generate_new_trace(self, folder, trace_num, initial_values):
        try:
            execution_path = os.path.join(folder, f"execution{trace_num}.json")
            program_path = os.path.join(folder, "program.txt")
            trace_out_path = os.path.join(folder, f"trace{trace_num}.txt")

            with open(execution_path, 'r') as f:
                execution_config = json.load(f)

            with open(program_path, 'r') as f:
                program_content = f.read()
                for const_name, const_value in execution_config.get('const', {}).items():
                    program_content = program_content.replace(const_name, str(const_value))

            input_stream = InputStream(program_content)
            lexer = repeat_arrLexer(input_stream)
            parser = repeat_arrParser(CommonTokenStream(lexer))
            ast = ProgramASTBuilder().visit(parser.program())

            start_func_id = execution_config.get('target', {}).get('epsilon')
            if start_func_id is None:
                if 'GAME' in execution_config.get('const', {}):
                    start_func_id = execution_config['const']['GAME']
                else:
                    raise ValueError("'epsilon' not found in target map and no 'GAME' constant.")

            generator = TraceGenerator(ast, execution_config, initial_values)
            
            # Prepare arguments for the first call
            # They should be the initial values of the parameters of the entry function
            # But wait, TraceGenerator._execute_function takes 'args' which are values.
            # And it maps them to func.params.
            
            func = None
            if start_func_id in ast.functions:
                func = ast.functions[start_func_id]
            else:
                for k, v in execution_config.get('const', {}).items():
                    if v == start_func_id and k in ast.functions:
                        func = ast.functions[k]
                        break
                    if k == start_func_id and v in ast.functions:
                        func = ast.functions[v]
                        break
            
            if not func:
                raise ValueError(f"Function {start_func_id} not found.")

            args = []
            for param in func.params:
                # initial_values[param] is a dict {index: value}
                val = initial_values.get(param, {0: 0})
                if len(val) == 1 and 0 in val:
                    args.append(val[0])
                else:
                    args.append(val)

            self.log(f"Generating trace for {start_func_id} with initial values {initial_values}...")
            trace, updated_target = generator.generate(start_func_id, args)

            # Save trace
            with open(trace_out_path, 'w') as f:
                f.write("\n".join(trace))
            
            # Update execution.json
            if 'target' not in execution_config:
                execution_config['target'] = {}
            execution_config['target'].update(updated_target)
            with open(execution_path, 'w') as f:
                json.dump(execution_config, f, indent=2)

            self.log(f"Successfully generated {trace_out_path} and updated {execution_path}")
            # messagebox.showinfo("Success", f"Trace {trace_num} generated successfully.")

        except Exception as e:
            self.log(f"Error generating trace: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("Error", f"Error generating trace: {str(e)}")
