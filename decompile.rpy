# RenPy code decompiler 1.4
# Decompiles PRYC files from RenPy runtime. Not for a faint of heart.

# 1.1: Update to support renpy 6.15.x Translate/EndTranslate constructs
# 1.1.1: Unicode fix
# 1.1.2: atl & with collision fix, 2+ behinds fix
# 1.2: full atl support
# 1.3: autopatch of "renpy/script.py" is added
# 1.4: screen language 2 is now supported

# ========
# CONTACTS
# ========
# Copyleft by lolbot, member of IIchan.ru eroge project.
#         _                             
#       ,' ".   ,-"-.                        
#      :     '.'▄██▄ '.
#     :      . ▐█▀ ▐█ ;                     
#     :      ; █▌ ▄█▌,   e r o g a m e       
#      :     ; █▐█▀ /                        
#      '.    ; █   /   _      "  __  __  |          
#       '.   ; █  / |," .''l  | /_/ /   -+-            
#        '.  ; ▌ /  |   l__'  | \__ \__  |              
#         '. ;  /           ._]          [_ 
#          '.; /                          
#           './                          
#            '           
# Written on hard day's nights of extremely cold winter 2012.
# You can mail me at: lolbot_iichan@mail.ru

# =============
# NO GUARANTIES
# =============
# Please, note, that this code is not perfect.
# IN FACT, THERE ARE ABSULUTELY NO GUARANTIES.
# Most problems must be marked by decompiler with "#TODO" comments in generated rpy file.
# However, even if there is no such comments, decompiled code still may be in some wrong way.
# Python is not my native language, so sorry for awful non-pythonic style.


# ==========
# WHAT IS IT
# ==========
# This code can be used to decompile game scenarios and python scripts of RenPy game back to source code.
# Notice, that it may be illegal to redistribute decompiled games, so use this code wisely.
#
# I hope that this code would be useful not only for datesim-cheaters, but also for some game developers.
# If you wrote a game long time ago and lost it's sources, you can try now getting them back.
# If you were writing a VN and accidentally lost everything but the rpyc files, you can try restoring your work.

# =============
# HOW TO USE IT
# =============
# There are three ways of using this script
#
# -> BEST WAY TO USE (decompiles python block from source, autopatches "renpy/script.py")
#    1. Put this file to your /game/ dir.
#    2. Run the game and get the "RESTART THE GAME AGAIN TO DECOMPILE IT !!!" error message.
#    3. Run the game again, this time without any error messages.
#
# -> IF IT FAILS (decompiles python block from source, but you patch "renpy/script.py")
#    1. Put this file to your /game/ dir.
#    2. Delete "i.source = None" line of "renpy/script.py" file
#    3. Run the game.
#
# -> IF IT FAILS TOO (decompiles python block from bytecode, tricky)
#    1. Put this file to your /game/ dir.
#    2. Change "__LB_decompile_bytecode = False" line below in this file to "__LB_decompile_bytecode = True"
#    3. Run the game.
#
# Decompiled rpyc will be put at root folder of your game.

# ==============
# MODE SELECTION
# ==============
# False -> decompile python blocks from source code (default, but a patch is needed at "renpy/script.py")
# True  -> decompile python blocks from bytecode (less stable, avaliable in case renpy/script.py is changed in future)
python early:
    __LB_decompile_bytecode = False

# =================
# IT'S NOT ALMIGHTY
# =================
# There are many versions of RenPy and Python, pryc format and bytecode may differ for them.
# Some Python constructions are not decompiled from bytecode, but can be decompiled from source (see "HOW TO USE IT").
# Screen statements are not supported in both modes, sorry.
#
# Tests results on some games that were using and syntetic unittests:
# |
# +-+-RenPy 4.x/5.x with Python 2.3:
# | '---TOTAL FAIL: code injection didn't work for me, imposible to add a new rpy file
# |
# +-+-RenPy 6.x with Python 2.3:
# | +-+-Successfully decompiled using python source or bytecode:
# | | '---Elven Relations 1.1.2
# | +-+-Successfully decompiled using python source only:
# | | '---Magical Boutique 1.2
# | +---Ren'Py statements - excelent, no known errors
# | '---Python blocks - bytecode decompilation works good, but fails on some constructions
# |
# +-+-RenPy 6.x with Python 2.5:
# | +-+-Successfully decompiled using python source or bytecode:
# | | +---Tentacularity-DEMO-1.0.2
# | | +---IIchan.ru Eroge Demo
# | | +---Katawa Shoujo Act 1
# | | '---Katawa Shoujo
# | +---Ren'Py statements - excelent, no known errors
# | +---Python blocks - no known errors in bytecode decompilation
# | '---ATL statements - good, most statements are supported
# |
# '-+-RenPy 6.x with Python 2.6:
#   +-+-Successfully decompiled using python source or bytecode:
#   | '---MiniBot 2.0
#   +-+-Successfully decompiled using python source only:
#   | '---Winter Tale
#   +---Ren'Py statements - excelent, no known errors
#   +---Python blocks - highly recommended to use python source
#   +---ATL statements - good, most statements are supported
#   '---Screen statements - not supported, only their names are detected



# ======================
# LICENSE? WHAT LICENSE?
# ======================
# It's mostly a Proof Of Concept during studying python bytecode. You can use this code however you want, I think.
# But be warned, you won't get any presents from Santa, if you delete all the copylefts and introduce this work as your's.

# =============
# SOME CONTROLS
# =============
# False -> just decompile
# True  -> verbose behavior

python early:
    __LB_renpy_error_on_python_fail = False
    __LB_unit_test_only = False
    __LB_condition_debug = False
    __LB_full_debug = False
    __LB_print_dis = False
    __LB__open = open

# ==================
# HERE GOES THE CODE
# ==================

init -9001 python:
    import re
    __LB_invisible_space = ""
    __LB_files_filtered_out = [re.compile(".*common.00[a-z_]*.rpy.*"),re.compile(".*common._[a-z_/]*.rpym.*"),re.compile(".*decompile.rpy.*"),re.compile(".*depack.rpy.*"),re.compile(".*injection.rpy.*")]
    __LB_decompiled_files = {}
    _LB_tried_to_patch_isource = False

    def __LB_patch_isource():
        import os, shutil
    
        global _LB_tried_to_patch_isource
        if  _LB_tried_to_patch_isource:
           return True
    
        scriptpath = os.path.join(config.renpy_base,"renpy","script.py")
        if  not os.path.exists(scriptpath):
            return False
    
        script = open(scriptpath, "r")
        script_lines = script.readlines()
        script.close()
        
        re_isource = re.compile("^ * i.source *= *None *$")
        for l in script_lines:
            if  re_isource.match(l):
                matched = l
                break
        else:
            return False
    
        shutil.copy2(scriptpath, scriptpath+".bak")

        f = open(scriptpath, "w")
        for l in script_lines:
            f.write(l.replace(matched,"#"+matched))
        f.close()
    
        _LB_tried_to_patch_isource = True
        return True

    def __LB_make_tab(tabs):
        return "    "*tabs

    def __LB_decompile_python(pycode,tabs=0,noreturn=False):
        if  __LB_decompile_bytecode:
            pyc = pycode.bytecode
            if  isinstance(pyc,str): 
                import marshal
                code = marshal.loads(pyc)
            else:
                code = pyc
            text,stack,is_class = __LB_decompile_python_code(code,tabs)
        else:
            text = pycode.source
            if  text == None:
                if  __LB_patch_isource():
                    renpy.error('Tried to patch "i.source = None" line in renpy/script.rpy. However, you need to restart RenPy manually to make this file reload.\n\n\n\n!!! RESTART THE GAME AGAIN TO DECOMPILE IT !!!\n\n\n\n')
                else:
                    renpy.error('Empty python source.\n\nNOTE: Make sure, that you\'ve really commented out "i.source = None" line in renpy/script.rpy\n\nIf it does not help, try setting "__LB_decompile_bytecode" flag to False')
            if  text.startswith("\n"):
                text = text[1:]
            if  text.endswith("\n"):
                text = text[:-1]
            if  tabs > 0:
                text = __LB_make_tab(tabs) + text.replace("\n","\n"+__LB_make_tab(tabs))
            text = text

        if  noreturn and text.startswith("return "):
            text = text[7:]
        if  noreturn and text.endswith("\n"):
            text = text[:-1]
        return text

# ====================
# SIMPLE dis-LIKE CODE
# ====================
    def __LB_decompile_python_dis(code,tabs):
        from dis import opname
        idx = 0
        result = ""
        while idx < len(code.co_code):
            op = opname[ ord(code.co_code[idx]) ]
            result += __LB_make_tab(tabs) + "#DIS: %d %s"%(idx,op)
            #no HAVE_ARGS in old pythons
            if  op in ['LOAD_CONST','LOAD_GLOBAL','LOAD_NAME','LOAD_FAST','LOAD_ATTR','LOAD_DEREF','STORE_GLOBAL','STORE_NAME','STORE_FAST','STORE_ATTR','STORE_DEREF','DELETE_GLOBAL','DELETE_NAME','DELETE_FAST','DELETE_ATTR','IMPORT_FROM','IMPORT_NAME','BUILD_TUPLE','BUILD_LIST','BUILD_MAP','CALL_FUNCTION','CALL_FUNCTION_VAR','CALL_FUNCTION_KW','CALL_FUNCTION_VAR_KW','COMPARE_OP','SETUP_LOOP','JUMP_ABSOLUTE','JUMP_FORWARD','UNPACK_SEQUENCE','DUP_TOPX','LOAD_CLOSURE','BUILD_SLICE','FOR_ITER','RAISE_VARARGS','BUILD_CLASS','MAKE_FUNCTION','MAKE_CLOSURE','JUMP_IF_FALSE', 'JUMP_IF_TRUE', 'SETUP_EXCEPT']:
                param = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                result += " %d"%(param)
                idx += 3
            else:
                idx += 1
            result += "\n"
        return result

