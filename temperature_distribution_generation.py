import sys

class temp_proj_gen(object):
    def __init__(self):
        self.baseline_dist = list()

    def load_proj_and_baseline(self, baseline, projections):
        if isinstance(baseline, str):
            try:
                with open(baseline, 'r') as f_:
                    self.baseline_dist = list(map(lambda x: x.strip(), f_.readlines()))
            except FileNotFoundError as f_not_found:
                raise f_not_found
        if (len(projections) > 0):
            self.proj_data = list()
            for proj in projections:
                if isinstance(proj, str):
                    try:
                        with open(proj, 'r') as f_:
                            self.proj_data.append(f_.read().splitlines())
                    except FileNotFoundError as f_not_found:
                        raise f_not_found
                elif isinstance(proj, list):
                    self.proj_data.append(proj)
                else:
                    raise ValueError((list, str))
        else:
            raise Exception(projections, "Invalid array of filenames or array of data")
    def proj_over_time(self, years_back, years_forward, baseline=None, projections=None):
        if (baseline != None) and (projections != None):
            try:
                self.load_proj_and_baseline(baseline, projections)
            except Exception as loading_error:
                raise loading_error
        elif (baseline != None) or (projections != None):
            raise ValueError((None, list))
        self.full_proj = list()
        for proj in self.proj_data:
            self.full_proj.append([])
        for i in range(1, 365*(years_back + years_forward)):
            for index, proj in enumerate(self.proj_data):
                if (i > years_back*365):
                    self.full_proj[index].append(proj[(i - years_back*365)])
                else:
                    count_back = len(self.baseline_dist)-1
                    self.full_proj[index].insert(0, self.baseline_dist[(count_back-(i % (count_back+1)))])
        return self.full_proj
    
    def proj_to_file(self, filename, full_proj=None):
        if (full_proj != None):
            if isinstance(full_proj, list):
                self.filewrite_main(filename, full_proj)
        else:
            self.filewrite_main(filename, self.full_proj)


    def filewrite_main(self, filename, data):
        if isinstance(filename, list):
            for index, _file in enumerate(filename):
                self.filewrite_sub(_file, data[index])
        elif isinstance(filename, str):
            try:
                self.filewrite_sub(filename, data[0])
            except IndexError as indx:
                raise indx

    def filewrite_sub(self, filename, float_list):
        try:
            with open(filename, 'w+') as _file:
                for _float in float_list:
                    _file.write(('{}\n').format(float(_float)))
        except (ValueError, FloatingPointError, OSError) as err:
            raise err

if __name__ == "__main__":
    test_proj = temp_proj_gen()
    test_proj.load_proj_and_baseline('./hist_for_50yr.txt', ['./_45_for_86yr.txt', './_85_for_86yr.txt'])
    t = test_proj.proj_over_time(67, 90)
    print(t[0][0:10])
    test_proj.proj_to_file(['rcp45_1950_2100.txt', "rcp85_1950_2100.txt"])