# Imports
import utils.stack as stack
import utils.queue as queue
import utils.token as token
import utils.tree as tree


# Class parser
class Parser:
    # Constructor
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    # Parse the tokens
    def parse(self, tokens, optimise=False):
        # Remove all whitespace tokens
        temp_tokens = []
        for current_token in tokens:
            if current_token["type"] not in [
                "whitespace",
                "single_line_comment",
                "multiline_comment",
            ]:
                temp_tokens.append(current_token)

        tokens = temp_tokens

        # Parse the tokens
        output_queue = self.shunting_yard(tokens)

        # Create the root node
        tree_root = tree.create_node(
            "", "root" if not optimise else 0, optimise
        )  # 0 is the index of the root node

        # Build the expression tree
        for current_queue in output_queue:
            queue.push(
                tree_root["children"] if not optimise else tree_root[2],
                tree.build_expression_tree(current_queue, optimise),
            )

        return tree_root

    # Shunting yard algorithm
    def shunting_yard(self, infix, is_next_token_function=False):
        output_elements = []
        output_queue = []
        operator_stack = []
        is_previous_token_identifier = False
        is_previous_token_function_call = False
        is_next_token_operator = False

        while not queue.is_empty(infix):
            # Get the current token
            current_token = queue.top(infix)

            # The token is a number or a string
            if (
                current_token["type"] in ["number", "string", "constant"]
                and not is_next_token_operator
            ):
                queue.push(output_queue, current_token)
                is_previous_token_identifier = False
                is_previous_token_function_call = False
                is_next_token_operator = True

            # The token is an identifier
            elif current_token["type"] == "identifier" and not is_next_token_operator:
                if not is_previous_token_identifier:
                    queue.push(output_queue, current_token)
                    is_previous_token_identifier = True
                    is_previous_token_function_call = False
                    is_next_token_operator = True

                else:
                    # Error: two identifiers in a row
                    print("Error: two identifiers in a row")

            elif current_token["type"] == "keyword" and not is_next_token_operator:
                # Get the keyword token name
                keyword_token_name = current_token["token"]

                # Pop the token from the queue
                queue.pop(infix)

                # Keyword case
                keyword_token = self.shunting_yard_keyword_case(
                    infix, keyword_token_name
                )
                queue.push(output_queue, keyword_token)

                # Push fake token to the infix
                queue.push_front(infix, {"token": "", "type": ""})

                is_previous_token_identifier = False
                is_previous_token_function_call = False
                is_next_token_operator = False

            # If the token is a newline
            elif current_token["type"] == "newline":
                # Pop the remaining operators from the operator stack
                while not stack.is_empty(operator_stack):
                    queue.push(output_queue, stack.top(operator_stack))
                    stack.pop(operator_stack)

                # Push the output queue to the output elements
                if not queue.is_empty(output_queue):
                    queue.push(output_elements, output_queue)

                # Clear the output queue
                output_queue = []

                is_previous_token_identifier = False
                is_previous_token_function_call = False

                # Reset the need for an operator
                is_next_token_operator = False

            # The token is an opening parenthesis
            elif current_token["token"] == "(":
                # Detect function calls
                if (
                    is_previous_token_identifier
                    or is_previous_token_function_call
                    or is_next_token_function
                ):
                    function_identifier_token = None
                    # Get the function identifier token
                    if not is_previous_token_function_call:
                        function_identifier_token = queue.pop_back(output_queue)

                    # Get the function token
                    function_token = self.shunting_yard_object_case(
                        infix,
                        "function_call" if not is_next_token_function else "function",
                        (
                            function_identifier_token["token"]
                            if function_identifier_token != None
                            else ""
                        ),
                    )

                    # Add the body of the function if the function is anonymous
                    if is_previous_token_function_call:
                        previous_function_call_token = queue.pop_back(output_queue)
                        queue.push_front(
                            function_token["children"], [previous_function_call_token]
                        )

                    # Push the function token to the output queue
                    queue.push(output_queue, function_token)

                    # Set the previous token as a function
                    is_previous_token_function_call = True

                else:
                    if not is_next_token_operator:
                        stack.push(operator_stack, current_token)

                    else:
                        # Error: invalid token
                        print("Error: invalid token", current_token)

                # The previous token is not an identifier
                is_previous_token_identifier = False

                # Reset the need for an operator
                is_next_token_operator = False

            # The token is a closing parenthesis
            elif current_token["token"] == ")":
                is_previous_token_identifier = False
                is_previous_token_function_call = False
                while (
                    not stack.is_empty(operator_stack)
                    and stack.top(operator_stack)["token"] != "("
                ):
                    queue.push(output_queue, stack.top(operator_stack))
                    stack.pop(operator_stack)

                stack.pop(operator_stack)

                #  Need for an operator
                is_next_token_operator = True

            # The token is a bracket
            elif current_token["token"] in ["[", "{"] and not is_next_token_operator:
                is_previous_token_identifier = False
                is_previous_token_function_call = False

                # Get the object token
                object_token = self.shunting_yard_object_case(
                    infix, "array" if current_token["token"] == "[" else "dictionary"
                )

                # Push the object token to the output queue
                queue.push(output_queue, object_token)

                #  Need for an operator
                is_next_token_operator = True

            # The token is an operator
            elif current_token["type"] == "operator" and is_next_token_operator:
                is_previous_token_identifier = False
                is_previous_token_function_call = False
                while (
                    # there is an operator token at the top of the stack
                    (not stack.is_empty(operator_stack))
                    and (stack.top(operator_stack)["type"] == "operator")
                    and
                    # with greater precedence
                    (
                        (
                            token.token_get_operator_priority(
                                stack.top(operator_stack)["token"]
                            )
                            > token.token_get_operator_priority(current_token["token"])
                        )
                        or
                        # or the operator at the top of the stack has equal precedence
                        (
                            (
                                token.token_get_operator_priority(
                                    stack.top(operator_stack)["token"]
                                )
                                == token.token_get_operator_priority(
                                    current_token["token"]
                                )
                            )
                            and
                            # and the operator at the top of the stack is left associative
                            token.token_operator_is_left_associative(
                                current_token["token"]
                            )
                        )
                    )
                    and
                    # the operator at the top of the stack is not a left bracket
                    stack.top(operator_stack)["token"] != "("
                ):
                    queue.push(output_queue, stack.top(operator_stack))
                    stack.pop(operator_stack)

                # Push the token to the operator stack
                stack.push(operator_stack, current_token)

                # Reset the need for an operator
                is_next_token_operator = False

            else:
                # Error: invalid token
                print("Error: invalid token 1", current_token)

            # Pop the token from the queue
            queue.pop(infix)

        # Pop the remaining operators from the operator stack
        while not stack.is_empty(operator_stack):
            queue.push(output_queue, stack.top(operator_stack))
            stack.pop(operator_stack)

        # Push the last output queue to the output elements
        if not queue.is_empty(output_queue):
            queue.push(output_elements, output_queue)

        return output_elements

    # Shunting yard object case
    def shunting_yard_object_case(self, infix, type, identifier=""):
        scope_level = 1
        object_elements = []
        current_element = []

        # Pop the token from the queue
        queue.pop(infix)

        # Go to the object end bracket
        while scope_level != 0:
            # Get the current token
            current_token = queue.top(infix)
            if current_token != None:
                # Check if the current token is a bracket
                if current_token["token"] in ["(", "[", "{"]:
                    scope_level += 1
                    queue.push(current_element, current_token)

                elif current_token["token"] in [")", "]", "}"]:
                    scope_level -= 1

                    # Push the current element to the object elements if the bracket level is not 0
                    if scope_level != 0:
                        queue.push(current_element, current_token)

                # if the current token is a comma push the current element to the object elements
                elif (
                    current_token["token"] in [",", ";"]
                    and scope_level == 1
                    and not queue.is_empty(current_element)
                ):
                    queue.push(object_elements, self.shunting_yard(current_element)[0])
                    current_element = []

                # if the current token is not a newline push the current token to the current element
                elif not current_token["type"] in ["newline"]:
                    queue.push(current_element, current_token)

                if scope_level != 0:
                    # Pop the token from the queue
                    queue.pop(infix)

                else:
                    # Push the current element to the object elements
                    if not queue.is_empty(current_element):
                        queue.push(
                            object_elements, self.shunting_yard(current_element)[0]
                        )
                        current_element = []

        # Create and return the object token
        return {
            "token": identifier,
            "type": type,
            "children": object_elements,
        }

    def shunting_yard_keyword_case(self, infix, keyword):
        scope_level = 1
        object_elements = []
        current_element = []
        current_token = None
        break_loop = False

        # If the keyword is inline keyword
        if keyword in token.INLINE_KEYWORDS:
            # Go to the object end bracket
            while scope_level != 0 and not break_loop:
                # Get the current token
                current_token = queue.top(infix)

                if current_token != None:
                    # Check if the current token is a newline
                    if current_token["type"] == "newline":
                        # Push  the current token to the current element
                        queue.push(current_element, current_token)

                        if scope_level == 1:
                            break_loop = True

                            # Push the current element to the object elements
                            if not queue.is_empty(current_element):
                                queue.push(
                                    object_elements,
                                    self.shunting_yard(current_element)[0],
                                )
                                current_element = []

                            scope_level = 0

                    # Check if the current token is a bracket
                    elif current_token["token"] in ["(", "[", "{"] or (
                        token.is_identifier_keyword(current_token["token"])
                        and not token.is_identifier_inline_keyword(
                            current_token["token"]
                        )
                    ):
                        scope_level += 1
                        queue.push(current_element, current_token)

                    elif current_token["token"] in [")", "]", "}", "end"]:
                        scope_level -= 1

                        # Push the current element to the object elements if the bracket level is not 0
                        if scope_level != 0:
                            queue.push(current_element, current_token)

                    else:
                        queue.push(current_element, current_token)

                    if scope_level != 0:
                        # Pop the token from the queue
                        queue.pop(infix)

                # If the current token is None
                else:
                    # Push the current element to the object elements
                    if not queue.is_empty(current_element):
                        queue.push(
                            object_elements, self.shunting_yard(current_element)[0]
                        )
                        current_element = []

                    break_loop = True

        else:
            # Go to the object end bracket
            while scope_level != 0 and not break_loop:
                # Get the current token
                current_token = queue.top(infix)

                if current_token != None:
                    # Check if the current token is a bracket or a block keyword
                    if current_token["token"] in ["(", "[", "{"] or (
                        token.is_identifier_keyword(current_token["token"])
                        and not token.is_identifier_inline_keyword(
                            current_token["token"]
                        )
                    ):
                        scope_level += 1
                        queue.push(current_element, current_token)

                    elif current_token["token"] in [")", "]", "}", "end"]:
                        scope_level -= 1

                        # Push the current element to the object elements if the bracket level is not 0
                        if scope_level != 0:
                            queue.push(current_element, current_token)

                    else:
                        queue.push(current_element, current_token)

                    # Pop the token from the queue
                    queue.pop(infix)

        # Get the keyword token
        keyword_token = {
            "token": keyword,
            "type": "keyword",
            "children": (
                object_elements
                if keyword in token.INLINE_KEYWORDS
                else self.shunting_yard(current_element, keyword in ["function", "for"])
            ),  # If the token if a function
        }

        return keyword_token
