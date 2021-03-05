#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Snow_cover:

    def __init__ (self, row):
        self.row = row
        self.station_index = ''
        self.year = ''
        self.month = ''
        self.day = '' 
        self.is_field = False
        self.is_forest = False
        self.is_error = False
        self.field_height = '///'
        self.field_coverage = '/'
        self.field_density  = '//'
        self.field_ice_thicknes = '//'
        self.field_water_supply = '///'
        self.field_soil_condition  = '/'
        self.forest_height = '///'
        self.forest_coverage = '/'
        self.forest_density  = '//'
        self.forest_ice_thicknes = '//'
        self.forest_water_supply = '///'
        self.forest_soil_condition  = '/'
        self.special_marks = ''
        self.error = ''

    def get_snow_cover(self):

        out = []
        self.parse_row()

        if self.is_field:
           out.append(self.get_field_snow_cover())
        if self.is_forest:
            out.append(self.get_forest_snow_cover())
        elif self.error:
            out.append(self.get_error())

        return out   

    def parse_row(self):

        blocks = list(map(str, self.row.split())) 
        if len(blocks) == 0:
           pass 
        elif blocks[0].isdigit() and len(blocks[0]) == 5:
            self.station_index = blocks[0]
            if blocks[1].isdigit() and len(blocks[1]) == 5:
                block = blocks[1]
                if blocks[1][4] == '9':
                    self.year = '2019' 
                else:
                    self.year = '202' + blocks[1][4] 
                self.month = blocks[1][2:4] 
                self.day = blocks[1][0:2] 
                for block in blocks[2:]:
                    if len(block) == 5 and block[0].isdigit():
                        self._parse_observation(block)
                    elif block.isalpha():
                        if block.find('NIL') != -1 or block.find('НИЛ') != -1:
                            self._set_error('ERROR: record has no content: '+self.row)
                        else:
                            self.special_marks = self.special_marks + block + ' '
                    elif len(block) != 5:
                        self._set_error('ERROR: incorrect block format: '+self.row)
                    else:
                        self._set_error('ERROR: impossible to parse the record: '+self.row)
            else:
                if blocks[1].find('NIL') != -1 or blocks[1].find('НИЛ') != -1:
                    self._set_error('ERROR: record has no content: '+self.row)
                else:
                    self._set_error('ERROR: incorrect date format: '+self.row)
        else:
            self._set_error('ERROR: impossible to parse the record: '+self.row)

    def _parse_observation(self, block):

        if block[0] == '1':
            self.is_field = True
            self.field_height = block[1:4]
            self.field_coverage = block[4]
        if block[0] == '2':
            self.is_field = True
            self.field_density = block[1:3]
            self.field_ice_thicknes = block[3:]
        if block[0] == '3':
            self.is_field = True
            self.field_water_supply = block[1:4]
            self.field_soil_condition = block[4]
        if block[0] == '4':
            self.is_forest = True
            self.forest_height = block[1:4]
            self.forest_coverage = block[4]
        if block[0] == '5':
            self.is_forest = True
            self.forest_density = block[1:3]
            self.forest_ice_thicknes = block[3:]
        if block[0] == '6':
            self.is_forest = True
            self.forest_water_supply = block[1:4]
            self.forest_soil_condition = block[4]

    def get_field_snow_cover(self):

        output = {}
             
        output['station_index'] = int(self.station_index)
        output['year'] = int(self.year) 
        output['month'] = int(self.month)
        output['day'] = int(self.day)
        output['rout_type'] = 1
        if self._is_valid(self.field_height):
            output['snow_cover_height'] = int(self.field_height)
        if self._is_valid(self.field_coverage):
            output['ice_crust_coverage'] = int(self.field_coverage)
        if self._is_valid(self.field_density):
            output['snow_density']  = int(self.field_density)
        if self._is_valid(self.field_ice_thicknes):
            output['ice_crust_thicknes'] = int(self.field_ice_thicknes)
        if self._is_valid(self.field_water_supply):
            output['water_supply'] = int(self.field_water_supply)
        if self._is_valid(self.field_soil_condition):
            output['soil_surface_condition'] = int(self.field_soil_condition)
        if self.special_marks != '':
            output['special_marks'] = self.special_marks
        if self.is_error:
            output['error'] = self.error

        return output   

    def get_forest_snow_cover(self):

        output = {}
             
        output['station_index'] = int(self.station_index)
        output['year'] = int(self.year) 
        output['month'] = int(self.month)
        output['day'] = int(self.day)
        output['rout_type'] = 1
        if self._is_valid(self.forest_height):
            output['snow_cover_height'] = int(self.forest_height)
        if self._is_valid(self.forest_coverage):
            output['ice_crust_coverage'] = int(self.forest_coverage)
        if self._is_valid(self.forest_density):
            output['snow_density']  = int(self.forest_density)
        if self._is_valid(self.forest_ice_thicknes):
            output['ice_crust_thicknes'] = int(self.forest_ice_thicknes)
        if self._is_valid(self.forest_water_supply):
            output['water_supply'] = int(self.forest_water_supply)
        if self._is_valid(self.forest_soil_condition):
            output['soil_surface_condition'] = int(self.forest_soil_condition)
        if self.special_marks != '':
            output['special_marks'] = self.special_marks
        if self.is_error:
            output['error'] = self.error

        return output   

    def get_error(self):

        output = {}

        if self.station_index !='': 
            output['station_index'] = int(self.station_index)
        if self.year != '':
            output['year'] = int(self.year) 
        if self.month != '':
            output['month'] = int(self.month)
        if self.day != '':
            output['day'] = int(self.day)
        if self.special_marks != '':
            output['special_marks'] = self.special_marks
        if self.is_error:
            output['error'] = self.error

        return output   

    def _is_valid(self, param):

        if param.isdigit() and param.find('/') == -1:
            return True 
    
    def _set_error(self, error):

        self.is_error = True
        self.error = self.error + error
