from fiora.untests import MetricTester



class ReportHandler:
    def __init__(self, datapath, json_ref ,json_test, validation_id):
        self.metrictester = MetricTester()
        self.json_ref = json_ref
        self.json_test = json_test
        self.validation_id = validation_id
        self.suitename = list(json_ref.keys())[0]
        self.report_components = []
        self.output = f"""<center><img src="https://github.com/MartinRovang/Fiora/blob/master/flc_design2022080460426.jpg?raw=true" width="200">  <br><br> Target: <p>{datapath}</p>
        <br></center>
        <style>
            .whole_table {{
                /* add some spacing between table*/
                margin-right: 25%;
                /* margin between columns  */
                margin-left: 25%;
                width: 100%;
                        }}
            .reference_table {{
                /* add some spacing between table*/
                margin-right: 20px;
                        }}
            th, td {{
                    padding: 10px;
                    }}
            </style> """
        self.report_components.append(self.output)
    
    def generate_report(self):
        markdown_document = """"""
        for component in self.report_components:
            markdown_document += component
        with open(
            f"Fiora_strc/validations/reports/{self.suitename}_{self.validation_id}.html",
            "w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(markdown_document)
        
        return self.metrictester.test_result_json
    
    def generate_report_json(self):
        return self.metrictester.test_result_json
    
    def generate_break(self):
        self.report_components.append("""<br>""")
    
    def generate_break_with_line(self):
        self.report_components.append("""<hr><br>""")
    
    def begin_table(self):
        self.report_components.append("""
            <div class="reference_table">
                <table>
                <thead>
                    <tr class="header">
                        <th>Test</th>
                        <th>Target</th>
                    </tr>
                </thead>
                <tbody>""")
    
    def end_table(self):
        self.report_components.append("""
                        </tbody>
                        </table>
                        </div>""")

    def generate_mean(self):
        key = "mean"
        component = """"""
        test_result = self.metrictester.test_mean(self.json_ref[self.suitename], self.json_test[self.suitename])
        min_val = self.json_ref[self.suitename][key]["min"]
        max_val = self.json_ref[self.suitename][key]["max"]

        min_val_target = self.json_test[self.suitename][key]["min"]
        max_val_target = self.json_test[self.suitename][key]["max"]

        if test_result:
            component += f'<tr><td>✅ mean must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'
        else:
            component += f'<tr><td>❌ mean must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'


        component += f'</td>'
        component += f'<td>{min_val_target}|{max_val_target}</td></tr>'

        self.report_components.append(component)
        # self.generate_break()
    

    def generate_max_values(self):
        key = "max_value"
        component = """"""
        test_result = self.metrictester.test_max_values(self.json_ref[self.suitename], self.json_test[self.suitename])
        min_val = self.json_ref[self.suitename][key]["min"]
        max_val = self.json_ref[self.suitename][key]["max"]

        min_val_target = self.json_test[self.suitename][key]["min"]
        max_val_target = self.json_test[self.suitename][key]["max"]

        if test_result:
            component += f'<tr><td>✅ max_values must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'
        else:
            component += f'<tr><td>❌ max_values must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'


        component += f'</td>'
        component += f'<td>{min_val_target}|{max_val_target}</td></tr>'
        
        self.report_components.append(component)
        # self.generate_break()

    def generate_min_values(self):
        key = "min_value"
        component = """"""
        test_result = self.metrictester.test_min_values(self.json_ref[self.suitename], self.json_test[self.suitename])
        min_val = self.json_ref[self.suitename][key]["min"]
        max_val = self.json_ref[self.suitename][key]["max"]

        min_val_target = self.json_test[self.suitename][key]["min"]
        max_val_target = self.json_test[self.suitename][key]["max"]

        if test_result:
            component += f'<tr><td>✅ min_values must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'
        else:
            component += f'<tr><td>❌ min_values must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>'

        component += "</td>"
        component += f'<td>{min_val_target}|{max_val_target}</td></tr>'

        self.report_components.append(component)
        # self.generate_break()
    
    def generate_percentage_foreground(self):

        key = "percentage_foreground"
        component = """"""
        test_result = self.metrictester.test_percentage_foreground(self.json_ref[self.suitename], self.json_test[self.suitename])
        min_val = self.json_ref[self.suitename][key]["min"]
        max_val = self.json_ref[self.suitename][key]["max"]

        min_val_target = self.json_test[self.suitename][key]["min"]
        max_val_target = self.json_test[self.suitename][key]["max"]

        if test_result:
            component += f'<tr><td>✅ percentage_foreground must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span>       {min_val_target}|{max_val_target}'
        else:
            component += f'<tr><td>❌ percentage_foreground must be greater than or equal to <span style="background-color: #525252; color:white">{min_val}</span> and less than or equal to <span style="background-color: #525252; color:white">{max_val}</span> {min_val_target}|{max_val_target}'
        
        component += "</td>"
        component += f'<td>{min_val_target}|{max_val_target}</td></tr>'

        self.report_components.append(component)
        # self.generate_break()
    
    def generate_num_nans(self):
        key = "num_nans"
        component = """"""
        test_result = self.metrictester.test_num_nans(self.json_ref[self.suitename], self.json_test[self.suitename])
        total = self.json_ref[self.suitename][key]["total"]
        number_target = self.json_test[self.suitename][key]["total"]

        if test_result:
            component += f'<tr><td>✅ must have same number of nans <span style="background-color: #525252; color:white">{total}</span>'
        else:
            component += f'<tr><td>❌ must have same number of nans <span style="background-color: #525252; color:white">{total}</span>'
        
        component += f'</td>'
        component += f'<td>{number_target}</td></tr>'
        self.report_components.append(component)
        # self.generate_break()
    
    def generate_num_infs(self):
        key = "num_infs"
        component = """"""
        test_result = self.metrictester.test_num_infs(self.json_ref[self.suitename], self.json_test[self.suitename])
        total = self.json_ref[self.suitename][key]["total"]
        number_target = self.json_test[self.suitename][key]["total"]

        if test_result:
            component += f'<tr><td>✅ must have same number of infs <span style="background-color: #525252; color:white">{total}</span>'
        else:
            component += f'<tr><td>❌ must have same number of infs <span style="background-color: #525252; color:white">{total}</span>'

        component += "</td>"
        component += f'<td>{number_target}</td></tr>'
        self.report_components.append(component)
        # self.generate_break()
    
    def generate_types(self):
        key = "types"
        component = """"""
        test_result = self.metrictester.test_types(self.json_ref[self.suitename], self.json_test[self.suitename])
        unique_types = self.json_ref[self.suitename][key]["unique_types"]
        unique_types_target = self.json_test[self.suitename][key]["unique_types"]
        if test_result:
            component += "<tr><td>✅ types must be any of the following "
        else:
            component += "<tr><td>❌ types must be any of the following   "
        for typ_ in unique_types:
            component += f"""<span style="background-color: #0000FF; color:white">{typ_}</span> """

        component += "</td>"
        component += f'<td>{unique_types_target}</td></tr>'

        self.report_components.append(component)
        # self.generate_break()
    
    def generate_shape_ax1(self):

        key = "shapes_ax1"
        component = """"""
        test_result = self.metrictester.test_shape_ax1(self.json_ref[self.suitename], self.json_test[self.suitename])
        
        unique_shapes = self.json_ref[self.suitename][key]["unique_shapes"]
        unique_target = self.json_test[self.suitename][key]["unique_shapes"]

        if test_result:
            component += "<tr><td>✅ shapes must be any of the following "
        else:
            component += (
                "<tr><td>❌ shape for axis 0 must be any of the following   "
            )
        for shape_ in unique_shapes:
            component += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """

        component += "</td>"
        component += f'<td>{unique_target}</td></tr>'
        self.report_components.append(component)
        # self.generate_break()

    
    def generate_shape_ax2(self):
            
        key = "shapes_ax2"
        component = """"""
        test_result = self.metrictester.test_shape_ax2(self.json_ref[self.suitename], self.json_test[self.suitename])

        unique_shapes = self.json_ref[self.suitename][key]["unique_shapes"]
        unique_target = self.json_test[self.suitename][key]["unique_shapes"]
        if test_result:
            component += "<tr><td>✅ shapes must be any of the following "
        else:
            component += (
                "<tr><td>❌ shape for axis 1 must be any of the following   "
            )
        for shape_ in unique_shapes:
            component += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """
        

        component += "</td>"
        component += f'<td>{unique_target}</td><tr>'
        self.report_components.append(component)
        # self.generate_break()
    
    def generate_shape_ax3(self):
        key = "shapes_ax3"
        component = """"""
        test_result = self.metrictester.test_shape_ax3(self.json_ref[self.suitename], self.json_test[self.suitename])

        unique_shapes = self.json_ref[self.suitename][key]["unique_shapes"]
        unique_target = self.json_test[self.suitename][key]["unique_shapes"]
        if test_result:
            component += "<tr><td>✅ shapes must be any of the following "
        else:
            component += (
                "<tr><td>❌ shape for axis 2 must be any of the following   "
            )
        for shape_ in unique_shapes:
            component += f"""<span style="background-color: #0000FF; color:white">{shape_}</span> """
        
        component += "</td>"
        component += f'<td>{unique_target}</td></tr>'
        self.report_components.append(component)
        # self.generate_break()

    def generate_distribution(self):
        key = "distribution"
        table = """ 
               <div class="reference_table">
                <table>
                <thead>
                    <tr class="header">
                        <th>Test</th>
                        <th>Quantile</th>
                        <th>Min value</th>
                        <th>Max value</th>
                    </tr>
                </thead>
                <tbody>
                """
        i = 0
        for quantile_ref, quantile_test in zip(
            self.json_ref[self.suitename][key], self.json_test[self.suitename][key]
        ):
            i += 1
            test_result = self.metrictester.test_distribution(
                self.json_ref[self.suitename][key][quantile_ref],
                self.json_test[self.suitename][key][quantile_test], quantile_test)
            if test_result:
                # if even
                if i % 2 == 0:
                    table += f"""
                    <tr class="even">
                        <td>✅</td>
                        <td>{quantile_ref}</td>
                        <td>{self.json_ref[self.suitename][key][quantile_ref]["min"]}</td>
                        <td>{self.json_ref[self.suitename][key][quantile_ref]["max"]}</td>
                    </tr>
                    """
                # if odd
                else:
                    table += f"""
                    <tr class="odd">
                        <td>✅</td>
                        <td>{quantile_ref}</td>
                        <td>{self.json_ref[self.suitename][key][quantile_ref]["min"]}</td>
                        <td>{self.json_ref[self.suitename][key][quantile_ref]["max"]}</td>
                    </tr>


                    """

            else:
                # if odd
                if i % 3 == 0:
                    table += f"""
                        <tr class="odd">
                            <td>❌</td>
                            <td>{quantile_ref}</td>
                            <td>{self.json_ref[self.suitename][key][quantile_ref]['min']}</td>
                            <td>{self.json_ref[self.suitename][key][quantile_ref]['max']}</td>
                        </tr>

                        
                        """
                # if even
                else:
                    table += f"""
                        <tr class="even">
                            <td>❌</td>
                            <td>{quantile_ref}</td>
                            <td>{self.json_ref[self.suitename][key][quantile_ref]['min']}</td>
                            <td>{self.json_ref[self.suitename][key][quantile_ref]['max']}</td>
                        </tr>

                        """
    
        table += """
                        </tbody>
                        </table>
                        </div>"""

        # Start target table

        table2 = """
               <div class="reference_table">
                <table>
                <thead>
                    <tr class="header">
                        <th>Min value</th>
                        <th>Max value</th>
                    </tr>
                </thead>
                <tbody>
                """
        i = 0
        for quantile_test in self.json_test[self.suitename][key]:
            i += 1
            # if even
            if i % 2 == 0:
                table2 += f"""
                <tr class="even">
                    <td>{self.json_test[self.suitename][key][quantile_test]["min"]}</td>
                    <td>{self.json_test[self.suitename][key][quantile_test]["max"]}</td>
                </tr>
                """
            # if odd
            else:
                table2 += f"""
                <tr class="odd">
                    <td>{self.json_test[self.suitename][key][quantile_test]["min"]}</td>
                    <td>{self.json_test[self.suitename][key][quantile_test]["max"]}</td>
                </tr>

                """

        table2 += """
                        </tbody>
                        </table>
                        </div>"""

        component = f"""
                        <center> 
                        <table>
                        <tr>
                        <td>
                        {table}
                        </td>
                        <td>
                        <table>
                        {table2} 
                        </table>
                        </td>
                        </tr>
                        </table>
                        </center>"""
        self.report_components.append(component)
        self.generate_break_with_line()



    def generate_orientation_correlation(self):
        component = """"""
        correlation_value, test_result = self.metrictester.test_orientation_correlation(self.json_ref[self.suitename], self.json_test[self.suitename])

        if test_result:
            component += f'<tr><td>✅ The correlation has to be larger than <span style="background-color: #525252; color:white">0.9</span> '
        else:
            component += f'<tr><td>❌ The correlation has to be larger than <span style="background-color: #525252; color:white">0.9</span>'


        component += f'</td>'
        component += f'<td>{correlation_value}</td></tr>'
        self.report_components.append(component)