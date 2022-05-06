import os
from typing import Dict, Type

import django
import pandas as pd
import streamlit as st
from django.db.models import Count

#%% Default value for setting is "totem.settings.production".
# To run this streamlit to the local database run:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classificationapp.settings")
django.setup()

from annotationsdatabase import models


# #%% App constants
# DATABASE_ENVIRONMENT = os.environ["DJANGO_SETTINGS_MODULE"].split(".")[-1]
# N_KPI_COLUMNS = 3
# # KPIs definitions
# QUALITY_TAG_KPIS = [
#     {
#         "model_class": models.BoundingBox,
#         "quality_fieldname": "_quality_tag_correctness",
#         "quality_tag_nomenclature": "1",
#         "quality_tag_description": "Bounding Boxes Correctness",
#     },
#     {
#         "model_class": models.TrayObject,
#         "quality_fieldname": "_quality_tag_container_label_correctness",
#         "quality_tag_nomenclature": "2",
#         "quality_tag_description": "Container Label Correctness",
#     },
#     {
#         "model_class": models.TrayObject,
#         "quality_fieldname": "_quality_tag_content_label_correctness",
#         "quality_tag_nomenclature": "3",
#         "quality_tag_description": "Content Label Correctness",
#     },
#     {
#         "model_class": models.Tray,
#         "quality_fieldname": "_quality_tag_image_completeness_left",
#         "quality_tag_nomenclature": "4.1",
#         "quality_tag_description": "Left Image Completeness",
#     },
#     {
#         "model_class": models.Tray,
#         "quality_fieldname": "_quality_tag_image_completeness_center",
#         "quality_tag_nomenclature": "4.2",
#         "quality_tag_description": "Center Image Completeness",
#     },
#     {
#         "model_class": models.Tray,
#         "quality_fieldname": "_quality_tag_image_completeness_right",
#         "quality_tag_nomenclature": "4.3",
#         "quality_tag_description": "Right Image Completeness",
#     },
#     {
#         "model_class": models.ServiceContentsForContainerStatus,
#         "quality_fieldname": "_quality_tag_service_contents_for_container",
#         "quality_tag_nomenclature": "5",
#         "quality_tag_description": "Contents for Container Status",
#     },
#     {
#         "model_class": models.Service,
#         "quality_fieldname": "_quality_tag_content_label_consistency",
#         "quality_tag_nomenclature": "6",
#         "quality_tag_description": "Content Labels Consistency",
#     },
#     {
#         "model_class": models.Service,
#         "quality_fieldname": "_quality_tag_ignored_status",
#         "quality_tag_nomenclature": "7",
#         "quality_tag_description": "IGNORED Status",
#     },
# ]
#
#
# #%% Compute util functions
# def compute_quality_tag_kpi(model_class: Type[models.ModelType], quality_fieldname: str) -> Dict[str, int]:
#     quality_counts_from_database = {
#         quality_tag_value[quality_fieldname]: quality_tag_value["count"]
#         for quality_tag_value in (
#             model_class.objects.values(quality_fieldname)
#             .order_by(quality_fieldname)
#             .annotate(count=Count(quality_fieldname))
#         )
#     }
#     return {
#         QualityTagValues.TO_BE_CHECKED: 0,
#         QualityTagValues.OK: 0,
#         QualityTagValues.KO: 0,
#         **quality_counts_from_database,
#     }
#
#
# #%% Rendering util functions
# def format_tag_kpi(quality_count_value: int, quality_count_total: int) -> str:
#     return f"{quality_count_value} ({round(quality_count_value / quality_count_total * 100, 2)}%)"
#
#
# def render_compute_quality_tag_kpi(
#     quality_tag_entity_name: str,
#     quality_tag_nomenclature: str,
#     quality_tag_description: str,
#     quality_counts: Dict[str, int],
# ):
#     quality_count_total = sum(quality_counts.values())
#
#     st.write(f"### 📊 #{quality_tag_nomenclature}: {quality_tag_description}")
#     st.write(f"Entity: {quality_tag_entity_name} ({quality_count_total} total)")
#
#     # Show altair bar chart
#     quality_counts_df = (
#         pd.DataFrame([quality_counts])
#         .T.reset_index()
#         .rename(columns={"index": "tag", 0: "count"})
#         .assign(
#             legend=lambda df: df.apply(
#                 lambda row: format_tag_kpi(quality_count_value=row["count"], quality_count_total=quality_count_total),
#                 axis=1,
#             ),
#             x_text=0,
#         )
#     )
#
#     quality_tags_chart = alt.Chart(quality_counts_df)
#     quality_tags_bars = quality_tags_chart.mark_bar().encode(y="tag:N", x="count:Q")
#     quality_tags_bars_text = quality_tags_chart.mark_text(align="left", dx=5).encode(
#         y="tag:N", x="x_text:Q", text="legend:N", color=alt.value("white")
#     )
#
#     st.altair_chart(quality_tags_bars + quality_tags_bars_text, use_container_width=True)
#
#
# def show_quality_tag_kpi(
#     model_class: Type[models.ModelType],
#     quality_fieldname: str,
#     quality_tag_nomenclature: str,
#     quality_tag_description: str,
# ):
#     quality_counts = compute_quality_tag_kpi(model_class=model_class, quality_fieldname=quality_fieldname)
#     render_compute_quality_tag_kpi(
#         quality_tag_entity_name=model_class.__name__,
#         quality_tag_nomenclature=quality_tag_nomenclature,
#         quality_tag_description=quality_tag_description,
#         quality_counts=quality_counts,
#     )
#
#
def show_header_metrics():
    metric_columns = st.columns(5)
    metric_columns[0].metric(
        label="Labels", value=models.ImageAnnotation.objects.count()
    )
    st.write("---")


def main():
    # Title
    st.set_page_config(
        page_title="Monitor Database Annotations", layout="wide", page_icon="📀"
    )
    st.title(f"Monitor Database Annotations")

    # Header metrics
    show_header_metrics()
    #
    # # KPIs metrics
    # kpis_columns = st.columns(N_KPI_COLUMNS)
    #
    # for quality_tag_kpi_index, quality_tag_kpi in enumerate(QUALITY_TAG_KPIS):
    #     with kpis_columns[quality_tag_kpi_index % N_KPI_COLUMNS]:
    #         show_quality_tag_kpi(**quality_tag_kpi)


#%%
if __name__ == "__main__":
    main()
