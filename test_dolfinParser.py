from LL_Drives.dolfinParser import *

def test_get_id_info():
    import time
    my_filter = {'Absorbance': [], 'Fluorescence': [], "Time": ['start_time', 'end_time']}
    blank_filter = {}
    for i in range(1, 9):
        my_filter['Time'].extend(['Merge ' + str(i)])
        my_filter['Fluorescence'].extend(['drop_' + str(i), 'blank_' + str(i)])
        blank_filter['drop_' + str(i)] = ['blank_' + str(i), 'Merge ' + str(i)]

    do = dolfinParser('16115.results.csv', my_filter, 'C:\Users\dhull\Documents\code_directory\dolfininterpreter\\test', 2.0)
    start_time = time.clock()
    print start_time
    do.get_id_info()
    print time.clock()-start_time

    for value in my_filter['Fluorescence']:
        assert len(do.output[value]['exp_time_sec']) == 10
        assert len(do.output[value]['results']) == 10
        assert len(do.output[value]['converted']) == 10
        assert do.output['drop_1']['description'] == ['fluorimeter']
    assert do.output['drop_1']['results']==[39.3269,71.8813,107.324,145.089, 184.325, 225.271, 267.589, 310.769, 354.708, 399.141]
    assert len(do.output['drop_1'].keys())== 4
    assert do.output['drop_1'].keys()==['description','converted','results','exp_time_sec']
    assert do.output['drop_1']['exp_time_sec'] == [352.346, 397.946, 443.546, 489.146, 534.746, 580.346, 625.946, 671.546, 717.146, 762.746]
    assert do.output['drop_1']['converted'][0] == 78.6538

    start_time = time.clock()
    print start_time
    do.get_blank_subtracted_vals(blank_filter, [1,10])
    print time.clock()-start_time

    import numpy as np

    for key in blank_filter.keys():
        id = 'blank_sub_'+key
        assert len(do.output[id]['exp_time_sec']) == 10
        assert len(do.output[id]['results']) == 10
        assert len(do.output[id]['converted']) == 10
        assert do.output[id]['description'] == ['fluorimeter']
    np.testing.assert_almost_equal(do.output['blank_sub_drop_1']['post_merge_time'],[31.460,77.060, 122.660, 168.260, 213.860, 259.460, 305.060, 350.660, 396.260, 441.860])
    np.testing.assert_almost_equal(do.output['blank_sub_drop_1']['results'], [30.07766, 62.78095,98.27585,136.09025,175.36537,216.34523,258.70416,301.9191,345.86949,390.34563])

test_get_id_info()
