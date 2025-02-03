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
            return ("Z", c // 4 + 1)
        elif mod4 == 1:
            return ("S", (c - 1) // 4 + 1)
        elif mod4 == 2:
            z = (c - 2) // 4
            m, n = self.inverse_pi(z)
            return ("T", m + 1, n + 1)
        else:
            z = (c - 3) // 4
            u, v = self.inverse_pi(z)
            m, n = self.inverse_pi(u)
            return ("J", m + 1, n + 1, v + 1)

    def decode_program(self, encoded_list):
        return [self.decode_instruction(c) for c in encoded_list]

    def print_decoded_program(self, decoded):
        print("\nDecoded Program:")
        for i, instr in enumerate(decoded, start=1):
            if instr[0] == "Z":
                print(f"{i}: Z({instr[1]})")
            elif instr[0] == "S":
                print(f"{i}: S({instr[1]})")
            elif instr[0] == "T":
                print(f"{i}: T({instr[1]},{instr[2]})")
            elif instr[0] == "J":
                print(f"{i}: J({instr[1]},{instr[2]},{instr[3]})")

    def simulate_urm_program(self, decoded, inputs):
        R = {i + 1: v for i, v in enumerate(inputs)}
        ip = 1
        n_instructions = len(decoded)
        trace_output = []

        print("\nStarting Simulation...\n")
        while 1 <= ip <= n_instructions:
            time.sleep(1)  

            instr = decoded[ip - 1]
            op = instr[0]
            if op == "Z":
                n = instr[1]
                R[n] = 0
                trace_output.append(f"{ip}: R{n} = 0")
            elif op == "S":
                n = instr[1]
                R[n] = R.get(n, 0) + 1
                trace_output.append(f"{ip}: R{n} = {R[n]}")
            elif op == "T":
                m, n = instr[1], instr[2]
                R[n] = R.get(m, 0)
                trace_output.append(f"{ip}: R{n} = {R[n]}")
            elif op == "J":
                m, n, q = instr[1], instr[2], instr[3]
                if R.get(m, 0) == R.get(n, 0):
                    trace_output.append(f"{ip}: Jump to {q}")
                    ip = q
                    continue
                else:
                    trace_output.append(f"{ip}: No jump")

            ip += 1 

           
            print("\n".join(trace_output[-1:]))  
            print("Registers:", R) 

        print("\nSimulation Completed.")
        print("Final Registers:", R)
        print(f"Output: R1 = {R.get(1, 0)}")


if __name__ == "__main__":
    urm = URM()
    
    encoded_str = input("Enter encoded URM instructions (space-separated integers): ")
    encoded_list = list(map(int, encoded_str.split()))
    
    decoded = urm.decode_program(encoded_list)
    urm.print_decoded_program(decoded)

    inputs_str = input("\nEnter initial register values (space-separated integers, starting from R1): ")
    inputs = list(map(int, inputs_str.split()))

    urm.simulate_urm_program(decoded, inputs)