# ==================================================
# HERE IS THE >  > >> P Y T H O N << <  < DECOMPILER
# ==================================================
# walks through bytecode
# decompiles known patterns
# lot's of copypaste, sorry

    def __LB_decompile_python_code(code,tabs,code_from=0,code_to=None,glob=[],exception_mode=0):
        from dis import opname, cmp_op
        import sys

        lbcode = {}
        lbcode["str"] = ""
        lbcode["stack"] = []

        idx = code_from
        if  code_to==None:
            if  __LB_print_dis:
                lbcode["str"] += __LB_decompile_python_dis(code,tabs)
            idx_max = len(code.co_code)
        else:
            idx_max = code_to

        if  __LB_unit_test_only and not code.co_filename.endswith("unit_test_current.rpy"):
            return "#TODO Only unit_test_current.rpy is parsed",[],False

        if  len([1 for matcher in __LB_files_filtered_out if matcher.match(code.co_filename)]) > 0:
            return "#TODO File name filtered",[],False

        if  code_to and code_from >= code_to:
            return __LB_make_tab(tabs) + "pass" + "\n",[],False

        if  exception_mode:
            extra_stack = 3
            lbcode["stack"] += ["_LB_EXCEPT_TYPE_MAGIC_CONST_","_LB_EXCEPT_EXCEPTION_MAGIC_CONST_"] + ["_LB_EXCEPT_MAGIC_CONST_"]*(extra_stack-2)
        else:
            extra_stack = 0
        original_extra_stack = extra_stack
        code_globals = [i for i in glob]
        import_mode = False
        loop_mode = False
        print_item_to_mode = False
        yield_mode = False
        if_condition = {}
        if_condition["list"] = []
        unpack = {}
        unpack["stack"] = []
        unpack["lvalue"] = ""
        unpack["op"] = ""
        for_loop = {}
        for_loop["should_jump"] = False
        for_loop["target"] = 0
        for_loop["body"] = None
        for_loop["active"] = False
        comprehention_stack = []
        is_class = False

        def __LB_decompile_if_condition_unused(arr, idx_to=None):
            original_idx_to = idx_to
            if  idx_to == None:
                idx_to = arr[-1][0]
            elems = [ item for item in arr if idx_to == item[1] ] + [ item for item in arr if idx_to == item[0] ]
            if  len(elems) == 0:
                return []
            if  len(elems) == 1:
                return [elems[0][0]]
            last_elem = elems[-1]
            elems = elems[:-1]
            result = [last_elem[0]]
            for elem in elems:
                result += __LB_decompile_if_condition_unused(arr,elem[0])
            if  original_idx_to != None:
                return result
            return [item for item in arr if not item[0] in result]
            

        def __LB_decompile_if_condition(arr, idx_to=None):
            original_idx_to = idx_to
            if  idx_to == None:
                idx_to = arr[-1][0]
            result = ""
            op = {'JUMP_IF_TRUE':' or ','JUMP_IF_FALSE':' and '}
            elems = [ item for item in arr if idx_to == item[1] ] + [ item for item in arr if idx_to == item[0] ]
            if  len(elems) == 0:
                return result
            if  len(elems) == 1:
                return elems[0][3]
            last_elem = elems[-1]
            elems = elems[:-1]
            result = ""
            for elem in elems:
                if  elem[2] == 'UNARY_NOT':
                    last_elem[3] = "not " + __LB_decompile_if_condition(arr,elem[0])
            result += "(" + "".join([__LB_decompile_if_condition(arr,elem[0])+op[elem[2]] for elem in elems if elem[2] != 'UNARY_NOT' ]+[last_elem[3]]) + ")"
            if  original_idx_to != None:
                return result

            unused_list = __LB_decompile_if_condition_unused(arr)
            if  len(unused_list) > 0:
                lbcode["str"] += "#TODO: unused if conditions " + `unused_list` + "\n"
            return result

        def __LB_decompile_printable_result_real(result,idx):
            if  len(if_condition["list"]) > 0:
                result = __LB_decompile_if_condition(if_condition["list"] + [[idx,idx+1,"JUMP_IF_FALSE",result]])
                if_condition["list"] = []
            return result

        def __LB_decompile_printable_result(result,idx):
            return result

        def __LB_decompile_unpack_add_value(name,result,tabs,idx):
            unpack["lvalue"] += name
            if  len(unpack["stack"]) > 0:
                unpack["stack"][-1] -= 1
                if  unpack["stack"][-1] > 0:
                    unpack["lvalue"] += ", "
                while len(unpack["stack"]) > 0 and unpack["stack"][-1]==0:
                    unpack["lvalue"] += ")"
                    unpack["stack"].pop()
                    if  len(unpack["stack"]) > 0 and unpack["stack"][-1]>0:
                        unpack["stack"][-1] -= 1
                        if  unpack["stack"][-1] > 0:
                            unpack["lvalue"] += ", "
            code_tmp = ""
            if  len(unpack["stack"]) == 0:
                result = __LB_decompile_printable_result(result,idx)
                if  for_loop["active"]:
                    tmp_target = for_loop["target"]
                    for_body, for_stack, for_class = __LB_decompile_python_code(code,tabs+1,idx+3,for_loop["body_end"],code_globals)
                    code_tmp = __LB_make_tab(tabs) + "for " + unpack["lvalue"] + result + ":" + "\n" + for_body
                    for_loop["target"] = tmp_target
                    for_loop["body_end"] = None
                    for_loop["active"] = False
                    for_loop["should_jump"] = True
                elif unpack["lvalue"].startswith("$"):
                    comprehention_stack.append([])
                elif len(comprehention_stack):
                    comprehention_stack[-1] += [ unpack["lvalue"] + result ]
                elif result == "_LB_EXCEPT_EXCEPTION_MAGIC_CONST_":
                    code_tmp = "#_LB_EXCEPTION_MAGIC_CONST_: " + unpack["lvalue"] + ":\n" # magical hardcode for future code restructuring
                else:
                    code_tmp = __LB_make_tab(tabs) + unpack["lvalue"] + " " + unpack["op"] + "= " + result + "\n"
                unpack["stack"] = []
                unpack["lvalue"] = ""
                unpack["op"] = ""
            lbcode["str"] += code_tmp

        try:
            while idx < idx_max:
                opcode = opname[ ord(code.co_code[idx]) ]
#http://docs.python.org/library/dis.html#python-bytecode-instructions

                if  not opcode in ['JUMP_IF_FALSE','JUMP_IF_TRUE','UNARY_NOT']:
                    if  len(if_condition["list"]) > 0 and len([item for item in if_condition["list"] if item[1] == idx]) > 0:
                        lbcode["stack"][-1] = __LB_decompile_printable_result_real(lbcode["stack"][-1],idx)

                if  import_mode:
                    if  opcode in ["STORE_NAME","STORE_FAST","STORE_GLOBAL","IMPORT_FROM"]:
                        pass
                    elif opcode in ["POP_TOP","IMPORT_STAR"]:
                        import_mode = False
                    else:
                        return lbcode["str"] + "#TODO python fail: " + opcode + " after import at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
                else:
                    if  opcode == 'LOAD_CONST':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  isinstance(code.co_consts[id],unicode):
                            code_tmp = code.co_consts[id].replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t").replace("\"","\\\"")
                            code_tmp = 'u"' + code_tmp + '"'
                        elif hasattr(code.co_consts[id],"co_code"):
                            code_tmp = code.co_consts[id]
                        else:
                            code_tmp = repr(code.co_consts[id])
                        lbcode["stack"] += [code_tmp]

                    elif opcode in ['LOAD_CLOSURE', 'LOAD_DEREF']:
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["stack"] += [(code.co_cellvars+code.co_freevars)[id]]
    
                    elif opcode == 'LOAD_FAST':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["stack"] += [code.co_varnames[id]]
    
                    elif opcode in ["LOAD_NAME","LOAD_GLOBAL"]:
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["stack"] += [code.co_names[id]]
    
                    elif opcode == 'STORE_DEREF':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        __LB_decompile_unpack_add_value((code.co_cellvars+code.co_freevars)[id],lbcode["stack"].pop(),tabs,idx)
    
                    elif opcode == 'STORE_FAST':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        __LB_decompile_unpack_add_value(code.co_varnames[id],lbcode["stack"].pop(),tabs,idx)
    
                    elif opcode in ["STORE_NAME","STORE_GLOBAL"]:
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  opcode == 'STORE_GLOBAL' and not code.co_names[id] in code_globals:
                            code_globals += [ code.co_names[id] ]
                            lbcode["str"] += __LB_make_tab(tabs) + "global " + code.co_names[id] + "\n"
                        value = lbcode["stack"].pop()
                        if  code.co_names[id] == "__module__" and value == "__name__":
                            is_class = True
                        else:
                            __LB_decompile_unpack_add_value(code.co_names[id],value,tabs,idx)
    
                    elif opcode == 'DELETE_FAST':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  code.co_varnames[id].startswith("$"):
                            code_tmp = "[" + comprehention_stack[-1][1] + " for " + comprehention_stack[-1][0]
                            if  len(comprehention_stack[-1]) == 3:
                                code_tmp += " if " + comprehention_stack[-1][2]
                            code_tmp += "]"
                            lbcode["stack"][-1] = code_tmp
                            comprehention_stack.pop()
                        else:
                            lbcode["str"] += __LB_make_tab(tabs) + "del " + code.co_varnames[id] + "\n"
    
                    elif opcode in ["DELETE_NAME","DELETE_GLOBAL"]:
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  code.co_names[id].startswith("$"):
                            code_tmp = "[" + comprehention_stack[-1][1] + " for " + comprehention_stack[-1][0]
                            if  len(comprehention_stack[-1]) == 3:
                                code_tmp += " if " + comprehention_stack[-1][2]
                            code_tmp += "]"
                            lbcode["stack"][-1] = code_tmp
                            comprehention_stack.pop()
                        else:
                            lbcode["str"] += __LB_make_tab(tabs) + "del " + code.co_names[id] + "\n"
    
                    elif opcode in ["SLICE+0","SLICE+1","SLICE+2","SLICE+3"]:
                        code_tmp1 = ""
                        code_tmp2 = ""
                        if  opcode in ["SLICE+2","SLICE+3"]:
                            code_tmp2 = lbcode["stack"].pop()
                        if  opcode in ["SLICE+1","SLICE+3"]:
                            code_tmp1 = lbcode["stack"].pop()
                        code_tmp = lbcode["stack"].pop() + "[" + code_tmp1 + ":" + code_tmp2 + "]"
                        lbcode["stack"] += [ code_tmp ]

                    elif opcode == 'BUILD_SLICE':
                        num = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  num == 3:
                            code_tmp3 = lbcode["stack"].pop()
                            if  code_tmp3 == "None":
                                code_tmp3 = ""
                        else:
                            code_tmp3 = ""
                        code_tmp2 = lbcode["stack"].pop()
                        if  code_tmp2 == "None":
                            code_tmp2 = ""
                        code_tmp1 = lbcode["stack"].pop()
                        if  code_tmp1 == "None":
                            code_tmp1 = ""
                        if  num == 3:
                            code_tmp = code_tmp1 + ":" + code_tmp2 + ":" + code_tmp3
                        else:
                            code_tmp = code_tmp1 + ":" + code_tmp2
                        lbcode["stack"] += [ code_tmp ]
    
                    elif opcode in ["STORE_SLICE+0","STORE_SLICE+1","STORE_SLICE+2","STORE_SLICE+3"]:
                        code_tmp1 = ""
                        code_tmp2 = ""
                        if  opcode in ["STORE_SLICE+2","STORE_SLICE+3"]:
                            code_tmp2 = lbcode["stack"].pop()
                        if  opcode in ["STORE_SLICE+1","STORE_SLICE+3"]:
                            code_tmp1 = lbcode["stack"].pop()
                        code_tmp = lbcode["stack"].pop() + "[" + code_tmp1 + ":" + code_tmp2 + "]"
                        __LB_decompile_unpack_add_value(code_tmp,lbcode["stack"].pop(),tabs,idx)
    
                    elif opcode in ["DELETE_SLICE+0","DELETE_SLICE+1","DELETE_SLICE+2","DELETE_SLICE+3"]:
                        code_tmp1 = ""
                        code_tmp2 = ""
                        if  opcode in ["DELETE_SLICE+2","DELETE_SLICE+3"]:
                            code_tmp2 = lbcode["stack"].pop()
                        if  opcode in ["DELETE_SLICE+1","DELETE_SLICE+3"]:
                            code_tmp1 = lbcode["stack"].pop()
                        code_tmp = lbcode["stack"].pop() + "[" + code_tmp1 + ":" + code_tmp2 + "]"
                        lbcode["str"] += __LB_make_tab(tabs) + "del " + code_tmp + "\n"
    
                    elif opcode == 'RAISE_VARARGS':
                        nargs = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        code_tmp = ""
                        for i in range(nargs):
                            code_tmp = lbcode["stack"].pop() + ", " + code_tmp
                        lbcode["str"] += __LB_make_tab(tabs) + "raise " + code_tmp[:-2] + "\n"

                    elif opcode == 'RETURN_VALUE':
                        code_tmp = __LB_decompile_printable_result(lbcode["stack"].pop(),idx)
                        if  code_tmp != "_LB_LOCALS_MAGIC_CONST_":
                            lbcode["str"] += __LB_make_tab(tabs) + "return " + code_tmp + "\n"
    
                    elif opcode == 'YIELD_VALUE':
                        code_tmp = __LB_decompile_printable_result(lbcode["stack"][-1],idx)
                        lbcode["str"] += __LB_make_tab(tabs) + "yield " + code_tmp + "\n"
