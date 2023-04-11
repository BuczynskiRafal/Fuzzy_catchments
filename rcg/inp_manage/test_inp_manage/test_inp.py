import os
import pytest
import tempfile
import unittest.mock
import pandas as pd

from unittest.mock import patch
from swmmio import Model
from rcg.inp_manage.inp import BuildCatchments
from rcg.fuzzy.engine import Prototype
from rcg.fuzzy.categories import LandForm, LandCover


class TestBuildCatchments:
    @pytest.fixture
    def model_path(self):
        return r"C:\Users\Dell\Documents\Git\rapid-catchment-generator\rcg\inp_manage\test_inp_manage\test_file.inp"

    def test_get_new_subcatchment_id(self, model_path):
        model = Model(model_path)
        with tempfile.TemporaryDirectory() as tempdir:
            inp_path = os.path.join(tempdir, f"{model.inp.name}.inp")
            model.inp.save(inp_path)
            test_model = BuildCatchments(inp_path)
            subcatchment_id = test_model._get_new_subcatchment_id()

            with open(inp_path, "r") as file:
                data = file.read()
                assert data.count(subcatchment_id) == 0

            with open(model_path, "r") as file:
                data = file.read()
                assert data.count(subcatchment_id) == 0

    def test_get_area_valid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch("builtins.input", return_value="10.5"):
            area = test_model._get_area()
            assert area == 10.5

    def test_get_area_invalid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch("builtins.input", side_effect=["abc", "10.5"]):
            area = test_model._get_area()
            assert area == 10.5

    def test_get_land_form_valid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch("builtins.input", return_value="hills_with_gentle_slopes"):
            land_form = test_model._get_land_form()
            assert land_form == "hills_with_gentle_slopes"

    def test_get_land_form_invalid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch(
            "builtins.input",
            side_effect=["invalid_land_form", "hills_with_gentle_slopes"],
        ):
            land_form = test_model._get_land_form()
            assert land_form == "hills_with_gentle_slopes"

    def test_get_land_cover_valid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch("builtins.input", return_value="urban"):
            land_cover = test_model._get_land_cover()
            assert land_cover == "urban"

    def test_get_land_cover_invalid_input(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch(
            "builtins.input",
            side_effect=["invalid_land_cover", "urban"],
        ):
            land_cover = test_model._get_land_cover()
            assert land_cover == "urban"

    def test_get_subcatchment_values(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        with patch.object(test_model, "_get_area", return_value=10.0), patch.object(
            test_model, "_get_land_form", return_value="hills_with_gentle_slopes"
        ), patch.object(test_model, "_get_land_cover", return_value="urban"):
            area, prototype = test_model._get_subcatchment_values()
            assert area == 10.0
            assert isinstance(prototype, Prototype)
            assert hasattr(prototype, "slope_result")
            assert hasattr(prototype, "impervious_result")
            assert hasattr(prototype, "catchment_result")

    def test_add_timeseries(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)
        initial_timeseries_count = len(test_model.model.inp.timeseries)

        test_model._add_timeseries()

        assert len(test_model.model.inp.timeseries) == initial_timeseries_count + 12
        added_timeseries = test_model.model.inp.timeseries.tail(12)
        assert all(added_timeseries.index == "generator_series")
        assert list(added_timeseries["Time"]) == [
            "1:00",
            "2:00",
            "3:00",
            "4:00",
            "5:00",
            "6:00",
            "7:00",
            "8:00",
            "9:00",
            "10:00",
            "11:00",
            "12:00",
        ]
        assert list(added_timeseries["Value"]) == [
            "1",
            "2",
            "4",
            "4",
            "12",
            "13",
            "11",
            "20",
            "15",
            "10",
            "5",
            "3",
        ]

    def test_get_timeseries_no_existing(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        test_model.model.inp.timeseries = test_model.model.inp.timeseries.iloc[0:0]

        first_timeseries_name = test_model._get_timeseries()
        assert first_timeseries_name == "generator_series"

    def test_get_timeseries_with_existing(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        assert len(test_model.model.inp.timeseries) > 0

        first_timeseries_name = test_model._get_timeseries()
        assert first_timeseries_name == test_model.model.inp.timeseries.index[0]

    def test_add_raingage(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        test_model.model.inp.raingages = test_model.model.inp.raingages.iloc[0:0]

        test_model._add_raingage()

        assert len(test_model.model.inp.raingages) == 1
        assert test_model.model.inp.raingages.index[0] == "RG1"
        assert test_model.model.inp.raingages.loc["RG1", "RainType"] == "INTENSITY"
        assert test_model.model.inp.raingages.loc["RG1", "TimeIntrvl"] == "1:00"
        assert test_model.model.inp.raingages.loc["RG1", "SnowCatch"] == "1.0"
        assert test_model.model.inp.raingages.loc["RG1", "DataSource"] == "TIMESERIES"
        assert (
            test_model.model.inp.raingages.loc["RG1", "DataSourceName"]
            == test_model._get_timeseries()
        )

    def test_get_raingage_no_existing_raingages(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        test_model.model.inp.raingages = test_model.model.inp.raingages.iloc[0:0]

        assert len(test_model.model.inp.raingages) == 0
        raingage_name = test_model._get_raingage()
        assert raingage_name == "RG1"
        assert len(test_model.model.inp.raingages) == 1

    def test_get_raingage_with_existing_raingages(self, model_path):
        model = Model(model_path)
        test_model = BuildCatchments(model_path)

        existing_raingage_name = test_model.model.inp.raingages.index[0]
        raingage_name = test_model._get_raingage()
        assert raingage_name == existing_raingage_name

    def test_get_outlet_no_existing_junctions(self, model_path):
        test_model = BuildCatchments(model_path)

        test_model.model.inp.junctions = test_model.model.inp.junctions.iloc[0:0]

        assert len(test_model.model.inp.junctions) == 0
        outlet = test_model._get_outlet()
        assert outlet is None

    def test_get_outlet_with_existing_junctions(self, model_path):
        test_model = BuildCatchments(model_path)

        existing_junction_name = test_model.model.inp.junctions.index[0]
        outlet = test_model._get_outlet()
        assert outlet == existing_junction_name

    def test_add_subarea(self, model_path):
        test_model = BuildCatchments(model_path)

        subcatchment_id = "test_subcatchment"
        prototype = Prototype(LandForm.mountains, LandCover.urban)

        test_model._add_subcatchment(subcatchment_id, (1.0, prototype))

        test_model._add_subarea(subcatchment_id, prototype)

        assert subcatchment_id in test_model.model.inp.subareas.index
        new_subarea = test_model.model.inp.subareas.loc[subcatchment_id]

        map_mannings = {
            "urban": (0.013, 0.15),
            "suburban": (0.013, 0.24),
            "rural": (0.013, 0.41),
            "forests": (0.40, 0.80),
            "meadows": (0.15, 0.41),
            "arable": (0.06, 0.17),
            "mountains": (0.013, 0.05),
        }
        map_depression = {
            "urban": (0.05, 0.20, 90),
            "suburban": (0.05, 0.20, 80),
            "rural": (0.05, 0.20, 70),
            "forests": (0.05, 0.30, 5),
            "meadows": (0.05, 0.20, 10),
            "arable": (0.05, 0.20, 10),
            "mountains": (0.05, 0.20, 80),
        }

        populate_key = Prototype.get_populate(prototype.catchment_result)

        expected_values = {
            "N-Imperv": map_mannings[populate_key][0],
            "N-Perv": map_mannings[populate_key][1],
            "S-Imperv": map_depression[populate_key][0] * 25.4,
            "S-Perv": map_depression[populate_key][1] * 25.4,
            "PctZero": map_depression[populate_key][2],
            "RouteTo": "OUTLET",
        }

        for key, value in expected_values.items():
            assert new_subarea[key] == pytest.approx(value)

    def test_get_existing_coordinates_no_polygons(self, model_path):
        test_model = BuildCatchments(model_path)
        test_model.model.inp.polygons = pd.DataFrame(columns=["X", "Y", "Subcatch"])

        expected_coordinates = [
            (0, 0),
            (0, 5),
            (5, 5),
            (5, 0),
        ]

        coordinates = test_model._get_existing_coordinates()
        assert coordinates == expected_coordinates

    def test_get_existing_coordinates_with_polygons(self, model_path):
        test_model = BuildCatchments(model_path)
        test_model.model.inp.polygons = pd.DataFrame(
            data={
                "X": [0, 0, 5, 5, 10, 10, 15, 15],
                "Y": [0, 5, 5, 0, 0, 5, 5, 0],
                "Subcatch": ["S1", "S1", "S1", "S1", "S2", "S2", "S2", "S2"],
            }
        )

        expected_coordinates = [
            (15, 0),
            (15, 5),
            (10, 5),
            (10, 0),
        ]

        coordinates = test_model._get_existing_coordinates()
        assert coordinates == expected_coordinates

    def test_add_coords_no_existing_polygons(self, model_path):
        test_model = BuildCatchments(model_path)
        test_model.model.inp.polygons = pd.DataFrame(columns=["X", "Y", "Name"])
        test_model.model.inp.polygons.set_index("Name", inplace=True)

        subcatchment_id = "S1"
        test_model._add_coords(subcatchment_id)

        expected_polygons = pd.DataFrame(
            data={
                "X": [0, 0, 5, 5],
                "Y": [-5, 0, 0, -5],
            },
            index=[subcatchment_id for _ in range(4)],
        )
        expected_polygons.index.names = ["Name"]
        expected_polygons["X"] = expected_polygons["X"].astype(object)
        expected_polygons["Y"] = expected_polygons["Y"].astype(object)
        pd.testing.assert_frame_equal(test_model.model.inp.polygons, expected_polygons)

    def test_add_coords_with_existing_polygons(self, model_path):
        test_model = BuildCatchments(model_path)
        test_model.model.inp.polygons = pd.DataFrame(
            data={
                "X": [0, 0, 5, 5],
                "Y": [0, 5, 5, 0],
                "Name": ["S1"] * 4,
            }
        )
        test_model.model.inp.polygons.set_index("Name", inplace=True)

        subcatchment_id = "S2"
        test_model._add_coords(subcatchment_id)

        expected_polygons = pd.DataFrame(
            data={
                "X": [0, 0, 5, 5, 5, 5, 0, 0],
                "Y": [0, 5, 5, 0, -5, 0, 0, -5],
                "Name": ["S1"] * 4 + ["S2"] * 4,
            }
        )
        expected_polygons.set_index("Name", inplace=True)

        pd.testing.assert_frame_equal(test_model.model.inp.polygons, expected_polygons)
