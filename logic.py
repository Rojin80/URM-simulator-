import math
import time 

class URM:
    def inverse_pi(self, z):
        w = int(math.floor((math.sqrt(8*z + 1) - 1) / 2))
        temp = w * (w + 1) // 2
        x = z - temp
        y = w - x
        return x, y

    def decode_instruction(self, c):
        mod4 = c % 4
        if mod4 == 0:
            n = c // 4 + 1
            return ("Z", n)
        elif mod4 == 1:
            n = (c - 1) // 4 + 1
            return ("S", n)
        elif mod4 == 2:
            z = (c - 2) // 4
            m_minus_1, n_minus_1 = self.inverse_pi(z)
            return ("T", m_minus_1 + 1, n_minus_1 + 1)
        else:
            z = (c - 3) // 4
            u, v = self.inverse_pi(z)
            m_minus_1, n_minus_1 = self.inverse_pi(u)
            return ("J", m_minus_1 + 1, n_minus_1 + 1, v + 1)

    def decode_program(self, encoded_list):
        return [self.decode_instruction(c) for c in encoded_list]

    def print_decoded_program(self, decoded):
        output_lines = []
        for i, instr in enumerate(decoded, start=1):
            op = instr[0]
            if op == "Z":
                output_lines.append(f"{i}: Z({instr[1]})")
            elif op == "S":
                output_lines.append(f"{i}: S({instr[1]})")
            elif op == "T":
                output_lines.append(f"{i}: T({instr[1]},{instr[2]})")
            elif op == "J":
                output_lines.append(f"{i}: J({instr[1]},{instr[2]},{instr[3]})")
        return "\n".join(output_lines)

    def simulate_urm_program(self, decoded, inputs, update_callback):
        R = {}
        def get_reg(i):
            return R.get(i, 0)
        def set_reg(i, val):
            R[i] = val

        for i, val in enumerate(inputs, start=1):
            set_reg(i, val)

        ip = 1
        n_instructions = len(decoded)
        trace_output = []

        while 1 <= ip <= n_instructions:
           
            
            instr = decoded[ip - 1]
            op = instr[0]
            if op == "Z":
                n = instr[1]
                set_reg(n, 0)
                trace_output.append(f"{ip}: R{n} = 0")
                update_callback(R)
                ip += 1
            elif op == "S":
                n = instr[1]
                new_val = get_reg(n) + 1
                set_reg(n, new_val)
                trace_output.append(f"{ip}: R{n} = {new_val}")
                update_callback(R)
                ip += 1
            elif op == "T":
                m, n = instr[1], instr[2]
                set_reg(n, get_reg(m))
                trace_output.append(f"{ip}: R{n} = {get_reg(n)}")
                update_callback(R)
                ip += 1
            elif op == "J":
                m, n, q = instr[1], instr[2], instr[3]
                if get_reg(m) == get_reg(n):
                    trace_output.append(f"{ip}: Jump to {q}")
                    ip = q
                else:
                    trace_output.append(f"{ip}: No jump")
                    ip += 1

        trace_output.append("Stop")
        trace_output.append(f"Output: R1 = {get_reg(1)}")

        return "\n".join(trace_output)



