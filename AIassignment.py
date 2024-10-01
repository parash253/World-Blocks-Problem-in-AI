from prettytable import PrettyTable

class BlockWorldAgent:
    def __init__(self,initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.hand1 = []
        self.hand2 = []
        self.unsatisfied_stack={}

    def begin(self):
        # ------------------Fancy Visual Design ------------------
        # Data Representation
        initial_representation = PrettyTable()

        print("The Objective is two convert initial state into goal state")
        initial_max_length = max(len(subarray) for subarray in self.initial_state)
        initial_padded_state = [subarray + [""] * (initial_max_length - len(subarray)) for subarray in self.initial_state]
        for i in range(len(initial_padded_state)):
            column_values = list(reversed(initial_padded_state[i]))
            initial_representation.add_column(f"L {i + 1}", column_values)
        initial_representation.add_column("", ["->"] * initial_max_length, align="c")
        

        goal_max_length = max(len(subarray) for subarray in self.goal_state)
        goal_padded_state = [subarray + [""] * (goal_max_length - len(subarray)) for subarray in self.goal_state]
        for i in range(len(goal_padded_state)):
            column_values = list(reversed(goal_padded_state[i]))
            initial_representation.add_column(f"L {i + 1}", column_values)
        initial_representation.add_row(["Initial", "State", "", "Final", "State"])
        print(initial_representation)

        print("\n") 
        
        print("The initial state")
        initial_state = PrettyTable()

        for i in range(len(initial_padded_state)):
            column_values = list(reversed(initial_padded_state[i]))
            initial_state.add_column(f"L {i + 1}", column_values)
        print(initial_state)
        
        print("\n") 
        # ------------------Fancy Visual Design ------------------

        # ------------------Main Algorithm Begins ------------------
        # Populating unsatisfied stack
        for i, bases in reversed(list(enumerate(self.goal_state))):
            for index, base in reversed(list(enumerate(bases))):
                self.unsatisfied_stack[i,index] = base

        State_number = 0

        while len(self.unsatisfied_stack)!=0:
            #Get the top of the stack
            destination,stack_top = self.unsatisfied_stack.popitem()
            # For running below loop both hands must be empty
            for i, inner_array in enumerate(self.initial_state):
                if stack_top in inner_array:
                    initial = (i,inner_array.index(stack_top))
                    print(stack_top)
                    if initial != destination:
                        top_elements = inner_array[inner_array.index(stack_top)+1:]
                        while top_elements:
                            element = top_elements.pop()
                            self.hand1,State_number = self.unstack(inner_array,element,self.hand1, State_number)
                            move_position,value,State_number = self.move(inner_array,self.hand1,State_number)
                            State_number = self.stack(move_position,self.hand1,State_number)
                        if not top_elements:
                            below_elements = inner_array[ :inner_array.index(stack_top)]
                            if below_elements:
                                self.hand2,State_number = self.unstack(inner_array,stack_top,self.hand2, State_number)
                            else: 
                                self.hand2,State_number = self.pick_up(inner_array,stack_top,self.hand2, State_number)
                            # self.hand2,State_number = self.unstack(inner_array,stack_top,self.hand2, State_number)
                            another_top_element = [x for x in self.initial_state[destination[0]]]
                            other_top = another_top_element[destination[1]:]

                            while other_top:
                                element = other_top.pop()
                                other_below = self.initial_state[:self.initial_state[destination[0]].index(element)]
                                if other_below:
                                    self.hand1,State_number = self.unstack(self.initial_state[destination[0]],element,self.hand1, State_number)
                                else: 
                                    self.hand1,State_number = self.pick_up(self.initial_state[destination[0]],element,self.hand1, State_number)

                                # self.hand1,State_number = self.unstack(self.initial_state[destination[0]],element,self.hand1, State_number)
                                move_position,value,State_number = self.move(self.initial_state[destination[0]],self.hand1,State_number)
                                if move_position:
                                    State_number = self.stack(move_position,self.hand1,State_number)
                                else:
                                    State_number = self.put_down(move_position,self.hand1,State_number)

                            if self.initial_state[destination[0]]:
                                State_number = self.stack(self.initial_state[destination[0]],self.hand2,State_number)
                            else:
                                State_number = self.put_down(self.initial_state[destination[0]],self.hand2,State_number)
                    else:
                        self.no_action(stack_top,'Already in Correct Position, No action required')
            print("\n")
        # ------------------Fancy Visual Design ------------------
        The_result = PrettyTable()
        print("The Final Result")
        result_max_length = max(len(subarray) for subarray in self.initial_state)
        result_padded_state = [subarray + [""] * (result_max_length - len(subarray)) for subarray in self.initial_state]
        for i in range(len(result_padded_state)):
            column_values = list(reversed(result_padded_state[i]))
            The_result.add_column(f"L {i + 1}", column_values)
        print(The_result)
        # ------------------Fancy Visual Design ------------------

    def pick_up(self,inner_array,element,hand, State_number):
        State_number +=1
        for i, j in enumerate(self.initial_state):
            side = 'right' if j == inner_array and i == 1 else 'left'

        _from = inner_array[inner_array.index(element)-1]
        picked_element = inner_array.pop(inner_array.index(element))
        from_ = self.display_process(_from,picked_element,side)
        print(f"==> PICK_UP({element}, From_Table, {'L1' if self.initial_state.index(inner_array) == 0 else 'L2'}), S{State_number})")
        hand.append(picked_element)
        print("\n")
        return hand,State_number
        
    
    def put_down(self,stacked_to,hand,State_number):
        value1 = hand[0]
        stacked_to.append(hand.pop())
        State_number +=1
        print(" " + "H1" +" " + " " + "H2" +" ")
        robotic_hand = PrettyTable(header=False)
        robotic_hand_value = [" ", " "]
        robotic_hand.add_row(robotic_hand_value)
        print(robotic_hand)
        initial_max_length = max(len(subarray) for subarray in self.initial_state)
        initial_padded_state = [subarray + [""] * (initial_max_length - len(subarray)) for subarray in self.initial_state]
        column_state = PrettyTable(header=False)
        for i in range(len(initial_padded_state)):
            column_values = list(reversed(initial_padded_state[i]))
            column_state.add_column('', column_values)
        print(column_state)
        print(" " + "L1" +" " + " " + "L2" +" ")
        print(f"PUT_DOWN({value1}, On_Table, {'L1' if self.initial_state.index(stacked_to) == 0 else 'L2'}), S{State_number})")
        print("\n")
        return State_number

    def stack(self,stacked_to,hand,State_number):
        value1 = hand[0]
        stacked_to.append(hand.pop())
        State_number +=1
        print(" " + "H1" +" " + " " + "H2" +" ")
        robotic_hand = PrettyTable(header=False)
        robotic_hand_value = [" ", " "]
        robotic_hand.add_row(robotic_hand_value)
        print(robotic_hand)
        initial_max_length = max(len(subarray) for subarray in self.initial_state)
        initial_padded_state = [subarray + [""] * (initial_max_length - len(subarray)) for subarray in self.initial_state]
        column_state = PrettyTable(header=False)
        for i in range(len(initial_padded_state)):
            column_values = list(reversed(initial_padded_state[i]))
            column_state.add_column('', column_values)
        print(column_state)
        print(" " + "L1" +" " + " " + "L2" +" ")
        print(f"==> S({value1}, {stacked_to[stacked_to.index(value1)-1]}, {'L1' if self.initial_state.index(stacked_to) == 0 else 'L2'}), S{State_number})")
        print("\n")
        return State_number


    def unstack(self,inner_array,element,hand, State_number):
        State_number +=1
        for i, j in enumerate(self.initial_state):
            side = 'right' if j == inner_array and i == 1 else 'left'

        _from = inner_array[inner_array.index(element)-1]
        picked_element = inner_array.pop(inner_array.index(element))
        from_ = self.display_process(_from,picked_element,side)
        # print("Hello, ", end="")
        # print("World!")
        print(f"==> U({element}, {from_}, {'L1' if self.initial_state.index(inner_array) == 0 else 'L2'}), S{State_number})")
        hand.append(picked_element)
        print("\n")
        return hand,State_number 

    def move(self,previous_array, value,State_number,direction=False):
        if direction == False:
            State_number += 1
            for i, j in enumerate(self.initial_state):
                side = 'left' if j == previous_array and i == 1 else 'right'
            self.display_process('',value,side)
            print(f"==> M({'L1' if self.initial_state.index(previous_array) == 0 else 'L2'}, {value[0]}, {'L1' if self.initial_state.index(previous_array) != 0 else 'L2'}), S{State_number})")
            for inside_array in self.initial_state:
                if inside_array != previous_array:
                    moved_to = inside_array
            print("\n")
            return moved_to,value,State_number
    
    def no_action(self,element,message):
        print(element,message)

    def special_case(self):
        # Unstack and stack are allowed when two robotic arms hold 2 different
        # boxes at the same time and will be “placed” on two different “locations”. Be careful on
        # conflicted scenarios (grabbing, stacking, …). Robotic arms DON’T EXCHANGE blocks.
        pass
    def display_process(self,_from,picked_element,side):
        print(" " + "H1" +" " + " " + "H2" +" ")
        robotic_hand = PrettyTable(header=False)
        robotic_hand_value = [" ", picked_element[0]] if side == 'right' else [picked_element[0], " "]
        robotic_hand.add_row(robotic_hand_value)
        print(robotic_hand)
        initial_max_length = max(len(subarray) for subarray in self.initial_state)
        initial_padded_state = [subarray + [""] * (initial_max_length - len(subarray)) for subarray in self.initial_state]
        column_state = PrettyTable(header=False)
        for i in range(len(initial_padded_state)):
            column_values = list(reversed(initial_padded_state[i]))
            column_state.add_column('', column_values)
        print(column_state)
        print(" " + "L1" +" " + " " + "L2" +" ")
        return _from


def test():
    # initial_state = [["A", "B", "C"], ["D", "E"]]
    # goal_state = [["A", "C"], ["D", "E", "B"]]

    initial_state = [["A", "C", "E"], ["B", "F","D", "G"]]
    goal_state = [["D", "G", "B"], ["F", "E", "A", "C"]] 
    # goal_state = [["C", "A", "F", "G"], ["E", "B", "D"]]

    # initial_state = [["D", "G", "B"], ["E", "F","A", "C"]]
    # goal_state = [["D", "G", "B"], ["F", "E", "A", "C"]]

    # initial_state = [["B", "A"], ["D", "C"]]
    # goal_state = [["C", "A"], ["D", "B"]]
    # goal_state = [["B", "A"], ["C", "D"]]

    # initial_state = [["C", "B", "D"], ["A"]]
    # goal_state = [[], ["D", "C", "B", "A"]]

    # initial_state = [["B"], ["A", "C"]]
    # goal_state = [[], ["A", "B", "C"]]

    # initial_state = [["A", "B", "C"],["D", "E", "F"]]
    # goal_state = [["D", "E", "F"],["A", "B", "C"]]

    test_agent = BlockWorldAgent(initial_state, goal_state)
    test_agent.begin()

if __name__ == "__main__":
    test()
    


