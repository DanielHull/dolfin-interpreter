

class GraphInterpreter:
    def __init__(self, do_object, save_loc, output_name ):
        self.do_object = do_object
        self.save_loc = save_loc
        self.output_name = output_name

    def plot_spectrums(self):
        from bokeh.plotting import figure, output_file, show
        from bokeh.models import Label
        import random, os
        from bokeh.layouts import gridplot
        output_file(self.do_object.file + '.html')
        tools = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
        fig = figure(title='All Spectrums Plotted', x_axis_label='wavelengths', y_axis_label='Spectrum Counts',
                    x_range=(337,824), tools=tools, width=1250, plot_height=500)
        absorbance_detections = self.do_object.filter['Absorbance']

        line_width = 1
        colors = [u'aliceblue', u'aqua', u'aquamarine', u'azure', u'bisque', u'black',
             u'blue',u'blueviolet',u'burlywood',u'cadetblue',u'chartreuse',
             u'chocolate',u'coral',u'cornflowerblue', u'crimson',u'cyan',u'darkblue',u'darkcyan',
             u'darkgray',u'darkgreen',u'darkkhaki',u'darkmagenta',u'darkolivegreen',
             u'darkorange', u'darkorchid', u'darkred', u'darksalmon', u'darkseagreen', u'darkslateblue',
             u'darkslategray', u'darkturquoise', u'darkviolet', u'deeppink', u'deepskyblue',
             u'dodgerblue', u'firebrick', u'floralwhite', u'forestgreen', u'fuchsia',
             u'gainsboro', u'gray', u'green', u'greenyellow', u'grey',
             u'honeydew', u'hotpink', u'indianred', u'indigo', u'lavender', u'lavenderblush',
             u'lawngreen', u'lemonchiffon', u'lightblue', u'lightcoral', u'lightcyan',
             u'lightgreen', u'lightpink', u'lightsalmon', u'lightseagreen', u'lightskyblue',
             u'lightsteelblue', u'lime', u'limegreen',
             u'magenta', u'maroon', u'mediumaquamarine', u'mediumblue', u'mediumorchid', u'mediumpurple',
             u'mediumseagreen', u'mediumslateblue', u'mediumspringgreen', u'mediumturquoise', u'mediumvioletred',
             u'midnightblue', u'mintcream', u'mistyrose', u'moccasin', u'navy', u'oldlace', u'olive',
             u'olivedrab', u'orange', u'orangered', u'orchid', u'palegreen', u'paleturquoise',
             u'palevioletred', u'papayawhip', u'peachpuff', u'peru', u'pink', u'plum', u'powderblue', u'purple', u'red',
             u'royalblue', u'salmon', u'seagreen', u'sienna', u'skyblue', u'slateblue', u'springgreen', u'steelblue',
             u'teal', u'thistle', u'tomato', u'turquoise', u'violet', u'yellow', u'yellowgreen']

        for det in absorbance_detections:
            color = random.randint(1 ,len(colors)-1)
            fig.line(self.do_object.output[det]['wavelengths'], self.do_object.output[det]['results'], legend=det,
                     line_width=line_width, line_color=colors[color])
            line_width += 1

        fig2 = figure(title='All Detections', x_axis_label='Seconds', y_axis_label='RFU Counts', width=1250,
                      plot_height=500)
        detection_labels = self.do_object.filter['Fluorescence']
        for det in detection_labels:
            color = random.randint(1, len(colors)-1)
            fig2.circle(self.do_object.output[det]['exp_time_sec'], self.do_object.output[det]['results'], legend=det, size=10,
                        color=colors[color])
            fig2.legend.location = 'top_center'
        blank_keys = [key for key in self.do_object.output.keys() if 'blank_sub_' in key]
        fig3 = figure(title='Blank Subtracted Detections', x_axis_label='Seconds', y_axis_label='RFU Counts',
                      width=1250, plot_height=500)
        y = 0
        for key in blank_keys:
            color = random.randint(1, len(colors)-1)
            fig3.circle(self.do_object.output[key]['exp_time_sec'], self.do_object.output[key]['results'], legend=key, size=10,
                        color=colors[color])
            mytext = Label(x=250, y=y,x_units='screen', y_units='screen',
                           text='slope of: '+str(key)+' is '+str(self.do_object.output[key]['slope per sec']),
                           render_mode='css', text_font_size='10pt')
            fig3.add_layout(mytext)
            fig3.legend.location = 'top_center'
            y = y + 15
        p = gridplot([[fig2], [fig3], [fig]])
        show(p)

    def export_data(self):
        """
        Function writes data set to an excel workbook defined in the constructor
        Removes the png from the file after writing it - adds blank subtracted in order

        :return: n/a
        """

        import xlsxwriter, os
        from KineticAssayTools import write_excel_file, name_data_file
        os.chdir(self.save_loc)

        workbook_object = xlsxwriter.Workbook(self.output_name + '.xlsx')
        summary_data = {}
        sorted_keys = sorted(self.do_object.output.keys())

        for key in sorted_keys:
            keyword = key[0:29]
            summary_data[key] =  self.do_object.output[key]['results']
            if 'blank_sub_' in key:
                write_excel_file(workbook_object, [self.do_object.output[key]], keyword)

        write_excel_file(workbook_object, [summary_data], 'a_Summary')
        workbook_object.close()
        name_data_file(self.output_name + '.xlsx', self.save_loc)
