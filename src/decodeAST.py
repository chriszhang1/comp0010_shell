from typing import List

rubbish = [
    ["WS", " "],
    ["RULE", "atomic"],
    ["RULE", "arg"],
    ["RULE", "redirection"],
    ["RULE", "quoted"],
    ["QUOTE_MARK", '"'],
    ["RULE", "rdr"],
]


def modify_tree(tree: str) -> str:
    tree = tree.replace("start2", "start")
    tree = tree.replace("pipe2", "pipe")
    tree = tree.replace("seq2", "seq")
    tree = tree.replace("atomic2", "atomic")
    tree = tree.replace("rdr2", "rdr")
    tree = tree.replace("arg2", "arg")
    tree = tree.replace("quoted2", "quoted")
    tree = tree.replace("redirection2", "redirection")
    tree = tree.replace("rdr_in2", "rdr_in")
    tree = tree.replace("rdr_out2", "rdr_out")
    return tree


def rmv_tree(input: List[str]):
    if input[0:4] == ["T", "r", "e", "e"]:
        del input[0:5]  # remove "Tree"
    return input


def rmv_token(input: List[str]):
    stopper = 0
    for i in range(len(input)):
        if input[i] == ")" and len(input) == i + 1:
            stopper = i
            break
        if input[i] == ")":
            if input[i + 1] == ",":
                stopper = i + 2
                break
    del input[0: stopper + 1]


def preprocess(input: List[str]):
    rmv_tree(input)


def addarg_insub(arg: List, answer: List[str], argstart: int):
    if len(arg) > 0:
        length = len(answer) - 1
        answer[length][len(answer[len(answer) - 1]) - 1].append("".join(arg))
        arg.clear()
        argstart -= 1
    return argstart


def addarg_nosub(arg: List, answer: List[str], argstart: int):
    if len(arg) > 0:
        answer[len(answer) - 1].append("".join(arg))
        arg.clear()
        argstart -= 1
    return argstart


