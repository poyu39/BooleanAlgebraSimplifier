import argparse
from TM import TM

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Boolean Algebra Simplifier use Tabulation Method by poyu39')
    parser.add_argument('-v', nargs='+', type=str, help='variables')
    parser.add_argument('-m', nargs='+', type=int, help='minterms')
    parser.add_argument('-M', nargs='+', type=int, help='maxterms')
    parser.add_argument('-d', nargs='+', type=int, help='dontcares')
    args = parser.parse_args()
    variables = args.v
    minterms = args.m
    maxterms = args.M
    dontcares = args.d
    
    if minterms:
        minterms = [f'm{minterm}' for minterm in minterms]
    else:
        minterms = []
    if maxterms:
        maxterms = [f'M{maxterm}' for maxterm in maxterms]
    else:
        maxterms = []
    if dontcares:
        dontcares = [f'd{dontcare}' for dontcare in dontcares]
    else:
        dontcares = []
    
    if minterms and not maxterms:
        tm = TM(variables)
        col1 = tm.group_by_one(minterms + dontcares)
        col1, col2 = tm.next_column(col1)
        col2, col3 = tm.next_column(col2)
        PIs = tm.get_PI([col1, col2, col3])
        EPIs, NEPIs ,EPIs_mark = tm.get_EPI(PIs, minterms + dontcares)
    
        # table
        tm.gen_table([col1, col2, col3], PIs)
        
        # PI_chart
        PI_chart = tm.gen_PI_chart(minterms, PIs, EPIs, NEPIs, EPIs_mark)
        print('Prime implicant chart')
        print(PI_chart)
        
        # boolean
        print('SOP logic function')
        SOP = tm.get_SOP(variables, EPIs, NEPIs)
        function = f'f({", ".join(variables)}) = {SOP}'
        print(function)
    elif maxterms and not minterms:
        tm = TM(variables)
        col1 = tm.group_by_one(maxterms + dontcares)
        col1, col2 = tm.next_column(col1)
        col2, col3 = tm.next_column(col2)
        PIs = tm.get_PI([col1, col2, col3])
        EPIs, NEPIs ,EPIs_mark = tm.get_EPI(PIs, maxterms + dontcares)
    
        # table
        tm.gen_table([col1, col2, col3], PIs)
        
        # PI_chart
        PI_chart = tm.gen_PI_chart(maxterms, PIs, EPIs, NEPIs, EPIs_mark)
        print('Prime implicant chart')
        print(PI_chart)
        
        # boolean
        print('POS logic function')
        POS = tm.get_POS(variables, EPIs, NEPIs)
        function = f'f({", ".join(variables)}) = {POS}'
        print(function)