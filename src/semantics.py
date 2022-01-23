from typing import List, Set
import importlib
import os
import unsafe


# p_out is parser output
# e.g. [['echo', 'foo'], ['echo', 'bar']]


# Import apps
def get_apps() -> Set[str]:
    self_path = __file__
    import_path = os.path.realpath(self_path).replace('semantics.py', 'app/')
    os_listdir = os.listdir(import_path)
    return set(i.replace(".py", "") for i in os_listdir if ".py" == i[-3:])


# Evaluates a single command that
# does not contain any pipe/substitution/sequence/redirection.
def eval_atomic(
        p_out: List[List[str]],
        stdin: List[str],
        stdout: List[str]
        ) -> int:
    app_name, *arguments = p_out[0]
    is_unsafe = False
    # Unsafe command
    if app_name[0] == "_":
        is_unsafe = True
        app_name = app_name[1:]
    # Normal evluation process
    available_apps = get_apps()
    # Correct app name
    if app_name in available_apps:
        app_module = importlib.import_module("app.{}".format(app_name))
        if is_unsafe:
            # introduce unsafe decorator.
            __app__ = unsafe.Unsafe(app_module.__app__)
        else:
            __app__ = app_module.__app__
        return __app__.exec(arguments, stdin, stdout)
    # Incorrect app name
    else:
        stdout.clear()
        stdout.append("Unsupported application {}".format(app_name))
        return 1


# Evalute a pipe command
def eval_pipe(
        p_out: List[List[str]],
        stdin: List[str],
        stdout: List[str]
        ) -> int:
    flag = 0
    index = p_out[0].index("""`'"|""")
    # Split the first command from pipe(s) and evaluate it
    command = p_out[0][:index]
    p_out = [p_out[0][index + 1:]]
    flag = evaluate([command], stdin, stdout)
    if flag:
        return flag
    stdin = stdout.copy()
    stdout.clear()
    # Evaluate the rest of pipe(s)
    evaluate(p_out, stdin, stdout)
    return flag


# Evaluate a redirection command
def eval_rdr(
        p_out: List[List[str]],
        stdin: List[str],
        stdout: List[str]
        ) -> int:
    out_file = None
    flag = 0
    for i in range(len(p_out[0])):
        if i >= len(p_out[0]):
            break
        # Input redirection
        if p_out[0][i] == """`'"<""":
            in_file = open(p_out[0][i+1])
            # Store the input file to stdin
            stdin.extend(in_file.readlines())
            in_file.close()
            del p_out[0][i]
            del p_out[0][i]
        if i >= len(p_out[0]):
            break
        # Output redirection
        if p_out[0][i] == """`'">""":
            # Open (Create) the output file
            out_file = open(p_out[0][i+1], "w+")
            del p_out[0][i]
            del p_out[0][i]
    # Evaluate the command
    flag = eval_atomic(p_out, stdin, stdout)
    if flag:
        return flag
    # Write to the output file
    if out_file is not None:
        for element in stdout:
            out_file.write(element + '\n')
        stdout.clear()
        out_file.close()
    return flag


# Evaluate a sequence command
def eval_seq(
        p_out: List[List[str]],
        stdin: List[str],
        stdout: List[str]
        ) -> int:
    flag = 0
    temp_stdout = []
    # Case 1: [[command1], [command2]]
    if len(p_out) > 1:
        # Split the first command from sequence(s) and evaluate it
        flag = evaluate([p_out[0]], stdin, temp_stdout)
        if flag:
            return flag
        # Evaluate the rest of sequence(s)
        stdout.extend(temp_stdout)
        temp_stdout.clear()
        p_out = p_out[1:]
        evaluate(p_out, stdin, temp_stdout)
        stdout.extend(temp_stdout)
    # Case 2: [[command1 ; command2]]
    else:
        index = p_out[0].index("""`'";""")
        p_out = [p_out[0][:index], p_out[0][index+1:]]
        flag = eval_atomic([p_out[0]], stdin, temp_stdout)
        if flag:
            return flag
        stdout.extend(temp_stdout)
        p_out = p_out[1:]
        evaluate(p_out, stdin, temp_stdout)
        stdout.extend(temp_stdout)
    return flag


# Determine the type of a command line
def evaluate(
        p_out: List[List[str]],
        stdin: List[str],
        stdout: List[str]
        ) -> int:
    if len(p_out) > 1:
        # Sequence case 1
        return eval_seq(p_out, stdin, stdout)
    # if len(p_out) == 1
    # If user enter nothing or just couple of space,
    # shell will continue to ask for another input,
    # so len(p_out) cannot be 0.
    else:
        # Substitution
        if """`'\"""" in p_out[0]:
            sub_command = [p_out[0][p_out[0].index("""`'\"""")+1]]
            evaluate(sub_command, stdin, stdout)
            p_out[0][p_out[0].index("""`'\"""")+1] = ' '.join(stdout)
            p_out[0].remove("""`'\"""")
            stdout.clear()
            i = 0
            # `'"p is to indicate that the preceding and following elements
            # need to be output together
            # e.g. ['echo', 'a', """`'"p""", 'b'] -> ['echo', 'ab']
            if """`'"p""" in p_out[0]:
                while i < len(p_out[0]):
                    if p_out[0][i] == """`'"p""":
                        p_out[0][i-1] += p_out[0][i+1]
                        del p_out[0][i]
                        del p_out[0][i]
                        i -= 1
                    i += 1
            return evaluate(p_out, stdin, stdout)
        # Sequence
        elif """`'";""" in p_out[0]:
            return eval_seq(p_out, stdin, stdout)
        # Pipe
        elif """`'"|""" in p_out[0]:
            return eval_pipe(p_out, stdin, stdout)
        # Redirection
        elif """`'"<""" in p_out[0] or """`'">""" in p_out[0]:
            return eval_rdr(p_out, stdin, stdout)
        # Atomic
        else:
            return eval_atomic(p_out, stdin, stdout)