#no pop() at python 2.5
                        if  sys.version_info[0] == 2 and sys.version_info[1] > 4:
                            yield_mode = True
                        else:
                            lbcode["stack"].pop()

                    elif opcode == 'LOAD_ATTR':
                        base = lbcode["stack"].pop()
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["stack"] += [base + "." + code.co_names[id]]
    
                    elif opcode == 'STORE_ATTR':
                        base = lbcode["stack"].pop()
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        code_tmp = base + "." + code.co_names[id]
                        __LB_decompile_unpack_add_value(code_tmp,lbcode["stack"].pop(),tabs,idx)
    
                    elif opcode == 'DELETE_ATTR':
                        base = lbcode["stack"].pop()
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["str"] += __LB_make_tab(tabs) + "del " + base + "." + code.co_names[id] + "\n"
    
                    elif opcode == 'BREAK_LOOP':
                        lbcode["str"] += __LB_make_tab(tabs) + "break" + "\n"
    
                    elif opcode == 'COMPARE_OP':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        op = cmp_op[id]
                        code_tmp = lbcode["stack"].pop()
                        if  op == "exception match":
                            lbcode["stack"].pop()
                            lbcode["stack"] += ["_LB_EXCEPTION_MATCH_MAGIC_CONST_"]
                            lbcode["stack"] += [code_tmp]
                        else:
                            code_tmp = "(" + lbcode["stack"].pop() + ") " + op + " (" + code_tmp + ")"
                            lbcode["stack"] += [code_tmp]
    
                    elif opcode in ['UNARY_POSITIVE','UNARY_NEGATIVE','UNARY_NOT','UNARY_INVERT']:
                        if  opcode == 'UNARY_NOT' and len(if_condition["list"])>0:
                            if_condition["list"] += [[idx,idx+1,opcode,lbcode["stack"][-1]]]
                        else:
                            op = {'UNARY_POSITIVE':"+",'UNARY_NEGATIVE':"-",'UNARY_NOT':"not ",'UNARY_INVERT':"~"}[opcode]
                            code_tmp = op + "(" + lbcode["stack"].pop() + ")"
                            lbcode["stack"] += [code_tmp]


    
                    elif opcode == 'UNARY_CONVERT':
                        code_tmp = "`" + lbcode["stack"].pop() + "`"
                        lbcode["stack"] += [code_tmp]
    
                    elif opcode in ['BINARY_POWER','BINARY_MULTIPLY','BINARY_DIVIDE','BINARY_MODULO','BINARY_ADD','BINARY_SUBTRACT','BINARY_FLOOR_DIVIDE','BINARY_TRUE_DIVIDE','BINARY_LSHIFT','BINARY_RSHIFT','BINARY_AND','BINARY_XOR','BINARY_OR']:
                        op = {'BINARY_POWER':"**",'BINARY_MULTIPLY':"*",'BINARY_DIVIDE':"/",'BINARY_MODULO':"%",'BINARY_ADD':"+",'BINARY_SUBTRACT':"-",'BINARY_FLOOR_DIVIDE':"//",'BINARY_TRUE_DIVIDE':"/",'BINARY_LSHIFT':"<<",'BINARY_RSHIFT':">>",'BINARY_AND':"&",'BINARY_XOR':"^",'BINARY_OR':"|"}[opcode]
                        code_tmp = lbcode["stack"].pop()
                        code_tmp = "(" + lbcode["stack"].pop() + ") " + op + " (" + code_tmp + ")"
                        lbcode["stack"] += [code_tmp]
    
                    elif opcode in ['INPLACE_ADD','INPLACE_SUBTRACT','INPLACE_MULTIPLY','INPLACE_DIVIDE','INPLACE_MODULO','INPLACE_POWER','INPLACE_FLOOR_DIVIDE','INPLACE_TRUE_DIVIDE','INPLACE_LSHIFT','INPLACE_RSHIFT','INPLACE_AND','INPLACE_XOR','INPLACE_OR']:
                        optype = opname[ ord(code.co_code[idx+1]) ]
                        op = {'INPLACE_ADD':"+",'INPLACE_SUBTRACT':"-",'INPLACE_MULTIPLY':"*",'INPLACE_DIVIDE':"/",'INPLACE_MODULO':"%",'INPLACE_POWER':"**",'INPLACE_FLOOR_DIVIDE':"//",'INPLACE_TRUE_DIVIDE':"/",'INPLACE_LSHIFT':"<<",'INPLACE_RSHIFT':">>",'INPLACE_AND':"&",'INPLACE_XOR':"^",'INPLACE_OR':"|"}[opcode]
                        unpack["op"] = op
                        code_tmp = lbcode["stack"].pop()
                        lbcode["stack"].pop()
                        lbcode["stack"] += [ code_tmp ]
    
                    elif opcode in ['CALL_FUNCTION','CALL_FUNCTION_VAR','CALL_FUNCTION_KW','CALL_FUNCTION_VAR_KW']:
                        nargs1 = ord(code.co_code[idx+1])
                        nargs2 = ord(code.co_code[idx+2])
                        code_last = ""
                        code_func = ""
                        code_params = ""
                        if  opcode in ['CALL_FUNCTION_KW','CALL_FUNCTION_VAR_KW']:
                            code_last = ", **" + lbcode["stack"].pop() + code_last
                        if  opcode in ['CALL_FUNCTION_VAR','CALL_FUNCTION_VAR_KW']:
                            code_last = ", *" + lbcode["stack"].pop() + code_last
                        if  nargs1 == 0 and nargs2 == 0:
                            if  code_last != "":
                                code_params = code_last[2:]
                        else:
                            code_tmp = ""
                            for i in range(nargs2):
                                val = lbcode["stack"].pop()
                                var = lbcode["stack"].pop().replace("'","")
                                code_tmp = var + "=" + val + ", " + code_tmp
                            for i in range(nargs1):
                                code_tmp = __LB_decompile_printable_result(lbcode["stack"].pop(),idx) + ", " + code_tmp
                            code_params = code_tmp[:-2] + code_last
                        code_func = lbcode["stack"].pop()
                        if  code_func in ["__renpy__list__", "__renpy__dict__"]:
                            lbcode["stack"] += [code_params]
                        elif code_func.startswith("$") and len(comprehention_stack)>0:
                            comprehention_stack[-1] += [ code_params ]
                            lbcode["stack"] += [code_params]
                        else:
                            code_tmp = code_func + "(" + code_params + ")"
                            lbcode["stack"] += [code_tmp]
    
                    elif opcode in ['BUILD_TUPLE','BUILD_LIST','BUILD_MAP']:
                        opening = {'BUILD_TUPLE':"(",'BUILD_LIST':"[",'BUILD_MAP':"{"}
                        closing = {'BUILD_TUPLE':")",'BUILD_LIST':"]",'BUILD_MAP':"}"}
                        nargs = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        if  nargs == 0 or opcode == 'BUILD_MAP':
                            code_tmp = opening[opcode] + closing[opcode]
                            lbcode["stack"] += [code_tmp]
                        else:
                            code_tmp = ""
                            if  opcode != "h":
                                for i in range(nargs):
                                    code_tmp = lbcode["stack"].pop() + ", " + code_tmp
                            if  nargs == 1 and opcode == 'BUILD_TUPLE':
                                code_tmp = opening[opcode] + code_tmp + closing[opcode]
                            else:
                                code_tmp = opening[opcode] + code_tmp[:-2] + closing[opcode]
                            lbcode["stack"] += [code_tmp]
    
                    elif opcode == 'BUILD_CLASS':
                        func,func_params = lbcode["stack"].pop()
                        class_bases = lbcode["stack"].pop()
                        if  class_bases.endswith(", )"):
                            class_bases = class_bases[:-3] + ")"
                        if  class_bases == "()":
                            class_bases = ""
                        class_name = lbcode["stack"].pop()
                        optype = opname[ ord(code.co_code[idx+1]) ]
                        if  optype in ['STORE_FAST','STORE_NAME','STORE_GLOBAL']:
                            id = ord(code.co_code[idx+2]) + ord(code.co_code[idx+3])*256
                            if  optype == 'STORE_FAST':
                                code_tmp = "class " + code.co_varnames[id] + class_bases + ":" + "\n" + func
                            else:
                                code_tmp = "class " + code.co_names[id] + class_bases + ":" + "\n" + func
                            lbcode["str"] += __LB_make_tab(tabs) + code_tmp
                        else:
                            return lbcode["str"] + "#TODO python fail: " + optype + " after " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
    
                    elif opcode in ['MAKE_FUNCTION','MAKE_CLOSURE']:
                        ndefaults = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        code_new = lbcode["stack"].pop()
                        code_args = [ [code_new.co_varnames[i]] for i in range(code_new.co_argcount) ]

                        if  opcode == 'MAKE_CLOSURE':
                            lbcode["stack"].pop()
                            for i in range(ndefaults):
                                code_args[code_new.co_argcount-1-i] += [ lbcode["stack"].pop() ]
                        else:
                            for i in range(ndefaults):
                                code_args[code_new.co_argcount-1-i] += [ lbcode["stack"].pop() ]

                        if  code_new.co_flags & 4:
                            code_args += [ [ "*" + code_new.co_varnames[code_new.co_argcount] ] ]
                            if  code_new.co_flags & 8:
                                code_args += [ [ "**" + code_new.co_varnames[code_new.co_argcount+1] ] ]
                        elif  code_new.co_flags & 8:
                            code_args += [ [ "**" + code_new.co_varnames[code_new.co_argcount] ] ]
                        code_tmp = ""
                        for arg in code_args:
                            code_tmp += ", " + arg[0]
                            if  len(arg)>1:
                                code_tmp += "=" + arg[1]
                        if  code_tmp != "":
                            code_tmp = code_tmp[2:]
                        func,func_stack,func_is_class = __LB_decompile_python_code(code_new,tabs+1)
                        if  len(func) == 0:
                            func = __LB_make_tab(tabs+1) + "pass" + "\n"

                        optype = opname[ ord(code.co_code[idx+3]) ]
                        decorators = []
                        while optype == 'CALL_FUNCTION' and not func_is_class and (ord(code.co_code[idx+4]) + ord(code.co_code[idx+5])*256) == 1:
                            idx += 3
                            optype = opname[ ord(code.co_code[idx+3]) ]
                            decorators += [lbcode["stack"].pop()]
                        while len(decorators):
                            lbcode["str"] += __LB_make_tab(tabs) + "@" + decorators.pop() + "\n"

                        if  optype in ['STORE_FAST','STORE_NAME','STORE_GLOBAL','STORE_DEREF']:
                            id = ord(code.co_code[idx+4]) + ord(code.co_code[idx+5])*256
                            if  optype == 'STORE_FAST':
                                code_tmp = "def " + code.co_varnames[id] + "(" + code_tmp + "):"
                            elif optype == 'STORE_DEREF':
                                code_tmp = "def " + (code.co_cellvars+code.co_freevars)[id] + "(" + code_tmp + "):"
                            else:
                                code_tmp = "def " + code.co_names[id] + "(" + code_tmp + "):"
                            code_tmp += "\n" + func
                            lbcode["str"] += __LB_make_tab(tabs) + code_tmp
                        elif optype == 'CALL_FUNCTION' and func_is_class:
                            lbcode["stack"] += [[func,code_tmp]]
                        elif optype == 'CALL_FUNCTION' and (ord(code.co_code[idx+4]) + ord(code.co_code[idx+5])*256) == 1:
                            lbcode["stack"] += [[func,code_tmp]]
                        else:
                            return lbcode["str"] + "#TODO python fail: " + opcode + " after " + opcode + " at %d/%d"%(idx,idx_max) + "\n" + func + `[(attr,getattr(code,attr)) for attr in dir(code)]` + "\n",lbcode["stack"],is_class
    
                    elif opcode == 'BINARY_SUBSCR':
                        key = lbcode["stack"].pop()
                        base = lbcode["stack"].pop()
                        code_tmp = base + "[" + key + "]"
                        lbcode["stack"] += [code_tmp]
    
                    elif opcode == 'STORE_SUBSCR':
                        key = lbcode["stack"].pop()
                        base = lbcode["stack"].pop()
                        if  base.startswith("{") and base.endswith("}"):
                            if  base == "{}":
                                code_tmp = "{" + key + ":" + lbcode["stack"].pop() + "}"
                            else:
                                code_tmp = base[:-1] + ", " + key + ":" + lbcode["stack"].pop() + "}"
                            if  lbcode["stack"][-1].startswith("{") and lbcode["stack"][-1].endswith("}"):
                                lbcode["stack"][-1] = code_tmp
                            else:
                                return lbcode["str"] + "#TODO python fail: " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
                        else:
                            code_tmp = base + "[" + key + "]" 
                            __LB_decompile_unpack_add_value(code_tmp,lbcode["stack"].pop(),tabs,idx)
    
                    elif opcode == 'STORE_MAP':
                        key = lbcode["stack"].pop()
                        value = lbcode["stack"].pop()
                        code_tmp = lbcode["stack"].pop()
                        if  code_tmp == "{}":
                            lbcode["stack"] += ["{" + key + ":" + value + "}"]
                        else:
                            lbcode["stack"] += [code_tmp[:-1] + ", " + key + ":" + value + "}"]

                    elif opcode == 'DELETE_SUBSCR':
                        key = lbcode["stack"].pop()
                        base = lbcode["stack"].pop()
                        code_tmp = base + "[" + key + "]"
                        lbcode["str"] += __LB_make_tab(tabs) + "del " + code_tmp + "\n"
    
                    elif opcode == 'UNPACK_SEQUENCE':
                        num = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        unpack["stack"] += [num]
                        unpack["lvalue"] += "("
                        lbcode["stack"] += ["_LB_UNPACK_MAGIC_CONST_"]*(num-1)
    
                    elif opcode == 'PRINT_ITEM':
                        lbcode["str"] += __LB_make_tab(tabs) + "print " + lbcode["stack"].pop() + ", " + "\n"

                    elif opcode == 'PRINT_NEWLINE':
                        lbcode["str"] += __LB_make_tab(tabs) + "print " + "\n"

                    elif opcode == 'PRINT_ITEM_TO':
                        print_item_to_mode = True
                        code_tmp = lbcode["stack"].pop()
                        lbcode["str"] += __LB_make_tab(tabs) + "print >> " + code_tmp + ", " + lbcode["stack"].pop() + ", " + "\n"

                    elif opcode == 'PRINT_NEWLINE_TO':
                        print_item_to_mode = False
                        lbcode["str"] += __LB_make_tab(tabs) + "print >> " + lbcode["stack"].pop() + "\n"

                    elif opcode == 'DUP_TOPX':
                        num = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        for i in range(num):
                            lbcode["stack"] += [lbcode["stack"][-num]]
    
                    elif opcode == 'DUP_TOP':
                        lbcode["stack"] += [lbcode["stack"][-1]]
    
                    elif opcode == 'ROT_FOUR':
                        tmp = lbcode["stack"][-1]
                        lbcode["stack"][-1] = lbcode["stack"][-2]
                        lbcode["stack"][-2] = lbcode["stack"][-3]
                        lbcode["stack"][-3] = lbcode["stack"][-4]
                        lbcode["stack"][-4] = tmp
    
                    elif opcode == 'ROT_THREE':
                        tmp = lbcode["stack"][-1]
                        lbcode["stack"][-1] = lbcode["stack"][-2]
                        lbcode["stack"][-2] = lbcode["stack"][-3]
                        lbcode["stack"][-3] = tmp
    
                    elif opcode == 'ROT_TWO':
                        tmp = lbcode["stack"][-1]
                        lbcode["stack"][-1] = lbcode["stack"][-2]
                        lbcode["stack"][-2] = tmp
    
                    elif opcode == 'POP_TOP':
                        code_tmp = lbcode["stack"].pop()
                        if  print_item_to_mode:
                            print_item_to_mode = False
                        elif extra_stack > 0:
                            extra_stack -= 1
                        elif yield_mode:
                            yield_mode = False
                        elif len(comprehention_stack):
                            pass
                        elif loop_mode:
                            if  len(if_condition["list"]) == 0:
                                loop_mode = False
                        elif len(if_condition["list"]) > 0:
                            pass
                        else:
                            lbcode["str"] += __LB_make_tab(tabs) + code_tmp + "\n"
    
                    elif opcode == 'POP_BLOCK':
                        pop = lbcode["stack"].pop()
                        if  pop not in ["_LB_LOOP_MAGIC_CONST_"]:
                                return lbcode["str"] + "#TODO python fail: " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
    
                    elif opcode == 'GET_ITER':
                        code_tmp = lbcode["stack"].pop()
                        lbcode["stack"] += [" in " + code_tmp]

                    elif opcode == 'FOR_ITER':
                        if  loop_mode and lbcode["stack"][-2] == "_LB_LOOP_MAGIC_CONST_":
                            loop_mode = False
                            delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                            for_loop["target"] = idx + delta + 3
                            for_loop["body_end"] = idx+delta
                            for_loop["active"] = True
                        elif len(comprehention_stack) > 0:
                            pass
                        else:
                            return lbcode["str"] + "#TODO python fail: " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
    
                    elif opcode == 'SETUP_LOOP':
                        loop_mode = True
                        lbcode["stack"] += ["_LB_LOOP_MAGIC_CONST_"]
    
                    elif opcode == 'CONTINUE_LOOP':
                        lbcode["str"] += __LB_make_tab(tabs) + "continue" + "\n"

                    elif opcode == 'JUMP_ABSOLUTE':
                        if  not len(comprehention_stack):
                            #FIXME: check where are we actually jumping, lol
                            lbcode["str"] += __LB_make_tab(tabs) + "continue" + "\n"

                    elif opcode == 'END_FINALLY':
                        #FIXME: maybe, do something else too
                        return lbcode["str"] + __LB_make_tab(tabs) + "pass #NOTE: END_FINALLY" + "\n",lbcode["stack"],is_class

                    elif opcode == 'SETUP_EXCEPT':
                        delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        lbcode["str"] += __LB_make_tab(tabs) + "try:" + "\n"
                        try_block, try_stack, try_is_class = __LB_decompile_python_code(code,tabs+1,idx+3,idx+delta-1,code_globals)
                        lbcode["str"] += try_block
                        optype = opname[ ord(code.co_code[idx+delta]) ]
                        if  optype == 'JUMP_FORWARD':
                            idx += delta
                            delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                            except_block, except_stack, except_is_class = __LB_decompile_python_code(code,tabs+1,idx+3,idx+delta-1,code_globals,True)
                            if  not except_block.startswith(__LB_make_tab(tabs) + "except"):
                                lbcode["str"] += __LB_make_tab(tabs) + "except:" + "\n"
                            lbcode["str"] += except_block
                            idx += delta+3
                        else:
                            return lbcode["str"] + "#TODO python fail: " + optype + " after " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class

                    elif opcode in ['JUMP_IF_FALSE','JUMP_IF_TRUE']:
                        if  loop_mode:
                            delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                            if_condition["list"] += [[idx,idx+delta+3,opcode,lbcode["stack"][-1]]]
                            if len(lbcode["stack"])>1 and lbcode["stack"][-2] == "_LB_LOOP_MAGIC_CONST_":
                                if  opname[ ord(code.co_code[idx+delta]) ] == 'JUMP_ABSOLUTE':
                                    if_block_code, if_block_stack, if_is_class = __LB_decompile_python_code(code,tabs+1,idx+3+1,idx+delta,code_globals)
                                    idx += delta
                                    delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                                    lbcode["stack"][-1] = __LB_decompile_if_condition(if_condition["list"])
                                    lbcode["str"] += __LB_make_tab(tabs) + "while " + lbcode["stack"][-1] + ":" + "\n"
                                    lbcode["str"] += if_block_code
                                    idx += 3
                                    if_condition["list"] = []
                                else:
                                    idx += 3
                            else:
                                import dis
                                lbcode["str"] += "#NOTE: " + dis.dis(code) + "\n"
                                lbcode["str"] += "#NOTE: " + "unsupported situation at idx %d in code "%idx + `[(attr,getattr(code,attr)) for attr in dir(code)]` + "\n"
                                return lbcode["str"] + "#TODO python fail: " + " no _LB_LOOP_MAGIC_CONST_ below TOS in LOOP mode " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
                        else:
                            delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                            if_condition["list"] += [[idx,idx+delta+3,opcode,lbcode["stack"][-1]]]

