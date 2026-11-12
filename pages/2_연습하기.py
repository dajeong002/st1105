import pandas as pd
import seaborn as sns
import streamlit as st


st.set_page_config(page_title="펭귄 데이터 분석", page_icon="🐧", layout="wide")

st.title("펭귄 데이터 분석")
st.caption("남극 펭귄의 종, 서식 섬, 부리와 날개 크기, 체중을 살펴보세요.")

REQUIRED_COLUMNS = {
    "species",
    "island",
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
    "sex",
}
SPECIES_LABELS = {
    "Adelie": "아델리 (Adelie)",
    "Chinstrap": "턱끈 (Chinstrap)",
    "Gentoo": "젠투 (Gentoo)",
}
ISLAND_LABELS = {"Biscoe": "비스코 (Biscoe)", "Dream": "드림 (Dream)", "Torgersen": "토르거슨 (Torgersen)"}
SEX_LABELS = {"Female": "암컷", "Male": "수컷", "미상": "미상"}
MEASURE_LABELS = {
    "bill_length_mm": "부리 길이 (mm)",
    "bill_depth_mm": "부리 높이 (mm)",
    "flipper_length_mm": "날개 길이 (mm)",
    "body_mass_g": "체중 (g)",
}


@st.cache_data(show_spinner="펭귄 데이터를 불러오는 중입니다...")
def load_penguins():
    return sns.load_dataset("penguins")


with st.sidebar:
    st.header("데이터와 필터")
    uploaded_file = st.file_uploader(
        "CSV 파일로 불러오기 (선택)",
        type="csv",
        help="species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex 컬럼이 필요합니다.",
    )

if uploaded_file is not None:
    try:
        penguins = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(f"CSV 파일을 읽지 못했습니다: {error}")
        st.stop()
else:
    try:
        penguins = load_penguins()
    except Exception:
        st.error(
            "펭귄 데이터를 온라인에서 불러오지 못했습니다. 사이드바에서 펭귄 데이터 CSV를 업로드해 주세요.",
            icon="⚠️",
        )
        st.stop()

missing_columns = REQUIRED_COLUMNS.difference(penguins.columns)
if missing_columns:
    st.error("필수 컬럼이 없습니다: " + ", ".join(sorted(missing_columns)))
    st.stop()

penguins = penguins.copy()
for column in MEASURE_LABELS:
    penguins[column] = pd.to_numeric(penguins[column], errors="coerce")
if penguins["body_mass_g"].notna().sum() == 0:
    st.error("체중 컬럼에 숫자 데이터가 없습니다. body_mass_g 컬럼을 확인해 주세요.")
    st.stop()

with st.sidebar:
    species_values = sorted(penguins["species"].dropna().unique().tolist())
    island_values = sorted(penguins["island"].dropna().unique().tolist())
    sex_values = sorted(penguins["sex"].dropna().unique().tolist())
    sex_options = sex_values + (["미상"] if penguins["sex"].isna().any() else [])

    selected_species = st.multiselect(
        "펭귄 종",
        species_values,
        default=species_values,
        format_func=lambda value: SPECIES_LABELS.get(value, str(value)),
    )
    selected_islands = st.multiselect(
        "서식 섬",
        island_values,
        default=island_values,
        format_func=lambda value: ISLAND_LABELS.get(value, str(value)),
    )
    selected_sexes = st.multiselect(
        "성별",
        sex_options,
        default=sex_options,
        format_func=lambda value: SEX_LABELS.get(value, str(value)),
    )

    mass_min = int(penguins["body_mass_g"].min())
    mass_max = int(penguins["body_mass_g"].max())
    mass_range = st.slider(
        "체중 범위 (g)",
        min_value=mass_min,
        max_value=mass_max,
        value=(mass_min, mass_max),
        step=100,
    )
    include_unknown_mass = True
    if penguins["body_mass_g"].isna().any():
        include_unknown_mass = st.checkbox("체중을 모르는 개체 포함", value=True)

sex_mask = penguins["sex"].isin([value for value in selected_sexes if value != "미상"])
if "미상" in selected_sexes:
    sex_mask |= penguins["sex"].isna()
mass_mask = penguins["body_mass_g"].between(*mass_range)
if include_unknown_mass:
    mass_mask |= penguins["body_mass_g"].isna()

