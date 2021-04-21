from typing import Dict
from ipywidgets import VBox, HBox, IntSlider, Layout, jslink, Play
from bqplot import (
    Mercator,
    Map,
    topo_load,
    Figure,
    Tooltip,
    ColorScale,
    ColorAxis,
    Lines,
    LinearScale,
    Axis,
)


class Dashboard:
    def __init__(self, df, map_file, province_id_to_name) -> None:
        self.df = df
        self.yearly_df = self.df.pipe(self.reshape_with_period_cols)
        self.years = list(self.yearly_df.columns)
        self.sc_x = LinearScale()
        self.sc_y = LinearScale()
        self.col_scale = ColorScale(scheme="Greens")
        self.geomap = self.create_map(map_file)
        self.lineplot = self.create_lineplot()
        self.province_id_to_name = province_id_to_name.copy()
        self.year_slider = IntSlider(
            description="year",
            min=1995,
            max=2001,
            continuous_update=False,
            layout=Layout(width="100%"),
        )

    def create_map(self, map_file):
        first_year = self.years[0]
        first_provincial_income_proportion = self.get_provincial_income_proportion(
            first_year
        )
        sc_geo = Mercator(scale_factor=7000, center=(5.5, 53.0))
        tooltip = Tooltip(fields=["name"], labels=["province"])
        return Map(
            map_data=topo_load(map_file),
            scales={"projection": sc_geo, "color": self.col_scale},
            colors={"default_color": "Grey"},
            color=first_provincial_income_proportion,
            tooltip=tooltip,
            interactions={"click": "select", "hover": "tooltip"},
            visible=True,
        )

    def create_map_figure(self):
        ax_col = ColorAxis(scale=self.col_scale, label="ratio", tick_format="0.2f")
        return Figure(
            marks=[self.geomap],
            axes=[ax_col],
            title="Wealth of The Netherlands",
            layout={
                "min_width": "400px",
                "width": "auto",
                "min_height": "400px",
                "width": "auto",
            },
        )

    def create_lineplot(self):
        return Lines(
            x=self.years,
            y=[],
            scales={"x": self.sc_x, "y": self.sc_y},
            display_legend=True,
        )

    def create_lineplot_figure(self):
        ax_x = Axis(scale=self.sc_x, label="Year", tick_values=self.years)
        ax_y = Axis(scale=self.sc_y, orientation="vertical", label="Thousands (Euro)")
        return Figure(
            marks=[self.lineplot],
            axes=[ax_x, ax_y],
            title="Income per Year (Click a provice to show)",
            subtitle="Click a province to show",
            layout={
                "min_width": "400px",
                "width": "auto",
                "min_height": "400px",
                "height": "auto",
            },
        )

    def plot_yearly_income_per_province(self, *_):
        """
        on_event, when a province is clicked
        """
        if self.geomap.selected is not None and len(self.geomap.selected) > 0:
            selected_provinces = self.geomap.selected
            self.lineplot.y = self.yearly_df.loc[selected_provinces]
            self.lineplot.labels = [
                self.province_id_to_name[province_id]
                for province_id in selected_provinces
            ]
        else:
            self.lineplot.labels = []
            self.lineplot.y = []

    def update_income(self, *_):
        """
        on_event, when a year slider is changed
        """
        year = self.year_slider.value
        id_to_income = self.get_provincial_income_proportion(year)
        geomap_color_scale = self.geomap.scales["color"]
        geomap_color_scale.min = min(id_to_income.values())
        geomap_color_scale.max = max(id_to_income.values())
        self.geomap.color = id_to_income

    def reshape_with_period_cols(_, input_df):
        """
        To get a yearly dataframe, in which years are pivoted as columns
        """
        input_df = input_df.pivot(index="province_id", columns="period")[["income"]]
        # Drop higher column level, i.e income
        input_df.columns = input_df.columns.droplevel()
        return input_df

    def get_provincial_income_proportion(self, year: int) -> Dict[int, float]:
        is_within_year = self.df["period"] == year
        yearly_income = self.df[is_within_year]
        income_proportion = yearly_income["income"] / sum(yearly_income["income"])
        id_to_income = dict(zip(yearly_income["province_id"], income_proportion))
        return id_to_income

    def build(self):
        self.geomap.observe(self.plot_yearly_income_per_province, "selected")
        play_button = Play(
            min=1995, max=2001, interval=1000, layout=Layout(width="100%")
        )
        self.year_slider.observe(self.update_income, "value")
        jslink((play_button, "value"), (self.year_slider, "value"))
        map_figure = self.create_map_figure()
        lineplot_figure = self.create_lineplot_figure()

        return VBox(
            [HBox([play_button, self.year_slider]), map_figure, lineplot_figure]
        )
