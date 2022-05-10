from annotationsdatabase.utils import django_setup

django_setup()


import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from annotationsdatabase import models


def get_annotations_from_db() -> pd.DataFrame:
    return pd.DataFrame.from_records(
        list(
            models.ImageAnnotation.objects.values(
                "label", "label_correctness", "image_correctness", "image_id"
            )
        )
    )


def show_header_metrics() -> None:
    metric_columns = st.columns(5)
    metric_columns[0].metric(
        label="Annotations in DataBase", value=models.ImageAnnotation.objects.count()
    )
    st.write("---")


def show_quality_metrics(annotations_df: pd.DataFrame, metric_name: str) -> None:
    with st.expander(f"{metric_name} metrics", expanded=True):
        metrics_df = annotations_df.pivot_table(
            columns=metric_name, index="label", values="image_id", aggfunc="count"
        )

        col_1, _, col_2 = st.columns([1, 1, 2])

        # Metrics
        col_1.success(
            f"Label OK: {metrics_df['OK'].sum() if 'OK' in metrics_df else 0}"
        )
        col_1.warning(
            f"Label to Review: {metrics_df['TO_BE_CHECKED'].sum() if 'TO_BE_CHECKED' in metrics_df else 0}"
        )
        col_1.error(f"Label KO: {metrics_df['KO'].sum() if 'KO' in metrics_df else 0}")

        # Plot
        fig, ax = plt.subplots()
        metrics_df.filter(items=["OK", "TO_BE_CHECKED", "KO"]).plot.bar(
            ax=ax, fontsize=15, alpha=0.5, grid=True, color=["green", "orange", "red"]
        )
        plt.legend(loc="upper left")
        col_2.pyplot(fig)
        plt.show()


def main():
    # Title
    st.set_page_config(
        page_title="Monitor Database Annotations", layout="wide", page_icon="📀"
    )
    st.title(f"Monitor Database Annotations")

    # Header metrics
    show_header_metrics()

    # Correctness metrics
    annotations_df = get_annotations_from_db()
    show_quality_metrics(annotations_df, "label_correctness")
    show_quality_metrics(annotations_df, "image_correctness")


# %%
if __name__ == "__main__":
    main()
