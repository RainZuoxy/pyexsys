import pandas as pd


##结果excel输出
class CreateOutput:
    def __init__(self, category, result_data_df, imt_data_df):
        self.category = category
        self.excel_output_fb = ''
        self.time_end = 0
        self.result_data_num = 0
        self.result_data_df = result_data_df
        self.imt_data_df = imt_data_df
        self.error_attr_fb = ""
        pass

    ####################imt_inde变量问题
    def _fill_default_value(self, dict, df, item):
        global df_cond
        # 默认值
        # df一般是result_data
        # default_rule_df=df_cond[df]
        # default_cons_df
        dict1 = {
            '17436': 'NOT DETERMINED',
            '1538': 'NOT DETERMINED',
            '75259': 'NO PROMOTION',
            '75305': 'NON-BANDED',
            '75250': '其他牌子',
            '75155': '其他厂家',
            '75157': 'ZZ2NA135_不适用',
            '75383': 'N'
        }
        default_dict = {**dict1, **dict}
        for key in default_dict.keys():
            try:
                if pd.isnull(df.loc[item, key]) or df.loc[item, key] == '':
                    df.loc[item, key] = default_dict[key]
            except:
                pass

    def _bg_color_red(self, sheet):
        columns = sheet.max_column
        rows = sheet.max_row
        for i in range(1, columns - 2):
            for j in range(2, rows + 1):
                if sheet.cell(j, i).value == "" or sheet.cell(j, i).value == "nan" or sheet.cell(j, i).value == None:
                    sheet.cell(j, i).fill = PatternFill("solid", fgColor="FF0000")

    def _bg_color_lime_prom(self, sheet):
        rows = sheet.max_row
        for j in range(2, rows + 1):
            if self._check_promotion(sheet.cell(j, 15).value):
                sheet.cell(j, 25).fill = PatternFill("solid", fgColor="00FF00")

    def _bg_color_lime_pack(self, sheet):
        rows = sheet.max_row
        for j in range(2, rows + 1):
            if self._check_packsize(sheet.cell(j, 15).value):
                sheet.cell(j, 18).fill = PatternFill("solid", fgColor="00FF00")

    def _bg_color_yellow_multierror(self, sheet):
        columns = sheet.max_column
        rows = sheet.max_row
        for i in range(16, columns - 2):  # range(29
            for j in range(2, rows + 1):
                if self._check_multierror(sheet.cell(j, i).value):
                    sheet.cell(j, i).fill = PatternFill("solid", fgColor="FFFF00")

    def _check_promotion(self, s):
        pattern = re.compile(r'(买)(\d+)?([一二三四五六七八九十])?(送)(\d+)?([一二三四五六七八九十])?', re.I)
        pack = re.search(pattern, s)
        if pack:
            return True
        else:
            return False
        pass

    def _check_packsize(self, s):
        pattern = re.compile(
            r'(\d+)(BAG|BL|CAP|CL|GM|KG|M|ML|PACK|PCS|RAZ|ROLL|STICK|TAB|G|L)?(\+)(\d+)(BAG|BL|CAP|CL|GM|KG|M|ML|PACK|PCS|RAZ|ROLL|STICK|TAB|G|L)?',
            re.I)
        pack = re.search(pattern, s)
        if pack:
            return True
        else:
            return False

    def _check_multierror(self, s):
        try:
            pattern = re.compile(r'.(\()(和)(\)).', re.I)
            multierror = re.search(pattern, s)
            if multierror:
                return True
            else:
                return False
        except:
            return False

    def organizedata(self, table_name, dict_default):  # self.table_name(12, len(self.table_name()) - 3)
        global output_path

        table_list = table_name
        self.result_data_num = str(len(self.result_data_df.index.values))
        for i in range(len(self.imt_data_df)):
            try:
                imt = self.imt_data_df.iloc[i]
                cons_keyword = ""
                if imt['code'] in table_list:
                    if (self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']] == "") or \
                            (self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']] is np.nan):
                        cons_keyword = imt['consequence']
                        self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']] = cons_keyword
                    else:
                        if str(imt["consequence"]) in str(
                                self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']]):
                            pass
                        else:
                            cons_keyword = self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']] + "(和)" + \
                                           imt[
                                               "consequence"]
                            self.result_data_df.loc[self.imt_data_df.iloc[i, 1], imt['code']] = cons_keyword
                # try:
                #     if (i == len(self.imt_data_df) - 1) or (self.imt_data_df.iloc[i, 1] != self.imt_data_df.iloc[i + 1, 1]):
                #         self._fill_default_value(dict_default, self.result_data_df, self.imt_data_df.iloc[i, 1])
                # except:
                #     jug=re.search(r"默认值出错请检查", self.error_attr_fb)
                #     if jug:
                #         pass
                #     else:
                #         self.error_attr_fb=self.error_attr_fb+"默认值出错请检查！问题可能存在但不限于“默认值code错误”等问题。\n"
            except:
                jug = re.search(r"专属属性出错请检查", self.error_attr_fb)
                if jug:
                    pass
                else:
                    self.error_attr_fb = self.error_attr_fb + "专属属性出错请检查!问题可能存在但不限于“slt_segment表专属属性重复”等。\n"
            finally:
                try:
                    if (i == len(self.imt_data_df) - 1) or (
                            self.imt_data_df.iloc[i, 1] != self.imt_data_df.iloc[i + 1, 1]):
                        self._fill_default_value(dict_default, self.result_data_df, self.imt_data_df.iloc[i, 1])
                except:
                    jug = re.search(r"默认值出错请检查", self.error_attr_fb)
                    if jug:
                        pass
                    else:
                        self.error_attr_fb = self.error_attr_fb + "默认值出错请检查！问题可能存在但不限于“默认值code错误”等问题。\n"

    def create_formatsetting_file(self, table_name_cn, time_start):
        global output_path
        try:
            filename = str(self.category) + "_" + str(self.result_data_num) + "_result.xlsx"
            self.result_data_df.loc[-1] = table_name_cn  # adding a row
            self.result_data_df.index = self.result_data_df.index + 1  # shifting index
            self.result_data_df = self.result_data_df.sort_index()  # sorting by index
            self.time_end = time.perf_counter()
            self.result_data_df.to_excel(output_path + '/' + filename, index=False)
        except PermissionError:
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            filename = str(self.category) + "_" + str(self.result_data_num) + "_result" + localtime.replace(' ',
                                                                                                           '_').replace(
                ':', '_') + ".xlsx"
            self.result_data_df.to_excel(output_path + '/' + filename, index=False)

        try:
            wb = openpyxl.load_workbook(output_path + '/' + filename)
            ws = wb.worksheets[0]
            self._bg_color_lime_prom(ws)
            self._bg_color_lime_pack(ws)
            self._bg_color_yellow_multierror(ws)
            self._bg_color_red(ws)
            wb.save(output_path + '/' + filename)
            wb.close
            self.excel_output_fb = '导出完成!共用时' + str(self.time_end - time_start) + '秒\n'
        except:
            self.result_data_df.to_excel(output_path + '/' + filename, index=False)
            self.excel_output_fb = 'EXCEL标注导出异常！\n'