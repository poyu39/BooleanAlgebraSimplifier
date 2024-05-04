from pprint import pprint
import prettytable as pt


class TM:
    '''
        Tabulation Method
    '''
    def __init__(self, variables_num, minterms) -> None:
        self.variables_num = variables_num
        self.minterms = minterms
    
    def dec2bin(self):
        '''
            將十進制的 minterm 轉換為二進制
        '''
        minterms_bin = []
        for i in self.minterms:
            minterms_bin.append(bin(i)[2:].zfill(self.variables_num))
        return minterms_bin
    
    def group_by_one(self, variables_num, minterms, minterms_bin):
        '''
            將 minterm 依照 1 的數量分組
        '''
        one_groups = []
        for i in range(variables_num + 1):
            one_groups.append([])
        for i in range(len(minterms_bin)):
            count = minterms_bin[i].count('1')
            one_groups[count].append([str(minterms[i]), minterms_bin[i]])
        return one_groups
    
    def _compare_01(self, a, b):
        '''
            比較兩個 minterm 是否只差一個 1
        '''
        count = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                count += 1
        return count == 1
    
    def _merge(self, a, b):
        '''
            合併兩個 minterm
        '''
        result = ''
        for i in range(len(a)):
            if a[i] != b[i]:
                result += '-'
            else:
                result += a[i]
        return result

    def _mark(self, row: list):
        '''
            將比較過的 minterm mark 起來 (不重複標記)
        '''
        if len(row) == 2:
            row.append('v')
        return row
    
    def next_column(self, last_col: list):
        '''
            依照 minterm 的 1 的數量進行合併
        '''
        next_groups = []
        # 下一個 group 數量會比上一個少一個
        for i in range(len(last_col) - 1):
            next_groups.append([])
            for j in range(len(last_col[i])):
                for k in range(len(last_col[i + 1])):
                    if self._compare_01(last_col[i][j][1], last_col[i + 1][k][1]):
                        # 將比較過的 minterms mark 起來
                        self._mark(last_col[i][j])
                        self._mark(last_col[i + 1][k])
                        # 合併 minterms key
                        key = f'{last_col[i][j][0]}, {last_col[i + 1][k][0]}'
                        next_groups[i].append([key, self._merge(last_col[i][j][1], last_col[i + 1][k][1])])
        return last_col, next_groups
    
    def _filter_redundant(self, prime_implicants):
        '''
            過濾掉重複的 prime implicant (保留先出現的)
        '''
        result = []
        for implicant in prime_implicants:
            is_redundant = False
            for prime_implicant in result:
                if implicant[1] == prime_implicant[1]:
                    is_redundant = True
                    break
            if not is_redundant:
                result.append(implicant)
        return result
    
    def get_PI(self, cols):
        '''
            取得 prime implicant
        '''
        prime_implicants = []
        for col in cols:
            for group in col:
                for implicant in group:
                    if len(implicant) == 2:
                        prime_implicants.append(implicant[0:2])
        prime_implicants = self._filter_redundant(prime_implicants)
        return prime_implicants
    
    def get_EPI(self, PIs, minterms):
        '''
            取得 essential prime implicant
        '''
        EPIs = []
        NEPIs = []
        minterm_in_PI = {}
        EPIs_minterm = []
        for i in minterms:
            minterm_in_PI[str(i)] = 0
        
        # 計算每個 minterm 在 PI 中出現的次數
        for PI in PIs:
            minterms = PI[0].split(', ')
            for minterm in minterms:
                minterm_in_PI[minterm] += 1
        
        # 判斷是否為 EPI
        for minterm in minterm_in_PI:
            count = minterm_in_PI[minterm]
            if count == 1:
                EPIs_minterm.append(minterm)
                for PI in PIs:
                    minterms = PI[0].split(', ')
                    if minterm in minterms and PI not in EPIs:
                        EPIs.append(PI)
                        
        # 取得 NEPI
        # 將 EPI 的 minterm 從 minterm_in_PI 中移除
        for EPI in EPIs:
            EPIs_minterm = EPI[0].split(', ')
            for minterm in EPIs_minterm:
                minterm_in_PI[minterm] = 0
        for minterm in minterm_in_PI:
            for PI in PIs:
                if minterm_in_PI[minterm] != 0:
                    minterms = PI[0].split(', ')
                    if minterm in minterms:
                        NEPIs.append(PI)
                        minterm_in_PI[minterm] = 0
        
        return EPIs, NEPIs, EPIs_minterm
    
    def gen_table(self, cols, PIs):
        '''
            產生 table
        '''
        # 用 Column 分成多個 table
        for i, col in enumerate(cols):
            table = pt.PrettyTable()
            if i == 0:
                table.field_names = ['Group', 'Decimal', 'Binary', '']
            else:
                table.field_names = ['Group', 'Minterm', 'Binary', '']
            for j, group in enumerate(col):
                for k, minterm in enumerate(group):
                    if k == 0:
                        row = [f'Group {j}']
                    else:
                        row = ['']
                    for m in minterm:
                        row.append(m)
                    while len(row) < 4:
                        row.append('')
                    if minterm not in PIs and len(minterm) == 2:
                        row[3] = 'redundant'
                    table.add_row(row)
            print(f'Column {i}')
            print(table)
    
    def gen_PI_chart(self, minterms, PIs, EPIs, NEPIs, EPIs_minterm):
        '''
            產生 Prime implicant chart ⛒ ✖
        '''
        PI_chart = pt.PrettyTable()
        field_names = ['', 'Prime Implicant']
        for minterm in minterms:
            field_names.append(f'm{minterm}')
        PI_chart.field_names = field_names
        for PI in PIs:
            PI_key = PI[0]
            row = ['', PI_key]
            PI_key = PI_key.split(', ')
            for minterm in minterms:
                minterm = str(minterm)
                if minterm in PI_key:
                    if minterm in EPIs_minterm:
                        row.append('⛒')
                    else:
                        row.append('✖')
                else:
                    row.append('')
            # 加上 EPI \ NEPI 標籤
            if PI in EPIs:
                row[0] = 'EPI'
            if PI in NEPIs:
                row[0] = 'NEPI'
            PI_chart.add_row(row)
        return PI_chart
    
    def _bin2bool(self, variables, bin):
        result = ''
        index = 0
        for bit in bin:
            if bit == '1':
                result += f'{variables[index]}'
            elif bit == '0':
                result += f'{variables[index]}\''
            index += 1
        return result
    
    def get_SOP(self, variables, EPIs, NEPIs):
        '''
            取得 SOP logic function
        '''
        result = []
        for EPI in EPIs:
            result.append(self._bin2bool(variables, EPI[1]))
        for NEPI in NEPIs:
            result.append(self._bin2bool(variables, NEPI[1]))
        return ' + '.join(result)

if __name__ == '__main__':
    variables = ['a', 'b', 'c', 'd']
    minterms = [0, 1, 2, 3, 4, 6, 7, 11, 12, 15]
    
    tm = TM(len(variables), minterms)
    minterms_bin = tm.dec2bin()
    col1 = tm.group_by_one(len(variables), minterms, minterms_bin)
    col1, col2 = tm.next_column(col1)
    col2, col3 = tm.next_column(col2)
    PIs = tm.get_PI([col1, col2, col3])
    EPIs, NEPIs ,EPIs_minterm = tm.get_EPI(PIs, minterms)
    
    # table
    tm.gen_table([col1, col2, col3], PIs)
    
    # PI_chart
    PI_chart = tm.gen_PI_chart(minterms, PIs, EPIs, NEPIs, EPIs_minterm)
    print('Prime implicant chart')
    print(PI_chart)
    
    # boolean
    print('SOP logic function')
    SOP = tm.get_SOP(variables, EPIs, NEPIs)
    function = f'f({", ".join(variables)}) = {SOP}'
    print(function)