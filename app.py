# app.py
from flask import Flask, render_template, request, jsonify
from logic import URM

app = Flask(__name__)

urm = URM()


simulation_state = {}

@app.route("/", methods=["GET", "POST"])
def index():

    global simulation_state

    if request.method == "POST":
       
        encoded_str = request.form.get("encoded_instructions", "")
        inputs_str = request.form.get("inputs", "")

      
        try:
            encoded_list = list(map(int, encoded_str.split()))
            decoded = urm.decode_program(encoded_list)
        except ValueError:
           
            return render_template(
                "index.html",
                decoded_output="Error: Invalid instructions.",
                trace_output="",
                registers_table=""
            )

       
        decoded_output_html = render_decoded_program_html(decoded)

     
        inputs = []
        if inputs_str.strip():
            try:
                inputs = list(map(int, inputs_str.split()))
            except ValueError:
                decoded_output_html += "<p style='color:red;'>Error: Invalid register inputs.</p>"

      
        simulation_state = {
            "decoded": decoded,
            "ip": 1,              
            "trace_output": [],
            "registers": {}
        }

       
        for i, val in enumerate(inputs, start=1):
            simulation_state['registers'][i] = val

      
        return render_template(
            "index.html",
            decoded_output=decoded_output_html,
            trace_output="",
            registers_table=build_registers_table(simulation_state['registers'])
        )

   
    return render_template(
        "index.html",
        decoded_output="",
        trace_output="",
        registers_table=""
    )


@app.route("/next_step", methods=["POST"])
def next_step():
    
    global simulation_state

    
    if not simulation_state or "decoded" not in simulation_state:
        return jsonify({"error": "No simulation in progress."}), 400

    decoded = simulation_state["decoded"]
    ip = simulation_state["ip"]
    reg = simulation_state["registers"]
    trace = simulation_state["trace_output"]

    if ip < 1 or ip > len(decoded):
        return jsonify({"error": "Simulation completed."}), 400

    instr = decoded[ip - 1]
    op = instr[0]

  
    if op == "Z":
        n = instr[1]
        reg[n] = 0
        trace.append(f"{ip}: R{n} = 0")
        simulation_state["ip"] = ip + 1

    elif op == "S":
        n = instr[1]
        reg[n] = reg.get(n, 0) + 1
        trace.append(f"{ip}: R{n} = {reg[n]}")
        simulation_state["ip"] = ip + 1

    elif op == "T":
        m, n = instr[1], instr[2]
        reg[n] = reg.get(m, 0)
        trace.append(f"{ip}: R{n} = {reg[n]}")
        simulation_state["ip"] = ip + 1

    elif op == "J":
        m, n, q = instr[1], instr[2], instr[3]
        if reg.get(m, 0) == reg.get(n, 0):
            trace.append(f"{ip}: Jump to {q}")
            simulation_state["ip"] = q
        else:
            trace.append(f"{ip}: No jump")
            simulation_state["ip"] = ip + 1

    return jsonify({
        "trace_output": "\n".join(trace),
        "registers_table": build_registers_table(reg),
        "ip": simulation_state["ip"]
    })


@app.route("/run_all", methods=["POST"])
def run_all():
    
    global simulation_state
    if not simulation_state or "decoded" not in simulation_state:
        return jsonify({"error": "No simulation in progress."}), 400

    decoded = simulation_state["decoded"]
    ip = simulation_state["ip"]
    reg = simulation_state["registers"]
    trace = simulation_state["trace_output"]
    n_instructions = len(decoded)

  
    if ip < 1 or ip > n_instructions:
        return jsonify({"error": "Simulation completed."}), 400

   
    while ip >= 1 and ip <= n_instructions:
        instr = decoded[ip - 1]
        op = instr[0]

        if op == "Z":
            n = instr[1]
            reg[n] = 0
            trace.append(f"{ip}: R{n} = 0")
            ip += 1

        elif op == "S":
            n = instr[1]
            reg[n] = reg.get(n, 0) + 1
            trace.append(f"{ip}: R{n} = {reg[n]}")
            ip += 1

        elif op == "T":
            m, n = instr[1], instr[2]
            reg[n] = reg.get(m, 0)
            trace.append(f"{ip}: R{n} = {reg[n]}")
            ip += 1

        elif op == "J":
            m, n, q = instr[1], instr[2], instr[3]
            if reg.get(m, 0) == reg.get(n, 0):
                trace.append(f"{ip}: Jump to {q}")
                ip = q
            else:
                trace.append(f"{ip}: No jump")
                ip += 1

   
    simulation_state["ip"] = ip

    return jsonify({
        "trace_output": "\n".join(trace),
        "registers_table": build_registers_table(reg),
        "ip": ip
    })


def render_decoded_program_html(decoded):
   
    lines = []
    for i, instr in enumerate(decoded, start=1):
        op = instr[0]
        if op == "Z":
            text = f"{i}: Z({instr[1]})"
        elif op == "S":
            text = f"{i}: S({instr[1]})"
        elif op == "T":
            text = f"{i}: T({instr[1]},{instr[2]})"
        elif op == "J":
            text = f"{i}: J({instr[1]},{instr[2]},{instr[3]})"

      
        line_html = f'<div id="instr_{i}" style="padding:2px;">{text}</div>'
        lines.append(line_html)
    return "\n".join(lines)


def build_registers_table(registers_dict):
    
    if not registers_dict:
        return "<table><tr><td>No registers</td></tr></table>"

    max_reg = max(registers_dict.keys())
    cells = []
    for i in range(1, max_reg + 1):
        val = registers_dict.get(i, 0)
        cells.append(f"<td><b>R{i}</b>: {val}</td>")
    row_html = "".join(cells)
    html = f"<table border='1'><tr>{row_html}</tr></table>"
    return html


if __name__ == "__main__":
    app.run(debug=True)
