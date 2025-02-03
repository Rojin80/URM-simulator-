import tkinter as tk
from tkinter import ttk
from logic import URM

class URMApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("URM Simulator")

        self.urm = URM()

        input_frame = ttk.Frame(self, padding="10 10 10 10")
        input_frame.grid(row=0, column=0, sticky="ew")

        ttk.Label(input_frame, text="Encoded URM Instructions:").grid(row=0, column=0, sticky="w")
        self.instructions_entry = ttk.Entry(input_frame, width=50)
        self.instructions_entry.grid(row=0, column=1, pady=5, padx=5)

        self.decode_button = ttk.Button(input_frame, text="Decode", command=self.decode_instructions)
        self.decode_button.grid(row=0, column=2, padx=5)

        self.canvas = tk.Canvas(self, width=1000, height=250, bg="white")
        self.canvas.grid(row=1, column=0, pady=20)

        ttk.Label(input_frame, text="Decoded Program:").grid(row=1, column=0, sticky="nw", pady=(10, 0))
        self.decoded_text = tk.Text(input_frame, width=50, height=5, state="disabled", wrap="none")
        self.decoded_text.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

        self.encoded_instructions_frame = ttk.Frame(self)
        self.encoded_instructions_frame.grid(row=1, column=2, sticky="n", padx=5)

        ttk.Label(input_frame, text="Input Registers (R1, R2, ...):").grid(row=2, column=0, sticky="w")
        self.inputs_entry = ttk.Entry(input_frame, width=50)
        self.inputs_entry.grid(row=2, column=1, pady=5, padx=5)

        self.simulate_button = ttk.Button(input_frame, text="Simulate", command=self.simulate_program)
        self.simulate_button.grid(row=2, column=2, padx=5)

        ttk.Label(input_frame, text="Simulation Trace:").grid(row=3, column=0, sticky="nw", pady=(10, 0))
        self.trace_text = tk.Text(input_frame, width=50, height=10, state="disabled", wrap="none")
        self.trace_text.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky="ew")

        self.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

    def decode_instructions(self):
        encoded_str = self.instructions_entry.get().strip()
        if not encoded_str:
            return

        try:
            encoded_list = list(map(int, encoded_str.split()))
            decoded = self.urm.decode_program(encoded_list)
            decoded_output = self.urm.print_decoded_program(decoded)
            self._write_to_text_widget(self.decoded_text, decoded_output)
            self._display_encoded_instructions(encoded_list)
        except ValueError:
            self._write_to_text_widget(self.decoded_text, "Error: Invalid input. Please enter integers.")

    def _display_encoded_instructions(self, encoded_list):
        for widget in self.encoded_instructions_frame.winfo_children():
            widget.destroy()

        for i, instruction in enumerate(encoded_list):
            label = ttk.Label(self.encoded_instructions_frame, text=str(instruction), relief="solid", width=10, height=2)
            label.grid(row=i, column=0, padx=2, pady=2)

    def simulate_program(self):
        encoded_str = self.instructions_entry.get().strip()
        if not encoded_str:
            return

        try:
            encoded_list = list(map(int, encoded_str.split()))
            decoded = self.urm.decode_program(encoded_list)
        except ValueError:
            self._write_to_text_widget(self.trace_text, "Error: Invalid instructions.")
            return

        inputs_str = self.inputs_entry.get().strip()
        inputs = []
        if inputs_str:
            try:
                inputs = list(map(int, inputs_str.split()))
            except ValueError:
                self._write_to_text_widget(self.trace_text, "Error: Invalid register inputs.")
                return

        def update_callback(registers):
            self.update_urm_tape(registers)
            self.print_tape_in_trace(registers)

        trace_output = self.urm.simulate_urm_program(decoded, inputs, update_callback)
        self._write_to_text_widget(self.trace_text, trace_output)

    def update_urm_tape(self, registers):
        self.canvas.delete("all")

        x_offset = 30
        register_width = 80
        height = 120
        for i in range(1, len(registers) + 1):
            register_value = registers.get(i, 0)
            y_offset = 20

            self.canvas.create_rectangle(x_offset, y_offset, x_offset + register_width, y_offset + height, outline="black", fill="lightblue", width=2)
            self.canvas.create_text(x_offset + register_width // 2, y_offset + 20, text=f"R{i}", font=("Helvetica", 10, "bold"))
            self.canvas.create_text(x_offset + register_width // 2, y_offset + 50, text=f"{register_value}", font=("Helvetica", 12))

            x_offset += register_width + 10

        self.update()

    def print_tape_in_trace(self, registers):
        tape_state = " | ".join([f"R{i}: {registers.get(i, 0)}" for i in range(1, len(registers) + 1)])
        self._write_to_text_widget(self.trace_text, f"\nTape: {tape_state}\n", append=True)

    def _write_to_text_widget(self, text_widget, content, append=False):
        text_widget.config(state="normal")
        if not append:
            text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.config(state="disabled")