#JUMP_ABSOLUTE at python 2.3
#JUMP_FORWARD at python 2.5
                            if  opname[ ord(code.co_code[idx+delta]) ] in [ 'JUMP_FORWARD', 'JUMP_ABSOLUTE' ]:
                                if  len(lbcode["stack"]) > 1 and lbcode["stack"][-2] == "_LB_EXCEPTION_MATCH_MAGIC_CONST_":
                                    if_block_code, if_block_stack, if_is_class = __LB_decompile_python_code(code,tabs,idx+3+1,idx+delta,code_globals,exception_mode)
                                else:
                                    if_block_code, if_block_stack, if_is_class = __LB_decompile_python_code(code,tabs+1,idx+3+1,idx+delta,code_globals,exception_mode)
                                idx += delta
                                if  opname[ ord(code.co_code[idx]) ] == 'JUMP_FORWARD':
                                    delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                                else:
                                    delta = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256 - idx
                                    delta_original = delta
                                    if  idx+delta >= idx_max:
                                        delta = idx_max - idx - 3
                                    if  delta < 1:
                                        delta = 1
                                if  __LB_condition_debug:
                                    lbcode["str"] += __LB_make_tab(tabs) + "#NOTE: " + `if_condition["list"]` + '\n'
                                lbcode["stack"][-1] = __LB_decompile_if_condition(if_condition["list"])
                                if  idx+delta+3 > idx+3+1:
                                    if  len(lbcode["stack"]) > 1 and lbcode["stack"][-2] == "_LB_EXCEPTION_MATCH_MAGIC_CONST_":
                                        else_block_code, else_block_stack, else_is_class = __LB_decompile_python_code(code,tabs,idx+3+1,idx+delta-1,code_globals,exception_mode)
                                        lbcode["str"] += __LB_make_tab(tabs-1) + "except " + lbcode["stack"].pop() + ":" + "\n"
                                        lbcode["stack"].pop() # "_LB_EXCEPTION_MATCH_MAGIC_CONST_"
                                        if  if_block_code.startswith("#_LB_EXCEPTION_MAGIC_CONST_: "):
                                            lbcode["str"] = lbcode["str"][:-2] + ", "
                                            if_block_code = if_block_code[len("#_LB_EXCEPTION_MAGIC_CONST_: "):]
                                        lbcode["str"] += if_block_code
                                        if  not else_block_code.startswith(__LB_make_tab(tabs-1) + "except"):
                                            lbcode["str"] += __LB_make_tab(tabs-1) + "except:" + "\n"
                                        if  len(else_block_code) > 0:
                                            lbcode["str"] += else_block_code
                                        else:
                                            lbcode["str"] += __LB_make_tab(tabs) + "pass" + "\n"
                                    else:
                                        else_block_code, else_block_stack, else_is_class = __LB_decompile_python_code(code,tabs+1,idx+3+1,idx+delta+3,code_globals,exception_mode)
                                        if  len(if_block_stack) > 0 and len(else_block_stack) > 0:
                                            code_tmp = if_block_stack[-1] + " if " + lbcode["stack"].pop() + " else " + else_block_stack[-1]
                                            lbcode["stack"] += [ code_tmp ]
                                        else:
                                            lbcode["str"] += __LB_make_tab(tabs) + "if " + lbcode["stack"].pop() + ":" + "\n"
                                            lbcode["str"] += if_block_code
                                            lbcode["str"] += __LB_make_tab(tabs) + "else:" + "\n"
                                            lbcode["str"] += else_block_code
                                elif len(comprehention_stack)>0:
                                    code_tmp = lbcode["stack"].pop()
                                    if_block_code = if_block_code[if_block_code.find("(")+1:if_block_code.rfind(")")]
                                    comprehention_stack[-1] += [if_block_code,code_tmp]
                                else:
                                    lbcode["str"] += __LB_make_tab(tabs) + "if " + lbcode["stack"].pop() + ":" + "\n"
                                    lbcode["str"] += if_block_code
                                    if  opname[ ord(code.co_code[idx]) ] == 'JUMP_ABSOLUTE' and delta_original<=1:
                                        lbcode["str"] += __LB_make_tab(tabs+1) + "continue" + "\n"
                                idx += delta + 3
                                if_condition["list"] = []
                            else:
                                idx += 3
    
                    elif opcode == 'LOAD_LOCALS':
                        lbcode["stack"] += ["_LB_LOCALS_MAGIC_CONST_"]
    
                    elif opcode == 'EXEC_STMT':
                        code_locals = lbcode["stack"].pop()
                        code_globals = lbcode["stack"].pop()
                        code_tmp = lbcode["stack"].pop()
                        if  code_globals != "None":
                            code_tmp += ", " + code_globals
                        if  code_locals != "None":
                            code_tmp += ", " + code_locals
                        if  code_tmp.startswith("(") and code_tmp.endswith(")"):
                            code_tmp = code_tmp[1:-1]
                        lbcode["str"] += __LB_make_tab(tabs) + "exec(" + code_tmp + ")" + "\n"

    
                    elif opcode == 'IMPORT_NAME':
                        id = ord(code.co_code[idx+1]) + ord(code.co_code[idx+2])*256
                        collection = lbcode["stack"].pop()
                        if  collection == "None":
                            lbcode["str"] += __LB_make_tab(tabs) + "import " + code.co_names[id] + "\n"
                            idx += 3
                        else:
                            import_mode = True
                            code_tmp = "from " + code.co_names[id] + " import " + collection.replace(",)",")")[1:-1].replace("'","")
                            if  code_tmp != "from __future__ import with_statement":
                                lbcode["str"] += __LB_make_tab(tabs) + code_tmp + "\n"
