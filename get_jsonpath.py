import json
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

def get_jsonpath(json_file, json_str, jsonpath_expr_str): 
    if json_file is None: 
        dat = json.loads(json_str)
    else: 
        with open(json_file) as f:
            dat = json.load(f)

    jsonpath_expr = parse(jsonpath_expr_str)

    results = jsonpath_expr.find(dat)

    results_list = []

    for match in results:
        results_list.append(match.value)

    return(results_list)

if __name__ == "__main__":

    # json_file = 'covid19_model_2020-03-22-03-16-47.json'
    # jsonpath_expr_str = "$..text_refs"
    # jsonpath_expr_str = "$..stmts[?(@.belief == 1)]"
    # jsonpath_expr_str = "$..stmts[?(@.stmt.type == 'IncreaseAmount')]"
    # jsonpath_expr_str = "$..stmts[?(@.stmt.obj.db_refs.UP == 'P16278')]"
    # jsonpath_expr_str = "$..stmts[?(@.stmt.evidence[*].text_refs.PMCID == 'PMC331007')]"

    json_file = None
    json_str = '[{"id": "a", "foo": [{"baz": 1}, {"baz": 2}]}, {"id": "b", "foo": [{"baz": 3}, {"baz": 4}]}]'
    jsonpath_expr_str = '$..foo[*].baz'
    jsonpath_expr_str = '$[?(@.id == "a")].foo'
    
    get_jsonpath(json_file, json_str, jsonpath_expr_str)
