from pprint import pprint
import prettytable as pt


class TM:
    '''
        Tabulation Method
    '''
    def __init__(self, variables) -> None:
        self.variables = variables
        self.variables_num = len(variables)
    
    def _dec2bin(self, dec: int):
        '''
            將十進制轉換為二進制
        '''
        return format(dec, f'0{self.variables_num}b')
    
    def group_by_one(self, terms):
        '''
            將 terms 依照 1 的數量分組
        '''
        one_groups = []
        for i in range(self.variables_num + 1):
            one_groups.append([])
        for term in terms:
            if term[0] == 'd' or term[0] == 'm' or term[0] == 'M':
                term_dec = int(term[1:])
                term_bin = self._dec2bin(term_dec)
                count = term_bin.count('1')
            one_groups[count].append([f'{term}', term_bin])
        return one_groups
    
    def _compare_01(self, a, b):
        '''
            比較兩個 term 是否只差一個 1
        '''
        count = 0
        for i in range(len(a)):
            if a[i] != b[i]:
                count += 1
        return count == 1
    
    def _merge(self, a, b):
        '''
            合併兩個 term
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
            將比較過的 term mark 起來 (不重複標記)
        '''
        if len(row) == 2:
            row.append('v')
        return row
    
    def next_column(self, last_col: list):
        '''
            依照 term 的 1 的數量進行合併
        '''
        next_groups = []
        # 下一個 group 數量會比上一個少一個
        for i in range(len(last_col) - 1):
            next_groups.append([])
            for j in range(len(last_col[i])):
                for k in range(len(last_col[i + 1])):
                    if self._compare_01(last_col[i][j][1], last_col[i + 1][k][1]):
                        # 將比較過的 terms mark 起來
                        self._mark(last_col[i][j])
                        self._mark(last_col[i + 1][k])
                        # 合併 terms key
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
    
    def get_EPI(self, PIs, terms):
        '''
            取得 essential prime implicant
        '''
        EPIs = []
        NEPIs = []
        term_in_PI = {}
        EPIs_mark = []
        for i in terms:
            term_in_PI[str(i)] = 0
        
        # 計算每個 term 在 PI 中出現的次數
        for PI in PIs:
            terms = PI[0].split(', ')
            for term in terms:
                term_in_PI[term] += 1
        
        # 判斷是否為 EPI
        for term in term_in_PI:
            count = term_in_PI[term]
            if count == 1 and term[0] != 'd':
                EPIs_mark.append(term)
                for PI in PIs:
                    terms = PI[0].split(', ')
                    if term in terms and PI not in EPIs:
                        EPIs.append(PI)
                        
        # 取得 NEPI
        # 將 EPI 的 term 從 term_in_PI 中移除
        for EPI in EPIs:
            EPIs_term = EPI[0].split(', ')
            for term in EPIs_term:
                term_in_PI[term] = 0
        for term in term_in_PI:
            for PI in PIs:
                if term_in_PI[term] != 0 and term[0] != 'd':
                    terms = PI[0].split(', ')
                    if term in terms:
                        NEPIs.append(PI)
                        term_in_PI[term] = 0
        
        return EPIs, NEPIs, EPIs_mark
    
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
                table.field_names = ['Group', 'Terms', 'Binary', '']
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
    
    def gen_PI_chart(self, terms, PIs, EPIs, NEPIs, EPIs_term):
        '''
            產生 Prime implicant chart ⛒ ✖
        '''
        PI_chart = pt.PrettyTable()
        field_names = ['', 'Prime Implicant']
        for term in terms:
            field_names.append(f'{term}')
        PI_chart.field_names = field_names
        for PI in PIs:
            PI_key = PI[0]
            row = ['', PI_key]
            PI_key = PI_key.split(', ')
            for term in terms:
                term = str(term)
                if term in PI_key:
                    if term in EPIs_term:
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
    
    def _bin2bool(self, variables, bin, positive, negative, split_by = ''):
        result = ''
        index = 0
        for bit in bin:
            if bit == positive:
                result += f'{variables[index]}'
                result += f'{split_by}'
            elif bit == negative:
                result += f'{variables[index]}\''
                result += f'{split_by}'
            index += 1
        # 去除最後一個 split
        result = result[:-len(split_by)]
        result = f'({result})'
        return result
    
    def get_SOP(self, variables, EPIs, NEPIs):
        '''
            取得 SOP logic function
        '''
        result = []
        for EPI in EPIs:
            result.append(self._bin2bool(variables, EPI[1], '1', '0', ' '))
        for NEPI in NEPIs:
            result.append(self._bin2bool(variables, NEPI[1], '1', '0', ' '))
        return ' + '.join(result)
    
    def get_POS(self, variables, EPIs, NEPIs):
        '''
            取得 POS logic function
        '''
        result = []
        for EPI in EPIs:
            result.append(self._bin2bool(variables, EPI[1], '0', '1', ' + '))
        for NEPI in NEPIs:
            result.append(self._bin2bool(variables, NEPI[1], '0', '1', ' + '))
        return ' * '.join(result)