filtered = penguins[
    penguins["species"].isin(selected_species)
    & penguins["island"].isin(selected_islands)
    & sex_mask
    & mass_mask
].copy()

if filtered.empty:
    st.warning("선택한 조건에 맞는 데이터가 없습니다. 사이드바 필터를 조정해 주세요.")
    st.stop()

avg_mass = filtered["body_mass_g"].mean()
avg_flipper = filtered["flipper_length_mm"].mean()
with st.container(horizontal=True):
    st.metric("분석 개체 수", f"{len(filtered):,}마리", border=True)
    st.metric("포함된 종", f"{filtered['species'].nunique()}종", border=True)
    st.metric("평균 체중", f"{avg_mass:,.0f} g" if pd.notna(avg_mass) else "데이터 없음", border=True)
    st.metric(
        "평균 날개 길이",
        f"{avg_flipper:.1f} mm" if pd.notna(avg_flipper) else "데이터 없음",
        border=True,
    )

st.subheader("측정값 비교")
measure_columns = list(MEASURE_LABELS)
control_col, chart_col = st.columns([1, 2], vertical_alignment="bottom")
with control_col:
    x_measure = st.selectbox(
        "가로축",
        measure_columns,
        index=0,
        format_func=lambda value: MEASURE_LABELS[value],
    )
    y_measure = st.selectbox(
        "세로축",
        measure_columns,
        index=2,
        format_func=lambda value: MEASURE_LABELS[value],
    )

with chart_col:
    scatter_data = filtered[[x_measure, y_measure, "species"]].dropna().rename(
        columns={
            x_measure: MEASURE_LABELS[x_measure],
            y_measure: MEASURE_LABELS[y_measure],
            "species": "종",
        }
    )
    st.scatter_chart(
        scatter_data,
        x=MEASURE_LABELS[x_measure],
        y=MEASURE_LABELS[y_measure],
        color="종",
        alt=f"{MEASURE_LABELS[x_measure]}과 {MEASURE_LABELS[y_measure]}의 관계를 종별로 비교한 산점도",
    )

species_summary = (
    filtered.groupby("species", observed=True)
    .agg(
        개체수=("species", "size"),
        평균체중_g=("body_mass_g", "mean"),
        평균날개길이_mm=("flipper_length_mm", "mean"),
    )
    .reset_index()
)
species_summary["종"] = species_summary["species"].map(
    lambda value: SPECIES_LABELS.get(value, str(value))
)

left_chart, right_chart = st.columns(2)
with left_chart:
    with st.container(border=True):
        st.subheader("종별 개체 수")
        species_counts = (
            filtered["species"]
            .map(lambda value: SPECIES_LABELS.get(value, str(value)))
            .value_counts()
            .rename_axis("종")
            .rename("개체 수")
            .reset_index()
        )
        st.bar_chart(species_counts, x="종", y="개체 수", color="종", alt="필터 조건별 펭귄 종 개체 수")

with right_chart:
    with st.container(border=True):
        st.subheader("종별 평균 체중")
        st.bar_chart(
            species_summary,
            x="종",
            y="평균체중_g",
            color="종",
            y_label="평균 체중 (g)",
            alt="펭귄 종별 평균 체중 비교",
        )

with st.container(border=True):
    st.subheader("종별 요약")
    display_summary = species_summary[["종", "개체수", "평균체중_g", "평균날개길이_mm"]].rename(
        columns={
            "개체수": "개체 수",
            "평균체중_g": "평균 체중 (g)",
            "평균날개길이_mm": "평균 날개 길이 (mm)",
        }
    )
    st.dataframe(
        display_summary,
        hide_index=True,
        column_config={
            "평균 체중 (g)": st.column_config.NumberColumn(format="%.0f g"),
            "평균 날개 길이 (mm)": st.column_config.NumberColumn(format="%.1f mm"),
        },
        alt="필터 조건에 따른 펭귄 종별 개체 수와 평균 측정값",
    )

with st.expander("필터링된 원본 데이터 보기"):
    st.caption(f"결측치가 포함된 행은 그래프와 평균에서 해당 측정값 계산 시 자동으로 제외됩니다. 전체 {len(filtered):,}행")
    st.dataframe(filtered, hide_index=True, alt="현재 필터 조건에 해당하는 펭귄 데이터")