#no pop() at python 2.5
                        if  sys.version_info[0] == 2 and sys.version_info[1] > 4:
                            lbcode["stack"].pop()
    
                    else:
                        return lbcode["str"] + "#TODO python fail: " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class

                if  __LB_full_debug:
                    lbcode["str"] += __LB_make_tab(tabs) + "#NOTE: done " + opcode + " | stack is " + `lbcode["stack"]` + " | comprehention_stack is " + `comprehention_stack` + " | if_condition is " + `if_condition["list"]` + "\n"

                if  for_loop["should_jump"]:
                    idx = for_loop["target"]
                    for_loop["target"] = None
                    for_loop["should_jump"] = False
                elif  opcode in ['LOAD_CONST','LOAD_GLOBAL','LOAD_NAME','LOAD_FAST','LOAD_ATTR','LOAD_DEREF','STORE_GLOBAL','STORE_NAME','STORE_FAST','STORE_ATTR','STORE_DEREF','DELETE_GLOBAL','DELETE_NAME','DELETE_FAST','DELETE_ATTR','IMPORT_FROM','IMPORT_NAME','BUILD_TUPLE','BUILD_LIST','BUILD_MAP','CALL_FUNCTION','CALL_FUNCTION_VAR','CALL_FUNCTION_KW','CALL_FUNCTION_VAR_KW','COMPARE_OP','SETUP_LOOP','JUMP_ABSOLUTE','UNPACK_SEQUENCE','DUP_TOPX','LOAD_CLOSURE','BUILD_SLICE','FOR_ITER','RAISE_VARARGS']:
                    idx += 3
                elif opcode in ['INPLACE_ADD','INPLACE_SUBTRACT','INPLACE_MULTIPLY','INPLACE_DIVIDE','INPLACE_MODULO','INPLACE_POWER','INPLACE_FLOOR_DIVIDE','INPLACE_TRUE_DIVIDE','INPLACE_LSHIFT','INPLACE_RSHIFT','INPLACE_AND','INPLACE_XOR','INPLACE_OR','POP_TOP','ROT_TWO','ROT_THREE','ROT_FOUR','DUP_TOP','BINARY_POWER','BINARY_MULTIPLY','BINARY_DIVIDE','BINARY_MODULO','BINARY_ADD','BINARY_SUBTRACT','BINARY_SUBSCR','BINARY_FLOOR_DIVIDE','BINARY_TRUE_DIVIDE','BINARY_LSHIFT','BINARY_RSHIFT','BINARY_AND','BINARY_XOR','BINARY_OR','STORE_SUBSCR','DELETE_SUBSCR','YIELD_VALUE','RETURN_VALUE','UNARY_POSITIVE','UNARY_NEGATIVE','UNARY_NOT','UNARY_CONVERT','UNARY_INVERT','IMPORT_STAR','SLICE+0','SLICE+1','SLICE+2','SLICE+3','DELETE_SLICE+0','DELETE_SLICE+1','DELETE_SLICE+2','DELETE_SLICE+3','STORE_SLICE+0','STORE_SLICE+1','STORE_SLICE+2','STORE_SLICE+3','POP_BLOCK','GET_ITER','BREAK_LOOP','CONTINUE_LOOP','PRINT_ITEM','PRINT_NEWLINE','PRINT_ITEM_TO','PRINT_NEWLINE_TO','LOAD_LOCALS','EXEC_STMT','END_FINALLY','STORE_MAP']:
                    idx += 1
                elif opcode in ['BUILD_CLASS']:
                    idx += 4
                elif opcode in ['MAKE_FUNCTION', 'MAKE_CLOSURE']:
                    idx += 6
                elif opcode in [ 'JUMP_IF_FALSE', 'JUMP_IF_TRUE', 'SETUP_EXCEPT']:
                    pass
                else:
                    return lbcode["str"] + "#TODO python fail: " + opcode + " at %d/%d"%(idx,idx_max) + "\n",lbcode["stack"],is_class