def decompress(tree: str):
    tree = modify_tree(tree)
    templist = list(tree)
    preprocess(templist)
    answer = []
    arg = []
    last = ["default", "default"]
    pipecounter = 0
    atmcounter = 0
    patmcounter = 0
    subcounter = 0
    substart = 0
    argstart = 0
    subseqcounter = 0
    subseqstart = 0
    sqacounter = 0
    while templist[0:5] == ["T" "o" "k" "e" "n"] or len(templist) > 6:
        item = tokenreader(templist)

        if item[0] == "RULE" and item[1] == "arg":
            argstart += 1
        if argstart == 2 and substart == 1:
            addarg_insub(arg, answer, argstart)
            arg = []
            argstart -= 1

        if argstart == 2 and subcounter == 0:
            addarg_nosub(arg, answer, argstart)
            arg = []
            argstart -= 1

        if (
            pipecounter > 0
            and item[0] == "RULE"
            and item[1] == "atomic"
            and subcounter == 0
        ):
            atmcounter += 1
            pass

        if (
            pipecounter > 0
            and item[0] == "RULE"
            and item[1] == "atomic"
            and subcounter > 0
        ):
            patmcounter += 1

        if atmcounter > 1 and subcounter == 0:
            argstart = addarg_nosub(arg, answer, argstart)
            answer[len(answer) - 1].append("""`'"|""")
            atmcounter -= 1
            pipecounter -= 1

        if (
            item[0] == "RULE"
            and item[1] == "atomic"
            and subseqcounter > 1
        ):
            sqacounter += 1

        if sqacounter > 1:
            argstart = addarg_insub(arg, answer, argstart)
            leng = len(answer) - 1
            answer[leng][len(answer[len(answer) - 1]) - 1].append("""`'";""")
            sqacounter -= 1

        if item not in rubbish and subcounter > 0:
            if item[0] == "BQM" and item[1] == "`":
                substart += 1
            if patmcounter > 1:
                argstart = addarg_insub(arg, answer, argstart)
                length = len(answer) - 1
                pt = """`'"|"""
                answer[length][len(answer[len(answer) - 1]) - 1].append(pt)
                patmcounter -= 1
                pipecounter -= 1

            if item[0] == "CMD":
                if argstart == 1:
                    argstart = addarg_insub(arg, answer, argstart)
                leng = len(answer) - 1
                answer[leng][len(answer[len(answer) - 1]) - 1].append(item[1])
            elif item[0] == "RULE" and item[1] == "seq":
                subseqcounter += 1
            elif item[0] == "RULE" and item[1] == "pipe":
                pipecounter += 1
                pass
            elif item[0] == "RULE" and item[1] == "rdr_in":
                argstart = addarg_insub(arg, answer, argstart)
                leng = len(answer) - 1
                rdri = """`'"<"""
                answer[leng][len(answer[len(answer) - 1]) - 1].append(rdri)
            elif item[0] == "RULE" and item[1] == "rdr_out":
                argstart = addarg_insub(arg, answer, argstart)
                leng = len(answer) - 1
                rdro = """`'">"""
                answer[leng][len(answer[len(answer) - 1]) - 1].append(rdro)
            elif (
                substart == 1
                and not (item[0] == "BQM" and item[1] == "`")
                and not item[1] == "start"
            ):
                arg.append(item[1])

            elif (
                item[0] == "RULE"
                and item[1] == "start"
                and subseqcounter == 1
            ):
                subseqstart += 1
            if subseqstart == 2:
                argstart = addarg_insub(arg, answer, argstart)
                leng = len(answer) - 1
                st = """`'";"""
                answer[leng][len(answer[len(answer) - 1]) - 1].append(st)
                subseqstart -= 1

            if substart == 2:
                if argstart == 1:
                    if len(arg) > 0:
                        answer[len(answer) - 1][
                            len(answer[len(answer) - 1]) - 1
                        ].append("".join(arg))
                    arg = []
                    argstart -= 1
                subcounter = 0
                substart = 0
                subseqstart = 0
                subseqcounter = 0

        if item not in rubbish and subcounter == 0:
            if item[0] == "RULE" and item[1] == "start":
                argstart = addarg_nosub(arg, answer, argstart)
                answer.append([])
            elif item[0] == "RULE" and item[1] == "seq":
                answer.pop()
            elif item[0] == "RULE" and item[1] == "pipe":
                pipecounter += 1
            elif item[0] == "RULE" and item[1] == "sub":
                argstart = addarg_nosub(arg, answer, argstart)
                subcounter += 1
                if not (
                    last == ["RULE", "arg"]
                    or last == ["RULE", "atomic"]
                    or last == ["QUOTE_MARK", '"']
                ):
                    answer[len(answer) - 1].append("""`'\"p""")
                answer[len(answer) - 1].append("""`'\"""")
            elif item[0] == "BQM" and item[1] == "`":
                pass
            elif item[0] == "RULE" and item[1] == "rdr_in":
                argstart = addarg_nosub(arg, answer, argstart)
                answer[len(answer) - 1].append("""`'"<""")
            elif item[0] == "RULE" and item[1] == "rdr_out":
                argstart = addarg_nosub(arg, answer, argstart)
                answer[len(answer) - 1].append("""`'">""")
            elif item[0] == "CMD":
                if argstart == 1:
                    argstart = addarg_nosub(arg, answer, argstart)
                answer[len(answer) - 1].append(item[1])
            else:
                if last == ['BQM', '`']:
                    answer[len(answer) - 1].append("""`'\"p""")
                arg.append(item[1])
        if subcounter > 0 and item[0] == "BQM" and item[1] == "`":
            argstart = addarg_nosub(arg, answer, argstart)
            answer[len(answer) - 1].append([])
        if not (item[0] == "RULE" and item[1] == "quoted"):
            if last == ['BQM', '`'] and item == ["QUOTE_MARK", '"']:
                pass
            else:
                last = item
        rmv_token(templist)
        rmv_tree(templist)
    if len(arg) > 0:
        answer[len(answer) - 1].append("".join(arg))

    return answer


def tokenreader(input: List[str]):
    token1 = "token1"
    token2 = "token2"
    relist = []
    for i in range(len(input)):
        if input[i] == "(" and input[i + 1] == "'":
            j = i + 2
            while j < len(input):
                if input[j] == "'" and input[j + 1] == ",":
                    token1 = "".join(input[i + 2: j])
                    break
                j += 1
        if input[i] == " " and input[i + 1] == "'":
            k = i + 2
            while k < len(input):
                if input[k] == "'" and input[k + 1] == ")":
                    token2 = "".join(input[i + 2: k])
                    break
                k += 1
            relist.append(token1)
            relist.append(token2)
            break
    return relist
