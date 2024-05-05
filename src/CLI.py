import argparse
from TM import TM

if __name__ == '__main__':
    # example: python CLI.py -v a b c d -m 0 1 2 3 4 6 7 11 12 15
    parser = argparse.ArgumentParser(description='Boolean Algebra Simplifier use Tabulation Method by poyu39')
    parser.add_argument('-v', nargs='+', type=str, help='variables')
    parser.add_argument('-m', nargs='+', type=int, help='minterms')
    parser.add_argument('-M', nargs='+', type=int, help='maxterms')
    parser.add_argument('-d', nargs='+', type=int, help='dontcare')
    args = parser.parse_args()
    variables = args.v
    minterms = args.m
    maxterms = args.M
    dontcare = args.d
    
    tm = TM(len(variables), minterms)
    minterms_bin = tm.dec2bin()
    col1 = tm.group_by_one(len(variables), minterms, minterms_bin)
    col1, col2 = tm.next_column(col1)
    col2, col3 = tm.next_column(col2)
    PIs = tm.get_PI([col1, col2, col3])
    EPIs, NEPIs ,EPIs_mark = tm.get_EPI(PIs, minterms)
    
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