#
#                                         *       *                 
#                    *                    ║               \/        
#                                  *      ║               /\    *   
#                             \/          ║      \ /                
#                             /\          ╬     --*--               
#                                       ╒═╩═╕    / \                
#                                       │:::│                       
#                   \ /                 │:::│             *         
#                  --*--     *          │:::│                  \/   
#                   / \                ╞╧╧╧╧╧╡                 /\   
#                                \ /   │::@::│   *     \ /          
#                               --*--  │:::::│        --*--         
#                   *            / \   │:::::│         / \          
#                        \/          ┌┐│:::::│┌┐                 *  
#                        /\         ╒╪╪╧═════╧╪╪╕                   
#                                   │││:::::::│││         *         
#                              *    │││:::::::│││    \/             
#                  ┌┐               │││:::::::│││    /\         ┌┐  
#                 ╞╧╧╡ *            │││:::::::│││              ╞╧╧╡ 
#                 │09│           ┌┐ │││:::::::│││ ┌┐           │lb│ 
#                ╞╧══╧╦══════════╪╧═╡││:::::::││╞═╧╪══════════╦╧══╧╡
#                │::::║::::::::::│::│││:::::::│││::│::::::::::║::::│
#                │::::║::::::::::│::│││:::::::│││::│::::::::::║::::│
#                │::::║::::::::::│::│││:::::::│││::│::::::::::║::::│
#                │::::║::::::::::│::│││:::▄:::│││::│::::::::::║::::│
#                │::::║::::::::::│┌─┴┴┴▀▀▀▀▀▀▀┴┴┴─┐│::::::::::║::::│
#                │::::║::::::::::││  In  another  ││::::::::::║::::│
#                │::::║::::::::::││castle? Or not?││::::::::::║::::│
#                └────╨──────────┴┴───────────────┴┴──────────╨────┘
#
#             Most bytecodes for 16-bit python are supported quite well.
#
        except:
            if  __LB_renpy_error_on_python_fail:
                raise
            lbcode["str"] += __LB_make_tab(tabs) + "# TODO: [%d] exception caught on opcode:"%idx + opcode + `lbcode["stack"]` + "\n"


        if  code_to == None and lbcode["str"].endswith("return None\n"):
            lbcode["str"] = "\n".join(lbcode["str"].split("\n")[:-2]+[""])
        if  len(lbcode["str"].split("\n")) == 1:
            lbcode["str"] = __LB_make_tab(tabs) + "pass" + "\n"
        for i in range(original_extra_stack):
            try:
                lbcode["stack"].pop()
            except: pass
        if  len(lbcode["stack"]) > 0:
            lbcode["str"] += __LB_make_tab(tabs) + "# TODO: non-empty stack on exit:" + `lbcode["stack"]` + "\n"
        return lbcode["str"],lbcode["stack"],is_class










# =============================
# LET'S DECOMPILE ATL COMMANDS
# =============================


    def __LB_decompile_atl(atl,tabs):
        lbcode_str = ""

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Pass_Statement
        if  len(atl.statements) == 0:
            lbcode_str += __LB_make_tab(tabs) + "pass" + "\n"
            
        for item in atl.statements:
#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Choice_Statement
            if  hasattr(renpy.atl, "RawChoice") and isinstance(item,renpy.atl.RawChoice):
                for chance, block in item.choices:
                    if  chance == "1.0":
                        lbcode_str += __LB_make_tab(tabs) + "choice:" + "\n"
                    else:
                        lbcode_str += __LB_make_tab(tabs) + "choice " + chance + ":" + "\n"
                    lbcode_str += __LB_decompile_atl(block,tabs+1)

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Parallel_Statement
            elif hasattr(renpy.atl, "RawParallel") and isinstance(item,renpy.atl.RawParallel):
                for block in item.blocks:
                    lbcode_str += __LB_make_tab(tabs) + "parallel:" + "\n"
                    lbcode_str += __LB_decompile_atl(block,tabs+1)

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Repeat_Statement
            elif hasattr(renpy.atl, "RawRepeat") and isinstance(item,renpy.atl.RawRepeat):
                if  item.repeats == None:
                    lbcode_str += __LB_make_tab(tabs) + "repeat" + "\n"
                else:
                    lbcode_str += __LB_make_tab(tabs) + "repeat " + item.repeats + "\n"

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Block_Statement
            elif hasattr(renpy.atl, "RawBlock") and isinstance(item,renpy.atl.RawBlock):
                lbcode_str += __LB_make_tab(tabs) + "block:" + "\n"
                lbcode_str += __LB_decompile_atl(item,tabs+1)                

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Function_Statement
            elif hasattr(renpy.atl, "RawFunction") and isinstance(item,renpy.atl.RawFunction):
                lbcode_str += __LB_make_tab(tabs) + "function " + item.expr + "\n"

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Interpolation_Statement
#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Expression_Statement
            elif hasattr(renpy.atl, "RawMultipurpose") and isinstance(item,renpy.atl.RawMultipurpose):
                expression = ""
                if item.warper == None and item.warp_function != None:
                    expression += "warp " + item.warp_function + __LB_invisible_space + item.duration + __LB_invisible_space
                elif item.warper != None:
                    expression += item.warper + " " + item.duration + __LB_invisible_space
                for i in item.expressions:
                    if  i[1]:
                        expression += " with ".join(i) + " "
                    else:
                        expression += i[0] + " "
                for i in item.properties:
                    if  i[1]:
                        expression += " ".join(i) + __LB_invisible_space
                    else:
                        expression += i[0] + " "
                for i in item.splines:
                    expression += i[0] + " "
                    expression += i[1][-1] + __LB_invisible_space
                    for idx in range(len(i[1])-1):
                        expression += "knot " + i[1][idx] + __LB_invisible_space
                if  item.revolution:
                    expression += item.revolution + " "
                if  item.circles != "0":
                    expression += "circles " + item.circles
                lbcode_str += __LB_make_tab(tabs) + expression + "\n"

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Contains_Statement
            elif hasattr(renpy.atl, "RawContainsExpr") and isinstance(item,renpy.atl.RawContainsExpr):
                lbcode_str += __LB_make_tab(tabs) + "contains " + item.expression + "\n"
            elif hasattr(renpy.atl, "RawChild") and isinstance(item,renpy.atl.RawChild):
                for i in item.children:
                    lbcode_str += __LB_make_tab(tabs) + "contains:" + "\n"
                    lbcode_str += __LB_decompile_atl(i,tabs+1)                

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Event_Statement
            elif hasattr(renpy.atl, "RawEvent") and isinstance(item,renpy.atl.RawEvent):
                lbcode_str += __LB_make_tab(tabs) + "event " + item.name + "\n"

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#On_Statement
            elif hasattr(renpy.atl, "RawOn") and isinstance(item,renpy.atl.RawOn):
                for name, block in item.handlers.iteritems():
                    lbcode_str += __LB_make_tab(tabs) + "on " + name + ":" + "\n"
                    lbcode_str += __LB_decompile_atl(block,tabs+1)                

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language#Time_Statement
            elif hasattr(renpy.atl, "RawTime") and isinstance(item,renpy.atl.RawTime):
                lbcode_str += __LB_make_tab(tabs) + "time " + item.time + "\n"


            else:
                result = "#TODO atl "+`item`
#
#                                    
#                                   /\
#                                  /~~\
#                                 /~~~~\
#                                '┬────┬'
#                                 │ ┌┐ │
#                     *          ┌┴─┴┴─┴┐          *
#                    /~\         └┬────┬┘         /~\
#                   /~~~\         │    │         /~~~\
#                  '┬───┬┌┐┌┐┌┐┌┐┌┤┌┐┌┐├┐┌┐┌┐┌┐┌┐┬───┬'
#                   │   ├┘└┘└┘└┘└┘└┘└┘└┘└┘└┘└┘└┘└┤   │
#                   │   │                        │   │
#                ───┴───┴────────────────────────┴───┴
#                       ... in another castle ...
#
#                     See "renpy/atl.py" for details.
#        
                lbcode_str += __LB_make_tab(tabs)+ result + "\n"
        return lbcode_str





# =============================
# LET'S DECOMPILE SL2 COMMANDS
# =============================


    def __LB_decompile_sl2(sl2,tabs,first_child=0):
        lbcode_str = ""

#http://www.renpy.org/doc/html/screens.html#screen-statement
        if  hasattr(renpy.sl2.slast, "SLScreen") and isinstance(sl2,renpy.sl2.slast.SLScreen):
            if  not "modal" in dict(sl2.keyword) and hasattr(sl2, "modal") and sl2.modal == None and sl2.modal != "False":
                lbcode_str += __LB_make_tab(tabs) + "modal " + sl2.modal + "\n"
            if  not "tag" in dict(sl2.keyword) and hasattr(sl2, "tag") and sl2.tag != None:
                lbcode_str += __LB_make_tab(tabs) + "tag " + sl2.tag + "\n"
            if  not "zorder" in dict(sl2.keyword) and hasattr(sl2, "zorder") and sl2.zorder != "0":
                lbcode_str += __LB_make_tab(tabs) + "zorder " + sl2.zorder + "\n"
            if  not "variant" in dict(sl2.keyword) and hasattr(sl2, "variant") and sl2.variant != None and sl2.variant != "None":
                lbcode_str += __LB_make_tab(tabs) + "variant " + `sl2.variant` + "\n"

        if  len(sl2.children) == first_child and len(sl2.keyword) == 0:
            lbcode_str += __LB_make_tab(tabs) + "pass" + "\n"
            
        for k in sl2.keyword:
            lbcode_str += __LB_make_tab(tabs) + k[0] + " " + k[1] + "\n"

        for item in sl2.children[first_child:]:
            if  hasattr(renpy.sl2.slast, "SLDisplayable") and isinstance(item,renpy.sl2.slast.SLDisplayable):
                if  item.displayable.__module__ == "renpy.ui" and item.displayable.__name__[0] == "_":
                    item_disp = item.displayable.__name__[1:]
                elif item.displayable.__module__ == "renpy.text.text" and item.displayable.__name__ in ["Text"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.im" and item.displayable.__name__ in ["image"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.motion" and item.displayable.__name__ in ["Transform"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.dragdrop" and item.displayable.__name__ in ["Drag","DragGroup"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.layout" and item.displayable.__name__ in ["Null","Grid","Side"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.layout" and item.displayable.__name__ in ["Window","MultiBox"]:
                    if  hasattr(item,"style"):
                        item_disp = item.style
                    else:
                        item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.behavior" and item.displayable.__name__ in ["Button","Input","Timer","MouseArea"]:
                    item_disp = item.displayable.__name__.lower()
                elif item.displayable.__module__ == "renpy.display.behavior" and item.displayable.__name__ in ["OnEvent"]:
                    item_disp = "on"
                elif item.displayable.__module__ == "renpy.sl2.sldisplayables" and item.displayable.__name__.startswith("sl2"):
                    item_disp = item.displayable.__name__[3:]
                else:
                    item_disp = "#TODO " + item.displayable.__module__ + "." + item.displayable.__name__
                lbcode_str += __LB_make_tab(tabs) + item_disp + (" " if len(item.positional) else "") + " ".join(item.positional)
                if  item.children or item.keyword:
                    lbcode_str += ":\n" + __LB_decompile_sl2(item,tabs+1)
                else:
                    lbcode_str += "\n"
#http://www.renpy.org/doc/html/screens.html#if
            elif  hasattr(renpy.sl2.slast, "SLIf") and isinstance(item,renpy.sl2.slast.SLIf):
                for i, (c, block) in enumerate(item.entries):
                    if  c != None and i == 0:
                        lbcode_str += __LB_make_tab(tabs) + "if " + c + ":\n"
                    if  c != None and i != 0:
                        lbcode_str += __LB_make_tab(tabs) + "elif " + c + ":\n"
                    if  c == None and i == 0:
                        lbcode_str += __LB_make_tab(tabs) + "if True:\n"
                    if  c == None and i != 0:
                        lbcode_str += __LB_make_tab(tabs) + "else:\n"
                    lbcode_str += __LB_decompile_sl2(block,tabs+1)
#http://www.renpy.org/doc/html/screens.html#for
            elif  hasattr(renpy.sl2.slast, "SLFor") and isinstance(item,renpy.sl2.slast.SLFor):
                item_variable = item.variable
                children_since = 0
                if  item.variable == "_sl2_i" and isinstance(item.children[0],renpy.sl2.slast.SLPython):
                    code = __LB_decompile_python(item.children[0].code,0)
                    if  len(code.split("\n")) == 1 and code.endswith(" = _sl2_i"):
                        item_variable = code[:-len(" = _sl2_i")]
                        children_since = 1
                lbcode_str += __LB_make_tab(tabs) + "for " + item_variable + " in " + item.expression + ":\n"
                lbcode_str += __LB_decompile_sl2(item,tabs+1,children_since)
#http://www.renpy.org/doc/html/screens.html#python
            elif  hasattr(renpy.sl2.slast, "SLPython") and isinstance(item,renpy.sl2.slast.SLPython):
                if  len(__LB_decompile_python(item.code,0).split("\n")) == 1:
                    lbcode_str += __LB_make_tab(tabs) + "$ " + __LB_decompile_python(item.code,0) + "\n"
                else:
                    lbcode_str += __LB_make_tab(tabs) + "python:\n"
                    lbcode_str += __LB_decompile_python(item.code,tabs+1) + "\n"
            else:
                result = "#TODO sl2 "+`item`
#
#                               !~~
#                           ┌┐┌┐│┌┐┌┐ 
#                           │└┘└┴┘└┘│                
#                  ┌┐       └┐     ┌┘       ┌┐       
#                ┌─┴┴─┐      │     │      ┌─┴┴─┐   
#                └┬──┬┘      │     │      └┬──┬┘   
#              ┌──┴──┴──┐    │     │    ┌──┴──┴──┐                           
#              └─┬────┬─┴────┴─────┴────┴─┬────┬─┘
#                │    │       ┌─┬─┐       │    │
#                │    │       │ │ │       │    │
#            ────┴────┴───────┴─┴─┴───────┴────┴────
#                       ... in another castle ...
#
#                     See "renpy/sl2/slatl.py" for details.
#        
                lbcode_str += __LB_make_tab(tabs)+ result + "\n"
        return lbcode_str






# ==============================================
# THIS AWFUL SWITCH WORKS WITH STRING COLLISIONS
# ==============================================
#
# "init:" + "python:" -> "init python:"
#
    
    def __LB_add_string(file,line,str,tabs):
        global __LB_decompiled_files
        if  not file in __LB_decompiled_files:
            __LB_decompiled_files[file] = {}
        if  not line in __LB_decompiled_files[file]:
            __LB_decompiled_files[file][line] = (tabs,str)
        else:
            (t,s) = __LB_decompiled_files[file][line]
            if  not s.startswith(str) and not str.startswith(s):
                if  s.startswith("call ") and str.startswith("label "):
                    if  not " from " in s:
                        s += " from "+str[5:-1]
                        __LB_decompiled_files[file][line] = (t,s)
                elif  str.startswith("call ") and s.startswith("label "):
                    if  not " from " in str:
                        str += " from "+s[5:-1]
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("init") and str.startswith("python"):
                    s = s[:-1] + " " + str
                    __LB_decompiled_files[file][line] = (t,s)
                elif  str.startswith("init") and s.startswith("python"):
                    str = str[:-1] + " " + s
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("init") and s.startswith("define"):
                    pass
                elif  s.startswith("init") and str.startswith("define"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("init") and str.startswith("screen"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("init") and s.startswith("screen"):
                    pass
                elif  str.startswith("init") and s.startswith("image"):
                    pass
                elif  s.startswith("init") and str.startswith("image"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("init") and s.startswith("transform"):
                    pass
                elif  s.startswith("init") and str.startswith("transform"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("init") and s.startswith("#TODO"):
                    pass
                elif  s.startswith("init") and str.startswith("#TODO"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("pass") and s.startswith("call"):
                    pass
                elif  s.startswith("pass") and str.startswith("call"):
                    __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("menu") and s.startswith("label "):
                    suffix = ""
                    if  str.find("\n") != -1:
                        suffix = str[str.find("\n"):]
                    __LB_decompiled_files[file][line] = (tabs,"menu "+s[6:]+suffix)
                elif  s.startswith("menu") and str.startswith("label "):
                    suffix = ""
                    if  s.find("\n") != -1:
                        suffix = s[s.find("\n"):]
                    __LB_decompiled_files[file][line] = (t,"menu "+str[6:]+suffix)
                elif  s.startswith("menu") and str.startswith("menu"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  str.startswith("menu") and not s.startswith("menu"):
                    __LB_decompiled_files[file][line] = (tabs,str + "\n" + __LB_make_tab(tabs+1) + s)
                elif  s.startswith("menu") and not str.startswith("menu"):
                    __LB_decompiled_files[file][line] = (t,s + "\n" + __LB_make_tab(t+1) + str)
                elif  s.startswith("python") and str.startswith("python"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("transform") and str.startswith("transform"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("image") and str.startswith("image"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("show") and str.startswith("show"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("scene") and str.startswith("scene"):
                    if  len(str) > len(s):
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  s.startswith("screen") and str.startswith("screen"):
                    if  tabs < t:
                        __LB_decompiled_files[file][line] = (tabs,str)
                elif  "with " in str:
                    if  "with " in s:
                        pass
                    else:
                        __LB_decompiled_files[file][line] = (tabs,s+" "+str)
                elif  "with " in s:
                    if  "with " in str:
                        pass
                    elif ":\n" in str:
                        __LB_decompiled_files[file][line] = (tabs,str.replace(":\n"," "+s+":\n",1))
                    else:
                        __LB_decompiled_files[file][line] = (tabs,str+" "+s)
                else:
                    __LB_decompiled_files[file][line] = (tabs,"#TODO: collision: " + str + " " + s)
            if  t < tabs and not str.startswith("screen"):
                __LB_decompiled_files[file][line] = (tabs,str)



# ====================================
# RENPY STATEMENTS LANGUAGE DECOMPILER
# ====================================

    def __LB_decompile_item(item,tabs=0):
        result = "#" + repr(item)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Call_Statement
        if  hasattr(renpy.ast, "Call") and isinstance(item,renpy.ast.Call):
            result = "call "
            if  item.expression:
                result += "expression "
            result += item.label
            if  hasattr(item, "arguments") and item.arguments:
                if  item.expression:
                    result += " pass"
                result_tmp = ""
                for (x,val) in item.arguments.arguments:
                    if  x:
                        result_tmp += ", "+x+"="+val
                    else:
                        result_tmp += ", "+val
                if item.arguments.extrapos:
                    result_tmp += ", *"+item.arguments.extrapos
                if item.arguments.extrakw:
                    result_tmp += ", **"+item.arguments.extrakw
                result += " (" + result_tmp[2:] + ")"
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Define_Statement
        elif  hasattr(renpy.ast, "Define") and isinstance(item,renpy.ast.Define):
            result = "define " + item.varname + " = "
            if  item.code.source:
                result += item.code.source
            else:
                result += __LB_decompile_python(item.code,0,True)
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#If_Statement
        elif  hasattr(renpy.ast, "If") and isinstance(item,renpy.ast.If):
            entries = [(condition, block) for condition, block in item.entries]
            (condition, block) = entries[0]
            result = "if "+condition+":"
            __LB_add_string(item.filename,item.linenumber,result,tabs)
            for (condition, block) in entries[1:-1]:                
                result = "elif "+condition+":"
                linenumber = block[0].linenumber-1
                __LB_add_string(item.filename,linenumber,result,tabs)
            if len(entries)>1:
                (condition, block) = entries[-1]
                if  condition == "True":
                    result = "else:"
                else:
                    result = "elif "+condition+":"
                linenumber = block[0].linenumber-1
                __LB_add_string(item.filename,linenumber,result,tabs)

            for (condition, block) in entries:                
                for it in block:
                    __LB_decompile_item(it,tabs+1)

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language
        elif  hasattr(renpy.ast, "Transform") and isinstance(item,renpy.ast.Transform):
            if  isinstance(item.varname,str) or isinstance(item.varname,unicode):
                result = "transform " + item.varname
            else:
                result = "transform " + " ".join(item.varname)
            if  item.parameters != None:
                result_tmp = ""
                for (x,val) in item.parameters.parameters:
                    if  val:
                        result_tmp += ", "+x+"="+val
                    else:
                        result_tmp += ", "+x
                if item.parameters.extrapos:
                    result_tmp += ", *"+item.parameters.extrapos
                if item.parameters.extrakw:
                    result_tmp += ", **"+item.parameters.extrakw
                result += " (" + result_tmp[2:] + ")"
            result += ":\n" + __LB_decompile_atl(item.atl,tabs+1)
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/Animation_and_Transformation_Language
#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Image_Statement
        elif  hasattr(renpy.ast, "Image") and isinstance(item,renpy.ast.Image):
            if  isinstance(item.imgname,str) or isinstance(item.imgname,unicode):
                name = item.imgname
            else:
                name = " ".join(item.imgname)
            if  item.code:
                result = "image " + name + " = " + __LB_decompile_python(item.code,0,True)
            else:
                result = "image " + name + ":\n" + __LB_decompile_atl(item.atl,tabs+1)
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Init_Statement
        elif  hasattr(renpy.ast, "Init") and isinstance(item,renpy.ast.Init):
            if  item.priority:
                result = "init " + "%d"%item.priority + ":"
            else:
                result = "init:"
            __LB_add_string(item.filename,item.linenumber,result,tabs)
            if  len(item.block)>1 or not isinstance(item.block[0],renpy.ast.Python) or item.block[0].linenumber != item.linenumber:
                for it in item.block:
                    __LB_decompile_item(it,tabs+1)


#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Jump_Statement
        elif  hasattr(renpy.ast, "Jump") and isinstance(item,renpy.ast.Jump):
            result = "jump "
            if  item.expression:
                result += "expression "
            result += item.target
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Label_Statement
        elif  hasattr(renpy.ast, "Label") and isinstance(item,renpy.ast.Label):
            result = "label " + item.name
            if  hasattr(item, "parameters") and item.parameters:
                result_tmp = ""
                for (x,val) in item.parameters.parameters:
                    if  val:
                        result_tmp += ", "+x+"="+val
                    else:
                        result_tmp += ", "+x
                if item.parameters.extrapos:
                    result_tmp += ", *"+item.parameters.extrapos
                if item.parameters.extrakw:
                    result_tmp += ", **"+item.parameters.extrakw
                result += " (" + result_tmp[2:] + "):"
            else:
                result += ":"
            __LB_add_string(item.filename,item.linenumber,result,tabs)
            for it in item.block:
                __LB_decompile_item(it,tabs+1)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Menu_Statement
        elif  hasattr(renpy.ast, "Menu") and isinstance(item,renpy.ast.Menu):
            result = "menu:"
            if  hasattr(item,"with_") and item.with_ != None:
                result += "\n" + __LB_make_tab(tabs+1) + "with " + item.with_
            if  hasattr(item,"set") and item.set != None:
                result += "\n" + __LB_make_tab(tabs+1) + "set " + item.set
            for (label, condition, block) in item.items:
                label = label.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t").replace("\"","\\\"")
                if  block == None:
                    result += "\n" + __LB_make_tab(tabs+1) + '"'+label+'"'
            __LB_add_string(item.filename,item.linenumber,result,tabs)

            for (label, condition, block) in item.items:
                label = label.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t").replace("\"","\\\"")
                if  block != None:
                    result = '"'+label+'"'
                    if  condition != "True":
                        result += " if " + condition
                    result += ":"
                    linenumber = block[0].linenumber-1
                    __LB_add_string(item.filename,linenumber,result,tabs+1)
                    for it in block:
                        __LB_decompile_item(it,tabs+2)


#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Pass_Statement
        elif  hasattr(renpy.ast, "Pass") and isinstance(item,renpy.ast.Pass):
            result = "pass"
            __LB_add_string(item.filename,item.linenumber,result,tabs)


#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Python_Statement
        elif  hasattr(renpy.ast, "Python") and isinstance(item,renpy.ast.Python):
            if  item.hide:
                result = "python hide:\n"
            else:
                result = "python:\n"
            if  __LB_renpy_error_on_python_fail:
                result += __LB_decompile_python(item.code,tabs+1)
            else:
                try:
                    result += __LB_decompile_python(item.code,tabs+1)
                except:
                    result += "#TODO: parse this python code"
            __LB_add_string(item.filename,item.linenumber,result,tabs)
        elif  hasattr(renpy.ast, "EarlyPython") and isinstance(item,renpy.ast.EarlyPython):
            if  item.hide:
                result = "python early hide:\n"
            else:
                result = "python early:\n"
            result += __LB_decompile_python(item.code,tabs+1)
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Return_Statement
        elif  hasattr(renpy.ast, "Return") and isinstance(item,renpy.ast.Return):
            result = "return"
            if  hasattr(item, "expression") and item.expression:
                result += " " + item.expression
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#With_Statement
        elif  hasattr(renpy.ast, "With") and isinstance(item,renpy.ast.With):
            result = "with "
            if  item.expr != "None":
                result += item.expr
                if  item.paired:
                    result += "#TODO with two expressions: " + item.paired
            else:
                if  item.paired:
                    result += item.paired
                else:
                    result += "None"
            __LB_add_string(item.filename,item.linenumber,result,tabs)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#While_Statement
        elif  hasattr(renpy.ast, "While") and isinstance(item,renpy.ast.While):
            result = "while "+item.condition+":"
            __LB_add_string(item.filename,item.linenumber,result,tabs)
            for it in item.block:
                __LB_decompile_item(it,tabs+1)

#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Scene_Statement
#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Show_Statement
#http://www.renpy.org/wiki/renpy/doc/reference/The_Ren'Py_Language#Hide_Statement
        elif  (hasattr(renpy.ast, "Scene") and isinstance(item,renpy.ast.Scene)) or (hasattr(renpy.ast, "Show") and isinstance(item,renpy.ast.Show)) or (hasattr(renpy.ast, "Hide") and isinstance(item,renpy.ast.Hide)):
            if isinstance(item,renpy.ast.Scene):
                result = "scene "
            elif isinstance(item,renpy.ast.Show):
                result = "show "
            elif isinstance(item,renpy.ast.Hide):
                result = "hide "

            if  item.imspec != None:
                zorder = 0
                expression = None
                tag = None
                behind = []
                if len(item.imspec) == 3:
                    name, at_list, layer = item.imspec
                elif len(item.imspec) == 6:
                    name, expression, tag, at_list, layer, zorder = item.imspec
                elif len(item.imspec) == 7:
                    name, expression, tag, at_list, layer, zorder, behind = item.imspec
                if  expression == None:
                    result += " ".join(item.imspec[0]) + " "
                else:
                    result += "expression " + expression + " "
                if  len(at_list) > 0:
                    result += "at " + ", ".join([i for i in at_list]) + " "
                if  tag != None:
                    result += "as " + tag + " "
                if  len(behind) > 0:
                    result += "behind " + (", ".join(behind)) + " "
                if  layer != "master":
                    result += "onlayer " + layer + " "
                if  zorder != 0 and zorder != None:
                    result += "zorder " + zorder + " "
                if  hasattr(item,"atl") and item.atl:
                    result += ":\n" + __LB_decompile_atl(item.atl,tabs+1)
            __LB_add_string(item.filename,item.linenumber,result,tabs)

        elif  hasattr(renpy.ast, "Screen") and isinstance(item,renpy.ast.Screen):
            if  isinstance(item.screen.name,str) or isinstance(item.screen.name,unicode):
                name = item.screen.name
            else:
                name = " ".split(item.screen.name)

            if  isinstance(item.screen,renpy.sl2.slast.SLScreen):
#WOOOOOH! SCREEN LANG 2.0 IS AWESOME
                result = "screen " + name + ":\n"
                result += __LB_decompile_sl2(item.screen,tabs+1)
            else:
                result = "#TODO screen " + name + ":"
#TODO item.screen.code.bytecode - python bycode for screen         
            __LB_add_string(item.filename,item.linenumber,result,tabs)

        elif  hasattr(renpy.ast, "Say") and isinstance(item,renpy.ast.Say):
            result = ""
            if  item.who == None:
                pass
            elif isinstance(item.who,unicode):
                result += item.who+" "
            what = item.what.replace("\\","\\\\").replace("\n","\\n").replace("\t","\\t").replace("\"","\\\"")
            result += "\""+what+"\""
            if  item.with_:
                result += " with " + item.with_
#TODO item.who_fast - True/False
#TODO item.interact - True/False
            __LB_add_string(item.filename,item.linenumber,result,tabs)

        elif  hasattr(renpy.ast, "Translate") and isinstance(item,renpy.ast.Translate):
            if  item.language is None:
                for it in item.block:
                    __LB_decompile_item(it,tabs)
            else:
                result = "translation " + item.language + " " + item.identifier + ":\n"
                for it in item.block:
                    __LB_decompile_item(it,tabs)
        elif  hasattr(renpy.ast, "EndTranslate") and isinstance(item,renpy.ast.EndTranslate):
            pass
        
        elif  hasattr(renpy.ast, "UserStatement") and isinstance(item,renpy.ast.UserStatement):
            result = item.line
            __LB_add_string(item.filename,item.linenumber,result,tabs)

        else:
            result = "#TODO" + repr(item)
#        
#                               !~~
#                              /~\
#                             /~~~\
#                            /~~~~~\            
#               ┌┐┌┐┌┐┌┐┌┐  '┬─────┬'  ┌┐┌┐┌┐┌┐┌┐
#               │└┘└┘└┘└┘│   │  █  │   │└┘└┘└┘└┘│
#               └┐      ┌┘   │     │   └┐      ┌┘
#                │  ▐▌  │    │     │    │  ▐▌  │
#                │      ├────┴─────┴────┤      │
#                │      │       V       │      │
#                │      │       ▄       │      │
#                │      │      ▐█▌      │      │
#            ────┴──────┴──────▀▀▀──────┴──────┴────
#                   ... in another castle ...
#        
#                See "renpy/ast.py" for details.
#        
            __LB_add_string(item.filename,item.linenumber,result,tabs)
        result = __LB_make_tab(tabs) + result + "\n"
        return result

    def __LB_decompile_all():
        for key,val in renpy.game.script.namemap.iteritems():
            __LB_decompile_item(val)
        for fname in __LB_decompiled_files:
            fname_print = fname.replace("/","_").replace("\\","_").replace(":","_")+".txt"
            if  len([1 for matcher in __LB_files_filtered_out if matcher.match(fname_print)]) > 0:
                continue
            out = __LB__open(fname_print,"wb")
            lines = [i for i in __LB_decompiled_files[fname]]
            lines.sort()
            for i in range(1,lines[-1]+1):
                if  not i in __LB_decompiled_files[fname]:
                    out.write("\n")
                elif  __LB_decompiled_files[fname][i] != None:
                    (tabs,str) = __LB_decompiled_files[fname][i]
                    if  str[-1:] == "\n":
                        str = str[:-1]
                    if  str.startswith("python:") and len(str.split("\n")) == 2:
                            str = str[7:]
                            while  str != str.replace("\n    ","\n"):
                                str = str.replace("\n    ","\n")
                            str = "$ " + str.replace("\n","")
                    try:
                        out.write(__LB_make_tab(tabs) + str.encode("utf-8") + "\n")
                    except:
                        renpy.error((fname_print,i,__LB_make_tab(tabs) + str + "\n"))
                    for j in range(1,len(str.split("\n"))):
                        if  i+j in __LB_decompiled_files[fname]:
                            break
                        __LB_decompiled_files[fname][i+j] = None
                    i += 1
            out.close()

    __LB_decompile_all()
